# README: How to Run the 6aus45 Matches Scraper Script

## Overview

This script uses Selenium to scrape match data from the Lotto Bayern website and saves it to a JSON file named `6aus45_matches.json`. The data includes match details such as home team, guest team, and trend.

## Prerequisites

To run the script, ensure the following requirements are met:

### 1. Install Python

- Python 3.8 or higher is recommended.
- Download and install Python from the [official website](https://www.python.org/downloads/).

### 2. Install Google Chrome

- The script uses Google Chrome as the browser.
- Download and install Google Chrome from the [official website](https://www.google.com/chrome/).

### 3. Install ChromeDriver

- The script uses ChromeDriver to interact with the browser.
- ChromeDriver is managed automatically via `webdriver_manager` in this script.

### 4. Install Required Python Packages

Run the following command to install the necessary Python packages:

```bash
pip install selenium webdriver-manager
```

## Script Configuration

### Headless Mode

The script is configured to run in headless mode by default (no browser UI). If you want to see the browser interactions, comment out the following line in the script:

```python
options.add_argument("--headless")
```

### Window Size

The browser window size is set to `800x600` by default. You can modify this line to change the dimensions:

```python
options.add_argument("window-size=800,600")
```

## Running the Script

1. **Clone or Download the Script**

   - Save the script to a file named `scrape_6aus45.py`.

2. **Navigate to the Script Directory**
   Open a terminal or command prompt and navigate to the directory containing the script.

3. **Run the Script**
   Use the following command to execute the script:

   ```bash
   python scrape_6aus45.py
   ```

4. **Wait for Completion**
   The script will load the website, scrape match data, and save it to a JSON file named `6aus45_matches.json` in the same directory.

5. **View the Output**
   Open the generated `6aus45_matches.json` file to see the scraped data.

## Troubleshooting

### Common Issues

1. **TimeoutException:**

   - Ensure you have a stable internet connection.
   - Increase the timeout duration in the script if the website takes longer to load:
     ```python
     wait = WebDriverWait(driver, 20)  # Increase timeout to 20 seconds
     ```

2. **StaleElementReferenceException:**

   - This is handled by the script with retries. If it persists, try running the script again.

3. **Driver Not Found Error:**

   - Ensure that `webdriver-manager` is installed correctly by running:
     ```bash
     pip install webdriver-manager
     ```

4. **ChromeDriver Version Mismatch:**
   - Update Google Chrome and ChromeDriver by running the script again; `webdriver-manager` will automatically fetch the correct version.

## License

This script is provided as-is for educational and personal use. Ensure compliance with the terms of use of the Lotto Bayern website.

## Author

- Igor Kovalevych
