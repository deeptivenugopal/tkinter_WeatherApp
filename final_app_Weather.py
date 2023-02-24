#import all the modules from tkinter
from tkinter import *
from configparser import ConfigParser
from tkinter import messagebox

#installed requests module(This module is used to handle API requests)
import requests

#Copy the Current Weather Data API
url_api = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

#Capture api key from the weather_config file
api_file = "weather_config"
file_a = ConfigParser()
file_a.read(api_file)
api_key = file_a['api_key']['key']

#Build a function to retrieve json response

def weather_find(city):
    final = requests.get(url_api.format(city,api_key))
    if final:
        json_file = final.json()
        city = json_file['name']
        country = json_file['sys']['country']
        k_temperature = json_file['main']['temp'] #kelvin temperature
        c_temperature = k_temperature - 273.15 #conversion to celsius
        f_temperature = (k_temperature - 273.15) * 9/5 +32
        weather_display = json_file['weather'][0]['main']
        result = (city,country,c_temperature,f_temperature,weather_display)
        return result
    else:
        return None

#Printing all the variables
def print_weather():
    city = search_city.get()
    weather = weather_find(city)
    if weather:
        location_entry['text'] = '{},{}'.format(weather[0],weather[1])
        temperature_entry['text'] ='{:.2f} C, {:.2f} F'.format(weather[2],weather[3])
        weather_entry['text'] = weather[4]
    else:
        messagebox.showerror('Error','Please enter valid city name')


#Clear the data
def clear_weather_data():
    location_entry.config(text='')
    temperature_entry.config(text='')
    weather_entry.config(text='')
    enter_city.delete(0,'end')

#****** Building of UI screen ******
# Windows Screen
root = Tk()
root.title("My Own Weather App")
#by default background color is grey
root.config(background="black")
root.geometry("700x400")

#UI Definitions
search_city = StringVar()
enter_city = Entry(root,textvariable = search_city,fg="blue",font=("Arial",30,"bold"))
enter_city.pack()

search_button = Button(root,text="SEARCH WEATHER",width=20,bg="red",fg="white",font=("Arial",15,"bold"),command = print_weather)
search_button.pack()

reset_button = Button(root,text="Clear",width=20,bg="grey",fg="black",font=("Arial",15,"bold"),command = clear_weather_data)
reset_button.pack()

location_entry = Label(root,text='',font=("Arial",35,"bold"),bg="lightblue",fg="white")
location_entry.pack()

temperature_entry = Label(root,text='',font=("Arial",35,"bold"),bg="lightpink")
temperature_entry.pack()

weather_entry = Label(root,text='',font=("Arial",35,"bold"),bg="lightgreen")
weather_entry.pack()

root.mainloop()