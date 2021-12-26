from tkinter import *
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import requests
import json
import pandas as pd
import numpy as np
import datetime
from datetime import datetime
import statistics
from statistics import mode

root = Tk()
root.title("Air Quality Lookup")

frame = LabelFrame(root)
frame.pack()

myLabel1 = Label(frame,text='Enter Any Date Since 11-27-2020')
e1 = Entry(frame,width=50,borderwidth=2)
myLabel1.grid(row=0,column=0)
e1.grid(row=1,column=0)
e1.insert(0,"mm-dd-yyyy")

myLabel2 = Label(frame,text='Enter Latitude Coordinate')
e2 = Entry(frame,width=50,borderwidth=2)
myLabel2.grid(row=2,column=0)
e2.grid(row=3,column=0)

myLabel3 = Label(frame,text='Enter Longitude Coordinate')
e3 = Entry(frame,width=50,borderwidth=2)
myLabel3.grid(row=4,column=0)
e3.grid(row=5,column=0)

def air_quality():
    
    date=e1.get()
    latitude=e2.get()
    longitude=e3.get() 
    
    s = str(date) + '-0'
    e = str(date) + '-23'
    start = datetime.strptime(s, '%m-%d-%Y-%H')
    end = datetime.strptime(e, '%m-%d-%Y-%H')

    start_time = timestamp = datetime.timestamp(start)
    end_time = timestamp = datetime.timestamp(end)
    
    api_key = '4438fa75e6ea6307215213be025d0c5c'

    #user inputs
    lat = latitude   
    lon = longitude

    #generated from user input of datetime format
    start = int(start_time)
    end = int(end_time)

    ap_url = f'http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={api_key}'
    ap_res = requests.get(ap_url)
    ap_data = json.loads(ap_res.text)
    
    lst = ap_data['list']
    df = pd.DataFrame(lst)
    
    comps = np.array(df['components'])
    
    co,no,no2,o3,so2,pm2_5,pm10,nh3 = [],[],[],[],[],[],[],[]
    for i in range(len(comps)):
        str_comps = str(comps[i])
        str_comps2 = str_comps.split(',')
        co.append(str_comps2[0].split(':')[1])
        no.append(str_comps2[1].split(':')[1])
        no2.append(str_comps2[2].split(':')[1])
        o3.append(str_comps2[3].split(':')[1])
        so2.append(str_comps2[4].split(':')[1])
        pm2_5.append(str_comps2[5].split(':')[1])
        pm10.append(str_comps2[6].split(':')[1])
        nh3.append(str_comps2[7].split(':')[1])
        
    df = df.drop(['main','components'],axis=1)
    df['co'],df['no2'],df['o3'],df['so2'],df['pm2_5'],df['pm10'],df['nh3'] = co,no2,o3,so2,pm2_5,pm10,nh3
    
    dt = np.array(df['dt'])
    d = []
    for i in dt:
        d.append(datetime.utcfromtimestamp(i).strftime('%m-%d-%Y'))

    df['dt'] = d
    
    for i in range(len(nh3)):
        nh3[i] = nh3[i].strip()
        nh3[i] = nh3[i].replace('}',"")
    df['nh3'] = nh3
    
    air_quality = []
    for i in range(len(no2)):

        if (float(no2[i]) > 400) or (float(pm10[i]) > 180) or (float(o3[i]) > 240) or (float(pm2_5[i]) > 110):
            air_quality.append('Very Poor')
        elif ((float(no2[i]) > 200) and (float(no2[i]) < 400)) or ((float(pm10[i]) > 90) and (float(pm10[i]) < 180)) or ((float(o3[i]) > 180) and (float(o3[i]) < 240)) or ((float(pm2_5[i]) > 55) and (float(pm2_5[i]) < 110)):
            air_quality.append('Poor')
        elif ((float(no2[i]) > 100) and (float(no2[i]) < 200)) or ((float(pm10[i]) > 50) and (float(pm10[i]) < 90)) or ((float(o3[i]) > 120) and (float(o3[i]) < 180)) or ((float(pm2_5[i]) > 30) and (float(pm2_5[i]) < 55)):
            air_quality.append('Moderate') 
        elif ((float(no2[i]) > 50) and (float(no2[i]) < 100)) or ((float(pm10[i]) > 25) and (float(pm10[i]) < 50)) or ((float(o3[i]) > 60) and (float(o3[i]) < 120)) or ((float(pm2_5[i]) > 15) and (float(pm2_5[i]) < 30)):
            air_quality.append('Fair')        
        elif ((float(no2[i]) > 0) and (float(no2[i]) < 50)) or ((float(pm10[i]) > 0) and (float(pm10[i]) < 25)) or ((float(o3[i]) > 0) and (float(o3[i]) < 60)) or ((float(pm2_5[i]) > 0) and (float(pm2_5[i]) < 15)):
            air_quality.append('Good')

    df['air_quality'] = air_quality  
    
    
    air_qual = mode(df['air_quality'])
    
    
    myLabel = Label(frame,text=f'The Air Quality for the coordinates {lat} ,{lon} on {date} was {air_qual}')
    myLabel.grid(row=7,column=0)


    
myButton = Button(frame,width=20,text="Find Air Quality",activebackground='#8af',command=air_quality)
myButton.grid(row=6,column=0)

root.mainloop()
