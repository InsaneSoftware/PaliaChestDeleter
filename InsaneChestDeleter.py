import pygetwindow as gw
import pyautogui
import time
import win32api
import win32con
import datetime
import tkinter as tk
from threading import Thread
import sys
import os

# Virtual key codes for keys
VK_CODE = {
    'i': 0x49,
    'end': 0x23,
    'del': 0x2E
}


root = None
label = None
paused = True

stop_pressed = False
catch_and_sell_count = 0
junk_count = 0

# Constants for mouse actions
MOUSE_LEFTDOWN = win32con.MOUSEEVENTF_LEFTDOWN
MOUSE_LEFTUP = win32con.MOUSEEVENTF_LEFTUP
MOUSE_RIGHTDOWN = win32con.MOUSEEVENTF_RIGHTDOWN
MOUSE_RIGHTUP = win32con.MOUSEEVENTF_RIGHTUP

def get_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return filename

def simulate_key_press(key):
    vk_code = VK_CODE.get(key, None)
    if vk_code is not None:
        win32api.keybd_event(vk_code, win32api.MapVirtualKey(vk_code, 0), 0, 0)
        time.sleep(0.1)  # Wait for a short duration
        win32api.keybd_event(vk_code, win32api.MapVirtualKey(vk_code, 0), win32con.KEYEVENTF_KEYUP, 0)


def simulate_right_click(x, y):
    # Move the mouse to the specified coordinates
    win32api.SetCursorPos((x, y))

    # Simulate a right mouse click
    win32api.mouse_event(MOUSE_RIGHTDOWN, x, y, 0, 0)  # Press the right mouse button
    win32api.mouse_event(MOUSE_RIGHTUP, x, y, 0, 0)  # Release the right mouse button


def simulate_mouse_click(x, y):
    win32api.SetCursorPos((x, y))

    win32api.mouse_event(MOUSE_LEFTDOWN, x, y, 0, 0)  # Press the left mouse button
    time.sleep(0.1)  # Wait for a short duration
    win32api.mouse_event(MOUSE_LEFTUP, x, y, 0, 0)  # Release the left mouse button


def create_overlay():  # Creating the overlay window
    global root, label

    root = tk.Tk()
    root.geometry('400x250+0+100')
    root.overrideredirect(1)
    root.attributes('-alpha', 1)
    root.attributes("-topmost", True)
    root.configure(bg='gray')  # border color

    inner_frame = tk.Frame(root, bg='black')
    inner_frame.pack(padx=2, pady=2, expand=True, fill='both')  # Ensure the frame expands and fills both X & Y

    info_text = "Press 'End' to start auto-clicker."
    label = tk.Label(inner_frame, text=info_text, bg='black', fg='white', anchor='nw', justify='left', font=("Arial", 10))
    label.pack(padx=10, pady=10, expand=True, fill='both')  # Ensure the label expands and fills both X & Y

    root.mainloop()


# Thread for the overlay window
overlay_thread = Thread(target=create_overlay)
overlay_thread.daemon = True  # Set the thread as daemon
overlay_thread.start()

def print_with_timestamp(message, update_count_only=False):
    current_time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    formatted_message = f"[{current_time}] {message}"

    catches_message = f"Total fish sold: {catch_and_sell_count}"
    junk_message = f"Total junk removed: {junk_count}"

    print(formatted_message)

    if label:
        existing_text = label.cget('text').split('\n')

        if update_count_only:
            if len(existing_text) > 2:
                existing_text[0] = catches_message  # update catch and sell count line
                existing_text[1] = junk_message     # update junk count line
            else:
                existing_text.insert(0, junk_message)
                existing_text.insert(0, catches_message)
        else:
            if len(existing_text) >= 13:
                existing_text.pop(2)  # Remove the oldest log, but keep count lines
            existing_text.append(formatted_message)  # Add the new message at the end
            existing_text[0] = catches_message      # Ensure the catch and sell count line is always at the top
            existing_text[1] = junk_message         # Ensure the junk count line is always second

        new_text = '\n'.join(existing_text)
        label.config(text=new_text)
        root.update()

while True:  # Infinite loop instead of stop_pressed
    try:
        # Check for the 'del' key to quit the program
        if win32api.GetAsyncKeyState(VK_CODE['del']) != 0:
            print_with_timestamp("DEL key pressed. Quitting the program...")
            if root:
                root.destroy()  # Close the Tkinter window
            sys.exit()  # Exit the program
        # Toggle pause state when the 'end' key is pressed
        if win32api.GetAsyncKeyState(VK_CODE['end']) != 0:
            paused = not paused  # Toggle the paused state

            if paused:
                print_with_timestamp("Auto-clicker paused. 'End' to continue.")
            else:
                print_with_timestamp("Auto-clicker resumed.")
            
            time.sleep(1)  # Sleep for a second to prevent accidental rapid toggling

        # Skip the rest of the loop if paused
        if paused:
            time.sleep(1)
            continue

        focused_window = gw.getActiveWindow()

        if focused_window is not None and 'Palia' in focused_window.title:  # find all palia windows

            # pause bot when in esc/options menu
            if pyautogui.locateOnScreen(get_path('img/options.png'), grayscale=True, confidence=0.80) is not None:
                print_with_timestamp("INFO: Waiting to get out of menu")
                time.sleep(3)
                continue

            # pause bot when in inventory
            if pyautogui.locateOnScreen(get_path('img/items.png'), grayscale=True, confidence=0.80) is not None:
                print_with_timestamp("INFO: Waiting to get out of inventory")
                time.sleep(3)
                continue

            simulate_mouse_click(1150, 450)  # right from the menu
            if pyautogui.locateOnScreen(get_path('img/perfect.png'), grayscale=True, confidence=0.80) is not None:
                if pyautogui.locateOnScreen(get_path('img/money.png'), grayscale=True, confidence=0.80) is not None:
                    catch_and_sell_count += 1  # Increment the counter
                    print_with_timestamp(f"INFO: Caught something and sold it")
                    time.sleep(2)

                else:
                    print_with_timestamp("WARNING: Detected Junk")
                    junk_count += 1
                    print_with_timestamp("", update_count_only=True)
                    # destroy chest
                    simulate_key_press('i')
                    time.sleep(1)
                    simulate_right_click(1100, 830)
                    time.sleep(1)
                    throwaway_position = pyautogui.locateCenterOnScreen(get_path('img/throwaway.png'), grayscale=True, confidence=0.80)
                    simulate_mouse_click(throwaway_position[0], throwaway_position[1])
                    time.sleep(1)
                    simulate_mouse_click(1030, 560)  # confirm destroy
                    time.sleep(1)
                    simulate_key_press('i')
                    print_with_timestamp("INFO: Junk deleted!")
                    time.sleep(1)

        else:
            print_with_timestamp("INFO: Waiting until Palia is focused")
            
    except Exception as e:
        print_with_timestamp("An error occurred: " + str(e))  # Print error message correctly
        time.sleep(1000)
        break