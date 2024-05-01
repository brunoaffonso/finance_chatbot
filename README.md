# Stock Price Analysis Tool

This Python script provides a tool for analyzing stock prices using OpenAI's GPT model and Yahoo Finance data. The script integrates with the OpenAI GPT model to interpret user queries about stock prices and provides responses based on historical stock data.

## Features

- **Stock Price Retrieval:** Fetches historical stock prices from Yahoo Finance for a specified period.
- **OpenAI Integration:** Uses OpenAI's GPT model to interpret user queries and formulate responses about stock analysis.
- **Interactive CLI:** A command-line interface allows users to ask questions about stocks in a conversational manner.

## Requirements

To run this script, you need to have the following installed:

- Python 3.8 or later
- Packages: `yfinance`, `openai`, `dotenv`

You can install the necessary packages using:

```bash
pip install yfinance openai python-dotenv
```

## Setup

1. **Environment Variables:** Create a `.env` file in the root directory and add your OpenAI API key:

   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

2. **Running the Script:**

   - Run the script by executing:

   ```bash
   python3 your_script_name.py
   ```

3. **Interacting with the Tool:**

   - Once the script is running, you can ask questions about stocks, such as:

   ```bash
   O que você deseja saber sobre ações brasileiras?
   ```

   - To exit the interactive session, type "exit".

## How It Works

1. **Stock Price Retrieval:**

   The function `get_stock_price()` retrieves historical stock prices from Yahoo Finance for a specified period and returns them in JSON format.

2. **GPT Integration:**

   The function `get_stock_analysis()` uses the OpenAI GPT model to interpret user queries. It integrates with `get_stock_price()` as a function tool to fetch stock prices and provides a comprehensive response back to the user.

## Notes

- Ensure you have an active internet connection for both OpenAI and Yahoo Finance API calls.
- The tool is designed to handle Brazilian stock codes.

---

If you need further assistance, feel free to reach out!

---

This README was generated using AI.
