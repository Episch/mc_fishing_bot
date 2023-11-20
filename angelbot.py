import pyautogui
import cv2
import numpy as np
import pygetwindow as gw
import time

def find_image_and_right_click(window_title, target_image_path, max_attempts=1, interval=0.1):
    attempts = 0
    counter = 0
    caught_fishes = 0

    while attempts < max_attempts:
        try:
            # Find the window with the specified title
            window = gw.getWindowsWithTitle(window_title)[0]
            window.activate()

            # Wait briefly to ensure the window has focus
            time.sleep(interval)

            # Take a screenshot of the current window
            screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # Read the target image
            target_image = cv2.imread(target_image_path)

            # Try to find the target image in the screenshot
            result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            # Define a threshold to decide if the image is found
            threshold = 0.98

            if max_val >= threshold:
                target_center = (max_loc[0] + target_image.shape[1] // 2, max_loc[1] + target_image.shape[0] // 2)
                pyautogui.click(target_center[0] + window.left, target_center[1] + window.top, button='right')
                caught_fishes += 1
                print(f"Image with threshold '{max_val}' found. Right-click done!!!.")
                print(f"Caught fishes: '{caught_fishes}'")
                time.sleep(0.2)
                pyautogui.click(target_center[0] + window.left, target_center[1] + window.top, button='right')             
                print("Right-click done!!!.")
                counter = 0
                time.sleep(3)

            else:
                print(f"Current threshold '{max_val}'. Attempt #{counter + 1}")

        except IndexError:
            print(f"Window with title '{window_title}' not found.")
        except Exception as e:
            print(f"Error: {e}")

        counter += 1 
        attempts += 1
        time.sleep(interval)

# Example call
window_title = 'Minecraft'
target_image_path = 'C:\\Users\\david\\mc_angelbot\\example.png'
find_image_and_right_click(window_title, target_image_path)
