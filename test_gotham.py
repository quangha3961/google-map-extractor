import requests
from bs4 import BeautifulSoup
import re

def test_gotham_buds():
    """Test script to get Gotham Buds phone number"""
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
        
        # Tìm kiếm số điện thoại trong HTML
        html_content = response.text
        
        # Pattern để tìm số điện thoại
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
        
        print("\nTìm kiếm số điện thoại:")
        for i, pattern in enumerate(phone_patterns):
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                print(f"Pattern {i+1}: {matches}")
            else:
                print(f"Pattern {i+1}: Không tìm thấy")
        
        # Tìm kiếm cụ thể số +16464100200
        target_phone = "+16464100200"
        if target_phone in html_content:
            print(f"\n✓ Tìm thấy số điện thoại mục tiêu: {target_phone}")
        else:
            print(f"\n✗ Không tìm thấy số điện thoại mục tiêu: {target_phone}")
        
        # Tìm kiếm các số điện thoại có thể có
        all_numbers = re.findall(r'\+?1?\s*\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', html_content)
        if all_numbers:
            print(f"\nTất cả số điện thoại tìm thấy:")
            for num in all_numbers:
                print(f"  - {num}")
        else:
            print("\nKhông tìm thấy số điện thoại nào")
            
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    test_gotham_buds() 