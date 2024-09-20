import tkinter as tk
from tkinter import filedialog, simpledialog
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json

# Function to send connection requests
def send_connection_request(username, password, profile_urls):
    driver = webdriver.Chrome()  # Use the appropriate WebDriver for your browser
    driver.get('https://www.linkedin.com/login')

    time.sleep(2)  # Wait for the page to load
    email_elem = driver.find_element(By.ID, 'username')
    email_elem.send_keys(username)
    password_elem = driver.find_element(By.ID, 'password')
    password_elem.send_keys(password)
    password_elem.send_keys(Keys.RETURN)

    time.sleep(5)  # Wait for login to complete

    for profile_url in profile_urls:
        driver.get(profile_url)
        time.sleep(3)  # Wait for the profile to load
        try:
            connect_button = driver.find_element(By.XPATH, '//button[text()="Connect"]')
            connect_button.click()
            time.sleep(2)

            add_note_button = driver.find_element(By.XPATH, '//button[text()="Add a note"]')
            add_note_button.click()
            time.sleep(2)

            note_elem = driver.find_element(By.XPATH, '//textarea')
            note_elem.send_keys("Hi, I'd like to connect with you on LinkedIn.")
            send_button = driver.find_element(By.XPATH, '//button[text()="Send"]')
            send_button.click()
        except Exception as e:
            print("Error:", e)

    time.sleep(5)
    driver.quit()

# Function to read profile URLs from different file types
def read_profile_urls(file_path):
    profile_urls = []
    file_extension = file_path.split('.')[-1].lower()

    if file_extension == 'csv':
        df = pd.read_csv(file_path)
        profile_urls = df['Profile URL'].tolist()  # Adjust based on your CSV structure
    elif file_extension in ['xlsx', 'xls']:
        df = pd.read_excel(file_path)
        profile_urls = df['Profile URL'].tolist()  # Adjust based on your Excel structure
    elif file_extension == 'json':
        with open(file_path, 'r') as f:
            data = json.load(f)
            profile_urls = [item['Profile URL'] for item in data]  # Adjust based on your JSON structure
    # Add code here for Word or other formats if needed

    return profile_urls

# Function to get user input from GUI
def get_user_input():
    username = simpledialog.askstring("Input", "Enter your LinkedIn email:")
    password = simpledialog.askstring("Input", "Enter your LinkedIn password:", show='*')
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("All Files", "*.*")])

    if username and password and file_path:
        profile_urls = read_profile_urls(file_path)
        send_connection_request(username, password, profile_urls)

# Set up the GUI
root = tk.Tk()
root.withdraw()  # Hide the root window
get_user_input()
