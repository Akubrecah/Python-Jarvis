import datetime
import os
import sys
import time
import webbrowser
import pyautogui
import pyttsx3
import speech_recognition as sr
import json
import pickle
import random
import subprocess
import psutil
from typing import List, Dict

# Initialize the text-to-speech engine
def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Change index to switch voices
    engine.setProperty('rate', 150)  # Adjust speech rate
    engine.setProperty('volume', 0.9)  # Adjust volume (0.0 to 1.0)
    return engine

# Speak function with error handling
def speak(text: str):
    try:
        engine = initialize_engine()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speech synthesis: {e}")

# Improved voice command recognition
def command() -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...", end="", flush=True)
        r.adjust_for_ambient_noise(source, duration=0.5)
        r.pause_threshold = 1.0
        r.phrase_threshold = 0.3
        audio = r.listen(source)
    
    try:
        print("\rRecognizing...", end="", flush=True)
        query = r.recognize_google(audio, language='en-in').lower()
        print(f"\rUser said: {query}\n")
        return query
    except sr.UnknownValueError:
        print("\rCould not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"\rCould not request results; {e}")
        return ""
    except Exception as e:
        print(f"\rError in recognition: {e}")
        return ""

# Date and time functions
def get_current_time() -> str:
    return time.strftime("%I:%M %p")

def get_current_day() -> str:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[datetime.datetime.today().weekday()]

def wish_me():
    hour = datetime.datetime.now().hour
    current_time = get_current_time()
    day = get_current_day()
    
    if 0 <= hour < 12:
        greeting = f"Good morning, it's {day} and the time is {current_time}"
    elif 12 <= hour < 16:
        greeting = f"Good afternoon, it's {day} and the time is {current_time}"
    else:
        greeting = f"Good evening, it's {day} and the time is {current_time}"
    
    speak(greeting)

# System information functions
def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    battery = psutil.sensors_battery()
    
    info = {
        "cpu": f"{cpu_usage}%",
        "memory": f"{memory.percent}%",
        "battery": f"{battery.percent}%",
        "charging": battery.power_plugged
    }
    
    return info

def report_system_condition():
    info = get_system_info()
    report = (
        f"System status: CPU usage at {info['cpu']}, "
        f"memory usage at {info['memory']}, "
        f"battery at {info['battery']}"
    )
    
    speak(report)
    
    if not info['charging']:
        battery_level = int(info['battery'].replace('%', ''))
        if battery_level < 20:
            speak("Warning! Battery critically low. Please connect to power immediately.")
        elif battery_level < 50:
            speak("Battery level is moderate. Consider connecting to power soon.")

# Web and social media functions
def open_website(url: str, name: str = None):
    try:
        if name:
            speak(f"Opening {name}")
        webbrowser.open(url)
    except Exception as e:
        speak(f"Sorry, I couldn't open {name or 'the website'}")
        print(f"Error opening website: {e}")

def handle_social_media(command: str):
    sites = {
        'facebook': 'https://www.facebook.com/',
        'whatsapp': 'https://web.whatsapp.com/',
        'discord': 'https://discord.com/',
        'instagram': 'https://www.instagram.com/',
        'twitter': 'https://twitter.com/',
        'linkedin': 'https://www.linkedin.com/',
        'youtube': 'https://www.youtube.com/',
        'reddit': 'https://www.reddit.com/',
        'github': 'https://github.com/Akubrecah/'
    }
    
    for site, url in sites.items():
        if site in command:
            open_website(url, site)
            return
    
    speak("I didn't recognize that social media platform")

# Application management
def open_application(command: str):
    app_map = {
  "calculator": "calc.exe",
  "notepad": "notepad.exe",
  "paint": "mspaint.exe",
  "wordpad": "write.exe",
  "command prompt": "cmd.exe",
  "powershell": "powershell.exe",
  "task manager": "Taskmgr.exe",
  "registry editor": "regedit.exe",
  "system configuration": "msconfig.exe",
  "disk cleanup": "cleanmgr.exe",
  "defragment and optimize drives": "dfrgui.exe",
  "resource monitor": "resmon.exe",
  "performance monitor": "perfmon.exe",
  "event viewer": "eventvwr.exe",
  "device manager": "devmgmt.msc",
  "disk management": "diskmgmt.msc",
  "services": "services.msc",
  "group policy editor": "gpedit.msc",
  "local security policy": "secpol.msc",
  "print management": "printmanagement.msc",
  "character map": "charmap.exe",
  "magnifier": "magnify.exe",
  "narrator": "Narrator.exe",
  "on-screen keyboard": "osk.exe",
  "sticky notes": "StikyNot.exe",
  "snipping tool": "SnippingTool.exe",
  "sound recorder": "SoundRecorder.exe",
  "windows media player": "wmplayer.exe",
  "windows photo viewer": "dllhost.exe",
  "internet explorer": "iexplore.exe",
  "edge browser": "MicrosoftEdge.exe",
  "remote desktop": "mstsc.exe",
  "windows explorer": "explorer.exe",
  "control panel": "control.exe",
  "settings": "SystemSettings.exe",
  "task scheduler": "taskschd.msc",
  "windows update": "wuapp.exe",
  "backup and restore": "sdclt.exe",
  "system restore": "rstrui.exe",
  "file history": "FileHistory.exe",
  "bitlocker": "manage-bde.exe",
  "firewall": "WF.msc",
  "windows defender": "MSASCui.exe",
  "windows fax and scan": "WFS.exe",
  "xps viewer": "xpsrchvw.exe",
  "math input panel": "mip.exe",
  "connect to a projector": "DisplaySwitch.exe",
  "windows mobility center": "mblctr.exe",
  "sync center": "mobsync.exe",
  "ease of access center": "utilman.exe",
  "speech recognition": "speechux\\SpeechUXWiz.exe"
}
    
    for app, path in app_map.items():
        if app in command:
            try:
                speak(f"Opening {app}")
                if path.startswith('ms-') or path.endswith(':'):
                    os.system(f'start {path}')
                else:
                    os.startfile(path)
                return
            except Exception as e:
                speak(f"Sorry, I couldn't open {app}")
                print(f"Error opening application: {e}")
                return
    
    # Special cases for Windows components
    if 'windows update' in command:
        os.system('start ms-settings:windowsupdate')
    elif 'printer' in command:
        os.system('start ms-settings:printers')
    elif 'bluetooth' in command:
        os.system('start ms-settings:bluetooth')
    elif 'wifi' in command or 'wireless' in command:
        os.system('start ms-settings:network-wifi')
    elif 'network' in command:
        os.system('start ms-settings:network')
    elif 'display' in command or 'screen' in command:
        os.system('start ms-settings:display')
    elif 'sound' in command or 'audio' in command:
        os.system('start ms-settings:sound')
    elif 'battery' in command:
        os.system('start ms-settings:batterysaver')
    elif 'storage' in command:
        os.system('start ms-settings:storagesense')
    elif 'theme' in command:
        os.system('start ms-settings:themes')
    elif 'mouse' in command:
        os.system('start ms-settings:mousetouchpad')
    elif 'keyboard' in command:
        os.system('start ms-settings:keyboard')
    else:
        speak("I didn't recognize that application")

def close_application(command: str):
    app_map = {
  "calculator": "calc.exe",
  "notepad": "notepad.exe",
  "paint": "mspaint.exe",
  "wordpad": "write.exe",
  "command prompt": "cmd.exe",
  "powershell": "powershell.exe",
  "task manager": "Taskmgr.exe",
  "registry editor": "regedit.exe",
  "system configuration": "msconfig.exe",
  "disk cleanup": "cleanmgr.exe",
  "defragment and optimize drives": "dfrgui.exe",
  "resource monitor": "resmon.exe",
  "performance monitor": "perfmon.exe",
  "event viewer": "eventvwr.exe",
  "device manager": "devmgmt.msc",
  "disk management": "diskmgmt.msc",
  "services": "services.msc",
  "group policy editor": "gpedit.msc",
  "local security policy": "secpol.msc",
  "print management": "printmanagement.msc",
  "character map": "charmap.exe",
  "magnifier": "magnify.exe",
  "narrator": "Narrator.exe",
  "on-screen keyboard": "osk.exe",
  "sticky notes": "StikyNot.exe",
  "snipping tool": "SnippingTool.exe",
  "sound recorder": "SoundRecorder.exe",
  "windows media player": "wmplayer.exe",
  "windows photo viewer": "dllhost.exe",
  "internet explorer": "iexplore.exe",
  "edge browser": "MicrosoftEdge.exe",
  "remote desktop": "mstsc.exe",
  "windows explorer": "explorer.exe",
  "control panel": "control.exe",
  "settings": "SystemSettings.exe",
  "task scheduler": "taskschd.msc",
  "windows update": "wuapp.exe",
  "backup and restore": "sdclt.exe",
  "system restore": "rstrui.exe",
  "file history": "FileHistory.exe",
  "bitlocker": "manage-bde.exe",
  "firewall": "WF.msc",
  "windows defender": "MSASCui.exe",
  "windows fax and scan": "WFS.exe",
  "xps viewer": "xpsrchvw.exe",
  "math input panel": "mip.exe",
  "connect to a projector": "DisplaySwitch.exe",
  "windows mobility center": "mblctr.exe",
  "sync center": "mobsync.exe",
  "ease of access center": "utilman.exe",
  "speech recognition": "speechux\\SpeechUXWiz.exe"
}
    
    for app, process in app_map.items():
        if app in command:
            try:
                speak(f"Closing {app}")
                os.system(f'taskkill /f /im {process}')
                return
            except Exception as e:
                speak(f"Sorry, I couldn't close {app}")
                print(f"Error closing application: {e}")
                return
    
    speak("I didn't recognize that application to close")

# System control functions
def control_system(command: str):
    if 'shutdown' in command:
        speak("Shutting down the computer in one minute")
        os.system('shutdown /s /t 60')
    elif 'restart' in command or 'reboot' in command:
        speak("Restarting the computer in one minute")
        os.system('shutdown /r /t 60')
    elif 'sleep' in command:
        speak("Putting the computer to sleep")
        os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
    elif 'lock' in command:
        speak("Locking the computer")
        os.system('rundll32.exe user32.dll,LockWorkStation')
    elif 'log off' in command or 'sign out' in command:
        speak("Signing out of the computer")
        os.system('shutdown /l')
    elif 'cancel shutdown' in command or 'abort shutdown' in command:
        speak("Cancelling the shutdown")
        os.system('shutdown /a')

# Media control functions
def control_media(command: str):
    if 'play' in command or 'pause' in command:
        pyautogui.press('playpause')
        speak("Media play/pause")
    elif 'next' in command or 'skip' in command:
        pyautogui.press('nexttrack')
        speak("Next track")
    elif 'previous' in command or 'back' in command:
        pyautogui.press('prevtrack')
        speak("Previous track")
    elif 'volume up' in command:
        pyautogui.press('volumeup')
        speak("Volume increased")
    elif 'volume down' in command:
        pyautogui.press('volumedown')
        speak("Volume decreased")
    elif 'mute' in command:
        pyautogui.press('volumemute')
        speak("Volume muted")
    elif 'fullscreen' in command or 'maximize' in command:
        pyautogui.press('f11')
        speak("Toggled fullscreen")

# File operations
def handle_files(command: str):
    if 'documents' in command:
        os.startfile(os.path.expanduser('~\\Documents'))
        speak("Opening Documents folder")
    elif 'downloads' in command:
        os.startfile(os.path.expanduser('~\\Downloads'))
        speak("Opening Downloads folder")
    elif 'pictures' in command:
        os.startfile(os.path.expanduser('~\\Pictures'))
        speak("Opening Pictures folder")
    elif 'music' in command:
        os.startfile(os.path.expanduser('~\\Music'))
        speak("Opening Music folder")
    elif 'videos' in command:
        os.startfile(os.path.expanduser('~\\Videos'))
        speak("Opening Videos folder")
    elif 'desktop' in command:
        os.startfile(os.path.expanduser('~\\Desktop'))
        speak("Opening Desktop folder")

# Web search
def web_search(query: str):
    if 'google' in query:
        speak("What would you like me to search on Google?")
        search_term = command()
        if search_term and search_term != "none":
            webbrowser.open(f"https://www.google.com/search?q={search_term}")
    elif 'youtube' in query:
        speak("What would you like me to search on YouTube?")
        search_term = command()
        if search_term and search_term != "none":
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_term}")
    elif 'wikipedia' in query:
        speak("What would you like me to search on Wikipedia?")
        search_term = command()
        if search_term and search_term != "none":
            webbrowser.open(f"https://en.wikipedia.org/wiki/{search_term}")

# Main execution loop
if __name__ == "__main__":
    wish_me()
    speak("I'm ready to assist you. How can I help?")
    
    while True:
        query = command().lower()
        
        if not query:
            continue
        
        # Exit condition
        if 'exit' in query or 'quit' in query or 'goodbye' in query:
            speak("Goodbye! Have a great day.")
            sys.exit()
        
        # Social media
        elif any(x in query for x in ['facebook', 'whatsapp', 'discord', 'instagram', 'twitter', 'linkedin', 'youtube', 'reddit', 'github']):
            handle_social_media(query)
        
        # Applications
        elif 'open' in query:
            open_application(query)
        elif 'close' in query or 'exit' in query:
            close_application(query)
        
        # System control
        elif any(x in query for x in ['shutdown', 'restart', 'reboot', 'sleep', 'lock', 'log off', 'sign out']):
            control_system(query)
        elif 'system condition' in query or 'system status' in query:
            report_system_condition()
        
        # Media control
        elif any(x in query for x in ['play', 'pause', 'next', 'previous', 'volume', 'mute', 'fullscreen']):
            control_media(query)
        
        # Files and folders
        elif any(x in query for x in ['documents', 'downloads', 'pictures', 'music', 'videos', 'desktop']):
            handle_files(query)
        
        # Web search
        elif any(x in query for x in ['google', 'youtube', 'wikipedia']):
            web_search(query)
        
        # Time and date
        elif 'time' in query:
            speak(f"The current time is {get_current_time()}")
        elif 'date' in query or 'day' in query:
            speak(f"Today is {get_current_day()}, {datetime.datetime.now().strftime('%B %d, %Y')}")
        
        # Help
        elif 'help' in query or 'what can you do' in query:
            help_text = """
            I can help you with many tasks including:
            - Opening applications like Calculator, Notepad, Word, Excel, etc.
            - Opening websites like Facebook, YouTube, Google, etc.
            - Controlling media playback (play/pause, next/previous, volume)
            - Managing system functions (shutdown, restart, sleep, lock)
            - Searching the web on Google, YouTube, or Wikipedia
            - Opening folders like Documents, Downloads, Pictures
            - Checking system status and battery level
            - Telling time and date
            """
            speak(help_text)
        
        else:
            speak("I'm not sure I understand. Could you please repeat or ask for help?")
