import pandas as pd
import time
import re
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def extract_phone_from_html(html_content):
    """Extract phone number from HTML content"""
    # Pattern để tìm số điện thoại trong HTML
    phone_patterns = [
        r'\+1\s*\d{3}-\d{3}-\d{4}',  # +1 646-410-0200
        r'\(\d{3}\)\s*\d{3}-\d{4}',  # (646) 410-0200
        r'\d{3}-\d{3}-\d{4}',        # 646-410-0200
        r'\d{10}',                    # 6464100200
        r'\+1\s*\d{10}',             # +1 6464100200
        r'tel:(\+?\d{1,2}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4})',  # tel: links
        r'phone[:\s]*(\+?\d{1,2}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4})',  # phone: text
        r'call[:\s]*(\+?\d{1,2}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4})',   # call: text
    ]
    
    for pattern in phone_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        if matches:
            phone = matches[0]
            # Clean up the phone number
            phone = re.sub(r'[^\d+]', '', phone)
            if len(phone) >= 10:
                return phone
    
    return ""

def extract_email_from_html(html_content):
    """Extract email from HTML content"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(email_pattern, html_content)
    if matches:
        return matches[0]
    return ""

def get_contact_info_from_website(website_url):
    """Get phone number and email from dispensary website"""
    try:
        if not website_url or website_url == "":
            return "", ""
        
        # Thêm protocol nếu cần
        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url
        
        print(f"  Đang truy cập: {website_url}")
        
        # Headers để giả lập browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Gửi request
        response = requests.get(website_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm kiếm số điện thoại và email
        phone = extract_phone_from_html(response.text)
        email = extract_email_from_html(response.text)
        
        if phone:
            print(f"    ✓ Tìm thấy số điện thoại: {phone}")
        else:
            print(f"    ✗ Không tìm thấy số điện thoại")
            
        if email:
            print(f"    ✓ Tìm thấy email: {email}")
        else:
            print(f"    ✗ Không tìm thấy email")
        
        return phone, email
        
    except Exception as e:
        print(f"    ✗ Lỗi khi truy cập website: {e}")
        return "", ""

def update_excel_with_contact_info():
    """Read Excel file, get contact info, and update"""
    try:
        # Đọc file Excel hiện tại
        print("Đang đọc file Excel...")
        df = pd.read_excel('ny_dispensaries.xlsx')
        print(f"Đã đọc {len(df)} dispensary")
        
        # Cập nhật thông tin liên hệ cho từng dispensary
        for index, row in df.iterrows():
            company_name = row['Company Name']
            website = row['Website']
            
            print(f"\n[{index + 1}/{len(df)}] Đang xử lý: {company_name}")
            
            # Bỏ qua nếu đã có đầy đủ thông tin
            if (pd.notna(row['Phone']) and row['Phone'] != '' and 
                pd.notna(row['Email']) and row['Email'] != ''):
                print(f"  Bỏ qua (đã có đầy đủ thông tin)")
                continue
            
            # Lấy thông tin từ website
            phone, email = get_contact_info_from_website(website)
            
            # Cập nhật DataFrame
            if phone:
                df.at[index, 'Phone'] = phone
            if email:
                df.at[index, 'Email'] = email
            
            # Lưu file sau mỗi 20 dispensary
            if (index + 1) % 20 == 0:
                print(f"\nĐã xử lý {index + 1}/{len(df)} dispensary, đang lưu file...")
                df.to_excel('ny_dispensaries_with_contacts.xlsx', index=False)
            
            # Đợi một chút để tránh bị block
            time.sleep(2)
        
        # Lưu file cuối cùng
        print("\nĐang lưu file cuối cùng...")
        df.to_excel('ny_dispensaries_with_contacts.xlsx', index=False)
        
        print(f"\nHoàn thành! Đã cập nhật {len(df)} dispensary")
        print("File mới: ny_dispensaries_with_contacts.xlsx")
        
        # Hiển thị thống kê
        phones_found = df['Phone'].notna().sum()
        emails_found = df['Email'].notna().sum()
        print(f"Số điện thoại đã tìm thấy: {phones_found}/{len(df)}")
        print(f"Số email đã tìm thấy: {emails_found}/{len(df)}")
        
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    print("Bắt đầu lấy thông tin liên hệ từ website của từng dispensary...")
    update_excel_with_contact_info() 