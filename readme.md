# Auto Delete Chests and Clicker for Palia Game

This script automates the process of deleting chests and handling item interactions within the Palia game. It utilizes various Python libraries and Windows API functions to simulate key presses and mouse actions to perform in-game actions automatically.

## Game Requirements

Before using this script, make sure the following game requirements are met:

- The game needs to be running in **1920x1080 fullscreen windowed mode** for proper GUI recognition.
- You must set up fish selling functionality as described in [this guide](https://www.unknowncheats.me/forum/other-mmorpg-and-strategy/596326-palia-multihack.html) before using this script.
- Ensure that your **inventory is empty** and does not contain any chests or fish (worms are okay) before running the script.

## Prerequisites

Before running the script, make sure you have the following libraries and tools installed:

- [pygetwindow](https://pypi.org/project/PyGetWindow/): A cross-platform library to manage windows.
- [pyautogui](https://pypi.org/project/PyAutoGUI/): A library for GUI automation and screen capture functions.
- [win32api](https://pypi.org/project/pywin32/): Part of the `pywin32` package, providing access to Windows API functions.
- [win32con](https://pypi.org/project/pywin32/): Also part of the `pywin32` package, containing Windows constants.

## Usage

1. Install the required libraries by running the following commands:

``` bash
pip install opencv-python PyGetWindow PyAutoGUI pywin32
```

2. Ensure you have appropriate image files (`options.png`, `items.png`, `catch.png`, `money.png`) available in a folder named `img` in the same directory as the script. These images are used for GUI recognition.

3. Run the script using a Python interpreter:

``` bash
python InsaneChestDeleter.py
```

4. Once the script is running, it will automatically perform actions within the Palia game as defined in the script. The script checks for specific windows and images to determine when to take actions.

## Configuration

- `VK_CODE`: Virtual key codes for certain keys used in the script.
- `MOUSE_LEFTDOWN`, `MOUSE_LEFTUP`, `MOUSE_RIGHTDOWN`, `MOUSE_RIGHTUP`: Constants for mouse actions.
- `stop_key`: The key that can be pressed to stop the script (`end` by default).

## Features

- The script automates clicking on certain positions on the screen.
- It identifies specific images on the screen to make decisions, such as determining if an item is catchable or sellable.
- If a catchable item is found, it automatically sells it. If a catchable item is not sellable, it attempts to delete the chest containing it.
- The script will pause its actions when the game is in the options menu or the inventory screen.

## Important Note

- This script is intended for educational and illustrative purposes. Make sure to review and understand the game's terms of use and policies before using any form of automation.

---

Make sure to customize the script according to your needs and ensure that you are complying with the terms of use of the game. Always exercise caution when using automation scripts for games.
