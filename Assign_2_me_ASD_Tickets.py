import time
# For Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


# Initialize the WebDriver
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

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
password.send_keys("202506#Jdmr")
password.send_keys(Keys.ENTER)

# Waiting for DUO
search_dashboard = wait.until(EC.presence_of_element_located((By.XPATH, '//h1[text()="Europe&Latam"]')))
print("Logged successfully into Jira - ", search_dashboard.text)

# Opening ASD Open Tickets
dailysanity_Jira = "https://jira.onmobile.com/issues/?filter=68337"
driver.get(dailysanity_Jira)
print("Opening the 'Daily Sanity' Filer Page: ", dailysanity_Jira)

# Waiting for the Filter Page
wait_issue_links = wait.until(EC.presence_of_element_located((By.XPATH, '//h1[text()="ASD_Europe_SiteOps"]')))
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

    # Assign To me
    try:
        assign_l3_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="action_id_131"]')))
        assign_l3_button.click()
        print(f"Clicked 'Assign to L3' button for {issue_key}")
        assign_l3_button_1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="assign-to-me-trigger"]')))
        assign_l3_button_1.click()
        assign_l3_button_2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="issue-workflow-transition-submit"]')))
        assign_l3_button_2.click()
        # Wait Assign is done
        WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.ID, 'workflow-transition-131-dialog')))
        print(f"Assigned to me Jira: {issue_key}")
    except Exception as e:
        print(f"Could not Assign to me Jira: {issue_key}: {e}")

# Quit the WebDriver
driver.quit()