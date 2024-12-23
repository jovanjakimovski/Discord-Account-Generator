import random
import string
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from src.api import GuerrillaMail, find_email_type, dfilter_email, pfilter_email  # Updated import
from src.ui import UI

def generate_username(base="user", length=5):
    """Generates a random username based on a base name and random string."""
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"{base}_{random_string}"

def password_gen(length=10):
    """Generates a random password."""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

class DiscordGen:
    def __init__(self, email, username, password, proxy=None):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        if proxy:
            options.add_argument(f"--proxy-server={proxy}")

        self.driver = webdriver.Chrome(options=options)
        self.email = email
        self.username = username
        self.password = password

    def register(self):
        try:
            self.driver.get("https://discord.com/register")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))

            # Fill out the registration form
            self.driver.find_element(By.XPATH, "//input[@type='email']").send_keys(self.email)
            self.driver.find_element(By.XPATH, "//input[@type='text' and @name='global_name']").send_keys(self.username)
            self.driver.find_element(By.XPATH, "//input[@type='text' and @name='username']").send_keys(self.username)
            self.driver.find_element(By.XPATH, "//input[@type='password']").send_keys(self.password)

            # Set random date of birth
            dob_fields = self.driver.find_elements(By.CLASS_NAME, "css-1hwfws3")
            actions = ActionChains(self.driver)
            actions.move_to_element(dob_fields[0]).click().send_keys(str(random.randint(1, 12))).send_keys(Keys.ENTER)
            actions.move_to_element(dob_fields[1]).click().send_keys(str(random.randint(1, 28))).send_keys(Keys.ENTER)
            actions.move_to_element(dob_fields[2]).click().send_keys(str(random.randint(1990, 2001))).send_keys(Keys.ENTER)
            actions.perform()

            # Click register button
            self.driver.find_element(By.CLASS_NAME, "contents_dd4f85").click()
            print("Registration submitted. Solve CAPTCHA manually.")
        except TimeoutException:
            print("Timeout while registering.")
        except WebDriverException as e:
            print(f"WebDriverException: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            time.sleep(100)  # Give time to solve CAPTCHA manually if needed

    def close(self):
        self.driver.quit()

def process_email(proxy=None):
    """Handles email fetching and Discord account creation."""
    try:
        guerrilla_mail = GuerrillaMail()  # Create instance of GuerrillaMail
        email = guerrilla_mail.get_email()  # Fetch temporary email from Guerrilla Mail API

        if not email:
            print("Failed to get email from Guerrilla Mail.")
            return

        # Email filtering logic (same as before)
        email_type = find_email_type(email)

        if email_type == 'dot':
            email = dfilter_email(email)
        elif email_type == 'plus':
            email = pfilter_email(email)

        # Generate username and password
        username = generate_username()
        password = password_gen()

        # Create the Discord account
        discord_gen = DiscordGen(email, username, password, proxy)
        discord_gen.register()
        discord_gen.close()
    except Exception as e:
        print(f"Error in process_email: {e}")

        
def worker(proxy=None):
    """Worker function for threaded account creation."""  
    try:
        process_email(proxy)
    except Exception as e:
        print(f"Error in worker: {e}")

def main():
    """Main entry point for the program."""
    UI.banner()
    user_choice = input("Choose an option:\n1. Single Account Creation\n2. Multithreaded Creation\n> ")

    if user_choice == '1':
        process_email()
    elif user_choice == '2':
        num_threads = int(input("Enter the number of threads: "))
        proxies = []  # Replace with logic to load proxies if needed
        threads = [
            threading.Thread(target=worker, args=(random.choice(proxies) if proxies else None,))
            for _ in range(num_threads)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
