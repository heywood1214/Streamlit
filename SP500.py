import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf


#title of the Web App
st.title('S&P 500 App')
st.markdown("""
This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")


st.sidebar.header('User Input Features')


#cache data so that you don't have to keep downloading the data again and again
#has to be a table format when scraping 
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header =0)
    df= html[0]
    return df

df=load_data()
df

#find sectors
sector_unique = df['GICS Sector'].unique()
sector_unique


#group everything by sector
sector = df.groupby('GICS Sector')

#Allow users to choose sectors 
sorted_sector_unique = sorted(df['GICS Sector'].unique())
user_selected_sector = st.sidebar.multiselect('Sector',sorted_sector_unique,sorted_sector_unique)

#filtering data in the sidebar
df_selected_sector = df[(df['GICS Sector'].isin(user_selected_sector))]


st.header('Display companies in Selected Sector')
st.write('Data Dimension: '+str(df_selected_sector.shape[0])+ 'rows' + str(df_selected_sector.shape[1])+'columns')
st.dataframe(df_selected_sector)

#tranform the dataframe into a CSV file
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href


st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

#Retrieve stock data
data = yf.download(
        tickers = list(df_selected_sector.Symbol),
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )

# Plot Closing Price of Query Symbol
def price_plot(symbol):
  df = pd.DataFrame(data[symbol].Close)
  df['Date'] = df.index
  plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
  plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
  plt.xticks(rotation=90)
  plt.title(symbol, fontweight='bold')
  plt.xlabel('Date', fontweight='bold')
  plt.ylabel('Closing Price', fontweight='bold')
  return st.pyplot()

#choose up to 5 companies
num_company = st.sidebar.slider('Number of Companies',1,5)

if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)

st.set_option('deprecation.showPyplotGlobalUse', False)








#the first companies for the 11 sectors
sector.first()

#show the descriptive statistics
sector.describe()

#examine data by Sector
sector.get_group('Health Care')


import yfinance as yf
list(df.Symbol)



