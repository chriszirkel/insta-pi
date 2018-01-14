import tkinter as tk
from PIL import Image, ImageTk
import random
import pprint
import os


class Viewer:
    def __init__(self, dir):
        self.root = tk.Tk()
        self.root.title('My Pictures')
        self.root.attributes('-fullscreen', True)
        self.root.configure(background='black')

        self.dir = dir
        self.images = []
        self.current_image = None

        # root has no image argument, so use a label as a panel
        self.panel = tk.Label(self.root) #, image=self.image1
        self.panel.configure(background='black')
        self.panel.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

    def view(self):
        print('view images')

        self.load_images()
        self.update_image()
        self.root.mainloop()

    def load_images(self):
        self.images = os.listdir(self.dir)

        print('%d images loaded' % len(self.images))

    def update_image(self):
        random_image = random.choice(self.images)

        self.current_image = ImageTk.PhotoImage(Image.open(os.path.join(self.dir, random_image)))
        self.panel.configure(image=self.current_image)
        self.root.after(5000, self.update_image)

        print('update image: %s' % random_image)