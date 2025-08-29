import requests
from bs4 import BeautifulSoup
import re

def test_gotham_buds_detailed():
    """Detailed test script to find Gotham Buds phone number"""
    website_url = "https://gothambudsny.com"
    
    print(f"Đang test website: {website_url}")
    
    # Headers để giả lập browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        # Gửi request
        response = requests.get(website_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        print(f"Status code: {response.status_code}")
        print(f"Content length: {len(response.text)} characters")
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm kiếm số điện thoại trong các thẻ cụ thể
        print("\n=== Tìm kiếm trong các thẻ cụ thể ===")
        
        # Tìm trong thẻ tel:
        tel_links = soup.find_all('a', href=re.compile(r'^tel:'))
        if tel_links:
            print("Thẻ tel: tìm thấy:")
            for link in tel_links:
                print(f"  - {link.get('href')} -> {link.get_text(strip=True)}")
        else:
            print("Không tìm thấy thẻ tel:")
        
        # Tìm trong thẻ có class chứa 'phone'
        phone_elements = soup.find_all(class_=re.compile(r'phone', re.IGNORECASE))
        if phone_elements:
            print("Thẻ có class chứa 'phone':")
            for elem in phone_elements:
                print(f"  - {elem.get_text(strip=True)}")
        else:
            print("Không tìm thấy thẻ có class chứa 'phone'")
        
        # Tìm trong thẻ có text chứa 'phone'
        phone_text_elements = soup.find_all(text=re.compile(r'phone', re.IGNORECASE))
        if phone_text_elements:
            print("Text chứa 'phone':")
            for text in phone_text_elements:
                parent = text.parent
                if parent:
                    print(f"  - {parent.get_text(strip=True)}")
        else:
            print("Không tìm thấy text chứa 'phone'")
        
        # Tìm kiếm số điện thoại trong toàn bộ HTML
        print("\n=== Tìm kiếm số điện thoại trong HTML ===")
        
        # Pattern cụ thể cho số +16464100200
        target_patterns = [
            r'\+1\s*646\s*410\s*0200',
            r'\+1\s*646-410-0200',
            r'646\s*410\s*0200',
            r'646-410-0200',
            r'\+16464100200',
            r'16464100200',
        ]
        
        for pattern in target_patterns:
            matches = re.findall(pattern, response.text, re.IGNORECASE)
            if matches:
                print(f"Pattern '{pattern}': {matches}")
            else:
                print(f"Pattern '{pattern}': Không tìm thấy")
        
        # Tìm kiếm các số điện thoại có thể có
        print("\n=== Tất cả số điện thoại tìm thấy ===")
        all_numbers = re.findall(r'\+?1?\s*\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', response.text)
        if all_numbers:
            # Loại bỏ các số không hợp lệ
            valid_numbers = []
            for num in all_numbers:
                # Clean số điện thoại
                cleaned = re.sub(r'[^\d]', '', num)
                if len(cleaned) == 10 or len(cleaned) == 11:
                    if len(cleaned) == 11 and cleaned.startswith('1'):
                        cleaned = cleaned[1:]
                    if len(cleaned) == 10:
                        valid_numbers.append(cleaned)
            
            # Loại bỏ trùng lặp
            unique_numbers = list(set(valid_numbers))
            print(f"Tìm thấy {len(unique_numbers)} số điện thoại hợp lệ:")
            for num in unique_numbers:
                print(f"  - {num}")
        else:
            print("Không tìm thấy số điện thoại nào")
        
        # Tìm kiếm trong JavaScript
        print("\n=== Tìm kiếm trong JavaScript ===")
        script_tags = soup.find_all('script')
        for i, script in enumerate(script_tags):
            script_content = script.get_text()
            if '+16464100200' in script_content or '6464100200' in script_content:
                print(f"Script {i+1} chứa số điện thoại mục tiêu!")
                # Tìm số điện thoại trong script
                phone_in_script = re.findall(r'\+?1?\s*\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', script_content)
                if phone_in_script:
                    print(f"  Số điện thoại trong script: {phone_in_script}")
            
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    test_gotham_buds_detailed() 