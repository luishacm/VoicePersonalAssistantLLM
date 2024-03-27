import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from external_commands import ExternalCommands
import time
import psutil
import pygetwindow as gw
import pyautogui
import re
import string

profile_path = "selenium/profiles"
#//div contains "Use default model"
class Browser:

    def __init__(self, popup_queue):
        self.popup_queue = popup_queue
        self.__close_chrome()
        self.__open_chrome()
        # self.__minimize_chrome()
        self.__goto_gpt_page()
        self.open_new_chat()

    def exec(self, message):
        print("Sending the prompt...")
        command = self.__check_commands(message)
        if command:
            return command
        if command is False:
            self.__send_message_to_chat(self.__generate_prompt(message))
            time.sleep(2)
            self.__check_finished_message()
            texto = self.__get_answer()
            return texto

    def open_new_chat(self, chat_name="text-davinci-002-render-sha"):
        new_chat_xpath = "//span[contains(text(), 'New Chat')]"
        element = self.driver.find_element(By.XPATH, new_chat_xpath)
        element.click()
        time.sleep(1)
        gpt_4_xpath = f"//li[@data-testid='{chat_name}']"
        element = self.driver.find_element(By.XPATH, gpt_4_xpath)
        element.click()
        time.sleep(1)

    def __open_chrome(self):
        chrome_options = uc.ChromeOptions()
        chrome_options.user_data_dir = profile_path
        self.driver = uc.Chrome(options=chrome_options)

    def __generate_prompt(self, message):
        message = f"{message}"
        return message
    
    def __goto_gpt_page(self):
        self.driver.get("https://chat.openai.com/?model=gpt-4")
        time.sleep(3)
        # self.driver.save_screenshot('nowsecure.png')

    def __send_message_to_chat(self, message: str):
        prompt_text_area = "//textarea[@id='prompt-textarea']"
        element = self.driver.find_element(By.XPATH, prompt_text_area)
        element.click()
        element.send_keys(message)
        element.send_keys(Keys.ENTER)

    def __get_answer(self):
        assistant_response = "//div[@data-message-author-role='assistant']"
        elements = self.driver.find_elements(By.XPATH, assistant_response)
        try:
            if elements:
                last_element = elements[-1]
            texto = last_element.text
            return texto
        except Exception:
            return ""

    def __check_finished_message(self):
        start_time = time.time()
        elapsed_time = 0
        while elapsed_time < 120:
            regenerate_xpath = "//div[contains(text(),'Regenerate')]"
            try:
                self.driver.find_element(By.XPATH, regenerate_xpath)
                return
            except Exception:
                self.popup_queue.put(self.__get_answer())
                time.sleep(0.5)
                elapsed_time = time.time() - start_time
        raise Exception
    
    def __close_chrome(self):
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if process.info['name'] == 'chrome.exe':
                psutil.Process(process.info['pid']).terminate()

    def __minimize_chrome(self):
        chrome_windows = gw.getWindowsWithTitle('Google Chrome')
        for window in chrome_windows:
            if window._hWnd:
                pyautogui.moveTo(window.left + 5, window.top + 5)
                pyautogui.click()
                pyautogui.hotkey('win', 'down')

    @classmethod
    def __check_commands(self, message):
        message_normalized = ExternalCommands.normalize_message(message)
        if "gpt4" == message_normalized.replace(" ", ""):
            self.open_new_chat("gpt-4")
            return message_normalized
        elif "gpt3" == message_normalized.replace(" ", ""):
            self.open_new_chat("text-davinci-002-render-sha")
            return message_normalized
        else:
            return ExternalCommands.execute_commands(message_normalized)
