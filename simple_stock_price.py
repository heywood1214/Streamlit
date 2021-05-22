import yfinance as yf
import streamlit as st

st.write("""
# Simple Stock Price App
Shown are the stock **closing price** and ***volume*** of Google!
""")

#define the ticker symbol
tickerSymbol = 'HQU.TO'
tickersymbol_list = ['HQU.TO']


#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')
# Open	High	Low	Close	Volume	Dividends	Stock Splits

st.write("""
## Closing Price
""")
st.line_chart(tickerDf.Close)
st.write("""
## Volume Price
""")
st.line_chart(tickerDf.Volume)


st.button('Hit me')

st.checkbox('I am a checkbox')

st.radio('Radio',[1,2,3])

st.text_input("Enter a ticker symbol")

for i in range(int(st.number_input('Num:'))): foo()




