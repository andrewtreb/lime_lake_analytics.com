from lla.database import database
import plotly.graph_objects as go
import plotly.express as px
import plotly
import datetime
import json
import pandas as pd

class visuals:
    def __init__(self):
        self.database = database()
        self.data = self.database.get_allWeatherData()

        self.data['data_time'] = pd.to_datetime(self.data['data_time'])

        self.text_color = "Green"
        self.title_size = 45
        self.font_family = "Gothic"

    def data_last_hour(self):
        weather = self.data
        last_time = weather.sort_values('data_time').tail(1)['data_time']

        print(str(last_time.values[0])[:19])

        return str(last_time.values[0])[:19]
        

    def current_temp_ind(self):
        weather = self.data


        last_x_weather = weather[weather['data_time'] > datetime.datetime.now() -
                                datetime.timedelta(hours=24)]

        if last_x_weather.shape[0] == 0 :
            print('No data recieved in last hour')
            last_x_weather = weather.tail(50)

        max_record_time = last_x_weather['data_time'].max()

        latest_record = last_x_weather[last_x_weather['data_time'] == max_record_time]

        cur_temp = latest_record['Temperature'].values[0]

        fig = go.Figure()

        temp_ind = go.Indicator(
            value = cur_temp,
            number = { 'suffix': "°F" },
            domain = {'row': 0,'column': 1},
            title = "Current Temp",
            title_font_color = self.text_color,
            title_font_size = self.title_size,
            title_font_family= self.font_family
            )


        fig.add_trace(temp_ind)
        #fig.add_scatter(temp_line)

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)