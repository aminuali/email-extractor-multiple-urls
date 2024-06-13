# email-extractor-with-Streamlit
This Streamlit application extracts email addresses from multiple websites. Enter URLs separated by commas and optionally filter emails by domain. The app uses BeautifulSoup for web scraping and regex for email extraction.
# Features:
Extracts emails from multiple websites. 

Optional domain filter to narrow down results.

Displays extracted emails in a table.

Allows download of extracted emails as a CSV file.
# Requirements:
requests

BeautifulSoup4

pandas

streamlit
# Usage:
Clone this repository or download the code.

Install required libraries:

pip install requests beautifulsoup4 pandas streamlit

Running the application: 

navigate to the file location in your command prompt e.g. C:\Users\NITRON 5\recent_programs\Scraper

run the application by typing "streamlit run app.py" (replace app.py with your actual filename)

Enter website URLs (comma-separated).

Optionally, specify a domain to filter emails.

Click "Extract Emails" to start extraction.

Download the extracted emails as a CSV file.

# Code Structure
The code consists of two main parts:

extract_emails function: This function takes a website URL and an optional domain filter as arguments. It scrapes the website using BeautifulSoup, extracts email addresses using a regular expression, and filters them by domain if provided.

Streamlit app: This part builds the user interface using Streamlit components. It allows users to enter website URLs, filter by domain, extract emails, and download the results as a CSV file.

# Customization
You can further customize the Streamlit app by modifying the CSS styles in the st.markdown block.

The regular expression for email validation can be improved based on specific needs.

# License
This code is provided under the MIT License. See the LICENSE file for details.

