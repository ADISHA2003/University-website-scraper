import requests
from bs4 import BeautifulSoup

# Sample URL (replace with the actual URL where the HTML content is located)
url = 'https://college.harvard.edu/financial-aid/apply-financial-aid'

# Send a GET request to fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize an empty list to hold the application process details
application_process = []

# Extract the "How to Apply for Aid" section
how_to_apply = soup.find(id='how-to-apply-for-aid')
if how_to_apply:
    how_to_apply_text = how_to_apply.get_text(strip=True)
    application_process.append({'section': 'How to Apply for Aid', 'content': how_to_apply_text})

# Extract the "Prospective Students" section
prospective_students = soup.find(id='prospective-students')
if prospective_students:
    prospective_students_text = prospective_students.get_text(strip=True)
    application_process.append({'section': 'Prospective Students', 'content': prospective_students_text})

# Extract the "Current Students" section
current_students = soup.find(id='current-students')
if current_students:
    current_students_text = current_students.get_text(strip=True)
    application_process.append({'section': 'Current Students', 'content': current_students_text})

# Extract the "Financial Aid Forms" section
financial_aid_forms = soup.find(id='financial-aid-forms')
if financial_aid_forms:
    financial_aid_forms_text = financial_aid_forms.get_text(strip=True)
    application_process.append({'section': 'Financial Aid Forms', 'content': financial_aid_forms_text})

# Print the extracted application process details
for item in application_process:
    print(f"Section: {item['section']}\nContent: {item['content']}\n")
