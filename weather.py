from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
import io


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Weather App')
        self.root.geometry('900x500+300+200')
        self.root.resizable(0, 0)

        # Search Box
        self.search_img = Image.open('search.png')
        self.search_img = ImageTk.PhotoImage(self.search_img)

        self.search_label = Label(self.root, image=self.search_img)
        self.search_label.place(x=20, y=20)

        self.text_input = tk.Entry(self.root, justify='center', width=18, font=('poppins', 20, 'bold'), bg='#404040',
                                   bd=0, fg='white', highlightthickness=0)
        self.text_input.place(x=50, y=40)
        self.text_input.focus()

        self.search_icon = Image.open('icon.png')
        self.search_icon = ImageTk.PhotoImage(self.search_icon)

        self.search_btn = Button(image=self.search_icon, borderwidth=0, cursor='hand2', bg='#404040',
                                 highlightthickness=0, command=self.get_weather)
        self.search_btn.place(x=420, y=42)

        # Weather Details
        self.details_box_img = Image.open('box.png')
        self.details_box_img = ImageTk.PhotoImage(self.details_box_img)

        self.details_box_label = Label(self.root, image=self.details_box_img, padx=5, pady=5)
        self.details_box_label.pack(side=BOTTOM)

        # Time
        self.weather = Label(self.root, font=('arial', 15, 'bold'))
        self.weather.place(x=30, y=100)
        self.clock = Label(self.root, font=('Helvetica', 20))
        self.clock.place(x=30, y=130)

        # Labels
        self.wind_label = Label(self.root, text='Wind', font=('Helvetica', 15, 'bold'), fg='white', bg='#1ab5ef')
        self.wind_label.place(x=100, y=410)

        self.humidity_label = Label(self.root, text='Humidity', font=('Helvetica', 15, 'bold'), fg='white',
                                    bg='#1ab5ef')
        self.humidity_label.place(x=270, y=410)

        self.description_label = Label(self.root, text='Description', font=('Helvetica', 15, 'bold'), fg='white',
                                       bg='#1ab5ef')
        self.description_label.place(x=480, y=410)

        self.pressure_label = Label(self.root, text='Pressure', font=('Helvetica', 15, 'bold'), fg='white',
                                    bg='#1ab5ef')
        self.pressure_label.place(x=700, y=410)

        self.temp_label = Label(font=('arial', 70, 'bold'), fg='#ee666d')
        self.temp_label.place(x=450, y=150)

        self.condition_label = Label(font=('arial', 15, 'bold'))
        self.condition_label.place(x=450, y=250)

        self.wnd = Label(text='....', font=('arial', 20, 'bold'), bg='#1ab5ef')
        self.wnd.place(x=100, y=430)
        self.humid = Label(text='....', font=('arial', 20, 'bold'), bg='#1ab5ef')
        self.humid.place(x=290, y=430)
        self.descript = Label(text='....', font=('arial', 20, 'bold'), bg='#1ab5ef')
        self.descript.place(x=480, y=430)
        self.press = Label(text='....', font=('arial', 20, 'bold'), bg='#1ab5ef')
        self.press.place(x=720, y=430)

        self.weather_icon_label = Label(self.root)
        self.weather_icon_label.place(x=320, y=150)

    def get_weather(self):
        try:
            API_key = 'YOUR API_KEY'
            city = self.text_input.get()

            geolocator = Nominatim(user_agent='weather')
            location = geolocator.geocode(city)
            obj = TimezoneFinder()
            result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

            home = pytz.timezone(result)
            local_time = datetime.now(home)
            current_time = local_time.strftime('%I:%M %p')
            self.clock.config(text=current_time)
            self.weather.config(text='Current Weather')

            # Weather API
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}'
            res = requests.get(url).json()
            condition = res['weather'][0]['main']
            description = res['weather'][0]['description']
            temp = int(res['main']['temp'] - 273.15)
            pressure = res['main']['pressure']
            humidity = res['main']['humidity']
            wind = res['wind']['speed']

            self.temp_label.config(text=(temp, '°'))
            self.condition_label.config(text=(condition, '|', 'Feels', 'Like', temp, '°'))

            self.wnd.config(text=wind)
            self.humid.config(text=humidity)
            self.descript.config(text=description)
            self.press.config(text=pressure)

            # Weather Icon
            icon_code = res['weather'][0]['icon']

            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"

            icon_data = requests.get(icon_url).content
            icon_img = Image.open(io.BytesIO(icon_data))
            icon_img = icon_img.resize((100, 100), Image.ANTIALIAS)
            icon_img = ImageTk.PhotoImage(icon_img)

            self.weather_icon_label.config(image=icon_img)
            self.weather_icon_label.image = icon_img

        except Exception as err:
            messagebox.showerror('Weather App', 'Wrong City, Please Try Again')


if __name__ == "__main__":
    root = Tk()
    app = WeatherApp(root)
    root.mainloop()
