#!/usr/bin/env python
from time import sleep
from selenium import webdriver
import urllib.request
import re
import os.path
import traceback
import pprint


class Parser:
    def __init__(self, url, dir, username, password):
        self.url = url
        self.dir = dir
        self.username = username
        self.password = password
        self.driver = None

    def parse(self):
        print('parse instagram')
        try:
            # self.options = webdriver.ChromeOptions()
            # self.options.add_argument('--lang=en')
            # self.driver = webdriver.Chrome(chrome_options=self.options)

            webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.Accept-Language'] = 'en-US'
            self.driver = webdriver.PhantomJS()
            self.driver.set_window_size(1920, 1080)
            self.driver.implicitly_wait(5)
            self.driver.get(self.url)

            if not os.path.exists(self.dir):
                os.makedirs(self.dir, exist_ok=True)

            files = os.listdir(self.dir)

            login = self.driver.find_element_by_xpath('//a[contains(text(),"Log in")]')

            if login:
                login.click()

            username = self.driver.find_element_by_xpath('//input[contains(@name,"username")]')
            password = self.driver.find_element_by_xpath('//input[contains(@name,"password")]')
            login = self.driver.find_element_by_xpath('//button[contains(text(),"Log in")]')

            if username and password and login:
                username.send_keys(self.username)
                password.send_keys(self.password)
                login.click()

            profile = self.driver.find_element_by_xpath('//a[contains(text(),"Profile")]')

            if profile:
                profile.click()

            saved = self.driver.find_element_by_xpath('//a[contains(string(),"SAVED")]')

            if saved:
                saved.click()

            self.scroll_to_bottom()

            images = self.driver.find_elements_by_xpath('//a[contains(@href,"?saved-by")]//img')

            print('%d images found' % len(images))

            for image in images:
                src = image.get_attribute('src')
                file = src.split('/')[-1]

                if file in files:
                    files.remove(file)
                    continue

                print('download image: %s' % src)
                urllib.request.urlretrieve(src, os.path.join(self.dir, file))

            for file in files:
                print('delete image: %s' % file)
                os.remove(os.path.join(self.dir, file))

            # for image in saved_images:
            #     href = image.get_attribute('href')
            #     img = image.find_element_by_tag_name('img')
            #     src = img.get_attribute('src')
            #     id = re.search('\/p\/(.+)\/\?.+', href).group(1)
            #
            #     file = id + '.jpg'
            #
            #     image = {
            #         'file':file,
            #         'src':src
            #     }
            #
            #     self.images.append(image)

        except Exception as e:
            traceback.print_exc()
            self.driver.save_screenshot('screenshot.png')

        finally:
            self.driver.close()

    def scroll_to_bottom(self):
        SCROLL_PAUSE_TIME = 1.5

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
