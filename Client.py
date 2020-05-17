import socket
import msvcrt
import select
import PIL
from PIL import Image,ImageTk
import tkinter as tk
import random
import time
import msvcrt as m
print ("client begin")
my_socket = socket.socket()
my_socket.connect(("127.0.0.1", 8820))
LARGE_FONT= ("Verdana", 12)
sent1=False
xxx1=-1
yyy1=-1
class new_but:
    def __init__(self,image1,root,g,b,okVar,xxx,yyy):
        self.Butt=tk.Button(root, image = image1,command=lambda:self.ret_tup(okVar,xxx,yyy))
        self.image=image1
        self.tup=(g,b)
        self.okVar=okVar
    def ret_but(self):
        return self.Butt
    def ret_img(self):
        return self.image
    def ret_tup(self,okVar,xxx,yyy):
        okVar.set(1)
        print (self.tup)
        global xxx1
        global yyy1
        xxx1=self.tup[0]
        yyy1=self.tup[1]
        return self.tup
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

class client:
    def __init__(self,name,imageObject,order,server_socket):
        self.name=name
        self.items=[[]]
        self.imageObject=imageObject
        self.all_image=self.crop_Array(imageObject)
        self.items=[[]]
        self.server_socket=server_socket
        self.root=tk.Tk()
        self.lastdata=""
        self.forgotten=[]
        self.anotherone=[]
        for i in range(len(order)):
            for t in range (len(order[i])):
                x1,y1=order[i][t]
                self.items[i].append((self.all_image[x1][y1],(x1,y1)))
            self.items.append([])
    def image_crop(self,x1,y1,imageObject): 	
        cropped = imageObject.crop((x1,y1,x1+(imageObject.size[0]/3),y1+imageObject.size[1]/3))
        return cropped
    
    def handling_server_msg(self,string):
        
        images=[[]]
        for i in range (3):
            images.append([])
            for t in range (3): 
                images[i].append("x")
            
        if(self.check(string)):
            print ("you wonnnnnnnn")
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
                    print("innnnnnnnnn",x[0])
                    x=x[1]
                if (len(y)>1):
                    print("innnnnnnnnn")
                    y=y[1]
                    print 
                if (len(y1)>1):
                    print("innnnnnnnnn",y1[0])
                    y1=y1[1]
                if(len(x1)>3):
                    print("innnnnnnnnn",x1[0])
                    x1=x1[1]
                if int(x)<3 and int(y)<3 and int(x1)<3 and int(y1)<3:
                    x=int(x)
                    y=int(y)
                    x1=int(x1)
                    y1=int(y1)
                    images[x][y]=(x1,y1)
                    tapir=((x,y),(x1,y1))
                    if tapir not in self.anotherone:
                        self.anotherone.append(tapir)
        
       
        
        # num=0
        # banana=[[]]
        
        # for a in range(len(self.all_image)):  
            # for n in range(len(self.all_image[a])):
                # banana[a].append(self.all_image[a][n])
            # banana.append([])
            
        
        # for y in range (len(banana)):
            # for m in range (len(banana[y])):
                # for choice in self.anotherone:
                    # if (y,m)==choice[0]:
                        # (s,h)=choice[1]
                        
                        # banana[y][m]=banana[s][h]
                        # banana[s][h]=self.all_image[y][m]
        
        # img=[[]]
        # for o in range (3):
            # for c in range (3):
                
                # img[o].append(ImageTk.PhotoImage(banana[o][c]))   
            # img.append([])
                
        # for g in range(3):
            # for b in range (3):
                    
                    # panel = tk.Button(self.root, image = img[g][b])
                    
                    # panel.grid(row=b,column=g)
        # for label in self.root.grid_slaves():
                    # flagy=False
                    # (s,h)= (int(label.grid_info()["row"]),int(label.grid_info()["column"]))
                    
                    # for choice1 in self.anotherone:
                        # if (s,h)==choice1[0]:
                            # flagy=True
                    # if flagy==False:
                        # label.config(image="" ,background="black")
        # self.root.after(100,self.create_panel)
        # self.root.mainloop()
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
                    print(g,b)
                    
                    panel[g].append(new_but(img[g][b],self.root,g,b,okVar,xxx1,yyy1))
                    
                    panel[g][b].ret_but().grid(row=g,column=b)
            panel.append([])
        for label in self.root.grid_slaves():
                    kkk=(int(label.grid_info()["row"]),int(label.grid_info()["column"]))
                    if (kkk in self.forgotten):
                        flag=True 
                        #label.config(image='',background="black")
                        
                      
        self.root.after(10,self.game)
        self.root.mainloop()    
    def check(self,string):
        tuple_Array=string.split("/r/n")
        
        for tup in tuple_Array:
            if(tup!=""):
                print ("tup:"+tup)
                arr=tup.split("|")
                x=arr[0].split(",")[0]
                y=arr[0].split(",")[1]
                x1=arr[1].split(",")[0]
                y1=arr[1].split(",")[1]
                if (x,y)!=(x1,y1):
                    return False
        if (len(tuple_Array)<9):
            return False
        return True

        
    def crop_Array(self,imageObject):
        x1=0
        y1=0
        all_image=[[]]
        for i in range (3):
            for t in range (3):
                
                all_image[i].append(self.image_crop(x1,y1,imageObject))
                y1=y1+(imageObject.size[1]/3)
            y1=0
            x1=x1+(imageObject.size[0]/3)
            all_image.append([])
        return all_image
    def show_items(self):

        return self.items
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
                            
                            banana[y][m]=banana[s][h]
                            banana[s][h]=self.all_image[y][m]
            
            img=[[]]
            for o in range (3):
                for c in range (3):
                    
                    img[o].append(ImageTk.PhotoImage(banana[o][c]))   
                img.append([])
                    
            for g in range(3):
                for b in range (3):
                        
                        panel = new_but(img[g][b],self.root,b,g,okVar,xxx1,yyy1)
                        
                        panel.ret_but().grid(row=b,column=g)
            for label in self.root.grid_slaves():
                        flagy=False
                        (s,h)= (int(label.grid_info()["row"]),int(label.grid_info()["column"]))
                        
                        for choice1 in self.anotherone:
                            if (s,h)==choice1[0]:
                                flagy=True
                        if flagy==False:
                            label.config(image="" ,background="black")
            
            self.root.wait_variable(okVar)
            del okVar
            x1=xxx1
            y1=yyy1
            self.forgotten.append((i,t))
            try:
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                for label in self.root.grid_slaves():
                    kkk=(int(label.grid_info()["row"]),int(label.grid_info()["column"]))
                    if (kkk in self.forgotten):
                        flag=True 
                        ##label.config(image="",background="black")
                        if (kkk==(i,t)):
                            str1=(str(self.items[i][t][1][0])+"/r/n"+str(self.items[i][t][1][1])+"/r/n"+str(x1)+"/r/n"+str(y1))
                            socket.send(str1.encode())
                    
                if flag==False:
                    print ("your numbers were wrong")
            except:
                print ("your numbers were wrongggggggggggggggggggggggggggggggggggg")
        
        
        
        while True:
            
            data=socket.recv(1024)
            if data.decode()!='' and data.decode()!=str1:
                print (data)
                self.handling_server_msg(data.decode())
                print ("outttttttttttttttttttttttttt")
                break

        self.lastdata=self.lastdata+data.decode()
        
        self.create_panel()
        


print ('what is your name?')
name = input()
#f = open('torecv.jpg','wb')

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
        #print (word)
        send = True
        print ('')
        
        if send:
            val =  word
            if my_socket in wlist:
                my_socket.send(val.encode())
        
            
         
                
        
        
    if my_socket in rlist and sent1==False:
       
      
        data = my_socket.recv(1024)

        print (data.decode())
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
                    
                #print ("client_rcv_data cnt:{0} len:{1}".format(cnt,len(data)))
                    
                #print (data)
                msg11 = msg11 + data
                cnt = cnt + len(data)
            data = msg11
            sent1=True
            with open("client_File.jpg" , 'wb') as filesent:
                filesent.write(data)
            sent1=True
            
        

print ("*************************************************now we will start *************************")
while True:
    data=my_socket.recv(1024)
    if(data.decode()!=""):
        order=start_game(data.decode())
        break
imageObject=Image.open("client_File.jpg")
c1=client(name,imageObject,order,my_socket)
c1.create_panel()