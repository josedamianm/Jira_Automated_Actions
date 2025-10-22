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

# Opening My Open Issues
myopenissues_Jira = "https://jira.onmobile.com/issues/?filter=64080"
driver.get(myopenissues_Jira)
print("Opening the 'MyOpenIssues' Filer Page: ", myopenissues_Jira)

# Waiting for the Filter Page
wait_issue_links = wait.until(EC.presence_of_element_located((By.XPATH, '//h1[text()="MyOpenIssues"]')))
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
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'key-val')))
    print(f"Opening issue page: {issue_key}")

    # Resolve Jira
    try:
        # Wait until Resolved button is present
        wait_resolved_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="action_id_41"]')))
        wait_resolved_button.click()
        print(f"Clicked 'Resolved' button for {issue_key}")
        # Security Incident
        select_security_incident = wait.until(EC.presence_of_element_located((By.ID, "customfield_27870")))
        select = Select(select_security_incident)
        select.select_by_value("52865")
        # Comments
        my_comment="Air conditioned failure on Pavone Site, the same was fixed by OpCo and we have restored all the services."
        Comments = wait.until(EC.presence_of_element_located((By.ID, "customfield_10041")))
        Comments.send_keys(my_comment)
        # Fault Attribution
        select_fault_attribution = wait.until(EC.presence_of_element_located((By.ID, "customfield_23979")))
        select = Select(select_fault_attribution)
        select.select_by_value("52870")
        # Closure Code
        select_closure_code = wait.until(EC.presence_of_element_located((By.ID, "customfield_15565")))
        select = Select(select_closure_code)
        select.select_by_value("56011")
        # Resolved By
        select_resolved_by = wait.until(EC.presence_of_element_located((By.ID, "customfield_22361")))
        select = Select(select_resolved_by)
        select.select_by_value("53259")
        # Resolved Missed SLA
        select_resolved_sla = wait.until(EC.presence_of_element_located((By.ID, "customfield_22716")))
        select = Select(select_resolved_sla)
        select.select_by_value("36882")
        # Service Impact
        select_service_impact = wait.until(EC.presence_of_element_located((By.ID, "customfield_29964")))
        select = Select(select_service_impact)
        select.select_by_value("55116")
        # Click Resolved
        click_resolved_button = wait.until(EC.presence_of_element_located((By.ID, "issue-workflow-transition-submit")))
        click_resolved_button.click()
        # Wait Resolved is completed
        WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.ID, 'workflow-transition-41-dialog')))
        print(f"Resolved Jira: {issue_key}")
    except Exception as e:
        print(f"Could not Resolve Jira: {issue_key}: {e}")

# Quit the WebDriver
driver.quit()