# EN.605.662 Data Visualization project 4

[Weather-Related Visualizations using Streamlit -Deployed at Streamlit.io](https://dataviz-tzfwuid99wcrhmxdqdawik.streamlit.app/)

Author: Anthony Sheller

## Overview
A Streamlit application  that processes three data sets [1,2,3], and presents three types of visualizations.  
1. Mapping using Streamlit of the World and Unitied States. Selection of Countries or U.S. states enables the map and data to zoom into that location.
2. Scatterplot with Trend lines.  This also *zooms* with the data when a Country or State is Selected.
3. Haeatmaps for Global and specific Countries. The global heatmap illustrates a *by-country* display. While the Country selection illustrates a *by-month* display.

### This folder contains:
1. `data` folder with adjusted CSV files used for the project. Note that datasets larger than 100MB are not able to be stored in GitHub so the data was preprocessed with the provides Jupyter Lab notebooks.
2. `images` folder uses to store images for the landing page of the Streamlit Application.
3. `.gitignore` to tell git not to check certain file and folder types into GitHub.
4. `*.ipnb` three Jupiter Lab notebooks used for preprocessing and analyzing the data.  These are not the assignment but supprot the assignment. [WeatherOutliersReview.ipynb,WeatherRadar.ipynb,GlobalTemps]
5. `main.py` This is the Stramlit application used to deploy the application at DataViz at
6. `requirements.txt` This is the list of Python modules necesasry for the application to operate. This is checked into GitHub. Streamlit hosting service will read this to install the necesary modules for the application.

## References:
1. Lewis, Carl. “U.S. Weather Outliers, 1964- - Dataset by Carlvlewis.” Data.World, 25 Apr. 2017, data.world/carlvlewis/u-s-weather-outliers-1964.
2. Homeland Infrastructure Foundation. “Weather Radar Stations - Dataset by DHS.” Data.World, 18 Aug. 2016, data.world/dhs/weather-radar-stations.
3. Earth, Berkeley. “Climate Change: Earth Surface Temperature Data.” Kaggle, 1 May 2017, www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data.