import requests
from bs4 import BeautifulSoup
import re

def get_artist_biography(url: str) -> str:
    """
    Extracts and returns the biography of an artist from an Artsper URL.

    Args:
        url: The Artsper URL of the artist's page.

    Returns:
        The artist's biography as a string, or "N/A" if not found.
    """
    # Request the page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        biography = soup.find("div", class_="section-biography__biography description-see-more").get_text(strip=True).split("Lire plus")[0].strip()
    except AttributeError:
        biography = "N/A"

    return biography


import requests
from bs4 import BeautifulSoup
import re


def get_artist_profile_link(artist_name: str) -> str:
    """
    Searches for an artist on Artsper and returns their profile link.

    Args:
        artist_name: The name of the artist to search for.

    Returns:
        The artist's profile link on Artsper, or None if not found.
    """
    # Construct the search URL
    search_url = f"https://www.artsper.com/fr/oeuvres-d-art-contemporain?query={artist_name.replace(' ', '%20')}"

    # Request the search page
    response = requests.get(search_url)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

    soup = BeautifulSoup(response.content, "html.parser")

    # Find the artist link.  This is the key part, and the selector needs to be robust.
    # We look for an 'a' tag with a 'href' attribute that matches the expected artist profile URL pattern.
    artist_link = soup.find('a', href=re.compile(
        r'/fr/artistes-contemporains/.*/\d+/' + re.escape(artist_name.replace(' ', '-').lower())))

    if artist_link:
        return "https://www.artsper.com" + artist_link['href']
    else:
        return None



# Example usage (using the same URL as before):
Name = 'Sophie Petetin'
url = get_artist_profile_link(Name)
biography = get_artist_biography(url)
print(biography)