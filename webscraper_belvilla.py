import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def get_data(url):
    # Set up the Selenium webdriver
    driver = webdriver.Chrome()  # Replace with appropriate webdriver for your browser

    # Navigate to the website
    driver.get(url)

    # Wait for the accommodation data to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.hotelCardListing__descriptionWrapper")))

    # Scroll down to load more accommodations (if needed)
    while True:
        try:
            load_more_button = driver.find_element(By.CSS_SELECTOR, "div.listing__content--loadMoreWrapper")
            load_more_button.click()
            time.sleep(2)  # Add a delay to allow time for data to load
        except NoSuchElementException:
            break

    # Extract accommodation data
    accommodations = []
    accommodation_elements = driver.find_elements(By.CSS_SELECTOR, "div.hotelCardListing__descriptionWrapper")
    for accommodation_element in accommodation_elements:
        # Extract relevant data from each accommodation element
        accommodation = {}
        accommodation['name'] = accommodation_element.find_element(By.CSS_SELECTOR, "h3.listingHotelDescription__hotelName").text
        accommodation['location'] = accommodation_element.find_element(By.CSS_SELECTOR, "div.listingHotelDescription__hotelAddress").text
        try:
            accommodation['price'] = accommodation_element.find_element(By.CSS_SELECTOR, "span.listingPrice__finalPrice").text
        except NoSuchElementException:
            accommodation['price'] = None
        try:
            accommodation['old_price'] = accommodation_element.find_element(By.CSS_SELECTOR, "span.listingPrice__slashedPrice").text
        except NoSuchElementException:
            accommodation['old_price'] = None
        try:
            accommodation['percentage'] = accommodation_element.find_element(By.CSS_SELECTOR, "span.listingPrice__percentage").text
        except NoSuchElementException:
            accommodation['percentage'] = None
        accommodation['rating'] = accommodation_element.find_element(By.CSS_SELECTOR, "span.hotelRating__rating").text
        accommodation['description'] = accommodation_element.find_element(By.CSS_SELECTOR, "div.c-px3wnf").text
        accommodations.append(accommodation)

    # Close the webdriver
    driver.quit()

    return accommodations


def main():
    country = input("What country do you want to scrape? ")
    if country.lower() == "belgie":
        url = "https://nl.belvilla.be/search/?filters%5Bcountry_id%5D=28&filters%5Bproperty_type%5D=bungalow%2Cchalet&guests=2&location=Belgi%C3%AB&searchType=country"
    else:
        url = "https://nl.belvilla.be/search/?filters%5Bcountry_id%5D=143&filters%5Bproperty_type%5D=bungalow%2Cchalet&guests=2&location=Nederland&searchType=country"
    data = get_data(url)
    with open(f"{country}.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


if __name__ == '__main__':
    main()