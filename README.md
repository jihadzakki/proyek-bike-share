# Bike-Share Dashboard and Analysis 🚲📊

## Overview of the Project
This project aims to perform data analysis on the bike-share dataset. The analysis is conducted using Python with various libraries, and the output is displayed on the web using Streamlit.

## Overview of the Dataset
Bike rental data is highly correlated with environmental and seasonal conditions. For example, weather conditions, precipitation, day of the week, season, time of day, etc., can affect rental behavior. The core dataset is related to two years' historical records corresponding to the years 2011 and 2012 from the Capital Bikeshare system, Washington D.C., USA, which is publicly available at http://capitalbikeshare.com/system-data. We aggregated the data on two-hourly and daily bases, then extracted and added corresponding weather and seasonal information. Weather information is extracted from http://www.freemeteo.com.

## Overview of the Repository Directory
- /dashboard: Contains main files displayed for the dashboard
- /data: Stores datasets used for analysis (Bike Sharing Dataset)
- notebook.ipynb: Jupyter notebook file containing the data analysis conducted
- README.md: Information file about this project
- requirements.txt: File containing the libraries used in this project

## Analysis Conducted
In conducting the data analysis related to the bike-share above, several business questions are needed to meet the company's needs. Here are some SMART business questions:

1. How is the performance of the bike ridership over the past two years?
2. At what time of day are the most and least bike riders?
3. In which season are the most and least bike riders?
4. How much does weather condition influence bike ridership?
5. What is the comparison of bike ridership between casual and registered users?

To see the analysis results starting from Data Wrangling, Exploratory Data Analysis (EDA), to Visualization & Explanatory Analysis, you can directly go to notebook.ipynb.

## Access the Bike-Share Web Dashboard
Online access can be found via the following link: [Bike-Share Dashboard](https://bike-share-jihadzakki.streamlit.app/)

## Access Local Bike-Share Dashboard and This Project
To run the dashboard locally, run the following command in the terminal:
'''
streamlit run dashboard.py
'''

## Screenshot Dashboard
![image](https://github.com/jihadzakki/proyek-bike-share/assets/109097390/1fbc6642-25a7-4479-91a0-0c12cc3159ae)
![image](https://github.com/jihadzakki/proyek-bike-share/assets/109097390/5777cc80-2656-41d3-b5d9-1fbd731c04fe)
![image](https://github.com/jihadzakki/proyek-bike-share/assets/109097390/38354b2d-2630-4e43-b37e-41779f8b567c)
![image](https://github.com/jihadzakki/proyek-bike-share/assets/109097390/fdad128d-6b49-4814-9aae-7d8b08db752f)
