from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select

import time
import random
from datetime import datetime
from dateutil.parser import parse

# Start a Chrome DevTools debugging session
service = Service("/Users/josemanco/Development/chromedriver")

# Use the DevTools Protocol to connect to the existing Chrome session
chrome_options = webdriver.ChromeOptions()

# Connect to the existing Chrome session
driver = webdriver.Chrome(service=service, options=chrome_options)

# Opening Jira WebPage
Jira_WebPage = "https://jira.onmobile.com/"
driver.get(Jira_WebPage)
print("Opening Jira WEB Page")

# Defining Waiting Object for 50 seconds
wait = WebDriverWait(driver, 60)

# Waiting for the username and password fields to be present
username = wait.until(EC.presence_of_element_located((By.ID, "login-form-username")))
password = wait.until(EC.presence_of_element_located((By.ID, "login-form-password")))

# Adding Login Details
username.send_keys("jose.manco")
password.send_keys("202407@Jdmr")
password.send_keys(Keys.ENTER)

# Waiting for DUO
search_dashboard = wait.until(EC.presence_of_element_located((By.XPATH, '//h1[text()="Europe&Latam"]')))
print("Logged successfully into Jira - ", search_dashboard.text)

# Opening Filter Page For Daily Sanity
dailysanity_Jira = "https://jira.onmobile.com/issues/?filter=70439"
driver.get(dailysanity_Jira)
print("Opening the 'Daily Sanity' Filer Page: ", dailysanity_Jira)

# Waiting for the Filter Page
wait_issue_links = wait.until(EC.presence_of_element_located((By.XPATH, '//h1[text()="Daily_Sanity_Completed"]')))
print("Opened Filter Page: ", wait_issue_links.text)

# Extract elements with the class 'issue-link'
issue_links = driver.find_elements(By.CLASS_NAME, "issue-link")

# Use a set to store unique issues
unique_issues = set()

# Extract and print the relevant attributes
for link in issue_links:
    issue_key = link.get_attribute("data-issue-key")
    href = link.get_attribute("href")
    unique_issues.add((issue_key, href))

# Print the unique issues
for issue_key, href in unique_issues:
    print(f"Issue Key: {issue_key}, URL: {href}")

# Visit each unique issue URL
for issue_key, href in unique_issues:
    driver.get(href)
    print(f"Opening issue page: {issue_key}")
    
    # Getting Creation date and generating New date
    time_element = driver.find_element(By.CLASS_NAME, 'livestamp')
    datetime_str = time_element.get_attribute('datetime')
    # Parse the datetime string to a datetime object
    creation_date = parse(datetime_str)
    # Generate a new random hour greater than the current hour
    current_hour = creation_date.hour
    new_hour = random.randint(current_hour + 4, 16)
    # Modify the datetime object with the new hour
    new_creation_date = creation_date.replace(hour=new_hour)
    # Store the final datetime object in a variable
    date_started = new_creation_date.strftime('%d/%b/%y %I:%M %p')
    print(f"Jira Creation Date: {creation_date}")
    print(f"Start Date: {date_started}")

    # Logging Work
    try:
        more_button = wait.until(EC.presence_of_element_located((By.ID, "opsbar-operations_more")))
        more_button.click()
        print(f"Clicked 'More' button for {issue_key}")
        logwork_button = wait.until(EC.presence_of_element_located((By.ID, "log-work")))
        logwork_button.click()
        # Adding Log Work
        input_log_work = wait.until(EC.presence_of_element_located((By.ID, "log-work-time-logged")))
        input_log_work.send_keys("1h")
        # Locate the input element
        input_element = driver.find_element(By.ID, 'log-work-date-logged-date-picker')
        # Clear the existing value (if needed)
        input_element.clear()
        # Set the new value using the formatted date
        input_element.send_keys(date_started)
        # Clicking Log Work Button
        logwork_click = wait.until(EC.presence_of_element_located((By.ID, "log-work-submit")))
        logwork_click.click()
        print("Logged Work")
    except Exception as e:
        print(f"Could not log work for {issue_key}: {e}")

    # Closing Jira
    try:
        # Wait until the dialog is no longer visible
        WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.ID, 'log-work-dialog')))
        close_button = wait.until(EC.presence_of_element_located((By.ID, "action_id_701")))
        close_button.click()
        print(f"Clicked 'Close' button for {issue_key}")
        closeissue_button = wait.until(EC.presence_of_element_located((By.ID, "issue-workflow-transition-submit")))
        closeissue_button.click()
        # Wait until the dialog is no longer visible
        WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.ID, 'workflow-transition-701-dialog')))
        print("Closed Jira")
    except Exception as e:
        print(f"Could not Close Jira: {issue_key}: {e}")


# Quit the WebDriver
driver.quit()
