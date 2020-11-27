import sys
import time
from threading import Thread
import random
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import tkinter as tk
#
start = time.time()
delay = .1
left_button = Button.left
right_button = Button.right
start_stop_key = ""
# start_stop_key = KeyCode(char='s')
# exit_key = KeyCode(char='e')
# run_key = KeyCode(char='r')
click_count = 0
randomize = 0
keybind_code = KeyCode(char='')

# Function to update click counter for UI
def update_clicks():
    global click_count # updates counter on every click
    click_count += 1
    click_counter['text'] = 'Total clicks: ' + str(click_count)
    if click_limit.get().isdigit():
        if click_count >= int(click_limit.get()): # Stops counter and resets if at limit
            click_thread.stop_clicking()
            click_count = 0

# Class to define mouse click functions
# Runs in its own thread
class ClickMouse(Thread):
    # Initiates mouse clicks with button set to left, default delay, and not running
    def __init__(self, delay, left_button):
        super().__init__()
        self.delay = delay
        self.button = left_button
        self.running = False
        self.program_running = True
    # Allows for changing delay between clicks
    def change_delay(self, delay):
        self.delay = delay
    # Starts clicking process
    def start_clicking(self):
        if self.running is False: # Resets click counter if originally not running
            global click_count
            click_count = 0
        if click_delay.get().isdigit(): # Changes click delay based on variable
            self.change_delay(float(click_delay.get()))
        self.running = True # Enables clicking
    # Allows for change between left click and right click
    # When called, swaps between left and right click
    def swap_button(self):
        if self.button == left_button:
            left_or_right['text'] = 'right click'
            self.button = right_button
        else:
            left_or_right['text'] = 'left click'
            self.button = left_button
    # Disables clicking
    def stop_clicking(self):
        self.running = False
    # Closes program
    def exit(self):
        self.stop_clicking()
        self.program_running = False
    # Function ran to keep track of delay and counter while clicking is enabled
    def run(self):
        while self.program_running:
            while self.running:
                # Calls function to click mouse
                mouse.click(self.button)
                global click_count
                # Updates click count
                update_clicks()
                # If randomize is on, randomize delay
                if randomize.get() == 1:
                    delay = (random.random() * .2 - .1) * self.delay + self.delay
                    print(delay)
                    # Sleep to create delay
                    time.sleep(delay)
                else:
                    time.sleep(self.delay)

# Screen sizes
HEIGHT = 400
WIDTH = 700
# Root window
root = tk.Tk()

# Debugging through print statements
def test_function(entry):
    print(entry)

# Sets up page based on window size
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# def get_weather(city):
# weather_key: 'key'
# url = 'url'
# params = {'APPID' : weather_key, 'q': city, 'units' : 'imperial'}
# response = requests.get(url, params=params)
# print(response.json())

# name = weather['name']
# print(weather['weather'][0]['description'])
# print(weather['main']['temp'])

# background_image = tk.PhotoImage(file='dancingBadger.png')
# background_label = tk.Label(root, image=background_image)
# background_label.place(x=0,y=0,relwidth=1, relheight=1)

# Window title
root.title("Autoclicker")

# First frame: Header text
frame = tk.Frame(root, bd=5, highlightbackground='black', highlightthickness=1)
frame.place(relwidth=.9, relheight=.9, relx=.05, rely=.05)
title = tk.Label(frame, font=10, text="Autoclicker by Joseph Zhou")
title.place(relx=.3, rely=0)

#Bottom left frame
half1 = tk.Frame(root, bd=5, highlightbackground='black', highlightthickness=1)
half1.place(relwidth=.45, relheight=.8, relx=.05, rely=.15)
# Contact
general_desc = tk.Label(half1, font=10, text="For issues or inquiries\n Contact me at\n josephzhou1234@gmail.com")
general_desc.place(relx=.08, rely=0)

# UI for setting keybind
key_explanation = tk.Label(half1, text="Click to set a keybind.", font=20)
key_explanation.place(relx=.17, rely=.3)
# Keybind variable
keybind = tk.IntVar()
# Start and stop button
start_stop_key = tk.Checkbutton(half1, font=10, variable=keybind)
start_stop_key.place(relx=.45, rely=.4)
# Outputs chosen key from keybind
key_bind = tk.Label(half1, text="Keybind: ", font=20)
key_bind.place(relx=.3, rely=.5)

# UI for left or right click
left_or_right = tk.Label(half1, font=20, text="left click")
# left_or_right.config(font=("Courier", 10))
left_or_right.place(relx=.65, rely=.7)
# Button for left or right click
swap_button = tk.Button(half1, text='swap', command=lambda: click_thread.swap_button())
swap_button.place(relx=.65, rely=.8, relwidth=.25, relheight=.15)
#Description for left or right click
swap_explanation = tk.Label(half1, font=10, text="Press to swap\nbetween left\n and right click")
swap_explanation.place(relx=.1, rely=.72)

# Bottom right frame
half2 = tk.Frame(root, bd=5, highlightbackground='black', highlightthickness=1)
half2.place(relwidth=.45, relheight=.8, relx=.5, rely=.15)
# UI for click limit
click_label = tk.Label(half2, text="Click limit: ", font=40)
click_label.place(relx=.27, rely=.1)
# Input for click limit
click_limit = tk.Entry(half2, font=20, bg='white')
click_limit.place(relheight=.1, relwidth=.3, relx=.6, rely=.1)

# UI for click speed
speed_label = tk.Label(half2, text="Click speed (s): ", font=30)
speed_label.place(rely=.3, relx=.1)
# Entry for click speed
click_delay = tk.Entry(half2, text=".1", font=20, bg='white')
click_delay.place(relheight=.1, relwidth=.3, relx=.6, rely=.3)

# UI for click randomizer
randomize = tk.IntVar()
# Entry for click randomizer
randomize_clicks = tk.Checkbutton(half2, font=10, text="Randomize clicks", variable=randomize)
randomize_clicks.place(relx=.27, rely=.5)

#Init of CLickMouse variable and start of thread
mouse = Controller()
click_thread = ClickMouse(delay, left_button)
click_thread.start()
# entry = tk.Entry(frame, bg='green', font=40)
# entry.place(relwidth=.65, relheight=1)

# UI for clicking
# Button to start clicking
start_clicking = tk.Button(half2, text="Start Clicking", font=40, command=lambda: click_thread.start_clicking())
start_clicking.place(relx=.05, rely=.65, relheight=.2, relwidth=.4)
# Button to stop clicking
stop_clicking = tk.Button(half2, text="Stop Clicking", font=40, command=lambda: click_thread.stop_clicking())
stop_clicking.place(relx=.55, rely=.65, relheight=.2, relwidth=.38)
# lower_frame = tk.Frame(root, bg='green', bd=10)
# lower_frame.place(relx=.5, rely=.25, relwidth=.75, relheight=.6, anchor='n')

# UI for click counter
click_counter = tk.Label(half2, text="Total clicks: ", bd=5, highlightthickness=2, font=30)
click_counter.config(highlightbackground='black', highlightcolor='black')
click_counter.place(relx=.25, rely=.87)

# Function to connect key presses to enabling and disabling clicker
# Even when window is not in focus
def on_press(key):
    global keybind_code
    print("running")
    if keybind.get() == 1:
        keybind_code = key
        key_bind['text'] = 'KeyBind: ' + str(keybind_code)
        keybind.set(0)
    elif key == keybind_code:
        print("working?")
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()

# Debug statement
def start_listener(event):
    print("listener running")


# root.bind_all('<KeyPress>', start)
# root.bind('<FocusOut>', start_listener)

# Starts listener to allow for events when window is not in focus
def listener_start():
    with Listener(on_press=on_press) as listener:
        listener.join()

# Closes program upon window closing
def on_closing():
    print("closed")
    root.destroy()

# Binds page to events
root.bind_all("<1>", lambda event: event.widget.focus_set())
# Starts thread for listener to connect to program
t2 = Thread(target=listener_start)

# Starts all parts of the application
end = time.time()
print('loading time:' + str(end - start))
root.protocol("WM_DELETE_WINDOW", on_closing)
t2.setDaemon(True)
t2.start()
root.mainloop()

# Closes all parts of the application when all threads end
click_thread.exit()
sys.exit()
