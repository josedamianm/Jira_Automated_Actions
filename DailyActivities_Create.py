# For Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

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
password.send_keys("JoJeMaNa@2010")
password.send_keys(Keys.ENTER)

# Waiting for DUO
search_dashboard = wait.until(EC.presence_of_element_located((By.XPATH, '//h1[text()="Europe&Latam"]')))
print("Logged successfully into Jira - ", search_dashboard.text)

############################################################################################################
# Creating My Daily Jira
############################################################################################################

# Click on Create Jira
create_button = wait.until(EC.presence_of_element_located((By.ID, "create_link")))
create_button.click()
print(f"Clicked on Create button")

# Select Project and Issue Type
project_options = wait.until(EC.presence_of_element_located((By.ID, 'project')))
driver.execute_script("arguments[0].value = '23052';", project_options)
issue_type = driver.find_element(By.ID, "issuetype-field")
driver.execute_script("""
    var inputElement = document.getElementById('issuetype-field');
    inputElement.setAttribute('aria-activedescendant', 'task-73');
""")
issue_type.send_keys(Keys.ENTER)

# Adding Data
summary = wait.until(EC.presence_of_element_located((By.ID, "summary")))
summary.send_keys("Daily Activities - Jose Manco")

select_tasktype = wait.until(EC.presence_of_element_located((By.ID, "customfield_10190")))
select = Select(select_tasktype)
select.select_by_value("48286")

select_subtasktype = wait.until(EC.presence_of_element_located((By.ID, "customfield_23875")))
select = Select(select_subtasktype)
select.select_by_value("48267")

select_customer = wait.until(EC.presence_of_element_located((By.ID, "customfield_10001")))
select = Select(select_customer)
if select.all_selected_options[0].get_attribute('value') == '-1':
    select.deselect_by_value('-1')
select.select_by_value("20315")
select.select_by_value("13910")
select.select_by_value("28958")
select.select_by_value("17911")

circle = wait.until(EC.presence_of_element_located((By.ID, "customfield_11342")))
circle.send_keys("Madrid")

expected_closure_date = wait.until(EC.presence_of_element_located((By.ID, "customfield_10072")))
expected_closure_date.clear()
expected_closure_date.send_keys("31/Dec/25 08:00 PM")

select_geography = wait.until(EC.presence_of_element_located((By.ID, "customfield_11563")))
select = Select(select_geography)
if select.all_selected_options[0].get_attribute('value') == '-1':
    select.deselect_by_value('-1')
select.select_by_value("15873")

assigntome = wait.until(EC.presence_of_element_located((By.ID, "assign-to-me-trigger")))
assigntome.click()

justify_reveneu = wait.until(EC.presence_of_element_located((By.ID, "customfield_10120")))
justify_reveneu.send_keys("Please execute the daily activities")

add_description = wait.until(EC.presence_of_element_located((By.ID, "description")))
add_description.send_keys("Please execute the daily activities")

click_create = wait.until(EC.presence_of_element_located((By.ID, "issue-create-submit")))
click_create.click()

# Waiting for Jira creation
jiracreated = wait.until(EC.presence_of_element_located((By.XPATH, '//h1[text()="[Orange Spain, Telefonica Spain, Vodafone Greece, Vodafone-Spain]-Daily Activities - Jose Manco"]')))
print("Created successfully the Jira - ", jiracreated.text)

# Quit the WebDriver
driver.quit()
