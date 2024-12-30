import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configure Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Uncomment to run in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("window-size=800,600")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL to scrape
url = "https://www.lotto-bayern.de/toto/spielplaene#:~:text=Meisterschaftsspiele%201%20%2D%2013%20(Spiele%201,Liga%20Italien%2FSerie%20A"
driver.get(url)

# Wait for the page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section[data-component="totoaw-gametables"]')))

# Initialize data structure
bets = []

# Function to scrape data from the section
def scrape_section_data():
    # Locate the section for 6aus45 Auswahlwette
    section = driver.find_element(By.CSS_SELECTOR, 'section[data-component="totoaw-gametables"]')
    
    # Extract start_date from h2 tag
    h2 = section.find_element(By.CSS_SELECTOR, 'h2[data-gametable-headline]')
    text = h2.text.strip()
    if "vom" in text:
        start_date = text[text.index("vom") + len("vom"):].strip().replace("/", "to")
        
        # Check if this start_date already exists
        bet_entry = next((bet for bet in bets if bet["start_date"] == start_date), None)
        if not bet_entry:
            bet_entry = {"start_date": start_date, "matches": []}
            bets.append(bet_entry)
        
        # Extract match details from the table
        for table in section.find_elements(By.CSS_SELECTOR, 'table'):
            for row in table.find_elements(By.CSS_SELECTOR, 'tbody tr'):
                home_cell = row.find_element(By.CSS_SELECTOR, 'td.text-right')  # Home team
                guest_cell = row.find_element(By.CSS_SELECTOR, 'td.text-left')  # Guest team
                trend_cell = row.find_element(By.CSS_SELECTOR, 'td.text-center span.tendency')  # Trend
                
                home = home_cell.text.strip() if home_cell else None
                guest = guest_cell.text.strip() if guest_cell else None
                trend = trend_cell.text.strip() if trend_cell else None
                
                if home and guest and trend:
                    # Add match details to the bet entry
                    bet_entry["matches"].append({
                        "home": home,
                        "guest": guest,
                        "trend": trend
                    })

# Scrape initial data
scrape_section_data()

# Locate and click the link to load new data within the section
try:
    # Find the clickable link inside the section
    link_to_click = driver.find_element(By.CSS_SELECTOR, 'section[data-component="totoaw-gametables"] a[data-gametable-index="1"]')
    
    # Click the link
    driver.execute_script("arguments[0].click();", link_to_click)
    
    # Wait for the page to update
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section[data-component="totoaw-gametables"]')))
    
    # Scrape the updated data
    scrape_section_data()
except Exception as e:
    print("Error clicking link or scraping updated data:", str(e))

# Close the WebDriver
driver.quit()

# Save the extracted data to a JSON file
output_file = "6aus45_matches.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump({"bets": bets}, file, indent=4, ensure_ascii=False)

# Print confirmation
print(f"Data has been saved to {output_file}")
