import os
import time
import threading
from tkinter import Tk, ttk, PhotoImage
from PIL import Image
import pyautogui
import cv2


def get_file_path():
    return os.path.dirname(os.path.abspath(__file__))


def capture_screen(Champion, Seconds):
    try:
        time.sleep(0.2)
        screen_width, screen_height = pyautogui.size() #support for many different resolutions above 1400x900 (i guess it won't work on resolutions under these 2 x and y values)
        reference_width = 2556
        reference_height = 1440
        scaling_factor_width = screen_width / reference_width
        scaling_factor_height = screen_height / reference_height
        region_x = int(2046 * scaling_factor_width)
        region_y = int(997 * scaling_factor_height)
        region_width = int(920 * scaling_factor_width)
        region_height = int(430 * scaling_factor_height)
        picture1 = pyautogui.screenshot(region=(region_x, region_y, region_width, region_height))

        path = get_file_path()
        picture1.save(os.path.join(path, "Jungle-Tracker-Picture.jpg"))

        TestJungle = cv2.imread(os.path.join(path, f"Champions_Jungle_Tracker/m{Champion}.PNG"), cv2.IMREAD_UNCHANGED)
        DesktopTest = cv2.imread(os.path.join(path, "Jungle-Tracker-Picture.jpg"), cv2.IMREAD_UNCHANGED)

        nesne = cv2.cvtColor(DesktopTest, cv2.COLOR_BGR2GRAY)
        nesne1 = cv2.cvtColor(TestJungle, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(nesne1, nesne, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val > 0.76:
            zuletzt_gesehen = pyautogui.screenshot(region=(2046, 997, 920, 430))
            time.sleep(0.5)
            zuletzt_gesehen.save(os.path.join(path, "Jungle-Tracker-Picture2.png"))
            return 0  

        if max_val < 0.76:
            time.sleep(0.5)
            return Seconds + 1 
    except Exception as e:
        print("error:", e)


class Picture:
    def __init__(self, parent):
        self.parent = parent
        path = get_file_path()
        img = PhotoImage(file=os.path.join(path, "Jungle-Tracker-Picture2.PNG"))
        self.label = ttk.Label(self.parent, image=img)
        self.label.pack()

        self.start_button = ttk.Button(self.parent, text='Start', command=self.start_thread)
        self.start_button.pack()

        self.stop_button = ttk.Button(self.parent, text="Stop", command=self.stop)
        self.stop_button.pack()

        self.champ_entry = ttk.Entry(self.parent)
        self.champ_entry.pack()

        self.count = 0
        self.seconds = 0

    def start_thread(self):
        self.count = 1
        threading.Thread(target=self.update).start()

    def stop(self):
        self.count = 0

    def update(self):
        champ = self.champ_entry.get().lower()
        while self.count:
            self.seconds = capture_screen(champ, self.seconds)
            path = get_file_path()
            img = PhotoImage(file=os.path.join(path, "Jungle-Tracker-Picture2.PNG"))
            self.label.config(image=img)
            self.label.image = img

            if hasattr(self, 'label1'):
                self.label1.destroy()

            self.label1 = ttk.Label(self.parent, text=f"{self.seconds} seconds since last seen")
            self.label1.pack()


def main():
    root = Tk()
    root.geometry('800x600')
    Picture(root)
    root.mainloop()


if __name__ == "__main__":
    main()
