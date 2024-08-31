import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException

def google_image_search(query, download_path, num_images=200):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Uncomment to run in headless mode
    driver = webdriver.Chrome(options=options)
    
    search_url = f"https://www.google.com/search?tbm=isch&q={query}"
    driver.get(search_url)
    print(f"Opened URL: {search_url}")
    
    time.sleep(2)

    for _ in range(num_images):
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
        except StaleElementReferenceException:
            print("StaleElementReferenceException encountered. Retrying...")
            continue
    
    selectors = [".rg_i.Q4LuWd", ".isv-r.PNCib.MSM1fd.BUooTd img", ".rg_i", ".H8Rx8c img"]
    thumbnails = []

    for selector in selectors:
        try:
            print(f"Trying selector '{selector}'")
            thumbnails = driver.find_elements(By.CSS_SELECTOR, selector)
            print(f"Tried selector '{selector}': found {len(thumbnails)} elements")
            if thumbnails:
                break
        except Exception as e:
            print(f"Error with selector '{selector}': {str(e)}")

    if not thumbnails:
        print("No thumbnails found with the selectors.")
        driver.quit()
        return

    dois_and_url = {'thumbnail_url': [], 'image_url': []}
    
    for thumbnail in thumbnails[:num_images]:
        print("Processing image...")
        
        try:
            thumbnail.click()
            time.sleep(1)
            
            thumbnail_url = thumbnail.get_attribute("src")
            dois_and_url['thumbnail_url'].append(thumbnail_url if thumbnail_url else 'Not_found')
            
            try:
                image_url_button = driver.find_element(By.CSS_SELECTOR, ".sFlh5c.FyHeAf.iPVvYb")
                image_url = image_url_button.get_attribute("src")
                dois_and_url['image_url'].append(image_url if image_url else 'Not_found')
            except NoSuchElementException:
                dois_and_url['image_url'].append('Not_found')
                print("No image URL found")
                
        except (StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException) as e:
            print(f"Exception encountered: {str(e)}. Skipping...")
            dois_and_url['thumbnail_url'].append('Processing_problems')
            dois_and_url['image_url'].append('Processing_problems')
            continue

    driver.quit()

    # Ensure all lists are the same length
    min_length = min(len(dois_and_url['thumbnail_url']), len(dois_and_url['image_url']))
    for key in dois_and_url.keys():
        dois_and_url[key] = dois_and_url[key][:min_length]

    data_table = pd.DataFrame(dois_and_url)
    
    file_path = os.path.join(download_path, f"{query.replace(' ', '_')}.xlsx")
    data_table.to_excel(file_path)  
    print(f"Saved data to {file_path}")
    
    return data_table

def save_data_as_excel(data_table, file_path):
    """Helper function to save the DataFrame to an Excel file."""
    data_table.to_excel(file_path)  
    print(f"Saved data to {file_path}")


if __name__ == "__main__":
    query = input("Enter the search query: ")
    download_path = "./"
    num_images = 200  # This can be changed later
    data_table = google_image_search(query, download_path, num_images=num_images)
