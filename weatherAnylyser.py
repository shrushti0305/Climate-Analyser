import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import requests
import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY') 
URL = "https://api.openweathermap.org/data/2.5/weather"

# ---------------- VIBE LOGIC ----------------
def get_vibe_tip(temp, description):
    desc = description.lower()
    
    if "rain" in desc or "drizzle" in desc:
        return "Time for some chai and pakoras! ☕☔"
    if "thunderstorm" in desc:
        return "Stay indoors and stay safe! ⚡🏠"
    
    if temp > 35:
        return "It's scorching! Stay hydrated and avoid the sun. 🥤🔥"
    elif temp > 25:
        return "A bit warm today, isn't it? Keep it cool! 😎"
    elif temp < 15:
        return "A bit chilly! Don't forget your jacket. 🧥"
    
    return "Weather looks good! Have a great day. ✨"

# ---------------- WEATHER LOGIC ----------------
def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(URL, params=params, timeout=5)
        data = response.json()

        if data.get("cod") != 200:
            return f"Error: {data.get('message', 'Unknown error')}"

        # Extract data
        weather_desc = data["weather"][0]["description"].capitalize()
        temp = round(data["main"]["temp"], 1)
        humidity = data["main"]["humidity"]

        # Get our smart tip
        tip = get_vibe_tip(temp, weather_desc)

        return (
            f"Weather: {weather_desc}\n"
            f"Temperature: {temp}°C\n"
            f"Humidity: {humidity}%\n\n"
            f"💡 {tip}"
        )

    except Exception as e:
        return f"Error: {str(e)}"

# ---------------- WINDOW CENTER ----------------
def center_window(window, width, height):
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# ---------------- MAIN ACTION ----------------
def start_weather_forecast():
    city = entry.get().strip()
    if not city:
        messagebox.showerror("Missing Input", "Please enter a city name.", parent=root)
        return

    def process():
        steps = [
            "Searching Location...",
            "Analyzing Cloud Patterns...",
            "Measuring Wind Speed...",
            "Gathering Satellite Data...",
            "Checking Temperature Trends...",
            "Finalizing Forecast..."
        ]

        progress_win = tk.Toplevel(root)
        progress_win.title("AI Weather Forecasting")
        progress_win.resizable(False, False)
        center_window(progress_win, 420, 150)
        progress_win.transient(root)
        progress_win.grab_set()

        lbl = ttk.Label(progress_win, text="Initializing...", font=("Segoe UI", 11))
        lbl.pack(pady=10)

        bar = ttk.Progressbar(progress_win, orient=tk.HORIZONTAL, length=360, mode="determinate")
        bar.pack(pady=10)
        
        # Force the window to show up
        progress_win.update()

        for i in range(100):
            time.sleep(0.03) # Slightly faster for better feel
            bar["value"] = i + 1
            step_index = (i * len(steps)) // 100
            if step_index < len(steps):
                lbl.config(text=steps[step_index])
            progress_win.update_idletasks()

        weather_result = get_weather(city)
        progress_win.destroy()
        root.after(100, lambda: messagebox.showinfo("Forecast Ready", weather_result, parent=root))

    threading.Thread(target=process, daemon=False).start()

# ---------------- GUI SETUP ----------------
root = tk.Tk()
root.title("AI Weather Forecasting")
root.resizable(False, False)
center_window(root, 420, 260)

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.configure("TLabel", font=("Segoe UI", 11))

header = ttk.Label(root, text="🌤 AI Weather Forecast", font=("Segoe UI", 16, "bold"))
header.pack(pady=(20, 10))

sub = ttk.Label(root, text="Enter your city name:")
sub.pack(pady=5)

entry = ttk.Entry(root, font=("Segoe UI", 12), justify="center", width=25)
entry.pack(pady=5)
entry.focus()

# Allow "Enter" key to trigger the button
root.bind('<Return>', lambda e: start_weather_forecast())

btn = ttk.Button(root, text="Get Forecast", command=start_weather_forecast)
btn.pack(pady=15)

footer = ttk.Label(root, text="Powered by OpenWeatherMap", font=("Segoe UI", 9), foreground="gray")
footer.pack(side="bottom", pady=8)

root.mainloop()