import database as weatherdb
import pandas as pd
import streamlit as st
import plotly.express as px


#Main Method that triggers first and organizes calls
def main():
    database = weatherdb.database()
    weatherData = database.get_allWeatherData()

    set_style()
    n_days = sidebar(weatherData)

    filtered_data = filter_weather_data(weatherData,n_days)

    page_body(filtered_data,n_days)

#Set the style of the streamlit page
def set_style():
    hide_decoration_bar_style = '''
        <style>
            header {visibility: hidden;}
        </style>
    '''
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

#Build the sidebar of the page and last N Days parameter
def sidebar(weatherData):
    latest_data_time = weatherData['data_time'].max()
    st.sidebar.write("Latest timestamp: {}".format(latest_data_time))
    n_days = st.sidebar.slider("Past N days",0,30)
    return n_days

#Pagebody which today triggers the building of the top level metric cards
#   and the line graphs
def page_body(lastNDaysData,n_days):

    metric_cards(lastNDaysData)

    metric_line_graphs(lastNDaysData,n_days)

#Method to control the data filter and transform new columns
def filter_weather_data(weatherData,n_days):
    today = pd.to_datetime('today').normalize()
    weatherData['data_time'] = pd.to_datetime(weatherData['data_time'])
    weatherData['rainfall_24_hour_total'] = weatherData['Rainfall'].rolling(287).sum()
    weatherData['data_day'] = weatherData['data_time'].apply(lambda x: x.date())


    lastNDaysData = weatherData[weatherData['data_time'] > (today - pd.offsets.Day(n_days))]
    lastNDaysData = lastNDaysData.sort_values('data_time')
    return lastNDaysData

#Build the line graphs for the page using plotly
def metric_line_graphs(lastNDaysData,n_days):
    st.title("Temperature Last {} Days".format(n_days))
    figTemp = px.line(lastNDaysData, x="data_time",y=["Temperature"])
    st.plotly_chart(figTemp)
    st.title("Pressure Last {} Days".format(n_days))
    figPres = px.line(lastNDaysData, x="data_time",y=["Pressure"])
    st.plotly_chart(figPres)
    st.title("Humidity Last {} Days".format(n_days))
    figHumi = px.line(lastNDaysData, x="data_time",y=["Humidity"])
    st.plotly_chart(figHumi)
    st.title("Rainfall (24 Hour running total) Last {} Days".format(n_days))
    figRain = px.line(lastNDaysData, x="data_time",y=["rainfall_24_hour_total"])
    st.plotly_chart(figRain)

#Build the Metric cards for the top of the page
def metric_cards(lastNDaysData):
    current_temp, current_pressure, current_humidity,\
          current_rainfall, current_windspeed,\
          current_windDir = get_current_metrics(lastNDaysData)
    
    dif_temp, dif_pressure, dif_humidity = get_diff_metrics(lastNDaysData)

    cur_temp_str = "{} °F".format(current_temp)
    cur_pressure_str = "{} hPa".format(current_pressure)
    cur_humidity_str = "{}%".format(current_humidity)
    cur_rainfall_str = "{} in".format(current_rainfall)
    cur_windspeed = "{} MPH".format(current_windspeed)

    col1, col2, col3 = st.columns(3)

    col1.metric("Current Temperature",cur_temp_str,dif_temp)
    col2.metric("Current Pressure",cur_pressure_str,dif_pressure)
    col3.metric("Current Humidity",cur_humidity_str,dif_humidity)
    col1.metric("Current 24hr Rainfall",cur_rainfall_str)
    col2.metric("Current Windspeed",cur_windspeed)
    col3.metric("Current Wind Direction",current_windDir)

#Retrieve the latest metrics which are used in the cards
def get_current_metrics(data):
    max_time = data['data_time'].max()

    current_record = data[data['data_time'] == max_time]
    current_temp = current_record['Temperature'].values[0].round(1)
    current_pressure = current_record['Pressure'].values[0].round(0).astype(int)
    current_humidity = current_record['Humidity'].values[0].round(0).astype(int)
    current_rainfall = current_record['rainfall_24_hour_total'].values[0].round(4)
    current_windspeed = current_record['Wind Speed (MPH)'].values[0].round(2)
    current_windDir = current_record['Wind Direction'].values[0]

    return current_temp, current_pressure, current_humidity,\
          current_rainfall, current_windspeed, current_windDir

#Retrieve the difference between the current metrics and the oldest
#   in the dataset for change analytics
def get_diff_metrics(data):
    current_temp, current_pressure, current_humidity,\
          current_rainfall, current_windspeed,\
          current_windDir = get_current_metrics(data)
    
    min_time = data['data_time'].min()
    
    min_record = data[data['data_time'] == min_time]
    min_temp = min_record['Temperature'].values[0].round(1)
    min_pressure = min_record['Pressure'].values[0].round(0).astype(int)
    min_humidity = min_record['Humidity'].values[0].round(0).astype(int)

    dif_temp = (current_temp - min_temp).round(1)
    dif_pressure = int(current_pressure - min_pressure)
    dif_humidity = int(current_humidity - min_humidity)

    return dif_temp, dif_pressure, dif_humidity


if __name__ == '__main__':
    main()