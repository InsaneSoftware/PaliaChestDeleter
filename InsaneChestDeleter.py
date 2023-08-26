import pygetwindow as gw
import pyautogui
import time
import win32api
import win32con
import datetime
import tkinter as tk
from threading import Thread

# Virtual key codes for keys
VK_CODE = {
    'i': 0x49,
    'end': 0x23
}

root = None
label = None

# Constants for mouse actions
MOUSE_LEFTDOWN = win32con.MOUSEEVENTF_LEFTDOWN
MOUSE_LEFTUP = win32con.MOUSEEVENTF_LEFTUP
MOUSE_RIGHTDOWN = win32con.MOUSEEVENTF_RIGHTDOWN
MOUSE_RIGHTUP = win32con.MOUSEEVENTF_RIGHTUP

# stop key
stop_key = 'esc'
stop_pressed = False


def print_with_timestamp(message):
    current_time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    print(f"[{current_time}] {message}")


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
    root.attributes("-transparentcolor", "white")
    root.configure(bg='white')

    label = tk.Label(root, text="", bg='black', fg='white', anchor='nw', justify='left', font=("Arial", 10))
    label.pack(padx=10, pady=10, expand=True, fill='both')

    root.mainloop()


# Thread for the overlay window
overlay_thread = Thread(target=create_overlay)
overlay_thread.daemon = True  # Set the thread as daemon
overlay_thread.start()


def print_with_timestamp(message):
    current_time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    formatted_message = f"[{current_time}] {message}"

    print(formatted_message)

    if label:
        existing_text = label.cget('text')
        new_text = existing_text + '\n' + formatted_message
        label.config(text=new_text)
        root.update()


while not stop_pressed:
    try:
        if win32api.GetAsyncKeyState(VK_CODE['end']) != 0:
            stop_pressed = True
            print_with_timestamp("INFO: Exit key pressed")
            break

        focused_window = gw.getActiveWindow()

        if focused_window is not None and 'Palia' in focused_window.title:  # find all palia windows

            # pause bot when in esc/options menu
            if pyautogui.locateOnScreen('img/options.png', grayscale=True, confidence=0.80) is not None:
                print_with_timestamp("INFO: Waiting to get out of menu")
                time.sleep(3)
                continue

            # pause bot when in inventory
            if pyautogui.locateOnScreen('img/items.png', grayscale=True, confidence=0.80) is not None:
                print_with_timestamp("INFO: Waiting to get out of inventory")
                time.sleep(3)
                continue

            simulate_mouse_click(1150, 450)  # right from the menu
            if pyautogui.locateOnScreen('img/perfect.png', grayscale=True, confidence=0.80) is not None:
                if pyautogui.locateOnScreen('img/money.png', grayscale=True, confidence=0.80) is not None:
                    print_with_timestamp("INFO: I caught something and sold it")
                    time.sleep(2)  # don`t spam pls xD
                else:
                    print_with_timestamp("WARNING: I caught Junk")

                    # destroy chest
                    simulate_key_press('i')
                    time.sleep(1)
                    simulate_right_click(1100, 830)
                    time.sleep(1)
                    throwaway_position = pyautogui.locateCenterOnScreen('img/throwaway.png', grayscale=True,
                                                                        confidence=0.80)  # Check for throwaway button instead. This is necessary because sometimes you don't get a chest and a collectable item
                    simulate_mouse_click(throwaway_position[0], throwaway_position[1])
                    time.sleep(1)
                    simulate_mouse_click(1030, 560)  # confirm destroy
                    time.sleep(1)
                    simulate_key_press('i')
                    print_with_timestamp("INFO: JUNK deleted!")
                    time.sleep(1)

        else:
            print_with_timestamp("INFO: Waiting until Palia is focused")
            time.sleep(3)
    except Exception as e:
        print_with_timestamp("An error occurred: " + str(e))  # Print error message correctly
        break  # Break the loop.
