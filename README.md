# 使用PyVisa取得電子負載RealTime電壓、電流



首先要搞定驅動程式的問題

先安裝 NI-VISA

裡面包含Chroma 6314A 驅動程式

安裝完接上儀器，裝置管理員應該會出現 "USB Test and Measurement Devices"

如果顯示 USB-6314A (!) 代表沒有成功安裝驅動程式，PyVisa會無法抓到儀器



#### 驅動程式下載

https://www.chromaate.com/tw/data_center/6310a_series_programmable_dc_electronic_load

https://www.ni.com/zh-tw/support/downloads/drivers/download.ni-visa.html#460225



#### chroma63102A 操作手冊下載

https://drive.google.com/drive/u/0/folders/1P06Ys03MZvkwHTO1Wy--Kkr4YbLeSc1h

## Python範例程式

```python


#安裝pyvisa
#pip install -U pyvisa

import pyvisa
rm = pyvisa.ResourceManager()
print(rm.list_resources())   #取得 裝置名稱

chroma63102A = rm.open_resource('USB0::0x0A69::0x084A::6314A0007663::INSTR')
#print(chroma63102A.query('*IDN?'))    #印出裝置詳細資訊


#chroma63102A.write("CHANnel:CHAN 1")            # 選擇Chanel 1
#chroma63102A.write("CURR:STAT:L1"+" "+ "0.95")  # 設定抽載電流 
#print(chroma63102A.query("CURR:STAT:L1?"))      # 確認電子負載 L1 目前定電流設定值
#chroma63102A.write("CONF:REM ON")               # 開啟遠端控制模式 (面板按鍵操作無效)
#chroma63102A.write("CHAN : ACT ON")             # 開啟目前選擇的 Chanel的負載

chroma63102A.write("LOAD OFF")     # 開啟
print(chroma63102A.query("LOAD?")) # 顯示　回送的電子負載是否有效


print(chroma63102A.query("MODE?"))  #問模式

print( chroma63102A.query("FETC:CURR?") )
print( chroma63102A.query("FETC:VOLT?") )
print( chroma63102A.query("FETC:POWer?") )
```

