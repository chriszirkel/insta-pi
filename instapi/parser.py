from time import sleep
from selenium import webdriver
import urllib.request
import os.path
import traceback


class Parser:
    def __init__(self, url, dir, username, password, browser):
        self.url = url
        self.dir = dir
        self.username = username
        self.password = password
        self.browser = browser
        self.driver = None

    def parse(self):
        try:
            self.start_webdriver()
            self.login()
            self.load_profile()

            images = self.search_images()
            self.download_images(images)

            return True
        except Exception as e:
            traceback.print_exc()

            if self.driver:
                self.driver.save_screenshot('screenshot.png')

            return False
        finally:
            if self.driver:
                self.driver.close()

    def start_webdriver(self):
        print('start webdriver with {}'.format(self.browser))

        if self.browser == 'Firefox':
            profile = webdriver.FirefoxProfile()
            profile.set_preference('intl.accept_languages', 'en')
            self.driver = webdriver.Firefox()
        elif self.browser == 'Chrome':
            options = webdriver.ChromeOptions()
            options.add_argument('--lang=en')
            self.driver = webdriver.Chrome(chrome_options=options)
        else:
            webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.Accept-Language'] = 'en-US'
            self.driver = webdriver.PhantomJS()  # service_args=['--load-images=no']

        self.driver.set_window_size(800, 600)
        self.driver.implicitly_wait(30)
        self.driver.get(self.url)

    def login(self):
        print('login')

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
        else:
            raise RuntimeError('login failed')

    def load_profile(self):
        print('load profile')

        profile = self.driver.find_element_by_xpath('//a[text() = "Profile"]')

        if profile:
            profile.click()
        else:
            raise RuntimeError('load profile failed')

        saved = self.driver.find_element_by_xpath('//a[contains(@href,"/saved/")]')

        if saved:
            saved.click()
        else:
            raise RuntimeError('load saved images failed')

    def search_images(self):
        print('search images')

        images = {}
        last_height = self.get_scroll_height()

        while True:
            img_tags = self.driver.find_elements_by_xpath('//a[contains(@href,"?saved-by")]//img')

            for img in img_tags:
                src = img.get_attribute('src')
                file = src.split('/')[-1]

                if file not in images:
                    images[file] = src

            # Calculate new scroll height and compare with last scroll height
            new_height = self.scroll_down()

            if new_height == last_height:
                break
            last_height = new_height

        print('{} images found'.format(len(images)))

        return images

    def download_images(self, images):
        print('download images')

        if not os.path.exists(self.dir):
            os.makedirs(self.dir, exist_ok=True)

        files = os.listdir(self.dir)

        for file, url in images.items():
            if file in files:
                files.remove(file)
                continue

            print('download image: %s' % url)
            urllib.request.urlretrieve(url, os.path.join(self.dir, file))

        for file in files:
            print('delete image: %s' % file)
            os.remove(os.path.join(self.dir, file))

    def scroll_down(self):
        print('scroll down')

        SCROLL_PAUSE_TIME = 30

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        return self.get_scroll_height()

    def get_scroll_height(self):
        return self.driver.execute_script("return document.body.scrollHeight")
