'''
EN.605.662 Data Visualization.

'''

import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.error import URLError


st.set_page_config(layout = "wide")

c1,c2 = st.columns(2)

page = st.sidebar.selectbox('Select View',['Start','U.S. Temperature Outliers','U.S. Weather Radars','Global Temperature Averages since 1849']) 


if page == 'Start':
    c1.subheader('EN.605.662 Data Visualization Project 4')
    c1.subheader('Author: Anthony Sheller')
    c1.markdown(
        """
        **Overview**
        The weather has always been a concern for humanity, but recently, even more so as temperatures rise and it becomes harder for everyone to adapt to a rapidly changing climate. To comprehend the magnitude of the problem, this work selected three weather-related data sets for analysis. 
        1.	U.S. Weather Outliers, 1964 to 2013 [1]. This data set is published on Data World and consists of over three million observations and eleven attributes, including longitude and latitude.
        2.	Weather Radar Stations [2]. This data set contains approximately two-hundred weather radar stations. Approximately seven attributes comprise the data set: the type of radar, its location (X, Y), id (object and site), name, and antenna elevation.
        3.	Climate Change: Earth Surface Temperature Data [3]. This data set comprises five files covering global land temperatures by city, country, major city, and state. The fifth data set covers global land and ocean temperatures.


        **Instructions**
        From the dropdown on the left select the visusalization you would like to view.
    """)
    c1.image('images/thunder.jpg',caption='Thunderstorm, Purple image. Free for use')
    c2.image("images/tree1.jpg",caption= 'Tree, Clouds, Fields image. Free for use')
    c2.markdown(
        """
        **References:**
        1.	Lewis, Carl. “U.S. Weather Outliers, 1964- - Dataset by Carlvlewis.” Data.World, 25 Apr. 2017, data.world/carlvlewis/u-s-weather-outliers-1964. 
        2.	Homeland Infrastructure Foundation. “Weather Radar Stations - Dataset by DHS.” Data.World, 18 Aug. 2016, data.world/dhs/weather-radar-stations. 
        3.	Earth, Berkeley. “Climate Change: Earth Surface Temperature Data.” Kaggle, 1 May 2017, www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data. 

    """
    )    
    

if page == 'U.S. Temperature Outliers':
    
    @st.cache_data(show_spinner=True)
    def get_WO_data():
        
        df = pd.read_csv('data/weather-anomalies-1964-2013-ymd-40k.csv',engine='pyarrow',dtype_backend='pyarrow')
        return df

    @st.cache_data(show_spinner=True)
    def get_max_temp_data_for_plot():
        
        df = pd.read_csv('data/weather-anomalies-1964-2013-ymd-40k.csv')
        results = df.groupby('year')['max_temp'].mean()
        return results.to_frame().reset_index()

    @st.cache_data(show_spinner=True)
    def get_min_temp_data_for_plot():
        
        df = pd.read_csv('data/weather-anomalies-1964-2013-ymd-40k.csv')
        results = df.groupby('year')['min_temp'].mean()
        return results.to_frame().reset_index()

    def plot_max_temp(df):
        import plotly.graph_objects as go
        import numpy as np
        coefficients = np.polyfit(df.year.to_numpy(),df.max_temp.to_numpy(),1)
        trendline = np.polyval(coefficients,df.year.to_numpy())
        sc_plot = go.Scatter(x=df.year, y=df.max_temp ,mode='markers',
                                 name='Max Outlier Temperatures')
        trend_plot = go.Scatter(x=df.year, y=trendline ,mode='lines',
                                 name='Trendline')
        fig = go.Figure(data=[sc_plot,trend_plot])
        fig.update_layout(title='Max US Temperature Outlier 1964 - 2013',
                        xaxis_title='Year',
                        yaxis_title='Temp in Degress C')

        return fig


    def plot_min_temp(df):
        import plotly.graph_objects as go
        import numpy as np
        coefficients = np.polyfit(df.year.to_numpy(),df.min_temp.to_numpy(),1)
        trendline = np.polyval(coefficients,df.year.to_numpy())
        # Add a line trace
        sc_plot = go.Scatter(x=df.year, y=df.min_temp ,mode='markers',
                                 name='Min Outlier Temperatures')
        trend_plot = go.Scatter(x=df.year, y=trendline ,mode='lines',
                                 name='Trendline')
        fig = go.Figure(data=[sc_plot,trend_plot])
        fig.update_layout(title='Min US Temperature Outlier 1964 - 2013',
                        xaxis_title='Year',
                        yaxis_title='Temp in Degress C')
        return fig

    try:
        c1.header("US Temperature Outlier 1964 - 2013")
        c1.markdown(
        """
        **Overview**
        This dataset is from [data.world](https://data.world/carlvlewis/u-s-weather-outliers-1964/workspace/intro) and presents
        temperature outliers from 1964 to 2013.
        
        Each entry represents a report from a weather station with high or low temperatures that were historical outliers 
        within that month, averaged over time. Note: This table's columns contain data that was collected from [NOAA](https://www.ncei.noaa.gov/).

        """

        )
        c1.map(get_WO_data())
        c1.dataframe(get_WO_data())
        c2.subheader('Temperature Trends 1964 - 2013')
        c2.markdown(
        """
        **Observations**

        The maximum and minimum temperatures were averaged over the year. What is disturbing is that both maximum and minimum are inceraseing.
        One might expect this with the climate situation the way it is (not very good: global warming for example).
        
        """

        )



        fig = plot_max_temp(get_max_temp_data_for_plot())
        c2.plotly_chart(fig)
        fig2 = plot_min_temp(get_min_temp_data_for_plot())
        c2.plotly_chart(fig2)


    except URLError as e:
        st.error(
            """
            **Something went wrong**

            Connection error: %s
        """
            % e.reason
        )

elif page == 'U.S. Weather Radars':

    def assign_color(row):
        if row['radartype'] == 'NEXRAD':
            return "#cc000000"

        else:
            return "#000000ff"
        

    #@st.cache_data(show_spinner=True)
    def get_WR_data(what=None,state = 'All'):
        df = pd.read_csv('data/weather_radar_stations_state.csv')
        print("State is {}".format(state))
        df.rename(columns={'y': 'lat','x':'lon'}, inplace=True)
        df['color']=df.apply(lambda row: assign_color(row),axis=1)
        print("What is {}".format(what))
        if what == None:
            if state == 'All':
                print("returning df for ALL")
                return df
            else:
                print("NOT ALL State is {}".format(state))
                df = df.loc[df['state'] == state]
                print("PAST CREATING DF\n {}".format(df))
                return df
        elif what == 'NEXRAD':
            df = df[df.radartype=='NEXRAD']
            if state == 'All':
                print("Returning nexrad All")
                return df
            else:
                print("Returning nexrad by state")
                return df[df.state == state]
        elif what == "TDWR":
            df = df[df.radartype=='TDWR']
            if state == 'All':
                return df
            else:
                return df[df.state == state]

    try:
        c1.header("US Weather Radar Stations")
        c1.markdown(
        """
        **Overview**
        This dataset is from [data.world](https://data.world/dhs/weather-radar-stations) and presents
        Next Generation Radar (NEXRAD) and Terminal Doppler Weather Radar (TDWR) stations within the US. 
        
        The NEXRAD radars are operatoed by National Oceanic and Atmospheric Administration (NOAA).
        The TWDR radar stations are operated by teh Federal Aviation Administration (FAA).

        Each radar can measure out to 460km.
        """

        )

        #c1.map(get_WR_data(), color='color')
        r_type = c2.radio("Select Radar Type",('All','NEXRAD','TDWR'))
        import numpy as np
        states_list =  list(get_WR_data(what=None).state.unique())
        #print(type(states_list))
        #print(states_list.sort())
        states_list.sort()
        ab = ['All']
        ab.extend(states_list)
        state = c2.selectbox("Choose a Specific State",ab )
        data = ""
        if r_type == 'All':
            st.subheader("Both TDWR and NEXRAD")
            if state == 'All':
                data = get_WR_data(what=None,state=state)
                print("Data size is {}".format(len(data)))
                st.map(data)
            else:
                print("State is {}".format(state))
                data = get_WR_data(what=None,state=state)
                st.map(data)
        elif r_type == 'TDWR':
            data = get_WR_data(what='TDWR',state=state)
            st.subheader("TDWR -- Terminal Doppler Weather Radar")
            if len(data) == 0:
                c2.markdown(
                    """
                    **No Data Available**
                    """)
            st.map(data)
        elif r_type == 'NEXRAD':
            st.subheader("NEXRAD -- Next Generation Radar Sites")
            data = get_WR_data(what='NEXRAD',state=state)
            if len(data) == 0:
                c2.markdown(
                    """
                    **No Data Available**
                    """)
            st.map(data)
        st.dataframe(data)
        
    except URLError as e:
        st.error(
            """
            **Something went wrong**

            Connection error: %s
        """
            % e.reason
        )

elif page == 'Global Temperature Averages since 1849':

    @st.cache_data(show_spinner=True)
    def get_gltm_data(what=None,country='All'):

        df = pd.read_csv('data/globallandtemperaturesbymajorcity-ymd.csv')
        if country=='All':
            print("Returning Country == All")
            return df.groupby('country', group_keys=False).apply(lambda x: x.sample(400))
        else:
            print("Returning country = {}".format(country))
            return df[df.country==country]



    #TODO --make a special dataframefor this
    def plot_temp(df):
        import plotly.graph_objects as go
        import numpy as np
        coefficients = np.polyfit(df.year.to_numpy(),np.array(df.averagetemperature.mean()),1)
        trendline = np.polyval(coefficients,df.year.to_numpy())
        sc_plot = go.Scatter(x=df.year, y=df.averagetemperature.mean() ,mode='markers',
                                 name='Global Temperatures')
        trend_plot = go.Scatter(x=df.year, y=trendline ,mode='lines',
                                 name='Trendline')
        fig = go.Figure(data=[sc_plot,trend_plot])
        fig.update_layout(title='Global Temperatures Trends',
                        xaxis_title='Year',
                        yaxis_title='Temp in Degress C')

        return fig

    def plot_heatmap(df):
        import plotly.express as px
        w31 = df.groupby(['country','year'])['averagetemperature'].mean().reset_index(name='avg_yrly_temp')
        w32 = w31.pivot(index='country', columns='year')['avg_yrly_temp'].fillna(0)

        fig = px.imshow(w32, x=w32.columns, y=w32.index)
        fig.update_layout(width=800,height=700)
        return fig        

    try:
        c1.header("Global Tempertures by Country since 1750")
        c1.markdown("""
        This data [Climate Change: Earth Surface Temperature Data](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data)
        Compiling global temperature readings  since 1750.

        Collection techniques have improved since 1750 and there is greater and more robust collection.
        Note that not all countries have data dating back to 1750.

        """
        )
        country_list =  list(get_gltm_data(what=None).country.unique())
        country_list.sort()
        ab = ['All']
        ab.extend(country_list)
        country = c2.selectbox("Choose a Specific Country",ab )

        data = get_gltm_data(what=None,country=country)

        c1.map(data)
        c1.dataframe(data)
        fig = plot_temp(data)
        c2.plotly_chart(fig)
        if country=='All':
            fig2 = plot_heatmap(data)
            c2.plotly_chart(fig2)

    except URLError as e:
        st.error(
            """
            **Something went wrong**

            Connection error: %s
        """
            % e.reason
        )
