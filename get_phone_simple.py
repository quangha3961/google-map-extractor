import pandas as pd
import time
import re
import requests
from urllib.parse import quote

def search_google_maps_simple(company_name):
    """Search Google Maps using requests and extract phone number"""
    try:
        # Tạo URL Google Maps
        search_query = f"{company_name} dispensary NY"
        encoded_query = quote(search_query)
        url = f"https://www.google.com/maps/search/{encoded_query}"
        
        print(f"Đang tìm kiếm: {company_name}")
        
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
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Tìm kiếm số điện thoại trong HTML
        html_content = response.text
        
        # Pattern để tìm số điện thoại
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
                phone = matches[0]
                print(f"  ✓ Tìm thấy số điện thoại: {phone}")
                return phone
        
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
        
        # Cập nhật số điện thoại cho từng dispensary
        for index, row in df.iterrows():
            company_name = row['Company Name']
            
            # Bỏ qua nếu đã có số điện thoại
            if pd.notna(row['Phone']) and row['Phone'] != '':
                print(f"Bỏ qua {company_name} (đã có số điện thoại)")
                continue
            
            # Tìm kiếm số điện thoại
            phone = search_google_maps_simple(company_name)
            
            # Cập nhật DataFrame
            df.at[index, 'Phone'] = phone
            
            # Lưu file sau mỗi 10 dispensary
            if (index + 1) % 10 == 0:
                print(f"Đã xử lý {index + 1}/{len(df)} dispensary, đang lưu file...")
                df.to_excel('ny_dispensaries_with_phones.xlsx', index=False)
            
            # Đợi một chút để tránh bị block
            time.sleep(3)
        
        # Lưu file cuối cùng
        print("Đang lưu file cuối cùng...")
        df.to_excel('ny_dispensaries_with_phones.xlsx', index=False)
        
        print(f"Hoàn thành! Đã cập nhật {len(df)} dispensary")
        print("File mới: ny_dispensaries_with_phones.xlsx")
        
        # Hiển thị thống kê
        phones_found = df['Phone'].notna().sum()
        print(f"Số điện thoại đã tìm thấy: {phones_found}/{len(df)}")
        
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    print("Bắt đầu lấy số điện thoại từ Google Maps...")
    update_excel_with_phones() 