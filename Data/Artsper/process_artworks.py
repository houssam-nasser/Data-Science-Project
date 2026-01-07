import csv
import os
import time  # Import the time module
# Assuming scrape_and_save_artwork_data is in a separate file called 'scraper.py'
import one_painting  # Import your scraping function


def process_artwork_range(csv_file, start_index, end_index, output_csv="artwork_data.csv", image_dir="Paintings"):
    """
    Processes a range of artwork links from a CSV file, scraping data for each
    link and saving it using the scrape_and_save_artwork_data function, with
    a delay between processing each artwork.

    Args:
        csv_file: Path to the CSV file containing artwork links.
        start_index: The starting index (inclusive) of the links to process.
        end_index: The ending index (inclusive) of the links to process.
        output_csv: The CSV for output.
        image_dir: The image directory

    Returns:
        None. Prints status messages.
    """

    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found.")
        return

    if start_index < 1:
        print("Error: start_index must be at least 1.")
        return
    if end_index < start_index:
        print("Error: end_index must be greater than or equal to start_index")

    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            links = [row['Link'] for row in reader]  # Read all links into a list

        # Adjust end_index if it exceeds the number of links
        end_index = min(end_index, len(links))


        for i in range(start_index - 1, end_index):  # Adjust indices for 0-based list
            url = links[i]
            print(f"Processing artwork {i + 1} of {end_index}: {url}")
            one_painting.scrape_and_save_artwork_data(url, output_csv, image_dir)  # Call scraper function
            time.sleep(2)  # Add a 2-second delay (adjust as needed)


    except FileNotFoundError:
        print(f"Error: Could not open {csv_file}")
    except OSError as e:
         print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred {e}")



# --- Example Usage ---
# Assuming you have a file named 'artwork_links.csv'
# and 'scraper.py' contains the scrape_and_save_artwork_data function.

#Create the scraper.py and put def scrape_and_save_artwork_data(url, output_csv="artwork_data.csv", image_dir="Paintings"): from the previous response
process_artwork_range('artwork_links.csv', 1, 1000)  # Process the first 5 artworks