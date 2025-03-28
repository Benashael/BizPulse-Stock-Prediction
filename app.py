import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime

# Set up Streamlit app
st.set_page_config(page_title="Stock Prediction App", page_icon="💰", layout="wide")
st.title("💰 Stock Prediction App")

# App Features
st.write("### Features of this Application:")
# Display a brief description with emojis
st.markdown("""
📈 **Stock Prediction**
Predict future stock prices using historical data and powerful machine learning algorithms.

📊 **Data Visualization**
Visualize stock trends, patterns, and market movement to make well-informed decisions.

💡 **Investment Insights**
Get accurate buy/sell recommendations based on market analysis and predictions to optimize your trading strategy.
""")

# Predefined stock symbols for each exchange
stock_options = {
    "NSE": [
        "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ITC.NS", "SBIN.NS", 
        "BAJFINANCE.NS", "BHARTIARTL.NS", "AXISBANK.NS", "KOTAKBANK.NS", "LARSEN.NS", "MARUTI.NS", "M&M.NS", 
        "WIPRO.NS", "HCLTECH.NS", "ULTRACEMCO.NS", "NTPC.NS", "ONGC.NS", "TATAMOTORS.NS", "ASIANPAINT.NS", 
        "SUNPHARMA.NS", "DRREDDY.NS", "TECHM.NS", "DIVISLAB.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "CIPLA.NS", 
        "HAVELLS.NS", "INDUSINDBK.NS", "BAJAJ-AUTO.NS", "EICHERMOT.NS", "UPL.NS", "GRASIM.NS", "POWERGRID.NS", 
        "MUTHOOTFIN.NS", "BPCL.NS", "VEDL.NS", "ZEE.NS", "TATACONSUM.NS", "GAIL.NS", "RELIANCEPOWER.NS", "IOC.NS", 
        "M&MFIN.NS", "ADANIPOWER.NS", "HDFCLIFE.NS", "LUPIN.NS", "SBILIFE.NS", "JSWSTEEL.NS"
    ],
    "BSE": [
        "500325.BO", "532540.BO", "500180.BO", "532174.BO", "500570.BO", "532641.BO", "532455.BO", "532155.BO", 
        "500010.BO", "532855.BO", "500209.BO", "500114.BO", "500470.BO", "500134.BO", "500827.BO", "532939.BO", 
        "533020.BO", "500104.BO", "500413.BO", "500408.BO", "500244.BO", "500312.BO", "500164.BO", "532634.BO", 
        "500376.BO", "532610.BO", "533287.BO", "500147.BO", "500692.BO", "532898.BO", "500124.BO", "500185.BO", 
        "500840.BO", "532179.BO", "500109.BO", "532780.BO", "500828.BO", "533091.BO", "532761.BO", "532832.BO", 
        "500181.BO", "532215.BO", "532374.BO", "500182.BO", "500260.BO", "500209.BO", "532540.BO", "500301.BO", 
        "532555.BO", "532674.BO"
    ],
    "LSE": [
        "HSBA.L", "VOD.L", "BP.L", "GLEN.L", "AZN.L", "TSCO.L", "GSK.L", "BHP.L", "RDSB.L", "SHEL.L", "LLOY.L", 
        "RMG.L", "BARC.L", "RR.L", "IMB.L", "SGRO.L", "DLG.L", "EXPN.L", "IWG.L", "RTO.L", "PSON.L", "STAN.L", 
        "III.L", "WPP.L", "DGE.L", "ULVR.L", "CNA.L", "LSEG.L", "SSE.L", "VOD.L", "CLLN.L", "RBS.L", "DPLM.L", 
        "BA.L", "MCRO.L", "SHB.L", "NXT.L", "LGEN.L", "MNG.L", "FOG.L", "FRES.L", "WEIR.L", "NDX.L", "VKG.L", 
        "RHP.L", "ABF.L", "SN.L", "YULE.L", "ARM.L", "HL.L", "BA.L", "MNDI.L", "DNO.L"
    ],
    "NYSE": [
        "MSFT", "AAPL", "GOOGL", "AMZN", "TSLA", "FB", "NFLX", "NVDA", "INTC", "BA", "DIS", "V", "JNJ", "PG", 
        "MA", "PYPL", "CSCO", "XOM", "WMT", "COST", "ORCL", "UPS", "IBM", "ADBE", "SPGI", "CVX", "PEP", "MCD", 
        "T", "NVDA", "UNH", "GE", "INTU", "KO", "MS", "MMM", "LMT", "GS", "ABT", "CAT", "LOW", "AMD", "QCOM", 
        "AXP", "HD", "USB", "SYF", "MELI", "RTX", "REGN", "AMGN", "TMO", "ISRG"
    ],
    "NASDAQ": [
        "AAPL", "GOOGL", "AMZN", "TSLA", "NFLX", "NVDA", "META", "MSFT", "INTC", "AMD", "PYPL", "CSCO", "WMT", 
        "INTU", "ADBE", "MU", "NFLX", "ZM", "LULU", "SNAP", "BIDU", "REGN", "ISRG", "QCOM", "AMAT", "NXPI", 
        "INTU", "GSX", "GILD", "VRTX", "PEP", "CVX", "BA", "NKE", "SBUX", "ISRG", "EBAY", "BABA", "SHOP", "ATVI", 
        "AAL", "ZM", "AMAT", "TWTR", "VRSK", "MAR", "PYPL", "MU", "JBL", "MRNA", "EBAY", "EXPE", "ALGN"
    ]
}

# Function to fetch historical stock data
def fetch_stock_data(exchange, symbol, start_date, end_date):
    ticker = f"{symbol}.{exchange}" if exchange != "NSE" else symbol  # For NSE, no need to prefix
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Function for stock price prediction (Linear Regression for demonstration)
def predict_stock_prices(data, end_date):
    # Ensure the index is a datetime object
    data['Date'] = pd.to_datetime(data.index)
    data['Date'] = data['Date'].map(pd.Timestamp.toordinal)

    # Prepare data for training
    X = data['Date'].values.reshape(-1, 1)
    y = data['Close'].values

    # Train the Linear Regression model
    model = LinearRegression()
    model.fit(X, y)

    # Generate future dates dynamically based on end_date
    last_date = pd.to_datetime(data.index[-1])  # Last date in the dataset
    business_days_diff = pd.bdate_range(last_date, end_date).size  # Number of business days
    
    # Limit the business days to 365 if it exceeds
    if business_days_diff > 365:
        st.warning("⚠️ The period exceeds 365 business days. Limiting to 365 business days. ⏳")
        business_days_diff = 365

    # Generate future dates
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=business_days_diff, freq="B")
    future_dates_ordinal = future_dates.map(pd.Timestamp.toordinal).values.reshape(-1, 1)

    # Predict future prices
    future_predictions = model.predict(future_dates_ordinal)

    return future_dates, future_predictions

def recommendation(past_data, future_predictions):
    # Extract the last 5 closing prices and calculate the average
    recent_closing_prices = past_data['Close'].tail(5).values
    recent_avg = float(sum(recent_closing_prices) / len(recent_closing_prices))  # Ensure scalar

    # Flatten future_predictions and calculate its average
    future_predictions_flat = future_predictions.flatten()  # Ensures a 1D array
    predicted_avg = float(sum(future_predictions_flat) / len(future_predictions_flat))  # Ensure scalar

    # Generate the recommendation
    if predicted_avg > recent_avg:
        recommendation_text = "📈 Buy"
    elif predicted_avg < recent_avg:
        recommendation_text = "📉 Sell"
    else:
        recommendation_text = "🤷‍♂️ Hold"

    # Return a detailed response
    return {
        "Recommendation": recommendation_text,
        "Recent Average Price": f"${round(recent_avg, 2)}",  # Scalar value
        "Predicted Average Price": f"${round(predicted_avg, 2)}",  # Scalar value
    }

st.header("📉 Stock Prediction and Analysis 📊")

# Dropdown for selecting exchange
exchange = st.selectbox("📍 Select Stock Exchange", list(stock_options.keys()))

# Dropdown for selecting stock symbol
company = st.selectbox("🔍 Select Stock Symbol", stock_options[exchange])

# Date inputs for historical data
start_date = st.date_input("📅 Start Date", datetime(2020, 1, 1))
end_date = st.date_input("📅 End Date", datetime.today())

if st.button("🔎 Get Stock Data"):
    data = fetch_stock_data(exchange, company, start_date, end_date)
    if data.empty:
        st.error("❌ No data found for the selected stock.")
    else:
        st.write(data.tail())

        # Plotting the stock's price data (Open, High, Low, Close)
        st.subheader("📈 Stock Prices Over Time")
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plotting each price type with a unique color and label
        ax.plot(data.index, data['Open'], label="Open Price", color="blue")
        ax.plot(data.index, data['High'], label="High Price", color="green")
        ax.plot(data.index, data['Low'], label="Low Price", color="red")
        ax.plot(data.index, data['Close'], label="Close Price", color="orange")
        
        # Adding labels, title, and legend
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.set_title(f"{company} Stock Prices Over Time")
        ax.legend(loc="upper left")  # Position of legend
        
        # Display the plot
        st.pyplot(fig)

        # Plotting the stock's Open Price
        st.subheader("📊 Open Price Over Time")
        fig_open, ax_open = plt.subplots(figsize=(10, 6))
        ax_open.plot(data.index, data['Open'], label="Open Price", color="blue")
        ax_open.set_xlabel("Date")
        ax_open.set_ylabel("Price")
        ax_open.set_title(f"{company} Open Price Over Time")
        ax_open.legend(loc="upper left")
        st.pyplot(fig_open)
        
        # Plotting the stock's High Price
        st.subheader("📈 High Price Over Time")
        fig_high, ax_high = plt.subplots(figsize=(10, 6))
        ax_high.plot(data.index, data['High'], label="High Price", color="green")
        ax_high.set_xlabel("Date")
        ax_high.set_ylabel("Price")
        ax_high.set_title(f"{company} High Price Over Time")
        ax_high.legend(loc="upper left")
        st.pyplot(fig_high)
        
        # Plotting the stock's Low Price
        st.subheader("📉 Low Price Over Time")
        fig_low, ax_low = plt.subplots(figsize=(10, 6))
        ax_low.plot(data.index, data['Low'], label="Low Price", color="red")
        ax_low.set_xlabel("Date")
        ax_low.set_ylabel("Price")
        ax_low.set_title(f"{company} Low Price Over Time")
        ax_low.legend(loc="upper left")
        st.pyplot(fig_low)
        
        # Plotting the stock's Close Price
        st.subheader("📊 Close Price Over Time")
        fig_close, ax_close = plt.subplots(figsize=(10, 6))
        ax_close.plot(data.index, data['Close'], label="Close Price", color="orange")
        ax_close.set_xlabel("Date")
        ax_close.set_ylabel("Price")
        ax_close.set_title(f"{company} Close Price Over Time")
        ax_close.legend(loc="upper left")
        st.pyplot(fig_close)

        # Predictions
        future_dates, future_predictions = predict_stock_prices(data, end_date)
        
        # Display predicted prices
        st.subheader("🔮 Future Predicted Prices")
        # Flatten the predictions array
        predictions_df = pd.DataFrame({
            "Date": future_dates, 
            "Predicted Price": future_predictions.flatten()
        })
        st.write(predictions_df)
        
        # Plot the original closing prices and the predicted future prices
        st.subheader(f"📉 Stock Price Prediction for {company}")
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot historical data
        ax.plot(data.index, data['Close'], label="Historical Close Price", color="blue")
        
        # Plot future predictions
        ax.plot(future_dates, future_predictions, label="Predicted Price", color="orange", linestyle="--")
        
        # Configure plot
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.set_title(f"{company} Stock Price Prediction")
        ax.legend()
        
        # Display the plot
        st.pyplot(fig)

        # Get recommendation based on past data and predictions
        recommendation_result = recommendation(data, future_predictions)
        
        # Display the recommendation and details
        st.subheader("📈 Investment Recommendation")
        st.write(f"**Recommendation**: {recommendation_result['Recommendation']}")
        st.write(f"**Recent Average Closing Price**: ${recommendation_result['Recent Average Price']}")
        st.write(f"**Predicted Average Closing Price**: ${recommendation_result['Predicted Average Price']}")
