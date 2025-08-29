import requests
import re
from urllib.parse import quote

def test_google_maps_gotham():
    """Test Google Maps search for Gotham Buds"""
    company_name = "Gotham Buds"
    search_query = f"{company_name} dispensary NY"
    encoded_query = quote(search_query)
    url = f"https://www.google.com/maps/search/{encoded_query}"
    
    print(f"Đang test Google Maps search: {company_name}")
    print(f"URL: {url}")
    
    # Headers để giả lập browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.google.com/',
    }
    
    try:
        # Gửi request
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        print(f"Status code: {response.status_code}")
        print(f"Content length: {len(response.text)} characters")
        
        # Tìm kiếm số điện thoại mục tiêu
        target_phone = "+16464100200"
        if target_phone in response.text:
            print(f"\n✓ Tìm thấy số điện thoại mục tiêu: {target_phone}")
        else:
            print(f"\n✗ Không tìm thấy số điện thoại mục tiêu: {target_phone}")
        
        # Tìm kiếm các số điện thoại có thể có
        print("\n=== Tìm kiếm số điện thoại trong Google Maps ===")
        phone_patterns = [
            r'\+1\s*\d{3}-\d{3}-\d{4}',  # +1 646-410-0200
            r'\(\d{3}\)\s*\d{3}-\d{3}',  # (646) 410-0200
            r'\d{3}-\d{3}-\d{4}',        # 646-410-0200
            r'\d{10}',                    # 6464100200
            r'\+1\s*\d{10}',             # +1 6464100200
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, response.text)
            if matches:
                print(f"Pattern '{pattern}': {matches}")
            else:
                print(f"Pattern '{pattern}': Không tìm thấy")
        
        # Tìm kiếm tất cả số điện thoại
        all_numbers = re.findall(r'\+?1?\s*\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', response.text)
        if all_numbers:
            print(f"\nTất cả số điện thoại tìm thấy:")
            for num in all_numbers:
                print(f"  - {num}")
        else:
            print("\nKhông tìm thấy số điện thoại nào")
        
        # Tìm kiếm trong các thẻ có thể chứa số điện thoại
        print("\n=== Tìm kiếm trong HTML ===")
        
        # Tìm kiếm text chứa "phone" hoặc "call"
        phone_keywords = ['phone', 'call', 'tel', 'contact']
        for keyword in phone_keywords:
            if keyword in response.text.lower():
                print(f"Tìm thấy keyword: {keyword}")
        
        # Tìm kiếm các thẻ có thể chứa thông tin liên hệ
        contact_patterns = [
            r'contact[^>]*>([^<]*)',
            r'phone[^>]*>([^<]*)',
            r'tel[^>]*>([^<]*)',
        ]
        
        for pattern in contact_patterns:
            matches = re.findall(pattern, response.text, re.IGNORECASE)
            if matches:
                print(f"Pattern '{pattern}': {matches}")
        
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    test_google_maps_gotham() 