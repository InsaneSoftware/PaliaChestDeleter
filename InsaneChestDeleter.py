import pygetwindow as gw
import pyautogui
import time
import win32api
import win32con
import datetime

# Virtual key codes for keys
VK_CODE = {
    'i': 0x49,
    'end': 0x23
}

# Constants for mouse actions
MOUSE_LEFTDOWN = win32con.MOUSEEVENTF_LEFTDOWN
MOUSE_LEFTUP = win32con.MOUSEEVENTF_LEFTUP
MOUSE_RIGHTDOWN = win32con.MOUSEEVENTF_RIGHTDOWN
MOUSE_RIGHTUP = win32con.MOUSEEVENTF_RIGHTUP

# stop key
stop_key = 'esc'
stop_pressed = False


def print_with_timestamp(message):
    current_time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')
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


print_with_timestamp("Started auto delete chests and clicker...")

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
                    print_with_timestamp("INFO: I catched something and sold it")
                    time.sleep(2)  # dont spam pls xD
                else:
                    print_with_timestamp("WARNING: I catched something but cannot sell it!")

                    # destroy chest
                    simulate_key_press('i')
                    time.sleep(1)
                    simulate_right_click(1100, 830)
                    time.sleep(1)
                    simulate_mouse_click(1150, 910)  # destroy chest
                    time.sleep(1)
                    simulate_mouse_click(1030, 560)  # confirm destroy
                    time.sleep(1)
                    simulate_key_press('i')
                    print("INFO: Chest deleted!")
                    time.sleep(1)
        else:
            print_with_timestamp("INFO: Waiting until Palia is focussed (opened)")
            time.sleep(3)
    except Exception as e:
        print_with_timestamp("An error occurred:", e)
