from tkinter import *
from tkinter import ttk
from pyknow import *
dictlist = [dict() for x in range(16)]

for i in range(16):
    s = "Builds/build"+str(i+1)+".txt"
    with open (s, "r") as myfile:
        dictlist[i] = dict(item.rstrip("\n").split(":") for item in myfile)
        
CPU_dict = {}
GPU_dict = {}
HardDrive_dict = {}
Motherboard_dict = {}

with open ("CPU.txt", "r") as myfile:
    CPU_dict = dict(item.rstrip("\n").split(":") for item in myfile)
with open ("GPU.txt", "r") as myfile:
    GPU_dict = dict(item.rstrip("\n").split(":") for item in myfile)
with open ("INTHD.txt", "r") as myfile:
    HardDrive_dict = dict(item.rstrip("\n").split(":") for item in myfile)
with open ("Motherboard.txt", "r") as myfile:
    Motherboard_dict = dict(item.rstrip("\n").split(":") for item in myfile)
root = Tk()
root.title('PC Builder')
root.geometry("720x480")

CPU = StringVar()
GPU = StringVar()
MB = StringVar()
HD = StringVar()
budget = StringVar()
usage = StringVar()

BUILDS = StringVar()

arr = []

class Engine(KnowledgeEngine):
    Spec = []
    budget = 0
    CPU =''
    GPU =''
    MB = ''
    HD = ''
    usage1 = ''
    
    def get_budget_usage(self,usage1,budget):
        #self.budget = input("What is your budget? ")
        self.budget = budget
        self.declare(Fact(budget = self.budget))
        #usage = input("What is your usage for the PC? ")
        self.usage1 = usage1
        self.declare(Fact(usage=self.usage1))
        
    
    def getSpec(self,Spec):
        self.Spec = Spec
        counter = 0
        for item in self.Spec:
            if item == '':
                counter = counter +1
                if(counter == 4):
                    self.declare(Fact(allclear = True))
        if(counter < 4):
            self.declare(Fact(allclear = False))
            
    def Display(self,i):
        name = dictlist[i]['name']
        usage = dictlist[i]['usage']
        cpu = dictlist[i]['CPU']
        gpu = dictlist[i]['GPU']
        mb = dictlist[i]['Motherboard']
        hd = dictlist[i]['Hard Drive']
                
        listbox.insert(END,"Name : " + name)
        listbox.insert(END,"Usage : " + usage)
        listbox.insert(END,"CPU : " + cpu)
        listbox.insert(END,"GPU : " + gpu)
        listbox.insert(END,"Motherboard : " + mb)
        listbox.insert(END,"Hard Drive : " + hd)
        listbox.insert(END,"\n_____________________________________________________________________________________\n")

    @Rule(OR(~Fact(CPU=W()),
             ~Fact(GPU=W()),
             ~Fact(HardDrive=W()),
             ~Fact(Motherboard=W())))
    def defRules(self):
        for word in self.Spec:
            if word in CPU_dict.keys():
                self.CPU = word
                self.declare(Fact(CPU=word))
            if word in GPU_dict.keys():
                self.GPU = word
                self.declare(Fact(GPU=word))
            if word in HardDrive_dict.keys():
                self.HD = word
                self.declare(Fact(HardDrive=word))
            if word in Motherboard_dict.keys():
                self.MB = word
                self.declare(Fact(Motherboard=word))
            
    @Rule(AND(Fact(usage='Gaming'),
             ~Fact(CPU=W()),
             ~Fact(GPU=W()),
             ~Fact(HardDrive=W()),
             ~Fact(Motherboard=W()),
             Fact(allclear = True)))
    def showgaming(self):
        for i in range(len(dictlist)):
            if 'Gaming' in dictlist[i]['usage']:
                self.Display(i)
                
    
    @Rule(AND(Fact(usage='Education'),
             ~Fact(CPU=W()),
             ~Fact(GPU=W()),
             ~Fact(HardDrive=W()),
             ~Fact(Motherboard=W()),
             Fact(allclear = True)))
    def showedu(self):
        for i in range(len(dictlist)):
            if 'Education' in dictlist[i]['usage']:
                self.Display(i)
    
    @Rule(AND(Fact(usage='Internet'),
             ~Fact(CPU=W()),
             ~Fact(GPU=W()),
             ~Fact(HardDrive=W()),
             ~Fact(Motherboard=W()),
             Fact(allclear = True)))
    def showinternet(self):
        for i in range(len(dictlist)):
            if 'Internet' in dictlist[i]['usage']:
                self.Display(i)
    
    @Rule(AND(Fact(CPU=W()),
              NOT(Fact(GPU=W())),
              NOT(Fact(Motherboard=W())),
              NOT(Fact(HardDrive=W())),
              Fact(budget=W())))
    def build1(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.CPU in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(CPU_dict[self.CPU])
                cost += (int(Motherboard_dict[dictlist[i]['Motherboard']]) + 
                        int(HardDrive_dict[dictlist[i]['Hard Drive']]) + int(GPU_dict[dictlist[i]['GPU']]))
                if cost <= int(self.budget):
                    self.Display(i)
    
    @Rule(AND(NOT(Fact(CPU=W())),
              Fact(GPU=W()),
              NOT(Fact(Motherboard=W())),
              NOT(Fact(HardDrive=W())),
              Fact(budget=W())))
    def build2(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.GPU in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(GPU_dict[self.GPU])
                cost += (int(Motherboard_dict[dictlist[i]['Motherboard']]) + 
                        int(HardDrive_dict[dictlist[i]['Hard Drive']]) + int(CPU_dict[dictlist[i]['CPU']]))
                if cost <= int(self.budget):
                    self.Display(i)
                    
    @Rule(AND(NOT(Fact(CPU=W())),
              NOT(Fact(GPU=W())),
              Fact(Motherboard=W()),
              NOT(Fact(HardDrive=W())),
              Fact(budget=W())))
    def build3(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.MB in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(Motherboard_dict[self.MB])
                cost += (int(GPU_dict[dictlist[i]['GPU']]) + 
                        int(HardDrive_dict[dictlist[i]['Hard Drive']]) + int(CPU_dict[dictlist[i]['CPU']]))
                if cost <= int(self.budget):
                    self.Display(i)
    
    
    @Rule(AND(NOT(Fact(CPU=W())),
              NOT(Fact(GPU=W())),
              NOT(Fact(Motherboard=W())),
              Fact(HardDrive=W()),
              Fact(budget=W())))
    def build4(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.HD in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(HardDrive_dict[self.HD])
                cost += (int(GPU_dict[dictlist[i]['GPU']]) + 
                        int(Motherboard_dict[dictlist[i]['Motherboard']]) + int(CPU_dict[dictlist[i]['CPU']]))
                if cost <= int(self.budget):
                    self.Display(i)
    
    @Rule(AND(Fact(CPU=W()),
              Fact(GPU=W()),
              NOT(Fact(Motherboard=W())),
              NOT(Fact(HardDrive=W())),
              Fact(budget=W())))
    def build12(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.CPU in dictlist[i].values() and self.GPU in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(CPU_dict[self.CPU]) + int(GPU_dict[self.GPU])
                cost += int(Motherboard_dict[dictlist[i]['Motherboard']]) + int(HardDrive_dict[dictlist[i]['Hard Drive']])
                if cost <= int(self.budget):
                    self.Display(i)
    
    @Rule(AND(NOT(Fact(CPU=W())),
              NOT(Fact(GPU=W())),
              Fact(Motherboard=W()),
              Fact(HardDrive=W()),
              Fact(budget=W())))
    def build34(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.MB in dictlist[i].values() and self.HD in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(HardDrive_dict[self.HD]) + int(Motherboard_dict[self.MB])
                cost += int(CPU_dict[dictlist[i]['CPU']]) + int(GPU_dict[dictlist[i]['GPU']])
                if cost <= int(self.budget):
                    self.Display(i)
    
    @Rule(AND(Fact(CPU=W()),
              NOT(Fact(GPU=W())),
              Fact(Motherboard=W()),
              NOT(Fact(HardDrive=W())),
              Fact(budget=W())))
    def build13(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.MB in dictlist[i].values() and self.CPU in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(Motherboard_dict[self.MB]) + int(CPU_dict[self.CPU])
                cost += int(GPU_dict[dictlist[i]['GPU']]) + int(HardDrive_dict[dictlist[i]['Hard Drive']])
                if cost <= int(self.budget):
                    self.Display(i)
    
    @Rule(AND(NOT(Fact(CPU=W())),
              Fact(GPU=W()),
              NOT(Fact(Motherboard=W())),
              Fact(HardDrive=W()),
              Fact(budget=W())))
    def build24(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.GPU in dictlist[i].values() and self.HD in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(GPU_dict[self.GPU]) + int(HardDrive_dict[self.HD])
                cost += int(CPU_dict[dictlist[i]['CPU']]) + int(Motherboard_dict[dictlist[i]['Motherboard']])
                if cost <= int(self.budget):
                    self.Display(i)
    
    @Rule(AND(Fact(CPU=W()),
              NOT(Fact(GPU=W())),
              NOT(Fact(Motherboard=W())),
              Fact(HardDrive=W()),
              Fact(budget=W())))
    def build14(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.CPU in dictlist[i].values() and self.HD in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(CPU_dict[self.CPU]) + int(HardDrive_dict[self.HD])
                cost += int(GPU_dict[dictlist[i]['GPU']]) + int(Motherboard_dict[dictlist[i]['Motherboard']])
                if cost <= int(self.budget):
                    self.Display(i)
    
    @Rule(AND(NOT(Fact(CPU=W())),
              Fact(GPU=W()),
              Fact(Motherboard=W()),
              NOT(Fact(HardDrive=W())),
              Fact(budget=W())))
    def build23(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.GPU in dictlist[i].values() and self.MB in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(GPU_dict[self.GPU]) + int(Motherboard_dict[self.MB])
                cost += int(CPU_dict[dictlist[i]['CPU']]) + int(HardDrive_dict[dictlist[i]['Hard Drive']])
                if cost <= int(self.budget):
                    self.Display(i)
    
    @Rule(AND(Fact(CPU=W()),
              Fact(GPU=W()),
              Fact(Motherboard=W()),
              NOT(Fact(HardDrive=W())),
              Fact(budget=W())))
    def build123(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.GPU in dictlist[i].values() and self.MB in dictlist[i].values() and self.CPU in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(GPU_dict[self.GPU]) + int(Motherboard_dict[self.MB]) + int(CPU_dict[self.CPU])
                cost += int(HardDrive_dict[dictlist[i]['Hard Drive']])
                if cost <= int(self.budget):
                    self.Display(i)
                    
    @Rule(AND(NOT(Fact(CPU=W())),
              Fact(GPU=W()),
              Fact(Motherboard=W()),
              Fact(HardDrive=W()),
              Fact(budget=W())))
    def build234(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.GPU in dictlist[i].values() and self.MB in dictlist[i].values() and self.HD in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(GPU_dict[self.GPU]) + int(Motherboard_dict[self.MB]) + int(HardDrive_dict[self.HD])
                cost += int(CPU_dict[dictlist[i]['CPU']])
                if cost <= int(self.budget):
                    self.Display(i)
     
    
    @Rule(AND(Fact(CPU=W()),
              NOT(Fact(GPU=W())),
              Fact(Motherboard=W()),
              Fact(HardDrive=W()),
              Fact(budget=W())))
    def build134(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.CPU in dictlist[i].values() and self.MB in dictlist[i].values() and self.HD in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(CPU_dict[self.CPU]) + int(Motherboard_dict[self.MB]) + int(HardDrive_dict[self.HD])
                cost += int(GPU_dict[dictlist[i]['GPU']])
                if cost <= int(self.budget):
                    self.Display(i)
    
    @Rule(AND(Fact(CPU=W()),
              Fact(GPU=W()),
              NOT(Fact(Motherboard=W())),
              Fact(HardDrive=W()),
              Fact(budget=W())))
    def build124(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.GPU in dictlist[i].values() and self.CPU in dictlist[i].values() and self.HD in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(GPU_dict[self.GPU]) + int(CPU_dict[self.CPU]) + int(HardDrive_dict[self.HD])
                cost += int(Motherboard_dict[dictlist[i]['Motherboard']])
                if cost <= int(self.budget):
                    self.Display(i)
                    
    
    @Rule(AND(Fact(CPU=W()),
              Fact(GPU=W()),
              Fact(Motherboard=W()),
              Fact(HardDrive=W()),
              Fact(budget=W())))
    def build1234(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if (self.GPU in dictlist[i].values() and self.CPU in dictlist[i].values() 
                and self.HD in dictlist[i].values() and self.MB in dictlist[i].values()) and dictlist[i]["usage"] == self.usage1:
                cost += int(GPU_dict[self.GPU]) + int(CPU_dict[self.CPU]) + int(HardDrive_dict[self.HD]) + int(Motherboard_dict[self.MB])
                if cost <= int(self.budget):
                    self.Display(i)                        
    
def build():
    CPU = entry2.get()
    GPU = entry3.get()
    HD = entry4.get()
    MB = entry5.get()
    budget = entry1.get()
    usage1 = dropDown.get()
    
    arr.append(CPU)
    arr.append(GPU)
    arr.append(HD)
    arr.append(MB)
    print(dropDown.get())
    engine = Engine()
    engine.reset()
    engine.getSpec(arr)
    engine.get_budget_usage(usage1,budget)
    engine.run()
    print(engine.facts)
    
topFrame = Frame(root, width=720, height=480)
topFrame.pack(fill = X)

LEFTFRAME = Frame(topFrame, width=360, height=400, bd=1, relief="ridge")
LEFTFRAME.pack(side=LEFT, padx=10, pady=10)

label1 = Label(LEFTFRAME, font=('arial', 12, 'bold'),text="Usage : ", width=10,anchor="w", justify=LEFT)
label1.pack(pady=5)

dropDown = StringVar(root)
dropDown.set("Gaming")
combobox = ttk.Combobox(LEFTFRAME,textvariable = dropDown)
combobox.pack(padx=10, pady=5)
combobox.config(values = ('Gaming','Internet','Education'))


label2 = Label(LEFTFRAME, font=('arial', 12, 'bold'), bd=5,text="Budget : ",width=10,anchor="w", justify=LEFT)
label2.pack(pady=5)
entry1 = ttk.Entry(LEFTFRAME,width=30)
entry1.pack(padx=10, pady=10)
entry1.insert(0,"Enter your budget $")

label3 = Label(LEFTFRAME, bd=5,text="CPU : ",width=10,anchor="w", justify=LEFT)
label3.pack()
entry2 = ttk.Entry(LEFTFRAME,width=30)
entry2.pack(padx=10, pady=5)
entry2.insert(0,"")

label4 = Label(LEFTFRAME, bd=5,text="GPU : ",width=10,anchor="w", justify=LEFT)
label4.pack()
entry3 = ttk.Entry(LEFTFRAME,width=30)
entry3.pack(padx=10, pady=5)
entry3.insert(0,"")

label5 = Label(LEFTFRAME, bd=5,text="Hard Drive : ",width=10,anchor="w", justify=LEFT)
label5.pack()
entry4 = ttk.Entry(LEFTFRAME,width=30)
entry4.pack(padx=10, pady=5)
entry4.insert(0,"")

label6 = Label(LEFTFRAME, bd=5,text="Motherboard : ",width=10,anchor="w", justify=LEFT)
label6.pack()
entry5 = ttk.Entry(LEFTFRAME,width=30)
entry5.pack(padx=10, pady=5)
entry5.insert(0,"")

button1 = ttk.Button(LEFTFRAME, text = "Build!")
button1.pack(padx=10, pady=15)
button1.config(command=build)


RIGHTFRAME = Frame(topFrame, width=360, height=400, bd=1, relief="ridge")
RIGHTFRAME.pack(side=LEFT, padx=10, pady=10, fill=BOTH)
RIGHTLABEL = Label(RIGHTFRAME, font=('arial', 12, 'bold'), bd=5,text="Avalible Builds :", anchor=E)
RIGHTLABEL.pack()

scrollbar = Scrollbar(RIGHTFRAME)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(RIGHTFRAME, yscrollcommand=scrollbar.set, width = "300")
listbox.pack(side=LEFT, fill=BOTH,padx=10, pady=15)

scrollbar.config(command=listbox.yview)

root.mainloop()