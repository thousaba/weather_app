import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

API_KEY = "428de79a71b9d8e1ef19969ea033b8b5"  # OpenWeatherMap API key


def get_weather():
    city = city_entry.get().strip()
    print("City:", city)
    if not city:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    print("URL:", url)

    try:
        response = requests.get(url)
        print("Status Code:", response.status_code)
        data = response.json()
        print("RESPONSE JSON:", data)

        if response.status_code == 200:
            temperature = data['main']['temp']
            condition = data['weather'][0]['description'].title()
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            result = (
                f"Weather in {city.title()}:\n\n"
                f"🌡 Temperature: {temperature}°C\n"
                f"☁ Condition: {condition}\n"
                f"💧 Humidity: {humidity}%\n"
                f"🌬 Wind Speed: {wind_speed} m/s"
            )
            result_label.config(text=result)

            # 🌤️ Hava Durumu İkonu
            icon_code = data['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

            try:
                icon_response = requests.get(icon_url)
                icon_data = BytesIO(icon_response.content)
                pil_image = Image.open(icon_data)
                tk_image = ImageTk.PhotoImage(pil_image)

                # Önceki ikon varsa sil
                for widget in icon_frame.winfo_children():
                    widget.destroy()

                icon_label = tk.Label(icon_frame, image=tk_image)
                icon_label.image = tk_image  # Referans tutma
                icon_label.pack()
            except Exception as icon_err:
                print("Icon load error:", icon_err)

        else:
            message = data.get('message', 'Unknown error')
            messagebox.showerror("API Error", f"Failed to fetch weather: {message}")

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Connection Error", "No internet connection.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


# GUI Setup
window = tk.Tk()
window.title("Weather App")
window.geometry("400x400")
window.resizable(False, False)

tk.Label(window, text="Enter City Name:", font=("Arial", 14)).pack(pady=10)
city_entry = tk.Entry(window, font=("Arial", 14))
city_entry.pack(pady=5)
city_entry.focus_set()

result_label = tk.Label(window, text="", font=("Arial", 12), justify="left")
result_label.pack(pady=10)

# 🖼️ İkon gösterimi için boş bir frame oluşturuyoruz
icon_frame = tk.Frame(window)
icon_frame.pack(pady=5)

tk.Button(window, text="Get Weather", command=get_weather, font=("Arial", 12)).pack(pady=10)

if __name__ == "__main__":
    window.mainloop()