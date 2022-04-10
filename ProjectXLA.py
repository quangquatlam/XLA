from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
from tkinter import  Label, filedialog as fd
import cv2
import imutils
import numpy as np

root=Tk()
root.geometry("320x650")
root.title('Nhận dạng biểu số xe')


labelInput=ttk.LabelFrame(root,text="Input Image")
labelInput.grid(column = 0, row = 1, padx = 5, pady = 5)

labelPath=ttk.LabelFrame(root,text="Path")
labelPath.grid(column = 0, row = 3, padx = 5, pady = 5)

labelImage=ttk.LabelFrame(root,text="Image")
labelImage.grid(column = 0, row = 4, padx = 5, pady = 5)

labelRun=ttk.LabelFrame(root,text="Run")
labelRun.grid(column = 0, row = 5, padx = 5, pady = 5)

filepath='' 


def Openfile():
    global filepath
    filepath=fd.askopenfilename(initialdir= '/',title = 'select file', filetype = (('jpeg','*.jpg'),('All Files','*.*')))
    showimg=Entry(labelPath,width=50)
    showimg.insert(0,filepath)
    showimg.grid(row=2, column=0, columnspan=50)

    filepath=filepath.replace('/','\\\\')
    print(filepath)
    
    pic = Image.open(filepath)
    resized = pic.resize((300, 300),Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(resized)
    myvar=ttk.Label(labelImage,image = tkimage)
    myvar.image = tkimage
    myvar.grid(column=0, row=4)

def Run():
    if(filepath==''):
        messagebox.showerror('Error','Vui lòng chọn ảnh')
    else:
        max_size = 5000
        min_size = 900

        img = cv2.imread(filepath, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (620, 480))
    
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
        Gray = cv2.bilateralFilter(gray, 11, 17, 17)  
        edged = cv2.Canny(Gray, 30, 200)  

        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True) 
  
        screenCnt = None

        for c in cnts:
            peri = cv2.arcLength(c, True)

            approx = cv2.approxPolyDP(c, 0.05 * peri, True)

            if len(approx) == 4 and max_size > cv2.contourArea(c) > min_size:
                screenCnt = approx
                break

        if screenCnt is None:
            detected = 0
            messagebox.showerror('Error','Không tìm thấy biển số nào')
        else:
            detected = 1

        if detected == 1:
            cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

            mask = np.zeros(gray.shape, np.uint8)
            cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
            cv2.bitwise_and(img, img, mask=mask)


            (x, y) = np.where(mask == 255)
            (topx, topy) = (np.min(x), np.min(y))
            (bottomx, bottomy) = (np.max(x), np.max(y))
            Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

            cv2.imshow('anh xe dau vao', img)
            #cv2.imshow('anh xam',gray)
            #cv2.imshow('anh loc min',Gray)
            #cv2.imshow('phat hien canh',edged)
            cv2.imshow('bien so xe', Cropped)

            cv2.waitKey(0)
            cv2.destroyAllWindows()

bt_open=ttk.Button(labelInput,text="Open File",width=50,command=Openfile)
bt_open.grid(column = 0, row = 1)

bt_run=ttk.Button(labelRun,text="Nhận dạng",width=50,command=Run)
bt_run.grid(column = 0, row = 1)



mainloop()