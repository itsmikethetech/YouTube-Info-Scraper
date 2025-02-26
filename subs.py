#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ANSI escape codes for colors.
GREEN = "\033[32m"
RESET = "\033[0m"

def get_main_page_data(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    # Get subscriber count.
    subscriber_element = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//span[contains(text(), 'subscribers')]")
    ))
    subscriber_count = subscriber_element.text
    
    # Get username (which starts with @).
    username_element = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//span[contains(@class, 'yt-core-attributed-string--link-inherit-color') and contains(text(), '@')]")
    ))
    username = username_element.text
    return subscriber_count, username

def get_about_page_data(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    # Get view count.
    view_element = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//td[contains(text(), 'views')]")
    ))
    view_count = view_element.text
    
    # Get video count.
    video_element = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//td[contains(text(), 'videos')]")
    ))
    video_count = video_element.text
    return view_count, video_count

def get_additional_details(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    details = {}
    
    # Channel description.
    try:
        desc_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//yt-attributed-string[@id='description-container']//span")
        ))
        details['description'] = desc_element.text
    except Exception as e:
        details['description'] = f"Error: {e}"
    
    # External links.
    external_links = []
    try:
        link_elements = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@id='link-list-container']//a")
        ))
        for link in link_elements:
            text = link.text
            href = link.get_attribute('href')
            external_links.append({'text': text, 'url': href})
    except Exception as e:
        external_links = f"Error: {e}"
    details['external_links'] = external_links
    
    # Join date.
    try:
        join_date_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//span[contains(text(),'Joined')]")
        ))
        details['join_date'] = join_date_element.text
    except Exception as e:
        details['join_date'] = f"Error: {e}"
    
    # Location.
    try:
        location_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//tr[td//yt-icon[@icon='privacy_public']]/td[2]")
        ))
        details['location'] = location_element.text
    except Exception as e:
        details['location'] = f"Error: {e}"
    
    return details

def main():
    base_url = "https://www.youtube.com/linustechtips"
    about_url = base_url + "/about"
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(options=chrome_options)
    try:
        # Main page details.
        subscriber_count, username = get_main_page_data(driver, base_url)
        
        # About page details.
        view_count, video_count = get_about_page_data(driver, about_url)
        additional_details = get_additional_details(driver, about_url)
        
        print("YouTube Scraper Successful! Data retrieved.")
        print("Username:", GREEN + username + RESET)
        print("Subscriber Count:", GREEN + subscriber_count + RESET)
        print("View Count:", GREEN + view_count + RESET)
        print("Video Count:", GREEN + video_count + RESET)
        print("Join Date:", GREEN + additional_details.get('join_date') + RESET)
        print("Location:", GREEN + additional_details.get('location') + RESET)
        print("Description:", GREEN + additional_details.get('description') + RESET)
    except Exception as e:
        print("Error retrieving channel data:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
