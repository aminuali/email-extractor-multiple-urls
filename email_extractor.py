# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 22:12:19 2024

@author: Aminu Ali
"""
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import streamlit as st

def extract_emails(url, domain_filter=None):
    """
    Extracts email addresses from a website using BeautifulSoup and regular expressions.

    Args:
        url (str): The URL of the website to scrape.
        domain_filter (str, optional): A domain to filter email addresses by.

    Returns:
        list: A list of email addresses found on the website.
    """

    # Make a request to the website and get the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all text elements (excluding script and style tags)
    text_elements = soup.find_all(text=True, recursive=True)
    emails = []

    # Regular expression for validating email addresses
    email_regex = r"(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}|(?:\d{1,3}\.){3}\d{1,3}(?::\d{1,5})?|\[(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|\[(?:[0-9a-fA-F]{1,4}:){1,7}:|\[(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|\[(?:[0-9a-fA-F]{1,4}:){1,5}:(?:[0-9a-fA-F]{1,4}:){1,4}[0-9a-fA-F]{1,4}|\[(?:[0-9a-fA-F]{1,4}:){1,4}:(?:[0-9a-fA-F]{1,4}:){1,5}[0-9a-fA-F]{1,4}|\[(?:[0-9a-fA-F]{1,4}:){1,3}:(?:[0-9a-fA-F]{1,4}:){1,6}[0-9a-fA-F]{1,4}|\[(?:[0-9a-fA-F]{1,4}:){1,2}:(?:[0-9a-fA-F]{1,4}:){1,7}[0-9a-fA-F]{1,4}|\[(?:[0-9a-fA-F]{1,4}:){1,1}:(?:[0-9a-fA-F]{1,4}:){1,8}[0-9a-fA-F]{1,4}|\[:(?::[0-9a-fA-F]{1,4}){1,9}|(?:[a-zA-Z0-9-]*[a-zA-Z0-9]:)?(?:\d{1,3}\.){3}\d{1,3}\])"

    # Loop through text elements and extract email addresses
    for element in text_elements:
        # Extract text content if element is not a script or style tag
        if not element.parent.name in ['script', 'style']:
            text = element.strip()
            # Find all email addresses matching the regex pattern
            matches = re.findall(email_regex, text)
            # Add valid email addresses to the list
            emails.extend(matches)

    # Filter emails by domain if a domain filter is provided
    if domain_filter:
        emails = [email for email in emails if email.endswith(f"@{domain_filter}")]

    return emails

# Streamlit App
st.set_page_config(page_title="Email Extractor", page_icon=":mailbox:", layout="centered")

st.markdown(
    """
    <style>
    .main {background-color: #f5f5f5;}
    .title {color: #0073e6; text-align: center; font-family: Arial, sans-serif;}
    .footer {position: fixed; left: 0; bottom: 0; width: 100%; background-color: #0073e6; color: white; text-align: center; padding: 10px;}
    .stTextInput > div > input {
        padding: 10px;
        border: 2px solid #0073e6;
        border-radius: 5px;
    }
    .stTextInput > div > label {
        font-weight: bold;
        color: #0073e6;
    }
    .stButton > button {
        background-color: #0073e6;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

st.title("Email Extractor")

urls = st.text_area("Enter Website URLs (separated by commas):", height=150)
domain_filter = st.text_input("Filter emails by domain (optional, e.g., example.com):")

if st.button("Extract Emails"):
    if urls:
        url_list = [url.strip() for url in urls.split(',')]
        all_emails = []

        for url in url_list:
            # Basic URL validation
            if not re.match(r'^https?://', url):
                st.warning(f"Invalid URL: {url}. Please enter a valid URL starting with http:// or https://")
                continue

            with st.spinner(f"Extracting emails from {url}..."):
                try:
                    emails = extract_emails(url, domain_filter)
                    all_emails.extend(emails)
                except Exception as e:
                    st.error(f"Error extracting emails from {url}: {e}")

        if all_emails:
            # Create a DataFrame from the list of email addresses
            df = pd.DataFrame(all_emails, columns=['Email'])
            
            # Display success message
            st.success("Extracted email addresses:")
            
            # Display the DataFrame as a table
            st.dataframe(df)
            
            # Download button
            csv_file = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Emails (CSV)",
                data=csv_file,
                file_name="extracted_emails.csv",
                mime="text/csv",
                key='download-csv'
            )
        else:
            st.write("No email addresses found on the provided websites.")
    else:
        st.warning("Please enter website URLs.")

st.markdown(
    """
    <div class="footer">
        &copy; 2024 Alitech Solutions. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)
