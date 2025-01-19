import os
import json
import requests
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime
from phi.agent import Agent
from phi.model.groq import Groq

# Load environment variables
load_dotenv(override=True)

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Brave Search API Configuration
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to fetch financial news using Brave API
def fetch_financial_news(query):
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": BRAVE_API_KEY,
    }
    params = {"q": query, "count": 5}

    print("Requesting URL:", url)
    print("With Parameters:", params)

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("web", {}).get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

# Function to save news into the Supabase database
def save_news_to_supabase(news_list, prefix):
    for news in news_list:
        try:
            timestamp = datetime.now().isoformat()
            # Add the prefix to indicate the type of news
            data = {
                "timestamp": timestamp,
                "finance_info": f"{prefix}: {news.get('title', 'No Title')} - {news.get('url', 'No URL')}",
            }
            print(f"Attempting to save: {data}")

            # Insert data into Supabase
            response = supabase.table("eco_info").insert(data).execute()

            if response.data:
                print(f"Saved: {data['finance_info']}")
            elif response.error:
                print(f"Supabase Error Message: {response.error.message}")
                print(f"Supabase Error Details: {response.error}")
            else:
                print(f"Unknown Supabase Response: {response}")
        except Exception as e:
            print(f"Error saving news: {e}")

# GroqCloud function definition for generating search queries
def groq_function_call(prompt):
    agent = Agent(
        model=Groq(id="llama-3.1-70b-versatile"),
        show_tool_calls=True,
        markdown=True,
        instructions=[
            "Generate specific, targeted search queries for financial news.",
            "Provide concise and relevant queries.",
        ],
        debug_mode=True,
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a financial news researcher. Your task is to generate search queries "
                "to retrieve the latest important financial news, focusing on:\n"
                "1. Major macroeconomic developments\n"
                "2. Significant Bitcoin and cryptocurrency news\n"
                "3. Important market trends and events\n\n"
                "Generate specific, targeted search queries that will yield relevant results."
            ),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    try:
        response = agent.run(messages)

        if response and "output" in response:
            query = response["output"].split("\n")[0].strip()
            if query:
                print(f"Generated query: {query}")
                return query

        print("No query generated. Defaulting to 'finance crypto'.")
        return "finance crypto"
    except Exception as e:
        print(f"Error during GroqCloud function call: {e}")
        return "finance crypto"

# Main function to run two searches
def run_info_agent():
    print("Running info_agent with GroqCloud...")

    # Bitcoin/crypto search
    print("Generating Bitcoin/crypto search query using AI...")
    crypto_query = groq_function_call("Generate a search query for Bitcoin and cryptocurrency news.")
    print(f"Using Bitcoin/crypto query: {crypto_query}")

    print("Fetching Bitcoin/crypto financial news...")
    crypto_news = fetch_financial_news(query=crypto_query)
    if crypto_news:
        print(f"Fetched {len(crypto_news)} Bitcoin/crypto news articles. Saving to database...")
        save_news_to_supabase(crypto_news, prefix="Crypto")
    else:
        print("No Bitcoin/crypto news articles fetched.")

    # General finance market search
    print("Generating general finance market search query using AI...")
    finance_query = groq_function_call("Generate a search query for general financial market news.")
    print(f"Using general finance query: {finance_query}")

    print("Fetching general finance market news...")
    finance_news = fetch_financial_news(query=finance_query)
    if finance_news:
        print(f"Fetched {len(finance_news)} general finance news articles. Saving to database...")
        save_news_to_supabase(finance_news, prefix="Finance")
    else:
        print("No general finance market news articles fetched.")

# Execute the agent
if __name__ == "__main__":
    run_info_agent()
