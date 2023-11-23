import requests
from bs4 import BeautifulSoup
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

province = str(input("Enter the province: "))
district = str(input("Enter the district"))
type_of_la = str(input("Enter the type_of_la"))
la = str(input("Enter the la"))


driver = webdriver.Chrome()
driver.get("https://pfm.smartcitylk.org/wp-admin/profile.php")

username_field = driver.find_element(By.NAME, "log")
password_field = driver.find_element(By.NAME, "pwd")

username_field.send_keys("kiruba00004@gmail.com")
password_field.send_keys("TAFpfm#99283")

login_button = driver.find_element(By.ID, "wp-submit")
login_button.click()

wait = WebDriverWait(driver, 10)

change_button = wait.until(EC.element_to_be_clickable((By.ID, "change")))
change_button.click()

province_select_element = wait.until(EC.presence_of_element_located((By.NAME, "province")))
province_select = Select(province_select_element)
province_select.select_by_visible_text(province)


dis_select_element = wait.until(EC.presence_of_element_located((By.NAME, "district")))
dis_select = Select(dis_select_element)
dis_select.select_by_visible_text(district)

Tla_select_element = wait.until(EC.presence_of_element_located((By.NAME, "type_of_la")))
Tla_select = Select(Tla_select_element)
Tla_select.select_by_visible_text(type_of_la)

la_select_element = wait.until(EC.presence_of_element_located((By.NAME, "la_name")))
la_select = Select(la_select_element)
la_select.select_by_visible_text(la)

change_button1 = driver.find_element(By.ID, "submit")
change_button1.click()



login_url = 'https://pfm.smartcitylk.org/wp-login.php'
target_url = 'https://pfm.smartcitylk.org/wp-admin/admin.php?page=annualBudget'
username = 'kiruba00004@gmail.com'
password = 'TAFpfm#99283'

# Create a session to persist the login credentials
session = requests.Session()

# Perform login
login_payload = {
    'log': username,
    'pwd': password,
    'wp-submit': 'Log In',
    'redirect_to': target_url,
}
login_response = session.post(login_url, data=login_payload)

# Check if login was successful
if 'wp-admin' in login_response.url:
    print("Login successful")
    
    
    # Fetch the target page
    target_page = session.get(target_url)
    
    # Parse HTML content
    soup = BeautifulSoup(target_page.content, 'html.parser')
    
    # Find all tables on the page
    tables = soup.find_all('table')

    # Create a new Excel workbook
    workbook = openpyxl.Workbook()
    # Create a new sheet
    sheet = workbook.active
    
    # Extract and add data from each table to the sheet
    for index, table in enumerate(tables):
        # Add a new sheet for each table
        sheet = workbook.create_sheet(title=f'Table {index + 1}')
        for row in table.find_all('tr'):
            # Extract data from each row
            columns = row.find_all(['th', 'td'])
            data = [column.text.strip() for column in columns]
            # Add data to the sheet
            sheet.append(data)

    # Save the workbook to a file
    workbook.save(la +'.xlsx')
    print("Excel file created successfully.")

else:
    print("Login failed")
