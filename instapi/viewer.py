import tkinter as tk
from PIL import Image, ImageTk
import random
import os
import sys


class Viewer(tk.Tk):
    def __init__(self, dir, interval):
        tk.Tk.__init__(self)
        self.title('My Pictures')
        self.attributes('-fullscreen', True)
        self.configure(background='black')
        self.config(cursor="none")
        self.bind('<Escape>', self.close)
        self.bind('<Configure>', self._resize_image)

        self.dir = dir
        # calculate microseconds
        self.interval = interval * 1000
        self.images = []
        self.current_image = None

        self.panel = tk.Label(self)
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
        print('load images')

        self.images = os.listdir(self.dir)

        print('%d images loaded' % len(self.images))

    def update_image(self):
        if not self.images:
            return

        random_image = random.choice(self.images)

        self.current_image = ImageTk.PhotoImage(self.resize_image(random_image))
        self.panel.configure(image=self.current_image)
        self.after(self.interval, self.update_image)

        print('update image: %s' % random_image)

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height

    def resize_image(self, original_image):
        image = Image.open(os.path.join(self.dir, original_image))
        image_width, image_height = image.size

        window_width = self.winfo_width()
        window_height = self.winfo_height()

        scale_x = image_width / window_width

        if scale_x > 1.0:
            image_width = image_width / scale_x
            image_height = image_height / scale_x

        scale_y = image_height / window_height

        if scale_y > 1.0:
            image_height = image_height / scale_y
            image_width = image_width / scale_y

        if scale_x > 1.0 or scale_y > 1.0:
            image.resize((int(image_width), int(image_height)), Image.ANTIALIAS)

        return image
