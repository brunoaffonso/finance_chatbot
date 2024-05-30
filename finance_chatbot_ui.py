import yfinance as yf
import streamlit as st
import openai
import json


MODEL = "gpt-4o"


def get_stock_price(stock, period="1d"):
    stock = yf.Ticker(f"{stock}")
    hist = stock.history(period=period)["Close"]
    # hist.index = hist.index.strftime("%m-%d-%Y")
    hist = round(hist, 2)
    if len(hist) > 30:
        slice_size = int(len(hist) / 30)
        hist = hist.iloc[::-slice_size][::-1]
    return hist.to_json()


def get_stock_analysis(message, openai_key):
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
                            "description": "The period of the stock price, e.g. 1d (1 day), 2mo (2 months), 1y (1 year). Options: ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']",
                        },
                    },
                    "required": ["stock"],
                },
            },
        }
    ]
    openai.api_key = openai_key
    response = openai.chat.completions.create(
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
    second_response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    return second_response.choices[0].message.content


def main_page():
    st.set_page_config(
        layout="wide",
        page_title="Chatbot",
        page_icon="🤖",
        initial_sidebar_state="expanded",
    )

    api_key = st.sidebar.text_input('OpenAI API Key', type='password')

    button = st.sidebar.button('Clear Chat')
    if button:
        st.session_state['messages'] = []

    if not 'messages' in st.session_state:
        st.session_state['messages'] = []

    messages = st.session_state['messages']

    st.header('🤖 Finance Chatbot 💵', divider=True)

    for message in messages:
        chat = st.chat_message(message['role'])
        chat.markdown(message['content'])

    if api_key:
        openai.api_key = api_key
        prompt = st.chat_input('Ask a question about brazilian stocks...')
        if prompt:
            new_message = {'role': 'user', 'content': prompt}
            chat = st.chat_message(new_message['role'])
            chat.markdown(new_message['content'])
            messages.append(new_message)

            chat = st.chat_message('assistant')
            placeholder = chat.empty()
            placeholder.markdown('▌')
            response = get_stock_analysis(prompt, api_key)
            placeholder.markdown(response)
            new_message = {'role': 'assistant', 'content': response}
            messages.append(new_message)

            st.session_state['messages'] = messages
    else:
        st.info('Please, enter your OpenAI API Key')

main_page()
