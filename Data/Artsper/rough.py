from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
import json

def scrape_artsper_with_selenium(url):
    """
    Extracts artwork details from an Artsper URL using Selenium.

    Args:
        url: The Artsper artwork URL.

    Returns:
        A dictionary containing the artwork details, or None on failure.
    """
    driver = webdriver.Chrome()  # Or webdriver.Firefox(), etc.
    try:
        driver.get(url)

        # --- Wait for critical elements to load ---
        # Adjust timeouts as needed.  Waiting for the price is a good indicator
        # that the main content has loaded.
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "top-information__price"))
        )

        # --- 1. Extract data from ld+json scripts (BEST SOURCE) ---
        ld_json_scripts = driver.find_elements(By.CSS_SELECTOR, 'script[type="application/ld+json"]')
        for script in ld_json_scripts:
            try:
                data = json.loads(script.get_attribute('innerHTML'))

                if data.get('@type') in ('Product', 'CreativeWork', 'Painting'):
                    artist_name = data.get('creator')
                    if isinstance(artist_name, dict):
                        artist_name = artist_name.get('name')
                    if not artist_name:
                        artist_name = data.get('accountablePerson')
                    painting_name = data.get('name')
                    year = None  # Try to get from title later
                    price = data.get('offers', {}).get('price')
                    description = data.get('description')
                    if description:  #Clean the description
                        description = BeautifulSoup(description, 'html.parser').text.strip()

                    if artist_name and painting_name and price is not None:
                        # --- Get year from <title> tag ---
                        try:
                            title_text = driver.find_element(By.TAG_NAME, 'title').text.strip()
                            year_part = title_text.split(",")[-1].split("|")[0].strip()
                            year = int(re.search(r"\b\d{4}\b", year_part).group(0))
                        except (ValueError, AttributeError, IndexError, NoSuchElementException):
                            pass

                        return {
                            "artist_name": artist_name,
                            "year": year,
                            "painting_name": painting_name,
                            "price": price,
                            "description": description,
                            "materials": None,  # Try to get from HTML
                            "dimensions": None,  # Try to get from HTML
                        }
            except json.JSONDecodeError:
                continue  # Move to the next script if JSON parsing fails

        # --- 2. Fallback: Extract from HTML if ld+json fails ---

        # --- Artist and Painting Name (from title tag) ---
        try:
            title_text = driver.find_element(By.TAG_NAME, 'title').text.strip()
            painting_name, rest = title_text.replace("▷", "").strip().split(" par ")
            artist_name, year_part = rest.split(",")
            year = int(re.search(r"\b\d{4}\b", year_part).group(0))
        except (NoSuchElementException, ValueError, AttributeError, IndexError):
            print("Error parsing title tag.")
            return None

        # --- Price ---
        try:
            price_div = driver.find_element(By.CLASS_NAME, "top-information__price")
            price_span = price_div.find_element(By.CLASS_NAME, "price.price__current") #Corrected
            price_text = price_span.text.strip()
            price_match = re.search(r"[\d\s ]+", price_text)
            price_str = price_match.group(0).replace(" ", "").replace(" ", "")
            price = int(price_str)
        except (NoSuchElementException, ValueError, AttributeError):
            print("Error extracting price.")
            price = None

        # --- Description ---
        try:
            description_element = driver.find_element(By.CLASS_NAME, "product-description")
            description = description_element.text.strip()
        except NoSuchElementException:
            print("Error: Description element not found.")
            description = None

        # --- Materials ---
        try:
            materials_container = driver.find_element(By.CLASS_NAME, 'typography__color--grey-4.mt-10.mb-20')
            dimensions_p = materials_container.find_element(By.XPATH, './p[contains(., "cm") or contains(., "inch")]')
            materials_p = dimensions_p.find_element(By.XPATH, './preceding-sibling::p[@class="typography--no-margin"]')
            material_spans = materials_p.find_elements(By.TAG_NAME, 'span')
            materials_list = [span.text.strip() for span in material_spans]
            materials = ", ".join(materials_list)

        except NoSuchElementException:
            print("Error: Materials element not found.")
            materials = None

        # --- Dimensions ---
        try:
            dimensions_container = driver.find_element(By.CLASS_NAME, 'typography__color--grey-4.mt-10.mb-20')
            dimensions_p = dimensions_container.find_element(By.XPATH, './p[contains(., "cm") or contains(., "inch")]')
            dimensions = dimensions_p.text.strip()
        except NoSuchElementException:
            print("Error: Dimensions element not found.")
            dimensions = None


        return {
            "artist_name": artist_name.strip(),
            "year": year,
            "painting_name": painting_name.strip(),
            "price": price,
            "description": description,
            "materials": materials,
            "dimensions": dimensions,
        }

    except TimeoutException:
        print(f"Timed out waiting for page to load: {url}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    finally:
        driver.quit()

# --- Example Usage ---
artsper_url = "https://www.artsper.com/fr/oeuvres-d-art-contemporain/peinture/2300112/evasion"
result = scrape_artsper_with_selenium(artsper_url)

if result:
    print(result)
else:
    print("Could not extract information from the URL.")