from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from openpyxl import Workbook
import time
from datetime import datetime

def scrape_valorant_prices():
    # Konfigurasi Selenium
    url = "https://www.g2g.com/id/categories/valorant-top-up"

    # Setup Chrome options
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Jalankan browser
    driver = webdriver.Chrome(options=options)
    
    # Apply stealth settings
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    try:
        print("Opening website...")
        driver.get(url)

        print("Waiting for page to load...")
        time.sleep(10)

        # Scroll ke bawah untuk load produk
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        # Tunggu sampai elemen produk muncul
        print("Waiting for product elements to be visible...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.full-height.column.cursor-pointer.g-card-no-deco"))
        )

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
                
                data.append((points, price))
            except Exception as e:
                print(f"Error extracting data from product #{idx+1}: {str(e)}")
                continue

        # Generate filename dengan timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"valorant_prices_{timestamp}.xlsx"

        # Simpan ke Excel
        if data:
            wb = Workbook()
            ws = wb.active
            ws.append(["Points", "Price"])

            for row in data:
                ws.append(row)

            wb.save(filename)
            return filename
        else:
            raise Exception("No data found to save.")

    finally:
        driver.quit() 