import requests
from bs4 import BeautifulSoup
import csv
import os
import re
import time


def scrape_artwork_links(base_url, output_csv="artwork_links.csv"):
    """
    Scrapes artwork links from a given Artsper base URL,
    incrementing the page number until a 404 error is encountered,
    saves the links to a CSV file after *each* page, and includes
    a delay between requests.

    Args:
        base_url: The base URL of the Artsper page to scrape.
        output_csv: The name of the CSV file.

    Returns:
        None.
    """

    all_artworks = []  # List to store *all* scraped artwork links
    page_num = 1
    more_pages = True

    # --- Initialize CSV (write header if file doesn't exist) ---
    file_exists = os.path.isfile(output_csv)
    try:
        with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
    except OSError as e:
        print(f"Error initializing CSV: {e}")
        return


    while more_pages:
        url = f"{base_url}?page={page_num}"
        print(f"Scraping page: {url}")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print("404 Page Not Found. Stopping.")
                more_pages = False
                break
            else:
                print(f"Error fetching URL {url}: {e}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        artwork_links = soup.find_all('a', href=re.compile(r'/fr/oeuvres-d-art-contemporain/peinture/\d+/.+'))

        if not artwork_links:
            print("No more artwork links found.  Stopping.")
            more_pages = False
            break

        # --- Process and save links *for the current page* ---
        page_artworks = []  # List for *current page* links
        for link in artwork_links:
            href = link['href']
            full_url = f"https://www.artsper.com{href}"
            page_artworks.append({'Link': full_url})

        if page_artworks:
            try:
                with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Link']  # Redefine for clarity (it's the same)
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerows(page_artworks)  # Write *only* current page data
                print(f"  Links from page {page_num} saved to: {output_csv}")
            except OSError as e:
                print(f"Error saving to CSV: {e}")
        else:
            print("  No artwork links found on this page.")

        page_num += 1

        # --- Sleep before the next request ---
        time.sleep(2)  # 2-second delay (adjust as needed)


# --- Example Usage ---
base_url = "https://www.artsper.com/fr/oeuvres-d-art-contemporain/peinture"
scrape_artwork_links(base_url)