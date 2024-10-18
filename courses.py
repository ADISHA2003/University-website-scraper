import requests
from bs4 import BeautifulSoup
import pandas as pd

# Create a list to hold course data
courses_data = []

# URL of the university course page
url = "https://www.harvardonline.harvard.edu/"

# Send a request to the website
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Scrape course data
course_teasers = soup.find_all('article', class_='content-type--course')

for course in course_teasers:
    course_title = course.find('h3').text.strip()
    course_description = course.find('div', class_='field--name-field-teaser-description').text.strip()
    course_tagline = course.find('div', class_='field--name-field-tagline').text.strip()
    course_link = course.find('a', class_='read-more-link')['href']
    
    # Create a dictionary for each course
    course_info = {
        'Title': course_title,
        'Tagline': course_tagline,
        'Description': course_description,
        'Link': url + course_link
    }
    
    # Add the course info to the list
    courses_data.append(course_info)

# Create a DataFrame from the list of courses
df_courses = pd.DataFrame(courses_data)

# Save the DataFrame to an Excel file
excel_file_path = 'harvard_courses.xlsx'
df_courses.to_excel(excel_file_path, index=False)

print(f'Scraped data has been saved to {excel_file_path}')
