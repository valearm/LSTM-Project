import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)

def day_number_to_date(day_number, year):
    # Construct the initial date for the given year
    start_date = datetime(year, 1, 1)

    # Calculate the target date by adding the day_number - 1 (since day_number starts from 1)
    target_date = start_date + timedelta(days=day_number - 1)

    # Format the date as yyyy/mm/dd
    formatted_date = target_date.strftime("%Y/%m/%d")

    return formatted_date

# Initialize an empty list to store data
data_list = []

# Iterate over years from 2018 to 2024
for year in range(2018, 2025):
    # Iterate over numbers from 1 to 365
    for number in range(1, 366):
        date = day_number_to_date(number, year)
        url = f"https://www.vincicasa.cloud/dettaglio-estrazione.php?numero={number}&anno={year}"

        try:
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            response.raise_for_status()

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract winning numbers
            winning_numbers = [ball.get_text() for ball in soup.find_all('span', class_='number')]

            if(len(winning_numbers) != 0):
                # Append data to the list
                data_list.append(', '.join(winning_numbers))

            # Log the information for the current year and number
            logging.info(f"Year: {year}, Number: {number}")
            logging.info(f"Winning Numbers: {', '.join(winning_numbers)}")
            logging.info("=" * 30)

            # Introduce a delay between requests
            # time.sleep(1)

        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to retrieve the webpage for Year: {year}, Number: {number}. Error: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred for Year: {year}, Number: {number}. Error: {e}")

# Write data to a text file ('data.txt') with comma-separated values and without the 'Date' column
with open('.\\data.txt', 'w') as file:
    for item in data_list:
        file.write(f"{item}\n")

logging.info("Data exported to data.txt")
