from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver import ActionChains
import time
import random
import os

# Load credentials from logs.txt
def load_credentials(file_name):
    credentials = []
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                credentials.append((username, password))
    return credentials

# Load crypto addresses from file
def load_addresses(file_name):
    addresses = []
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            addresses = [line.strip() for line in file]
    return addresses

# Prompt user to select ETH or SOL
def select_crypto():
    print("Select which crypto addresses to comment:")
    print("1. Ethereum (ETH)")
    print("2. Solana (SOL)")
    choice = input("Enter your choice (1 or 2): ")
    if choice == "1":
        return "eth.txt"
    elif choice == "2":
        return "sol.txt"
    else:
        print("Invalid choice. Defaulting to Ethereum (ETH).")
        return "eth.txt"

# Main automation function
def automate_comments(credentials, addresses, tweet_url):
    for username, password in credentials:
        try:
            print(f"Logging in as {username}...")
            driver = webdriver.Chrome()
            driver.maximize_window()

            # Log in to Twitter
            driver.get("https://twitter.com/i/flow/login")
            time.sleep(7)
            email = driver.find_element(By.NAME, 'text')
            email.send_keys(username)
            email.send_keys(Keys.ENTER)
            time.sleep(3)
            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys(password)
            password_field.send_keys(Keys.ENTER)
            time.sleep(5)

            # Navigate to the tweet
            driver.get(tweet_url)
            time.sleep(5)

            counter = 0
            while counter < 5:  # Customize the number of comments
                try:
                    # Select the comment input
                    comment_box = driver.find_element(By.CLASS_NAME, 'public-DraftStyleDefault-ltr')
                    comment = random.choice(addresses)
                    comment_box.send_keys(comment)
                    time.sleep(1)

                    # Post the comment
                    post_button = driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
                    post_button.click()
                    time.sleep(2)

                    counter += 1
                    print(f"Commented: {comment}")

                except Exception as e:
                    print(f"Error while commenting: {e}")
                    break

            print(f"Finished commenting as {username}")
            driver.quit()

        except Exception as e:
            print(f"Error with account {username}: {e}")
            if 'driver' in locals():
                driver.quit()

# Main execution
if __name__ == "__main__":
    # Load credentials
    credentials_file = "logs.txt"
    credentials = load_credentials(credentials_file)
    if not credentials:
        print(f"No credentials found in {credentials_file}. Exiting...")
        exit()

    # Load crypto addresses
    addresses_file = select_crypto()
    addresses = load_addresses(addresses_file)
    if not addresses:
        print(f"No addresses found in {addresses_file}. Exiting...")
        exit()

    # Specify the tweet URL
    tweet_url = "https://twitter.com/elonmusk/status/1708660084992029126"  # Replace with your desired tweet URL

    # Start automation
    automate_comments(credentials, addresses, tweet_url)
