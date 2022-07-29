from ctypes import alignment
import threading
import tkinter as tk
from tkinter import filedialog

import time
from typing import Text

import pyvisa
rm = pyvisa.ResourceManager()


#chroma63102A.write("CHANnel:CHAN 1")            # 選擇Chanel 1
#chroma63102A.write("CURR:STAT:L1"+" "+ "0.95")  # 設定抽載電流 
#print(chroma63102A.query("CURR:STAT:L1?"))      # 確認電子負載 L1 目前定電流設定值
#chroma63102A.write("CONF:REM ON")               # 開啟遠端控制模式 (面板按鍵操作無效)
#chroma63102A.write("CHAN : ACT ON")             # 開啟目前選擇的 Chanel的負載


rec_time_sec = 0

try:
    chroma63102A = rm.open_resource('USB0::0x0A69::0x084A::6314A0007663::INSTR')
    chroma63102A.write("CHANnel:CHAN 1")
    chroma63102A.write("CURR:STAT:L1"+" "+ "0.95")
    print(chroma63102A.query("CURR:STAT:L1?"))

except:
    chroma63102A = 0
    print("chroma63102A open error")


def getBatCurrent():
    global BatCurrent_Str
    if chroma63102A:
        str_temp = chroma63102A.query("FETC:CURR?")
        BatCurrent_Str = str_temp.replace('\n','')
    

def getBatVolt():
    global BatVolt_Str
    if chroma63102A:
        str_temp = chroma63102A.query("FETC:VOLT?")
        BatVolt_Str = str_temp.replace('\n','')


        

def getBatPow():
    global BatPow_Str
    if chroma63102A:
        str_temp = chroma63102A.query("FETC:POWer?")
        BatPow_Str = str_temp.replace('\n','')

Title = "電池抽載紀錄器"


def Window_on_Close():
    global win
    global chroma63102A
    global record_file
    global rec_permin_file


    try:
        record_file.close()
        rec_permin_file.close()
    except:
        print("record_file close error!\n")

    chroma63102A = 0
    print("Windows close")
    win.destroy()
    win = 0    


def RecBtn_Click():
    global record_file
    global rec_permin_file
    global rec_time_sec

    save_file_path = filedialog.asksaveasfilename(filetypes=[( 'csv檔案','*.csv')])
    save_permin_file_path = save_file_path + '_Per_Minute.csv'
    
    if not save_file_path.endswith('.csv'):    # 如果使用者輸入的檔名結尾不是 .csv 
        save_file_path += '.csv'   

    try:
        
        record_file = open( save_file_path ,"w")  
        rec_permin_file = open( save_permin_file_path ,"w")  

        str_line =  "電壓"+ ',' + "電流" + ',' + "功率" + ',' + "當下時間" + ',' + "放電時間" + '\n'

        record_file.write(str_line) 
        rec_permin_file.write(str_line) 

        rec_time_sec = 0  # 紀錄時間初始化

        print("Start record " + save_file_path +"  !! \n")
    except:
        print("open " + save_file_path +"  failed !!\n")


    print("click")

def Create_Win():
    global win
    global Label_V
    global Label_I
    global Label_P
    global Label_T

    win = tk.Tk()
    win.title(Title)
    win.geometry('400x400')
    #==========  UI code here ====================

    Label_V = tk.Label(win,text= "電壓:",font=('Arial', 20) ,anchor='w',bg='white' )
    Label_V.pack(padx=20,ipady=10,fill=tk.BOTH)

    Label_I = tk.Label(win,text= "電流:",font=('Arial', 20) ,anchor='w',bg='white')
    Label_I.pack(padx=20,ipady=10,fill=tk.BOTH)

    Label_P = tk.Label(win,text= "功率:",font=('Arial', 20) ,anchor='w',bg='white')
    Label_P.pack(padx=20,ipady=10,fill=tk.BOTH)

    Label_T = tk.Label(win,text= "時間:",font=('Arial', 20) ,anchor='w',bg='white')
    Label_T.pack(padx=20,ipady=10,fill=tk.BOTH)

    RecBtn = tk.Button(win,text="開始記錄", font=('Arial', 20) ,command=RecBtn_Click)
    RecBtn.pack(padx=20,ipady=10,fill=tk.BOTH)

    #=========================================
    win.protocol("WM_DELETE_WINDOW", Window_on_Close)
    win.mainloop()
    

def UI_Update():
    global Label_V
    global Label_I
    global Label_P
    global Label_T

    global BatVolt_Str
    global BatCurrent_Str    
    global BatPow_Str

    Label_V.config(text= "電壓:" + BatVolt_Str)
    Label_I.config(text= "電壓:" + BatCurrent_Str)
    Label_P.config(text= "功率:" + BatPow_Str)
    Label_T.config(text= "時間:" + str(rec_time_sec))



def Background_Task():

    global BatVolt_Str
    global BatCurrent_Str    
    global BatPow_Str

    global rec_time_sec

    BatCurrent_Str = ''
    BatVolt_Str = ''
    BatPow_Str = ''

    sec_r = 0
    sec_check = 0


    sys_cnt = 0
    while True:
        #==========  Do Something Background  ==============

        getBatCurrent()
        getBatVolt()
        getBatPow()

        if chroma63102A: 
            UI_Update()

            BatCurrent_int =  int(float(BatCurrent_Str) * 100)
            #print(BatCurrent_int)

            BatVolt_int =  int(float(BatVolt_Str) * 100)
            #print(BatVolt_int)

            BatPow_int =  int(float(BatPow_Str) * 100)
            #print(BatPow_int)


            # if(win != 0):
            #     print( '電壓:' + BatVolt_Str  + " 電流:" + BatCurrent_Str + " 功率:" + BatPow_Str)

        #===================================================
        localtime = time.localtime()   
        sec_r = time.strftime("%S", localtime)
        if(sec_check != sec_r):
            sec_check = sec_r
            time_str = time.strftime("%Y/%m/%d %I:%M:%Ss", localtime)   # 

            if(win != 0):               
                #print( '電壓:' + BatVolt_Str  + " 電流:" + BatCurrent_Str + " 功率:" + BatPow_Str + " 時間:" + time_str)
                data_str_line = BatVolt_Str + ',' + BatCurrent_Str  + ',' + BatPow_Str + ',' + time_str +  ',' + str(rec_time_sec) +'\n'
                #print(data_str_line)

            #print(str(time_str))
            try:     
                record_file.write(data_str_line)

                if rec_time_sec % 60 == 0:
                    rec_permin_file.write(data_str_line)

                rec_time_sec += 1                
            except:
                pass
        #===================================================



        sys_cnt+=1
        if(sys_cnt % 10 == 0):       
            non=0     
            #print("sys:",sys_cnt/10)

        time.sleep(0.1)    


if __name__ == "__main__":
    # 建立 TK UI Window 視窗
    task_1 = threading.Thread(target = Create_Win)
   
    # setDaemon 可以讓背景程序 Background_Task 隨視窗關閉結束
    task_2 = threading.Thread(target = Background_Task)
    task_2.setDaemon(True)

    task_1.start()
    task_2.start()