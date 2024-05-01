import yfinance as yf
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()
MODEL = "gpt-3.5-turbo-0125"


def get_stock_price(stock, period="1d"):
    stock = yf.Ticker(f"{stock}")
    hist = stock.history(period=period)
    hist.index = hist.index.strftime("%m-%d-%Y")
    return hist["Close"].to_json()


def get_stock_analysis(message):
    messages = [{"role": "user", "content": message}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_stock_price",
                "description": "Get the price of a stock",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "stock": {
                            "type": "string",
                            "description": "The stock code, e.g. ABEV3.SA",
                        },
                        "period": {
                            "type": "string",
                            "description": "The period of the stock price, e.g. 1d (1 day), 2mo (2 months), 1y (1 year)",
                        },
                    },
                    "required": ["stock"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model=MODEL, messages=messages, tools=tools, tool_choice="auto"
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        available_functions = {"get_stock_price": get_stock_price}
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                stock=function_args.get("stock"), period=function_args.get("period")
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
    second_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    return second_response.choices[0].message.content


message = ""

while message != "exit":
    message = input("O que você deseja saber sobre ações brasileiras? ")
    if message != "exit":
        response = get_stock_analysis(message)
        print(response)
