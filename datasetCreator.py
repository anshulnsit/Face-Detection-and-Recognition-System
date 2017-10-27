# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 17:49:41 2017

@author: LALIT ARORA
"""

import cv2
import sqlite3
import datetime




def check(a):
    conn=sqlite3.connect("data.sqlite")
    c=conn.cursor()
    conn.commit()
    tempe=[]
    for val in c.execute('SELECT * from people WHERE Username=?',(a,)):
        tempe.append(val)
    conn.commit()
    conn.close()
    if len(tempe)==0:
        return "TRUE"
    else:
        return "FALSE"

def counttablerows():
    conn=sqlite3.connect('data.sqlite')
    c=conn.cursor()
    conn.commit()
    count=0
    for val in c.execute("select count(Name) from people"):
        count=int(val[0])
    conn.commit()
    conn.close()
    return count
    
def adddata(a,b,c,d,e):
    inicount=counttablerows()
    conn=sqlite3.connect("data.sqlite")
    c=conn.cursor()
    conn.commit()
    c.execute('INSERT INTO people (Name,Username,Mobile,Email,Id) VALUES (?,?,?,?,?)',(a,b,d,c,e))
    conn.commit()
    fincount=counttablerows()
    if fincount==(inicount+1):
        return "OK"
    else:
        return "ERROR"
    
def takedata():
    now = datetime.datetime.now()
    while True:
    name=input("Enter Your Name: ")
    while True:
        username=input("Enter Username: ")
        if check(username)=="TRUE":
            break
        else:
            print("Username already exists.")
            continue
    mobile=input("Enter your Mobile Number: ")
    email=input("Enter your Email ID: ")
    Id = int(str(now.day)+str(now.microsecond)+str(now.second))
    res=adddata(name,username,email,mobile,Id)
    if res=="OK":
        print("DATA Added Successfully.")
        break
    else:
        print("Error Occured")
        continue
    return Id
    

cam = cv2.VideoCapture(0)
detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

Id=takedata()
#Id=input('Enter Your ID : ')

sampleNum=0
while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        #incrementing sample number 
        sampleNum=sampleNum+1
        #saving the captured face in the dataset folder
        cv2.imwrite("dataSet/User."+str(Id) +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])

        cv2.imshow('Face',img)
    #wait for 100 miliseconds 
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    # break if the sample number is morethan 20
    elif sampleNum>20:
        break
cam.release()
cv2.destroyAllWindows()