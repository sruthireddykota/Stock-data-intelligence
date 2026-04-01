import streamlit as st
import pandas as pd
import requests

from datetime import datetime

from config.settings import settings


BASE_URL = settings.BASE_URL

st.set_page_config(
    page_title="Stock Data Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Stock Data Dashboard")
     
def get_insights(symbol,period):
    return requests.get(
        url=f"{BASE_URL}/insights/{symbol}",
        params={
            "symbol":symbol,
            "period":period,
        }).json()    

def compare(symbol1, symbol2,period):
    return requests.get(
        url=f"{BASE_URL}/compare", 
        params={
            "symbol1": symbol1, 
            "symbol2": symbol2,
            "period":period}).json() 

def get_summary(symbol,period):
    response= requests.get(
        url=f"{BASE_URL}/data/summary",
        params={
            "symbol":symbol,
            "period":period
        }
    )
    data=response.json()

    if "data" not in data:
        return pd.DataFrame()

    df = pd.DataFrame(data["data"])
    return df

def volume_close_data(symbol, start, end):
    response = requests.get(
        url=f"{BASE_URL}/data/close",
        params={"symbol": symbol, "start": start, "end": end}
    )

    data = response.json()

    # Handle error case
    if "data" not in data:
        return pd.DataFrame()

    df = pd.DataFrame(data["data"])
    return df

with st.sidebar:
    st.header("Filters")
    company = st.selectbox("Choose a Company", 
                           ["INFY", "TCS", "WIPRO", "TECHM"], 
                           key="company")
    
    period = st.selectbox("Choose Period", 
                          ["1y", "2y", "3y"], 
                          key="period")
    period_map = {
        "1y": "13mo",
        "2y": "25mo",
        "3y": "37mo"
    }
    # Since we are losing 30 days of Data due to 30 day moving average, 
    # Predated by 1 month for completely 1 year values 
    mapped_period = period_map.get(period, period)
    
    st.button("Update Dashboard", key="update")

metrics_insights = get_insights(symbol=company,period=mapped_period)

summary=metrics_insights.get("data")

tab1, tab2 = st.tabs(["Company Insights","Comparison"])

with tab1:
    st.subheader(f"{company} Summary Metrics, Period: ({period})")

    col1, col2, col3, col4,col5 = st.columns(5)
    col1.metric("Latest Close", summary["latest_close"])
    col2.metric("52-Week High", summary["52w_high"])
    col3.metric("52-Week Low", summary["52w_low"])

    
    col4.metric("Last Day Trend", summary["latestday_trend"])
    col5.metric("Last Day Risk", summary["latestday_risk"])

    st.subheader(f"{company} Volume & Close Pricer")

    d_col1,d_col2=st.columns(2)
    with d_col1:
        start_date=st.date_input(label="Start data",key="select start date")
    with d_col2:
        end_date=st.date_input(label='End date',key='selct end data')

    if start_date!=end_date and start_date!=datetime.now().date():
        volume_close_df=volume_close_data(symbol=company,
                                        start=str(start_date),
                                        end=str(end_date))
        st.line_chart(data=volume_close_df,x='Date',y='Volume')
        st.line_chart(data=volume_close_df,x='Date',y='Close')
    else:
        st.warning("Start Data shouldn't be the Current Date")
    

with tab2:
    st.subheader("Compare Two Companies")

    company1 = st.selectbox("Company 1", ["INFY", "TCS", "WIPRO", "TECHM", "LTIM"], key="comp1")
    company2 = st.selectbox("Company 2", ["INFY", "TCS", "WIPRO", "TECHM", "LTIM"], key="comp2")

    if company1 and company2 and company1 != company2:
        comparison_data = compare(company1, company2,period=mapped_period)

        summary_df1=get_summary(symbol=company1,period=mapped_period)
        summary_df2=get_summary(symbol=company2,period=mapped_period)

        comparison=comparison_data.get("data")

        comp_df = pd.DataFrame({
            "Metric": ["Latest Close", "Avg Return", "52w High", "52w Low","Latestday Trend", "Latestday Risk"],
            company1: [
                comparison["symbol1"]["latest_close"],
                comparison["symbol1"]["avg_return"],
                comparison["symbol1"]["52w_high"],
                comparison["symbol1"]["52w_low"],
                comparison["symbol1"]["latestday_trend"],
                comparison["symbol1"]["latestday_risk"]
            ],
            company2: [
                comparison["symbol2"]["latest_close"],
                comparison["symbol2"]["avg_return"],
                comparison["symbol2"]["52w_high"],
                comparison["symbol2"]["52w_low"],
                comparison["symbol2"]["latestday_trend"],
                comparison["symbol2"]["latestday_risk"]
            ]
        })
        st.table(comp_df.astype(str))

        st.subheader("Moving Average Plots")

        summary_df1["Date"] = pd.to_datetime(summary_df1["Date"])
        summary_df2["Date"] = pd.to_datetime(summary_df2["Date"])

        df1 = summary_df1[["Date", "MA_7", "MA_30"]].rename(columns={
            "MA_7": f"{company1}_MA7",
            "MA_30": f"{company1}_MA30"
        })

        df2 = summary_df2[["Date", "MA_7", "MA_30"]].rename(columns={
            "MA_7": f"{company2}_MA7",
            "MA_30": f"{company2}_MA30"
        })

        # Merge on Date
        merged_df = pd.merge(df1, df2, on="Date", how="inner")

        # MA_7 comparison
        st.line_chart(
            merged_df.set_index("Date")[[f"{company1}_MA7", f"{company2}_MA7"]]
        )

        # MA_30 comparison
        st.line_chart(
            merged_df.set_index("Date")[[f"{company1}_MA30", f"{company2}_MA30"]]
        )


    elif company1 == company2:
        st.warning("Please select two different companies.")
