import pyautogui
import cv2
import numpy as np
import time
import os
from heroes import scrape_hero_data, download_hero_images

# Load hero data
heroes = scrape_hero_data()

# Ensure hero images are downloaded
download_hero_images(heroes)

def take_screenshot():
    region = (0, 0, pyautogui.size()[0], pyautogui.size()[1] - 100)  # Adjust this to your screen resolution
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save("screenshot.png")

def recognize_heroes():
    img = cv2.imread("screenshot.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    recognized_heroes = []
    
    for hero in heroes:
        hero_img_path = f"heroes/{hero['name'].replace(' ', '-').lower()}.png"
        if os.path.exists(hero_img_path):
            hero_img = cv2.imread(hero_img_path, cv2.IMREAD_GRAYSCALE)
            res = cv2.matchTemplate(gray, hero_img, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)
            
            if len(loc[0]) > 0:
                recognized_heroes.append(hero['name'])
    
    return recognized_heroes

def main():
    take_screenshot()
    heroes_in_screenshot = recognize_heroes()
    print(f"Recognized heroes: {heroes_in_screenshot}")

# Adding a button click event
def on_button_click():
    main()

if __name__ == "__main__":
    time.sleep(5)  # Delay to allow you to bring up the Dota 2 screen
    on_button_click()