import requests
import os
import csv
from bs4 import BeautifulSoup
import re
import time


def scrape_and_save_artwork_data(url, output_csv="artwork_data.csv", image_dir="Paintings"):
    """
    Scrapes artwork data from an Artsper URL, saves it to a CSV file,
    and downloads the associated image.

    Args:
        url: The URL of the artwork page on Artsper.
        output_csv: The name of the CSV file to save the data to.
        image_dir: The name of the directory to save the images to.

    Returns:
        None.  Prints status messages to the console.
    """

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    artwork_data = {}  # Dictionary to store the scraped data

    # --- 1. Title, Artist, and Year ---
    title_tag = soup.find("title")
    if title_tag:
        title_text = title_tag.text.strip()
        try:
            # Attempt to extract year
            year_part = title_text.split(",")[-1].split("|")[0].strip()
            artwork_data['year'] = year_part if year_part.isdigit() else "Year Not Found"

            name = title_text.split(",")[0].split('par')[0]
            artwork_data['title'] = re.sub(r"[^a-zA-Z0-9\s]", "", name).strip()

            artwork_data['artist'] = title_text.split(",")[0].split('par')[1].strip()


        except (IndexError, ValueError):
            artwork_data['year'] = "Year Extraction Failed"
            artwork_data['title'] = "Title Extraction Failed"
            artwork_data['artist'] = "Artist Extraction Failed"
    else:
        artwork_data['year'] = "Year Not Found"
        artwork_data['title'] = "Title Not Found"
        artwork_data['artist'] = "Artist Not Found"
    # --- 2. Price ---
    try:
        price_element = soup.select_one('div.top-information__price span.price.price__current.typography--bold')
        artwork_data['price'] = price_element.text.strip() if price_element else "Price Not Found"
    except AttributeError:  # Handle if price_element is None
        artwork_data['price'] = "Price Not Found"

    # --- 3. Techniques ---
    techniques = []
    for a_tag in soup.find_all('a', class_='pointer'):
        if a_tag.get('data-infos') and 'peinturestcdsq' in a_tag['data-infos']:
            if "Peinture" not in a_tag.text:  # Avoid the "Peinture:" label
                techniques.append(a_tag.text.strip().rstrip(','))
    artwork_data['techniques'] = ", ".join(techniques) if techniques else "Techniques Not Found"

    # --- 4. Dimensions ---
    dimensions_found = []
    for item in soup.find_all('div', class_='about__block__item'):
      title_tag = item.find('p', class_='about__block__item__title')
      if title_tag:
          title = title_tag.get_text(strip = True)
          if "Dimensions" in title:
            dim_desc = item.find('div', class_="about__block__item__description")
            if dim_desc:
              cm_span = dim_desc.find('span', class_='measure--cm')
              if cm_span:
                dimensions_found.append(("Unframed Dimensions", cm_span.get_text(strip=True)))
              in_span = dim_desc.find('span', class_='measure--inch')
              if in_span:
                dimensions_found.append(("Unframed Dimensions (inch)", in_span.get_text(strip=True)))

    # Assign dimensions to specific keys, handling cases where one is missing
    if len(dimensions_found) >= 1:
      artwork_data[dimensions_found[0][0]] = dimensions_found[0][1]
    else:
      artwork_data['Unframed Dimensions'] = 'Not Found'
    if len(dimensions_found) >= 2:
      artwork_data[dimensions_found[1][0]] = dimensions_found[1][1] #Keep if inches is important, otherwise, remove it
    #No framed dimensions from the new approach


    # --- 5. Tags ---
    tags = []
    for tag in soup.find_all(['a', 'span'], class_='button'):
        if tag.get('data-category') == 'Interaction' and tag.get('data-label') == 'Tags':
            h3_tag = tag.find('h3', class_='typography__text')
            if h3_tag:
                tags.append(h3_tag.get_text(strip=True))
    artwork_data['tags'] = ", ".join(tags) if tags else "No Tags Found"

    # --- 6. Support and Encadrement ---
    about_items = soup.find_all('div', class_='about__block__item')
    for item in about_items:
        title_tag = item.find('p', class_='about__block__item__title')
        if title_tag:
            title = title_tag.get_text(strip=True)
            if "Support" in title:
                description_tag = item.find('div', class_='about__block__item__description')
                if description_tag:
                    a_tag = description_tag.find('a', class_='pointer', attrs={'data-infos': lambda x: x and 'support-toile' in x})
                    artwork_data['support'] = a_tag.get_text(strip=True) if a_tag else 'Not Found'
            elif "Encadrement" in title:
                description_tag = item.find('div', class_='about__block__item__description')
                artwork_data['encadrement'] = description_tag.get_text(strip=True) if description_tag else 'Not Found'

    # --- 7. Image Download and Filename ---
    img_tag = soup.find('img', id='img-viar')
    if img_tag:
        image_url = img_tag.get('data-src')
        if image_url:
            try:
                # Create image directory if it doesn't exist
                os.makedirs(image_dir, exist_ok=True)

                # Sanitize title and artist for filename
                safe_title = re.sub(r'[\\/*?:"<>|]', "", artwork_data['title'])
                safe_artist = re.sub(r'[\\/*?:"<>|]', "", artwork_data['artist'])
                safe_year = re.sub(r'[\\/*?:"<>|]', "", artwork_data['year'])

                image_filename = f"{safe_title}_{safe_artist}_{safe_year}.jpg"
                image_path = os.path.join(image_dir, image_filename)


                response = requests.get(image_url, stream=True)
                response.raise_for_status()
                with open(image_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                artwork_data['image_filename'] = image_filename  # Store filename
                print(f"Image saved to: {image_path}")


            except requests.exceptions.RequestException as e:
                print(f"Error downloading image: {e}")
                artwork_data['image_filename'] = "Image Download Failed"
            except OSError as e:
                print(f"Error saving image: {e}")
                artwork_data['image_filename'] = "Image Save Failed"

        else:
            artwork_data['image_filename'] = "Image URL Not Found"
    else:
        artwork_data['image_filename'] = "Image Tag Not Found"


    # --- 8. Save data to CSV ---
    try:
      # Check if the CSV file exists
      file_exists = os.path.isfile(output_csv)
      with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:  # 'a' for append
          fieldnames = list(artwork_data.keys()) #Dynamically get the headers
          writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

          if not file_exists:
              writer.writeheader()  # Write header only if file doesn't exist
          writer.writerow(artwork_data)
          print(f"Data appended to: {output_csv}")
    except OSError as e:
        print(f"Unable to write csv file: {e}")

# Example usage (you would loop over a list of URLs in a real application)
scrape_and_save_artwork_data("https://www.artsper.com/fr/oeuvres-d-art-contemporain/peinture/2300112/evasion") #Example 1
# scrape_and_save_artwork_data("https://www.artsper.com/fr/oeuvres-d-art-contemporain/peinture/2272663/discogolf")  # Example 2