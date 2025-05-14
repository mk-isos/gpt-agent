from datetime import datetime
import pytz
import yfinance as yf
import streamlit as st
import pandas as pd

def get_current_time(timezone: str = 'Asia/Seoul'):
    tz = pytz.timezone(timezone)
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    now_timezone = f'{now} {timezone}'
    print(now_timezone)
    return now_timezone

def get_yf_stock_info(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info
    print(info)
    
    # Streamlit 표 형태 출력
    st.subheader(f"📊 {ticker.upper()} 종목 정보")
    info_df = pd.DataFrame.from_dict(info, orient='index', columns=["Value"])
    st.dataframe(info_df)

    return str(info)

def get_yf_stock_history(ticker: str, period: str):
    stock = yf.Ticker(ticker)
    history = stock.history(period=period)

    # Streamlit 표로 출력
    st.subheader(f"📈 {ticker.upper()}의 최근 {period}간 주가 히스토리")
    st.dataframe(history)

    history_md = history.to_markdown()
    print(history_md)
    return history_md

def get_yf_stock_recommendations(ticker: str):
    stock = yf.Ticker(ticker)
    recommendations = stock.recommendations

    if recommendations is None or recommendations.empty:
        st.warning(f"{ticker.upper()}에 대한 추천 정보가 없습니다.")
        return "추천 정보가 없습니다."

    st.subheader(f"🧠 {ticker.upper()} 종목에 대한 애널리스트 추천")
    st.dataframe(recommendations)

    recommendations_md = recommendations.to_markdown()
    print(recommendations_md)
    return recommendations_md

# 🔧 Function tool 등록
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "해당 타임존의 날짜와 시간을 반환합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    'timezone': {
                        'type': 'string',
                        'description': '현재 날짜와 시간을 반환할 타임존을 입력하세요. (예: Asia/Seoul)',
                    },
                },
                "required": ['timezone'],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_yf_stock_info",
            "description": "해당 종목의 Yahoo Finance 정보를 반환합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    'ticker': {
                        'type': 'string',
                        'description': 'Yahoo Finance 정보를 반환할 종목의 티커를 입력하세요. (예: AAPL)',
                    },
                },
                "required": ['ticker'],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_yf_stock_history",
            "description": "해당 종목의 Yahoo Finance 주가 정보를 반환합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    'ticker': {
                        'type': 'string',
                        'description': 'Yahoo Finance 주가 정보를 반환할 종목의 티커를 입력하세요. (예: AAPL)',
                    },
                    'period': {
                        'type': 'string',
                        'description': '주가 정보를 조회할 기간을 입력하세요. (예: 1d, 5d, 1mo, 1y, 5y)',
                    },
                },
                "required": ['ticker', 'period'],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_yf_stock_recommendations",
            "description": "해당 종목의 Yahoo Finance 추천 정보를 반환합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    'ticker': {
                        'type': 'string',
                        'description': 'Yahoo Finance 추천 정보를 반환할 종목의 티커를 입력하세요. (예: AAPL)',
                    },
                },
                "required": ['ticker'],
            },
        }
    },
]

# 🧪 테스트 용도
if __name__ == '__main__':
    get_yf_stock_history('AAPL', '5d')
    print('----')
    get_yf_stock_recommendations('AAPL')
