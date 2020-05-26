import socket
import msvcrt
import select
import PIL
from PIL import Image,ImageTk,ImageDraw, ImageFilter
import tkinter as tk
import random
import time
import msvcrt as m
my_socket = socket.socket()
ip=input("enter the ip")
port=input("entee port")
my_socket.connect(("ip",int(port)))
LARGE_FONT= ("Verdana", 12)
sent1=False
xxx1=-1
yyy1=-1
numm =0
starter=False
class new_but:
    def __init__(self,image1,root,g,b,okVar,xxx,yyy):
        self.Butt=tk.Button(root, image = image1,command=lambda:self.ret_tup(okVar,xxx,yyy))
        self.image=image1#התמונה הנמצאתבכפתור 
        self.tup=(g,b)#מיקום כל כפתור 
        self.okVar=okVar# משתנה המודיע על לחיצת הכפתור 
    # משתנה המחזיר את הכפתור 
    def ret_but(self):
        return self.Butt
    #מחזיר את תהמונה הכפתור 
    def ret_img(self):
        return self.image
    # מחזיר את מיקום הכפתור 
    def ret_tup(self,okVar,xxx,yyy):
        okVar.set(1)
        global xxx1#מיקום הכתור הלחוץ כרגע 
       
        global yyy1#מיקום הכפתור הלחוץ כרגע 
        xxx1=self.tup[0]
        yyy1=self.tup[1]
        return self.tup
# פעולת קבלת הסדר של המחסן בתחילת המשחק 
def start_game(string):
    order=[[]]
    arr=string.split("|||")
    
    for i in range(len(arr)):
        tup=arr[i].split("/r/n")
       
        for t in range (len(tup)):
            if tup[t]!="":
                x=tup[t].split(",")[0]
                #print ("x",x)
                y=tup[t].split(",")[1]
               
                #print ("y:",y)
                x=int(x)
                y=int(y)
                order[i].append((x,y))
        order.append([])
    return order 
def starting_window():
    start_wind=tk.Tk()
    canvas1 = tk.Canvas(start_wind, width = 400, height = 300,  relief = 'raised')
    canvas1.pack()

    label1 = tk.Label(start_wind, text='hello welcome to puzzles ')
    label1.config(font=('helvetica', 14))
    canvas1.create_window(200, 25, window=label1)

    label2 = tk.Label(start_wind, text='enter how many parts you want in a row ')
    label2.config(font=('helvetica', 10))
    canvas1.create_window(200, 100, window=label2)

    entry1 = tk.Entry (start_wind) 
    
    canvas1.create_window(200, 140, window=entry1)
    
    button1 = tk.Button(text='submit the answer', command=lambda: submit(entry1,start_wind), bg='brown', fg='white', font=('helvetica', 9, 'bold'))
    canvas1.create_window(200, 180, window=button1)
    start_wind.mainloop()
#פעולה המופעלת מתוך לחיצת הכפתור ומקבלת את הטקס שהוקלד בתוך תיבת הטקסט ומעדכנת את מספר החלקים לפיו 
def submit (entry1,star_wind):
    global numm
   
    numm = entry1.get()
    numm=int(numm)
    star_wind.destroy()
    


class client:
    def __init__(self,imageObject,order,server_socket,starter):
        self.items=[[]]#מערך דו מימדי המכיל את כל החלקים 
        self.imageObject=imageObject#שם תמונת הפאזל
        self.all_image=self.crop_Array(imageObject)# התמונה הראשונית מחלוקת לחלקים 
        self.items=[[]]#מחסן המשתמשים 
        self.server_socket=server_socket
        self.root=tk.Tk()#חלון הגרפיקה
        self.lastdata=""
        self.starter=starter
        self.forgotten=[]# רשימת החלקים שבהם עשינו שימוש במהלך המשחק
        self.anotherone=[]# רשימת  החלקים המופיע על לוח הפאזל ואיזה חלקים אלו 
        for i in range(len(order)):
            for t in range (len(order[i])):
                x1,y1=order[i][t]
                self.items[i].append((self.all_image[x1][y1],(x1,y1)))
            self.items.append([])
        self.transparenty=self.crop_Array(self.make_trans())
    #פעולה הלוקחת תמונה וחותכת אותה לחלק    
    def image_crop(self,x1,y1,imageObject): 	
        cropped = imageObject.crop((x1,y1,x1+(imageObject.size[0]/numm),y1+imageObject.size[1]/numm))
        return cropped
    #פעולה המפענחת את המיגע המתקבל מהלקוח ומעדכנת את רשימת הנוכחים על המסך 
    def make_trans(self):
        im_rgba = self.imageObject.copy()
        im_rgba.putalpha(10)
        im_rgba.show()
        return im_rgba
    
    def handling_server_msg(self,string):
        self.anotherone=[]
        global numm
        images=[[]]
        for i in range (numm):
            images.append([])
            for t in range (numm): 
                images[i].append("x")
            
        
        tuple_Array=string.split("/r/n")
        
        print (self.anotherone)
        for tup in tuple_Array:
            if(tup!=""):
                print ("tup:"+tup)
                arr=tup.split("|")
                x=arr[0].split(",")[0]
                y=arr[0].split(",")[1]
                x1=arr[1].split(",")[0]
                y1=arr[1].split(",")[1]
                if (len(x)>1):
                    x=x[1]
                if (len(y)>1):
                    y=y[1]
                if (len(y1)>1):
                    y1=y1[1]
                if(len(x1)>3):
                    x1=x1[1]
                if int(x)<numm and int(y)<numm and int(x1)<numm and int(y1)<numm:
                    x=int(x)
                    y=int(y)
                    x1=int(x1)
                    y1=int(y1)
                    images[x][y]=(x1,y1)
                    tapir=((x,y),(x1,y1))
                    if tapir not in self.anotherone:
                        self.anotherone.append(tapir)
        
       
       
    # הפעולה היוצרת את הלוח הראשוני ומוסיפה אליו את התמונות ואת הכפתורים יוצרת רשימה של כפתורים ואת מסך המחסן 
    def create_panel(self):
        img=[[]]
        mix=self.items
        
        for label in self.root.grid_slaves():
                    
            label.config(image="",background="black")
                        
                    
        all_image=[[]]
        for i in range (len(mix)):
            for t in range (len(mix[i])):
                all_image[i].append(mix[i][t][0])
        
            all_image.append([])
        for i in range (len(all_image)):
            for t in range (len(all_image[i])):
                
                img[i].append(ImageTk.PhotoImage(all_image[i][t]))
                
                
            img.append([])
            
        global okVar
        
        xxx1=-1
        yyy1=-1
        okVar = tk.IntVar()
        panel=[[]] 
        for g in range(len(img)):
            for b in range (len(img[g])):
                    
                    panel[g].append(new_but(img[g][b],self.root,g,b,okVar,xxx1,yyy1))
                    
                    panel[g][b].ret_but().grid(row=g,column=b)
            panel.append([])
        for label in self.root.grid_slaves():
                    kkk=(int(label.grid_info()["row"]),int(label.grid_info()["column"]))
                    if (kkk in self.forgotten):
                        flag=True 
                        # label.destroy()
                    # if(kkk[0]>=len(panel)):
                       # label.destroy()
                    
                    # if(kkk[1]>=len(panel[len(panel[kkk[0]])-1])):
                        # label.destroy()
        if self.starter==False:
            data=self.server_socket.recv(1024)
            if data.decode()=="game_over":
                self.root.destroy()
                win_wind=tk.Tk()
                            
                label1 = tk.Label(win_wind, text='you wonnnnnnn!!')
                label1.pack()
                win_wind.mainloop()
                quit()
            if data.decode()=="you_lost":
                self.root.destroy()
                win_wind=tk.Tk()
                            
                label1 = tk.Label(win_wind, text='you')
                label1.pack()
                win_wind.mainloop()
                quit()
            #if data.decode()!='':
            self.check(data.decode())
            self.handling_server_msg(data.decode())
                #break             
            self.lastdata=self.lastdata+data.decode()

        self.root.after(10,self.game)
        self.root.mainloop()    
    #פעולה הבודקת האם המשתתפים סיימו את הפאזל 
    def check(self,string):
        tuple_Array=string.split("/r/n")
        won =True
        counter=0
        if won==True:
            for tup in tuple_Array:
                if(tup!=""):
                    arr=tup.split("|")
                    x3=arr[0].split(",")[0]
                    y3=arr[0].split(",")[1]
                    x4=arr[1].split(",")[0]
                    y4=arr[1].split(",")[1]
                   
                    counter=counter+1
                    if (x3,y3)!=(y4,x4):
                        won = False
                        print ("you lost")
                        self.server_socket.send("you_lost".encode())
                        self.root.destroy()
                        win_wind=tk.Tk()
                                        
                        label1 = tk.Label(win_wind, text='you lost:(')
                        label1.pack()
                        win_wind.mainloop()
                        quit()
        if (counter <(numm*numm)):
            
            won= False
        if (won==True):
            
            self.server_socket.send("game_over".encode())
            self.root.destroy()
            win_wind=tk.Tk()
                            
            label1 = tk.Label(win_wind, text='you wonnnnnnn!!')
            label1.pack()
            win_wind.mainloop()
            quit()
        

    #פעולה היוצרת מערך של תמונות חתוכות אשר משלימות את התמונה 
    def crop_Array(self,imageObject):
        x1=0
        y1=0
        all_image=[[]]
        global numm
        for i in range (numm):
            for t in range (numm):
                
                all_image[i].append(self.image_crop(x1,y1,imageObject))
                y1=y1+(imageObject.size[1]/numm)
            y1=0
            x1=x1+(imageObject.size[0]/numm)
            all_image.append([])
        return all_image
    #פעולה המחזירה את רשימת ה items
    def show_items(self):

        return self.items
    #הפעולה שבה בעצם קורה המשחק מחכה ללחיצת השחקן על התמונה ואז משנה את המסך למסך לוח הפאזל ומחכה לכך שיבחר מיקום על המסך ואחרי הבחירה שלו מחזירה למסך המחסן 
    #ושולחת את המידע על התזוזה לשרת 
    def game(self):
        socket=self.server_socket
        
        
        
       
        

            
                
        flag=False
        global okVar
        num=0
        banana=[[]]
        self.root.wait_variable(okVar)
        del okVar
        okVar=tk.IntVar()
        print (self.anotherone)
        while (flag==False):
            i=xxx1
            t=yyy1
            for a in range(len(self.all_image)):  
                for n in range(len(self.all_image[a])):
                    banana[a].append(self.all_image[a][n])
                banana.append([])
                
            
            for y in range (len(banana)):
                for m in range (len(banana[y])):
                    for choice in self.anotherone:
                        if (y,m)==choice[0]:
                            (s,h)=choice[1]
                            
                            banana[y][m]=self.all_image[s][h]
                            banana[s][h]=self.all_image[y][m]
            
            img=[[]]
            for o in range (numm):
                for c in range (numm):
                    
                    img[o].append(ImageTk.PhotoImage(banana[o][c]))   
                img.append([])
                    
            for g in range(numm):
                for b in range (numm):
                        
                        panel = new_but(ImageTk.PhotoImage(self.transparenty[g][b]),self.root,b,g,okVar,xxx1,yyy1)
                        
                        panel.ret_but().grid(row=b,column=g)
            for label in self.root.grid_slaves():
                        flagy=False
                        (s,h)= (int(label.grid_info()["row"]),int(label.grid_info()["column"]))
                        
                        for choice1 in self.anotherone:
                            if (s,h)==choice1[0]:
                                label.config(image=img[s][h])
            
            self.root.wait_variable(okVar)
            del okVar
            x1=xxx1
            y1=yyy1
            self.forgotten.append((i,t))
            try:
                for label in self.root.grid_slaves():
                    kkk=(int(label.grid_info()["row"]),int(label.grid_info()["column"]))
                    if (kkk in self.forgotten):
                        flag=True 
                        ##label.config(image="",background="black")
                        if (kkk==(i,t)):
                            str1=(str(self.items[i][t][1][0])+"/r/n"+str(self.items[i][t][1][1])+"/r/n"+str(x1)+"/r/n"+str(y1))
                socket.send(str1.encode())
                    
                if flag==False:
                    print("")
            except:
                print ("your numbers were wrongggggggggggggggggggggggggggggggggggg")
        
        
        if self.starter==True:
            #while True:
            data=socket.recv(1024)
            if data.decode()=="game_over":
                self.root.destroy()
                win_wind=tk.Tk()
                            
                label1 = tk.Label(win_wind, text='you wonnnnnnn!!')
                label1.pack()
                win_wind.mainloop()
                quit()
            if data.decode()=="you_lost":
                self.root.destroy()
                win_wind=tk.Tk()
                            
                label1 = tk.Label(win_wind, text='you lost :(')
                label1.pack()
                win_wind.mainloop()
                quit()
            if data.decode()!='':
                self.check(data.decode())
                self.handling_server_msg(data.decode())
                #break

            self.lastdata=self.lastdata+data.decode()
        
        self.create_panel()
       
baa=int(my_socket.recv(1024).decode())
if(baa==1):
    starter=True
    starting_window()
    my_socket.send(str(numm).encode())
else:
    numm=int(my_socket.recv(1024).decode())
#f = open('torecv.jpg','wb')
my_socket.send("sendme".encode())
while(sent1==False):
# select
    rlist, wlist, xlist = select.select([my_socket], [my_socket], [])

    word = ('')
    send = False
    # waiting for a key press
    while msvcrt.kbhit() and sent1==False:
        # input the command
        char=msvcrt.getch()  
        word=char.decode()
        # input the message
        while ord(char) != 13 and sent1==False:
            char = msvcrt.getch()
            
            if ord(char) != 13:
                word = word + char.decode()
        send = True
        
        if send:
            val =  word
            if my_socket in wlist:
                my_socket.send(val.encode())
        
            
         
                
        
        
    if my_socket in rlist and sent1==False:
       
      
        data = my_socket.recv(1024)
        #תהליך קבלת התמונה מהשרת 
        if (data.decode()=="sendmesendme"):
            
            my_socket.send("ready".encode())
            sent1=True
            file_len=my_socket.recv(1024)
            file_len=int(file_len)
            cnt = 0
            msg11 = b""
            while cnt < file_len:
                data = my_socket.recv(file_len)  #in some computers we need to collect the whole data in lot of packets
                #data = data.decode('latin-1')
                    
                
                msg11 = msg11 + data
                cnt = cnt + len(data)
            data = msg11
            sent1=True
            with open("client_File.jpg" , 'wb') as filesent:
                filesent.write(data)
            sent1=True
            
        
while True:
    data=my_socket.recv(1024)
    if(data.decode()!=""):
        order=start_game(data.decode())
        break
imageObject=Image.open("client_File.jpg")
c1=client(imageObject,order,my_socket,starter)
c1.create_panel()