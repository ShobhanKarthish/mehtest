# Import libraries
import time
import logging
import openpyxl  # Writing to Excel files
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.chrome.service import Service

# Initializing logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Excel setup
wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(["Hotel Name", "Price"])

# Initializing ChromeDriver
service = Service(r"D:\selenium\trivago\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()
wait = WebDriverWait(driver, 15)

# Open Trivago
driver.get("https://www.trivago.in")

try:
    # 1) Search city
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='input-auto-complete']")))
    search_box.send_keys("Chennai")
    logging.info("Entered city name.")
    time.sleep(2)
    search_box.send_keys(Keys.ARROW_DOWN)
    search_box.send_keys(Keys.ENTER)

    # 2) Select check-in and check-out dates
    time.sleep(4)
    dates = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[@data-testid='calendar-day']")))
    dates[0].click()  # Check-in
    dates[1].click()  # Check-out
    logging.info("Selected check-in and check-out dates.")

    # 3) Wait for hotel results to load
    time.sleep(6)

    # 4) Take a screenshot
    screenshot_path = "trivago_results.png"
    driver.save_screenshot(screenshot_path)
    logging.info(f"Screenshot saved at {screenshot_path}")

    # 5) Simulate alert box
    driver.execute_script("alert('This is a test alert!')")
    time.sleep(2)
    try:
        alert = driver.switch_to.alert
        logging.info("Alert text: " + alert.text)
        alert.accept()
        logging.info("Alert accepted.")
    except NoAlertPresentException:
        logging.warning("No alert found.")

    # 6) Extract hotel names and prices
    hotels = driver.find_elements(By.XPATH, "//h3[@itemprop='name']")
    prices = driver.find_elements(By.XPATH, "//strong[@itemprop='price']")

    assert len(hotels) > 0, "No hotels found!"
    logging.info(f"Found {len(hotels)} hotel results.")

    for i in range(min(5, len(hotels))):
        hotel_name = hotels[i].text.strip()
        price = prices[i].text.strip() if i < len(prices) else "N/A"
        logging.info(f"{i+1}. {hotel_name} - ₹{price}")
        sheet.append([hotel_name, price])

    # 7) Save data to Excel
    excel_path = "trivago_hotels.xlsx"
    wb.save(excel_path)
    logging.info(f"Excel file saved as {excel_path}")

except Exception as e:
    logging.error(f"Error occurred: {e}")

finally:
    driver.quit()
    logging.info("Test completed and browser closed.")
