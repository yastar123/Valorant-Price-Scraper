from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook
import time

# Konfigurasi Selenium
url = "https://www.g2g.com/id/categories/valorant-top-up"

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Jalankan browser dengan ChromeDriver otomatis
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

print("Opening website...")
driver.get(url)

print("Waiting for page to load...")
time.sleep(10)  # Increase wait time

# Scroll ke bawah untuk load produk
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

# Tunggu sampai elemen produk muncul
print("Waiting for product elements to be visible...")
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.full-height.column.cursor-pointer.g-card-no-deco"))
    )
except Exception as e:
    print(f"Timeout waiting for product elements: {str(e)}")

# Ambil semua elemen produk
product_cards = driver.find_elements(By.CSS_SELECTOR, "a.full-height.column.cursor-pointer.g-card-no-deco")
print(f"Found {len(product_cards)} product cards.")

data = []
for idx, card in enumerate(product_cards):
    try:
        # Ambil points
        points_elem = card.find_element(By.CSS_SELECTOR, ".text-body1.ellipsis-2-lines span")
        points = points_elem.text.strip()
        
        # Ambil harga
        price_elem = card.find_element(By.CSS_SELECTOR, ".row.items-baseline.q-gutter-xs.text-body1.justify-end")
        price = price_elem.text.strip()
        
        print(f"\n--- Product #{idx+1} ---")
        print(f"Points: {points}")
        print(f"Price: {price}")
        
        data.append((points, price))
    except Exception as e:
        print(f"Error extracting data from product #{idx+1}: {str(e)}")
        continue

print(f"\nTotal products scraped: {len(data)}")

# Simpan ke Excel
if data:
    print("Saving to Excel...")
    wb = Workbook()
    ws = wb.active
    ws.append(["Points", "Price"])

    for row in data:
        ws.append(row)

    wb.save("valorant_prices.xlsx")
    print("Excel file saved successfully!")
else:
    print("No data found to save.")

driver.quit()
