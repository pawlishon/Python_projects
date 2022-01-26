import matplotlib.pyplot as plt
from datetime import date
import os

data = si.get_dividends(ticker, start_date)
data = data.reset_index()
data.columns = ['Date', 'Amount USD', 'Ticker']

fig = plt.figure()
plt.plot(data['Date'], data['Amount USD'])
plt.show()
plt.savefig('/static/images/plot_'+str(date.today())+'.png')

os.listdir(r'C:\Users\6112272\PycharmProjects\url-shortener\static\images')
os.remove('C:\Users\\6112272\PycharmProjects\url-shortener\static\images\\'+'plot_2022-01-07.png')