from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
def get_timing(flight_num,days_back):
    chrome_options = Options()
    chrome_options.add_argument("disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/92.0.4515.159 Safari/537.36 '
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome('chromedriver',options=chrome_options)
    url="https://www.planemapper.com/flights/{}".format(flight_num)
    driver.get(url)
    # Fetch and print the page source
    data = driver.page_source
    driver.close()
    tables = pd.read_html(data)
    flights_table = tables[4]
    def analyze_flight_data(df,days_back):
        days_back=int(days_back)
        print(days_back)
        # Drop the first row if it contains any null values
        df = df.iloc[1:].dropna()
        df = df.head(days_back)
        # Extract only the time from the scheduled and estimated columns
        df['Scheduled', 'Arrival'] = df['Scheduled', 'Arrival'].str.split(' ').str[0]
        df['Estimated', 'Arrival'] = df['Estimated', 'Arrival'].str.split(' ').str[0]
        # Calculate delays based on the scheduled time being later than the estimated time
        df['Delayed'] = (df['Scheduled', 'Arrival'] < df['Estimated', 'Arrival'])
        num_delays = df['Delayed'].sum()
        departure_airport = df.iloc[0]['Departure Airport', 'Departure Airport']
        arrival_airport = df.iloc[0]['Arrival Airport', 'Arrival Airport']

        result = {
            'Departure Airport': departure_airport,
            'Arrival Airport': arrival_airport,
            'Number of Delays': str(num_delays),
            'Delay Probability' : str(round((num_delays/days_back),2))
        }
        return result

    return(analyze_flight_data(flights_table,days_back))

