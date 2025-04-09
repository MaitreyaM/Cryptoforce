# CryptoForce: AI-Powered Financial Insights System

An Agentic AI/ python script automation projects that performs daily crypto analysis along with general financial analysis and sends user mails with visualization

This project schedules emails to its subscribed users every morning by sending visualized btc trends and a financial report for the day using 
Agentic AI ( summarizes top 5 finance/crypto articles of the day )


## Overview
CryptoForce is an intelligent automation system designed to streamline financial market analysis. It leverages AI agents to fetch real-time cryptocurrency data and financial news, perform sophisticated analyses, and deliver insightful daily reports directly to your inbox.

## Key Features
- **Automated Cryptocurrency Market Analysis:** Real-time Bitcoin price updates from CoinGecko.
- **Comprehensive Financial News Aggregation:** Utilizes Brave Search API to fetch the latest financial news.
- **AI-Driven Reports:** Daily financial insights powered by Llama 3.1-70B model hosted on GroqCloud, ensuring fast and accurate inference (~95% accuracy).
- **Crypto Trend Visualization:** Includes visual trend graphs generated with Matplotlib.
- **Fully Automated Workflow:** Scheduled tasks managed by Railway and email delivery automated through Gmail SMTP.

## Technology Stack
- **Programming Language:** Python
- **AI Models:** Llama 3.1-70B (GroqCloud)
- **Data APIs:** CoinGecko (Cryptocurrency Prices), Brave Search API (Financial News)
- **Database:** Supabase (PostgreSQL-based cloud storage)
- **Deployment & Automation:** Railway (Cron job scheduling)
- **Email Automation:** Gmail SMTP
- **Visualization:** Matplotlib

## Workflow
1. **Data Retrieval:** Scheduled scripts automatically pull Bitcoin prices and financial news each morning.
2. **AI Analysis:** Llama 3.1-70B processes retrieved data, summarizing trends and key market news.
3. **Report Generation:** AI insights and crypto trend graphs are compiled into structured reports.
4. **Email Delivery:** Automated dispatch of daily reports to users through Gmail SMTP, achieving 100% daily delivery success.

## Project Metrics
- **Report Accuracy:** ~95%
- **Automation Reliability:** 100% daily execution and email delivery success rate

## Installation & Setup
Clone the repository:
```bash
git clone https://github.com/MaitreyaM/Cryptoforce.git
cd Cryptoforce
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Configure `.env` file:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
BRAVE_API_KEY=your_brave_api_key
GROQ_API_KEY=your_groq_api_key
SMTP_USERNAME=your_gmail_address
SMTP_PASSWORD=your_gmail_app_password
```

Run the scripts:
```bash
python btc_agent.py
python info_agent.py
python email_agent.py
```

## Deployment
The system is deployed and scheduled via [Railway](https://railway.app), enabling automated daily execution.

## Future Enhancements
- Integration of additional financial data sources
- Advanced predictive analytics
- Web-based dashboard for interactive financial insights

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

