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
wait = WebDriverWait(driver, 50)

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

# Opening Filter Page
localUser_Jira = "https://jira.onmobile.com/issues/?filter=68337"
driver.get(localUser_Jira)
print("Opening the 'Local User Login' Filer Page: ", localUser_Jira)

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
    
    # Clicking on the "Assign to L3" button
    try:
        assign_button_anchor = wait.until(EC.presence_of_element_located((By.ID, "action_id_131")))
        assign_button_anchor.click()
        print(f"Clicked 'Assign to L3' Anchor button for {issue_key}")
    except Exception as e:
        print(f"Could not click 'Assign to L3' Anchor button for {issue_key}: {e}")

    # Send Enter key for the "Assign to L3"
    try:
        click1 = wait.until(EC.presence_of_element_located((By.ID, "issue-workflow-transition-submit")))
        click1.send_keys(Keys.RETURN)
        print(f"Clicked 'Assign to L3' Confirmation button for {issue_key}")
    except Exception as e:
        print(f"Could not Clicked 'Assign to L3' Confirmation button: {e}")

    # Clicking on Resolved
    try:
        clickResolved = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='trigger-label' and text()='Resolved']")))
        clickResolved.click()
        print("Clicked on Resolved")

        # Selecting the Options:
        select_Security = wait.until(EC.presence_of_element_located((By.ID, "customfield_27870")))
        select = Select(select_Security)
        select.select_by_value("52865")

        select_FaultAtribution = driver.find_element(By.ID, "customfield_23979")
        select = Select(select_FaultAtribution)
        select.select_by_value("52869")

        select_ClosureCode = driver.find_element(By.ID, "customfield_15565")
        select = Select(select_ClosureCode)
        select.select_by_value("53234")
    
        select_ResolvedBy = driver.find_element(By.ID, "customfield_22361")
        select = Select(select_ResolvedBy)
        select.select_by_value("53259")

        # Filling SLA
        try:
            ReasonMissedSLA = driver.find_element(By.ID, "customfield_22716")
            select = Select(ReasonMissedSLA)
            select.select_by_value("36882")
        except Exception as e:
            print("Not Found Reason for Missed Resolution SLA")
    
        select_ServiceImpact = driver.find_element(By.ID, "customfield_29964")
        select = Select(select_ServiceImpact)
        select.select_by_value("55118")

        # Confirm Resolved
        try:
            confirmResolved = driver.find_element(By.ID, "issue-workflow-transition-submit")
            confirmResolved.click()
            print("Clicked on Confirm Resolved")
        except Exception as e:
            print(f"Could not Confirm Resolved {e}")

    except Exception as e:
        print(f"Could not Clicked on Resolved {e}")


# Quit the WebDriver
driver.quit()
