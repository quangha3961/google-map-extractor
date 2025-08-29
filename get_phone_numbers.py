import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def setup_driver():
    """Setup Chrome driver with options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        print(f"Không thể khởi tạo Chrome driver: {e}")
        return None

def extract_phone_from_html(html_content):
    """Extract phone number from HTML content"""
    # Pattern để tìm số điện thoại trong HTML
    phone_patterns = [
        r'\+1\s*\d{3}-\d{3}-\d{4}',  # +1 646-410-0200
        r'\(\d{3}\)\s*\d{3}-\d{4}',  # (646) 410-0200
        r'\d{3}-\d{3}-\d{4}',        # 646-410-0200
        r'\d{10}',                    # 6464100200
        r'\+1\s*\d{10}',             # +1 6464100200
    ]
    
    for pattern in phone_patterns:
        matches = re.findall(pattern, html_content)
        if matches:
            return matches[0]
    
    return ""

def search_google_maps(driver, company_name):
    """Search Google Maps for company and extract phone number"""
    try:
        # Tạo URL Google Maps
        search_query = f"{company_name} dispensary NY"
        url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
        
        print(f"Đang tìm kiếm: {company_name}")
        driver.get(url)
        
        # Đợi trang load
        time.sleep(3)
        
        # Tìm kiếm số điện thoại trong HTML
        page_source = driver.page_source
        
        # Tìm số điện thoại từ các pattern khác nhau
        phone = extract_phone_from_html(page_source)
        
        if phone:
            print(f"  ✓ Tìm thấy số điện thoại: {phone}")
            return phone
        else:
            print(f"  ✗ Không tìm thấy số điện thoại")
            return ""
            
    except Exception as e:
        print(f"  ✗ Lỗi khi tìm kiếm {company_name}: {e}")
        return ""

def update_excel_with_phones():
    """Read Excel file, get phone numbers, and update"""
    try:
        # Đọc file Excel hiện tại
        print("Đang đọc file Excel...")
        df = pd.read_excel('ny_dispensaries.xlsx')
        print(f"Đã đọc {len(df)} dispensary")
        
        # Khởi tạo driver
        driver = setup_driver()
        if not driver:
            print("Không thể khởi tạo browser")
            return
        
        # Cập nhật số điện thoại cho từng dispensary
        for index, row in df.iterrows():
            company_name = row['Company Name']
            
            # Bỏ qua nếu đã có số điện thoại
            if pd.notna(row['Phone']) and row['Phone'] != '':
                print(f"Bỏ qua {company_name} (đã có số điện thoại)")
                continue
            
            # Tìm kiếm số điện thoại
            phone = search_google_maps(driver, company_name)
            
            # Cập nhật DataFrame
            df.at[index, 'Phone'] = phone
            
            # Lưu file sau mỗi 10 dispensary
            if (index + 1) % 10 == 0:
                print(f"Đã xử lý {index + 1}/{len(df)} dispensary, đang lưu file...")
                df.to_excel('ny_dispensaries_with_phones.xlsx', index=False)
            
            # Đợi một chút để tránh bị block
            time.sleep(2)
        
        # Lưu file cuối cùng
        print("Đang lưu file cuối cùng...")
        df.to_excel('ny_dispensaries_with_phones.xlsx', index=False)
        
        print(f"Hoàn thành! Đã cập nhật {len(df)} dispensary")
        print("File mới: ny_dispensaries_with_phones.xlsx")
        
        # Hiển thị thống kê
        phones_found = df['Phone'].notna().sum()
        print(f"Số điện thoại đã tìm thấy: {phones_found}/{len(df)}")
        
        driver.quit()
        
    except Exception as e:
        print(f"Lỗi: {e}")
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    print("Bắt đầu lấy số điện thoại từ Google Maps...")
    update_excel_with_phones() 