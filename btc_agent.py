# file: fetch_btc_price_and_save.py

import requests
from supabase import create_client, Client
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(override=True)

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_btc_price_in_inr():
    """
    Fetch the current price of Bitcoin (BTC) in Indian Rupees (INR) using the CoinGecko API.
    Send the price to the Supabase database.
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin',  # Specify Bitcoin as the cryptocurrency
        'vs_currencies': 'inr'  # Fetch the price in INR
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        data = response.json()
        
        # Extract BTC price in INR
        btc_price_inr = data.get('bitcoin', {}).get('inr', None)
        if btc_price_inr is not None:
            # Format the price with commas
            formatted_price = f"{btc_price_inr:,.2f}"
            print(f"The current price of Bitcoin (BTC) in INR is: ₹{formatted_price}")
            
            # Save the price to the Supabase database
            save_to_supabase(btc_price_inr, "INR")
        else:
            print("Failed to retrieve BTC price in INR.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the BTC price in INR: {e}")

def save_to_supabase(price: float, currency: str):
    """
    Save the BTC price to the Supabase database.
    """
    try:
        timestamp = datetime.now().isoformat()  # Current timestamp
        data = {
            "price": price,
            "currency": currency,
            "timestamp": timestamp
        }
        response = supabase.table("btc_price").insert(data).execute()
        
        # Check the response
        if response.data:
            print(f"Successfully saved BTC price to Supabase: ₹{price} ({currency})")
        elif response.error:
            print(f"Failed to save BTC price to Supabase: {response.error.message}")
        else:
            print("Unknown error occurred while saving to Supabase.")
    except Exception as e:
        print(f"An error occurred while saving to Supabase: {e}")

# Call the function
fetch_btc_price_in_inr()
