import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def scrape_dispensaries():
    cookies = {
        '__cf_bm': 'SIx5blX4RbWsBUQ88CDERFWcDUk9sA2YbpQnAo3fyCQ-1756394249-1.0.1.1-xIXsyhbZ8cr1WVUXF6PTn4etZzkKnRu351uw2ceCEXHwUiQuHoT5HZLhihPrGBlSsRw1hPQ_r38yByFSm7M9bC6k.O_uZd22upUb3WqeQEo',
        '_ga': 'GA1.3.2090772781.1756394250',
        '_gid': 'GA1.3.500492869.1756394254',
        'nmstat': 'd438d7a5-d5dc-5a0b-32ba-35da19354cba',
        '_gat_UA-46452137-3': '1',
        '_ga_LV2BXW6D8Q': 'GS2.1.s1756394249$o1$g1$t1756394894$j55$l0$h0',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    try:
        response = requests.get('https://cannabis.ny.gov/dispensary-location-verification', 
                              cookies=cookies, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table with dispensary data
        table = soup.find('table')
        if not table:
            print("Không tìm thấy bảng dữ liệu")
            return None
            
        dispensaries = []
        
        # Find all table rows (skip header)
        rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 5:  # Ensure we have enough columns
                company_name = cells[0].get_text(strip=True)
                address = cells[1].get_text(strip=True)
                city = cells[2].get_text(strip=True)
                zip_code = cells[3].get_text(strip=True)
                
                # Extract website from the last cell
                website_cell = cells[4]
                website = ""
                if website_cell.find('a'):
                    website = website_cell.find('a').get('href', '')
                
                # Combine address components
                full_address = f"{address}, {city}, NY {zip_code}"
                
                dispensaries.append({
                    'Company Name': company_name,
                    'Address': full_address,
                    'Phone': '',  # Empty for now
                    'Email': '',   # Empty for now
                    'Website': website
                })
        
        return dispensaries
        
    except Exception as e:
        print(f"Lỗi: {e}")
        return None

def export_to_excel(dispensaries, filename='ny_dispensaries.xlsx'):
    if not dispensaries:
        print("Không có dữ liệu để xuất")
        return
    
    # Create DataFrame
    df = pd.DataFrame(dispensaries)
    
    # Export to Excel
    df.to_excel(filename, index=False, sheet_name='NY Dispensaries')
    
    print(f"Đã xuất {len(dispensaries)} dispensary vào file: {filename}")
    print(f"File được lưu tại: {filename}")
    
    # Display first few rows
    print("\nMẫu dữ liệu:")
    print(df.head())

if __name__ == "__main__":
    print("Đang lấy dữ liệu dispensary từ NY Cannabis...")
    dispensaries = scrape_dispensaries()
    
    if dispensaries:
        print(f"Đã lấy được {len(dispensaries)} dispensary")
        export_to_excel(dispensaries)
    else:
        print("Không thể lấy dữ liệu") 