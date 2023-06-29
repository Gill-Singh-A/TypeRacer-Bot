#! /usr/bin/env python3

from datetime import date
from selenium import webdriver
from optparse import OptionParser
from selenium.webdriver.common.by import By
from colorama import Fore, Back, Style
from time import strftime, localtime, sleep

status_color = {
    '+': Fore.GREEN,
    '-': Fore.RED,
    '*': Fore.YELLOW,
    ':': Fore.CYAN,
    ' ': Fore.WHITE
}

def display(status, data, start='', end='\n'):
    print(f"{start}{status_color[status]}[{status}] {Fore.BLUE}[{date.today()} {strftime('%H:%M:%S', localtime())}] {status_color[status]}{Style.BRIGHT}{data}{Fore.RESET}{Style.RESET_ALL}", end=end)

def get_arguments(*args):
    parser = OptionParser()
    for arg in args:
        parser.add_option(arg[0], arg[1], dest=arg[2], help=arg[3])
    return parser.parse_args()[0]

WPM = 99

class TypeRacer:
    website = "https://play.typeracer.com"
    def __init__(self, wpm):
        self.browser = webdriver.Firefox()
        display('+', "Created Browser")
        display(':', f"Loading the TypeRacer Page {Back.MAGENTA}({TypeRacer.website}){Back.RESET}")
        self.browser.get(TypeRacer.website)
        display('+', f"Loaded the TypeRacer Page {Back.MAGENTA}({TypeRacer.website}){Back.RESET}")
        self.wpm = wpm
    def start(self):
        while True:
            try:
                start_tag = [tag for tag in self.browser.find_elements(By.TAG_NAME, "a") if tag.text == "Enter a Typing Race"][0]
                start_tag.click()
                return
            except:
                pass
    def next(self):
        next_tag = [tag for tag in self.browser.find_elements(By.TAG_NAME, "a") if tag.text == "Race again"][0]
        next_tag.click()
    def check_ad(self):
        try:
            close_tag = [tag for tag in self.browser.find_elements(By.TAG_NAME, "div") if tag.get_attribute("title") == "close this popup"]
            if len(close_tag) > 0:
                close_tag[0].click()
        except:
            pass
    def get_text(self):
        return self.browser.find_element(By.XPATH, "//span[@unselectable='on']").find_element(By.XPATH, "..").text
    def checkTrafficLight(self):
        while len(self.browser.find_elements(By.XPATH, "//img[@class='trafficLight']")) > 0:
            pass
    def simulate_typing(self):
        text = self.get_text()
        cps = 12 / self.wpm
        self.checkTrafficLight()
        typing_tag = self.browser.find_element(By.XPATH, "//input[@class='txtInput']")
        for character in text:
            typing_tag.send_keys(character)
            sleep(cps)
    def close(self):
        self.browser.close()
        display('+', "Browser Closed")

if __name__ == "__main__":
    data = get_arguments(('-w', "--wpm", "wpm", f"Speed with which to simulate Typing (should be less than 100) (Default={WPM})"))
    if not data.wpm:
        display('*', "Speed not specified")
        data.wpm = WPM
        display(':', f"Typing with speed {data.wpm}")
    else:
        data.wpm = int(data.wpm)
    type_racer = TypeRacer(data.wpm)
    try:
        type_racer.start()
        races = 0
        while True:
            type_racer.check_ad()
            sleep(2)
            type_racer.simulate_typing()
            sleep(2)
            type_racer.next()
            sleep(2)
            races += 1
            display('*', f"Races Done = {Back.MAGENTA}{races}{Back.RESET}", start='\r', end='')
    except KeyboardInterrupt:
        print()
        display(':', "Keyboard Interrupt Detected...")
        display('+', "Quitting")
    type_racer.close()