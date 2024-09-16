
import tkinter as tk
from tkinter import messagebox

from datetime import datetime

API_KEY = 'xxxxxxxxxxxxxxxxx'  
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Forecast")
        self.root.geometry("500x600")

        # Load default background image (initial state)
        self.bg_image_label = tk.Label(root)
        self.bg_image_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title Label
        self.title_label = tk.Label(root, text="Weather Forecast", font=("Helvetica", 20, "bold"), bg="white")
        self.title_label.pack(pady=10)

        # Current Date and Time
        self.time_label = tk.Label(root, text="", font=("Helvetica", 12), bg="white")
        self.time_label.pack(pady=5)
        self.update_time()

        # Entry for City or ZIP Code
        self.label = tk.Label(root, text="Enter City or ZIP Code:", font=("Arial", 14, "bold"), bg="white")
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, font=("Arial", 14), width=25)
        self.entry.pack(pady=5)

        # Search Button
        self.search_button = tk.Button(root, text="Get Weather", command=self.get_weather, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white")
        self.search_button.pack(pady=10)

        # Weather Result Label
        self.result_label = tk.Label(root, text="", font=("Arial", 14), bg="white")
        self.result_label.pack(pady=20)

        # Weather Icon
        self.weather_icon = tk.Label(root, bg="white")
        self.weather_icon.pack()

        # Additional Information
        self.additional_info_label = tk.Label(root, text="", font=("Arial", 12), bg="white")
        self.additional_info_label.pack(pady=10)

    def update_time(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=f"Current Date & Time: {now}")
        self.root.after(1000, self.update_time)  # Update every second

    def set_background(self, image_file):
        bg_image = Image.open(image_file)
        bg_image = bg_image.resize((500, 600), Image.ANTIALIAS)
        self.bg_image = ImageTk.PhotoImage(bg_image)
        self.bg_image_label.config(image=self.bg_image)

    def get_weather(self):
        location = self.entry.get()
        if not location:
            messagebox.showerror("Input Error", "Please enter a city or ZIP code.")
            return

        try:
            response = requests.get(BASE_URL, params={
                'q': location,
                'appid': API_KEY,
                'units': 'metric'
            })
            data = response.json()

            if response.status_code == 200:
                # Check if the API returned a valid city
                if data.get('cod') != 200:
                    messagebox.showerror("Error", "City not found.")
                    return

                # Weather Data
                weather = data['weather'][0]['description']
                temp = data['main']['temp']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                icon_code = data['weather'][0]['icon']
                sunrise_time = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')
                sunset_time = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')

                # Displaying the weather details
                result_text = (f"Location: {data['name']}, {data['sys']['country']}\n"
                               f"Weather: {weather.capitalize()}\n"
                               f"Temperature: {temp}°C\n"
                               f"Humidity: {humidity}%\n"
                               f"Wind Speed: {wind_speed} m/s")
                self.result_label.config(text=result_text)

                additional_info = (f"Sunrise: {sunrise_time}\n"
                                   f"Sunset: {sunset_time}")
                self.additional_info_label.config(text=additional_info)

                # Load and display the weather icon
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                icon_response = requests.get(icon_url, stream=True)
                if icon_response.status_code == 200:
                    image_data = icon_response.raw
                    image = Image.open(image_data)
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(image)
                    self.weather_icon.config(image=photo)
                    self.weather_icon.image = photo

                # Change background image based on weather conditions
                if 'clear' in weather.lower():
                    self.set_background("C:\\Users\\DELL\\OneDrive\\Pictures\\sunny.jpeg")  
                elif 'cloud' in weather.lower():
                    self.set_background("C:\\Users\\DELL\\OneDrive\\Pictures\\cloudy.jpeg")  
                elif 'rain' in weather.lower():
                    self.set_background("C:\\Users\\DELL\\OneDrive\\Pictures\\rainy.jpeg")  
                else:
                    self.set_background("C:\\Users\\DELL\\OneDrive\\Pictures\\weather1.jpeg")  
            else:
                messagebox.showerror("Error", "City not found.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to retrieve data: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()