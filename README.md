# Python_projects

The repo contains mostly a stock evaluation tool in 2 versions (Desktop and web app) together with some Machine Learning projects for data I found on Kaggle. 

# Yfinanace SET (Stock Evaluation Tool)

The  stock evaluation tool is getting its data from Yahoo finance. I created several tools for processing these informations to get the view of the companies conditions in order to identify companies with durable competitive advantage.

First feature is called stock evaluation and its purpose is just to get the glimpse of the most common financial ratios and to display them in one coherent table. The difference between the original Yahoo finance wepage and my app is that you can export multiple companies of your choice at once or even upload the identifiers from the file. The results are also exportable.

The second option is to take a look at companies dividends. Since I tend to invest in value companies I find it extremely important for companies to have long lasting trend of distributing some money back to their shareholders. With this tool you can not only check dividends for last years, but also display them on a chart.

The third option is a price prediction model. It uses the timeseries forecasting to predict next close prices. I used the approach that the user is providing the data on which the model is trained on and the tool predicts next 10% of the length of provided period. The model used for this feature is ARIMA where parameters are determined by a grid search.

The fourth feature is the financial statement comparison. The script is downloading financial statements for up to two companies in order to compare them. There are also few ratios derived from the original data. Next, there is possibility to plot any position in financial statement or even ratio for any ticker or both tickers simultanously.

# Desktop app

It is created in PyQT library. Intended for personal use for large amount of data. The app can be exported to exe file using pyinstaller.

# Web app.

Created in flask. If you'd like to see how it looks like, please contact me on paw.piatkowski7@gmail.com and I will set up a server for the app to work on. Due to a limited resources the app is not intended for processing large amount of data, hence the possibility of downloading desktop app is there included. 


