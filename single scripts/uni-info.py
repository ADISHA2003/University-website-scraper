import requests
from bs4 import BeautifulSoup

def scrape_url(url):
    # Send a GET request to the URL
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example: Extracting the title of the webpage
        title = soup.title.string if soup.title else 'No title found'

        # Example: Extracting all paragraphs
        paragraphs = soup.find_all('p')
        paragraph_texts = [p.get_text() for p in paragraphs]

        # Example: Extracting specific sections based on your needs
        # You can modify this part to scrape other elements
        # For example, all headings (h1, h2, etc.)
        headings = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])]

        # Output the scraped data
        return {
            'title': title,
            'paragraphs': paragraph_texts,
            'headings': headings
        }

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Example usage
url_to_scrape = 'https://www.harvard.edu/about/history/'  # Replace with the URL you want to scrape
scraped_data = scrape_url(url_to_scrape)

# Print the scraped data
if scraped_data:
    print(f"Title: {scraped_data['title']}")
    print("Paragraphs:")
    for p in scraped_data['paragraphs']:
        print(f"- {p}")
    print("Headings:")
    for h in scraped_data['headings']:
        print(f"- {h}")
