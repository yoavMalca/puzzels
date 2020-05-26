import socket
import select
import sys
import PIL
from PIL import Image,ImageTk
import tkinter as tk
import random
import time
import msvcrt as m
import math 
import sqlite3
server_socket=socket.socket()
server_socket.bind(('0.0.0.0',8820))
server_socket.listen(5)
open_client_sockets=[]
messages_to_send=[]
numm=0
file_location="watermelon.jpg"


conn = sqlite3.connect('game.db')
num = random.randrange(0, 4)
cursor = conn.execute("SELECT * from yoav")
rows = cursor.fetchall()
theRow = rows[num]
image = theRow[0]







class game:
    def __init__(self,ImageObject,open_client_sockets):
        self.ImageObject=ImageObject# תמונת פתירת הפאזל
        self.open_client_sockets=open_client_sockets# רשימת השחקנים המשתתפים
        mix=self.mixing_numbers()#המיקום של כל חתיכה בפאזל כפי שהיא נשלחת ללקוח
        self.items=[[]]#רשימת חלקי הפאזל המעורביםכפי שהם קיבלו ברנדומליות במיקס 
        self.empty=[]# רשימת החלקים המתקבלת כל  פעם מהלקוחות
        
        #מכניסים את הערכים של מיקס לתוך אייטמס
        for i in range (len(mix)):
            for t in range (len(mix[i])):
                self.items[i].append(mix[i][t])
            self.items.append([])
                
    #פעולת ההתחלה בה השרת שולח לכל אחד מהלקוחות מה הם החלקים שלהם     
    def start1(self):
        
        wlist=self.open_client_sockets
        
        for g in range (len(wlist)):
            sender=""
            if wlist[0]!=wlist[1]:
                mix=self.to_send(g)
                for i in range (len(mix)):
                    for t in range(len(mix[i])):
                        if t!=(len(mix[i])-1):
                            sender=sender+str(mix[i][t][0])+","+str(mix[i][t][1])+"/r/n"
                        else:
                            sender=sender+str(mix[i][t][0])+","+str(mix[i][t][1])
                    if i!=(len(mix)-1):   
                        sender=sender+"|||"
                wlist[g].send(sender.encode())
    #תפעולת המשחק עצמו השרת יקבל כל תור את המידע מאחד מהלקוחות וימיר אותו לשורת טקסט בצורה שבה הלקוח יבין וישלח את המידע לשני הלקוחות 
    def play(self):
    
        global server_socket
       
        
        chachaw=False
        for socket in self.open_client_sockets:
            messages_to_send=[]
            #socket.send("your turn".encode())
            #while (True):
            string=socket.recv(1024).decode()
            if string=="game_over":
                for yoav_socket in self.open_client_sockets:
                    if yoav_socket!=socket:
                        yoav_socket.send("game_over".encode())
                quit()
            if string=="you_lost":
                for yoav_socket in self.open_client_sockets:
                    if yoav_socket!=socket:
                        yoav_socket.send("you_lost".encode())
                quit()
            if (string!=''):
                arr=string.split("/r/n")
                x=arr[0]
                y=arr[1]
                x1=arr[2]
                y1=arr[3]
                tupl=(x,y,x1,y1)
                
                for ttt in self.empty:
                    chachaw=False
                    #if x1 in ttt and y1 in ttt:
                        #chachaw=True
                if chachaw==False and tupl not in self.empty:
                    self.empty.append(tupl)
                #break
            string1=""
            for tup in self.empty:
                
                
                string1=string1+"/r/n"+tup[2]+","+tup[3]+"|"+tup[0]+","+tup[1]
            messages_to_send.append((socket,string1))   
            self.send_waiting_messages1(self.open_client_sockets,messages_to_send)
    # פעולת ההכנה לשליחה של חלקי הפאזל ללקוח שולחת לשחקן הראשון חצי ולשחקן השני חצי מהחלקים המעורבבים במיקס                 
    def to_send(self,name):
        global numm
        half=int(numm/2)
        if numm%2==0:
            if name ==0:
                mix=[[]]
                for i in range (half):
                    for t in range (numm):
                        mix[i].append(self.items[i][t])
                    mix.append([])
                mix.append([])
                return mix
            elif name==1:
                mix1=[[]]
                for i in range (half,numm):
                    for t in range (numm):
                        mix1[i-half].append(self.items[i][t])
                    mix1.append([])
                mix1.append([])
                return mix1
        else: 
            half_down=math.floor(numm/2)
            if (name==0):
                
                mix=[[]]
                for i in range (half_down):
                    for t in range (numm):
                        mix[i].append(self.items[i][t])
                    mix.append([])
                mix.append([])
                for t in range (half_down):
                    mix[half_down].append(self.items[half_down][t])
                return mix 
            elif(name==1):
                mix1=[[]]
                for i in range (half_down+1,numm):
                    for t in range (numm):
                        mix1[i-half_down-1].append(self.items[i][t])
                    mix1.append([])
                mix1.append([])
                for k in range (half_down,numm):
                    popai=self.items[half_down][k]
                    mix1[half_down].append(popai)
                
                return mix1 
    #פעולה היוצרת עירבוב של מיקומים במערך דו מימדי 
    def mixing_numbers(all_image):
        list1=[[]]
        list1.append([])
        list2=[]
        for i in range (numm): 
            for t in range(numm):
                list1[i].append(t)
            list1.append([])
        
        for i in range (numm):
            list2.append(i)
        mix=[[]]
        Flag = False
        for i in range (numm):
            for t in range (numm):
                mix[i].append(None)
            mix .append([])
        for i in range(numm):
            for f in range (numm):
                
                while (Flag==False):
                
                    y=random.choice(list2)
                    m=random.choice(list1[y])
                    
                    
                    list1[y].remove(m)
                    
                    if(len(list1[y])==0):
                        list2.remove(y)
                    
                    
                    if mix[i][f]==None:
                        
                        mix[i][f]=(y,m)
                        Flag=True
                    else:
                        print ("byyyyyy")
                    

                   
                Flag=False		
                
        return mix  
        
        
    #פעולה המקבלת רשימה של הודעות  ושולחת אותן ללקוחות השונים        
    def send_waiting_messages1(self,wlist, messages_to_send):
        for message in messages_to_send:
            (client_socket, data) = message
            
            # if it possible to write to the socket
            
            for my_socket in self.open_client_sockets:
                if my_socket!=client_socket:
                    my_socket.send(data.encode())
                if my_socket==client_socket:
                    print ("")
            messages_to_send.remove(message)
#פעולה המקבלת רשימה של הודעות  ושולחת אותן ללקוחות השונים        
def send_waiting_messages(wlist, messages_to_send):
    for message in messages_to_send:
        (client_socket, data) = message
        
        # if it possible to write to the socket
        if client_socket in wlist:
            client_socket.send(data.encode())
            messages_to_send.remove(message)
sent=False
preperd=[]
waiting=False
while (not sent):
    rlist,wlist,xlist=select.select([server_socket]+open_client_sockets,open_client_sockets,[])
    
    for current_socket in rlist:
        # אם לקוח הוא לקוח חדש יצטרף לתוך רדשימת הלקוחות הפתוחים 
        if current_socket is server_socket:
            (new_socket,adress)=server_socket.accept()
            if new_socket not in open_client_sockets:
                open_client_sockets.append(new_socket)
                new_socket.send(str(len(open_client_sockets)).encode())
                if (len(open_client_sockets)!=1):
                    new_socket.send(str(numm).encode())
                if len(open_client_sockets)==1:
                    
                    numm=open_client_sockets[0] .recv(1024).decode()
                    numm=int(numm)
                    
           
        else:
            
            # read the data from the client
            data = current_socket.recv(1024)
            
            #אם אחד הלקוחותישלח את מילת הקוד אז השרת ישלח לו אותה חזרה 
            if (data.decode()=="sendme" and len(open_client_sockets)==2):
                for ha_socket in open_client_sockets:
                        ha_socket.send("sendme".encode())
            #אחרי שהלקוחקיבלאת מילת הקוד הוא ישלח שהוא מוכן לקבל את התמונה ואז השרת ישלח לו את תמונת הפאזל             
            if data.decode()=="ready":
                preperd.append(current_socket)
                waiting=True
                
            if(len(preperd)==len(open_client_sockets)):
                with open(file_location, 'rb') as filesent:
                    data = filesent.read()
                    file_len = len(data)

                    msg_data1 = file_len
                    msg = str(msg_data1)
                    
                    msg = msg.encode('latin-1')
                    for socket in open_client_sockets:
                        socket.send(msg)
                    #data = data.encode('latin-1')
                    for socket in open_client_sockets:
                        if socket in wlist:
                            socket.sendall(data)
                            
                     #wait here untill finish to send the whole fil
                    sent=True#מסמן שהשליחהקרתה ומפסיק את הלולאה ויתחיל את המשחק
                    
            
            
            
            
            
            
            
            elif(waiting==False):
                for the_socket in open_client_sockets:
                
                    # add the message from the client to the list of the messages that weren't sent
                    messages_to_send.append((the_socket, data.decode()))
      
    send_waiting_messages(wlist,messages_to_send)
imageObject=Image.open(file_location)

g1=game(imageObject,open_client_sockets)
#שליחה ללקוחות את רשימת החלקים שלהם 
g1.start1()
while True:
#תחילת המשחק 
    g1.play()