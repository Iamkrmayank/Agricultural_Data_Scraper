import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

# Streamlit app
st.title('Agricultural Land Scraper')

# Input URL
url = st.text_input('Enter the URL of the page to scrape:', '')

if url:
    # Fetch the webpage
    response = requests.get(url)
    
    if response.status_code == 200:
        html = response.text

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Initialize lists to store data
        property_names = []
        owners = []
        locations = []
        areas = []
        dimensions = []
        prices = []

        # Find all listings
        listings = soup.find_all('div', class_='mb-srp__list')

        for listing in listings:
            # Extract the required information
            name = listing.find('h2', class_='mb-srp__card--title')
            owner = listing.find('div', class_='mb-srp__card__ads--name')
            location = listing.find('p', class_='plot-desc')
            area = listing.find_all('div', class_='mb-srp__card__summary--value')
            price = listing.find('div', class_='mb-srp__card__price--amount')

            # Append the information to respective lists
            property_names.append(name.text.strip() if name else 'N/A')
            owners.append(owner.text.strip() if owner else 'N/A')
            locations.append(location.text.strip() if location else 'N/A')

            # Handle multiple summary values for area and dimension
            if area and len(area) > 1:
                areas.append(area[0].text.strip())
                dimensions.append(area[1].text.strip())
            else:
                areas.append('N/A')
                dimensions.append('N/A')

            prices.append(price.text.strip() if price else 'N/A')

        # Create a DataFrame
        data = {
            'Property Name': property_names,
            'Owner': owners,
            'Location': locations,
            'Area': areas,
            'Dimension': dimensions,
            'Price': prices
        }
        df = pd.DataFrame(data)

        # Show the DataFrame in the Streamlit app
        st.dataframe(df)

        # Provide a download link for the DataFrame
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label='Download data as CSV',
            data=csv,
            file_name='agricultural_land.csv',
            mime='text/csv',
        )
    else:
        st.error(f"Failed to retrieve the webpage. Status code: {response.status_code}")
