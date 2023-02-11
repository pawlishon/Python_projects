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

# Django recipies app
The app is a browser of recipies I have stored on my external server in MySQL Database. It allows user to browse recipies by title and/or category and redirects to recipe page. Page content is in Polish. 
I run this app as well as the database and Ubuntu machine and deploy using MySQL server together with Apache server for the app.
If you want to see how does it work just let me know and I'll set it up.

# Yoga bot
From time to time I attend yoga classes. There are a lot of people willing to participate and the number of attendees is limited.
There is the website app set up by provider in order to keep track of people signing up for classes. In that system you can choose the class you want to attend exactly 1 week before it starts (to single second). Most interesting classes are being filled within 3 min from the start. It's very hard to sign up if you are not paying attention a week before a start.
That's why I invented this script. After initialization it opens selenium driver which navigates through browser and signs up to all classes provided in input file. In order to work you need also to provide your credentials. The input reservations.txt file should have a line for every class a person wants to attend. Example line below:
email@gmail.com,password,2022-12-19,SALA 2,VINJASA 0,20:00
(webpage is in Polish)
There can be multiple classes or users in input file.
The script should be initialized at specific time. To do that I create a .bat file which opens python and this script. The bat file is initialized by Window Task Scheduler.

# NBA match checker
I'm a big NBA fan and I watch a lot of games. Not all matches are good. I try not to check the results before watching any match, which was causing me to watch a lot of bad games, since I was choosing them at random. That's why I decided to create a program which will help me choose the most interesting game without giving me result explicitly.
The tool goes to NBA webpage and scrapps the results together with leaderboard. Then it assigns points to every match for things that I like watching the game (close match, two teams that have similar records, big statlines for the leader, overtimes and so on). At the end the result file is produced with the teams and the match score. The bigger, the better the match is.

The script is also available on Google Colab under:
https://colab.research.google.com/drive/1mqOj9nRETdq9bFkmoUzpJOBoxHmPXWjI?usp=sharing

# Unrelated scripts
Scripts mostly with machine learning projects, which I wrote learning these techniques. Except that there is also one bot program and some scripts I used for my stock data database. One scripts tests as well CAPM model (Capital Asset Pricing Model) and whether it is true that expected payoff from the stock investment is linearly dependent on the risk taken. 


