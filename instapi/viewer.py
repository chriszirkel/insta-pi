import tkinter as tk
from PIL import Image, ImageTk
import random
import os
import sys


class Viewer(tk.Tk):
    def __init__(self, dir, interval):
        #self.root = tk.Tk()
        tk.Tk.__init__(self)
        self.title('My Pictures')
        self.attributes('-fullscreen', True)
        self.configure(background='black')
        self.bind('<Escape>', self.close)

        self.dir = dir
        # calculate microseconds
        self.interval = interval * 1000
        self.images = []
        self.current_image = None

        # root has no image argument, so use a label as a panel
        self.panel = tk.Label(self) #, image=self.image1
        self.panel.configure(background='black')
        self.panel.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

    def view(self):
        print('view images')

        self.load_images()
        self.update_image()
        self.mainloop()

    def close(self, event):
        self.destroy()
        sys.exit()

    def load_images(self):
        self.images = os.listdir(self.dir)

        print('%d images loaded' % len(self.images))

    def update_image(self):
        if not self.images:
            return

        random_image = random.choice(self.images)

        self.current_image = ImageTk.PhotoImage(Image.open(os.path.join(self.dir, random_image)))
        self.panel.configure(image=self.current_image)
        self.after(self.interval, self.update_image)

        print('update image: %s' % random_image)