import requests
from bs4 import BeautifulSoup
import openpyxl
import re  # Regular expressions to help with URL extraction

# Step 1: Fetch the HTML content from the URL
def get_html(url):
    response = requests.get(url)
    return response.text

# Step 2: Scrape the university name from the <h1> tag
def scrape_university_name(soup):
    h1_tag = soup.find('h1', class_='page-title h1')
    if h1_tag:
        return h1_tag.text.strip()
    else:
        return "University name not found"

# Step 3: Scrape the university logo from the <link rel="icon"> tag
def scrape_university_logo(soup):
    logo_tag = soup.find('link', rel='icon')
    if logo_tag and 'href' in logo_tag.attrs:
        return logo_tag['href']
    else:
        return "University logo not found"

# Step 4: Scrape university pictures from the <div> with the specified class
def scrape_university_picture(soup):
    image_div = soup.find('div', class_='c-image__image')
    if image_div and 'style' in image_div.attrs:
        # Extract URL from the style attribute using regex
        match = re.search(r'url\(["\']?([^"\')]+)["\']?\)', image_div['style'])
        if match:
            return match.group(1)
    return "University picture not found"

# Step 5: Scrape the university URL from the <meta property="og:url">
def scrape_university_url(soup):
    meta_tag = soup.find('meta', property='og:url')
    if meta_tag and 'content' in meta_tag.attrs:
        return meta_tag['content']
    return "University URL not found"

# Step 6: Scrape the university contact number and full address
def scrape_contact_info(soup):
    contact_info_div = soup.find('div', class_='s-sink t-sink c-subheader__desc')
    if contact_info_div:
        paragraphs = contact_info_div.find_all('p')
        contact_number = ""
        full_address = ""
        for p in paragraphs:
            text = p.get_text(strip=True)
            # Check if the text contains a contact number
            if text.startswith("For general inquiries"):
                contact_number = text.split("call ")[1]  # Get number after "call "
            elif "Mailing address:" in text:
                # Get the mailing address from subsequent paragraphs
                full_address = "\n".join([p.get_text(strip=True) for p in paragraphs[paragraphs.index(p)+1:]])
        return contact_number, full_address
    return "Contact number not found", "Address not found"

# Step 7: Save the data to an Excel file
def save_to_excel(university_name, university_logo, university_picture, university_url, contact_number, full_address, file_name="university_data.xlsx"):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "University Info"
    
    # Add headers
    sheet['A1'] = 'University Name'
    sheet['B1'] = 'University Logo'
    sheet['C1'] = 'University Picture'
    sheet['D1'] = 'University URL'
    sheet['E1'] = 'Contact Number'
    sheet['F1'] = 'Full Address'
    
    # Add the scraped data
    sheet['A2'] = university_name
    sheet['B2'] = university_logo
    sheet['C2'] = university_picture
    sheet['D2'] = university_url
    sheet['E2'] = contact_number
    sheet['F2'] = full_address
    
    # Save the workbook
    workbook.save(file_name)
    print(f"Data saved to {file_name}")

# Main function to perform scraping and saving
def main():
    university_url = 'https://www.harvard.edu/'  # Replace with actual URL
    html_content = get_html(university_url)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    university_name = scrape_university_name(soup)
    university_logo = scrape_university_logo(soup)
    university_picture = scrape_university_picture(soup)
    university_url = scrape_university_url(soup)
    contact_number, full_address = scrape_contact_info(soup)
    
    save_to_excel(university_name, university_logo, university_picture, university_url, contact_number, full_address)

# Run the script
main()
