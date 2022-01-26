from datetime import datetime
from flask import Flask, render_template, session, request, send_file, redirect, url_for, flash
import os
from datetime import date
from model.evaluation import *
from werkzeug.utils import secure_filename
import csv
import matplotlib.pyplot as plt
import model.Stock_price_prediction as spp
from model.financial_statements import *

app = Flask(__name__)
app.secret_key = 'h432hi5olkj3h5i5hi3o2hi'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/Home.html')
def home_alternative():
    return render_template('home.html')


@app.route('/About.html')
def about():
    return render_template('About.html')


@app.route('/Contact.html')
def contact():
    session.clear()
    return render_template('Contact.html')


@app.route('/Financial-Statements.html')
def financial_statements():
    if 'image_report' in session.keys():
        plt_image = session['image_report']
    else:
        plt_image = 'images/default-logo.png'
    if 'fs1' not in session.keys() and 'fs2' not in session.keys():
        return render_template('Financial-Statements.html', plt_reports = plt_image, ticker1='First Company', ticker2='Second Company')
    elif 'fs1' in session.keys() and 'fs2' not in session.keys():
        table1 = pd.read_json(session['fs1'])
        ratios1 = pd.read_json(session['ratios_1'])
        return render_template('Financial-Statements.html', table1=table1.to_html(header=True, index=False).replace('dataframe', 'table-style'), plt_reports = plt_image, ticker1=session['report_ticker_1'], ticker2='Second Company', ratios1=ratios1.to_html(header=True, index=False).replace('dataframe', 'table-style'))
    elif 'fs1' not in session.keys() and 'fs2' in session.keys():
        table2 = pd.read_json(session['fs2'])
        ratios2 = pd.read_json(session['ratios_2'])
        return render_template('Financial-Statements.html', table2=table2.to_html(header=True, index=False).replace('dataframe', 'table-style'), plt_reports = plt_image, ticker1='First Company', ticker2=session['report_ticker_2'], ratios2=ratios2.to_html(header=True, index=False).replace('dataframe', 'table-style'))
    else:
        table1 = pd.read_json(session['fs1'])
        table2 = pd.read_json(session['fs2'])
        ratios1 = pd.read_json(session['ratios_1'])
        ratios2 = pd.read_json(session['ratios_2'])
        return render_template('Financial-Statements.html', table1=table1.to_html(header=True, index=False).replace('dataframe', 'table-style'), table2=table2.to_html(header=True, index=False).replace('dataframe', 'table-style'), plt_reports = plt_image, ticker1=session['report_ticker_1'], ticker2=session['report_ticker_2'], ratios1=ratios1.to_html(header=True, index=False).replace('dataframe', 'table-style'), ratios2=ratios2.to_html(header=True, index=False).replace('dataframe', 'table-style'))


@app.route('/Price-History.html')
def price_history():
    return render_template('Price-History.html', plt='images/default-logo.png')


@app.route('/Download.html')
def download():
    return render_template('Download.html')


@app.route('/Dividends-History.html')
def div_history():
    return render_template('Dividends-History.html', plt='images/default-logo.png')


@app.route('/download_desktop_app')
def download_desktop_app():
    path = os.getcwd() + "/static/stock_eval_app.exe"
    return send_file(path, as_attachment=True)


@app.route('/Stock-Evaluation.html', methods = ['GET', 'POST'])
def stock_evaluation():
    if 'tickers' not in session.keys():
        session['tickers'] = {}
    if 'result' not in session.keys():
        return render_template('Stock-Evaluation.html', tickers = session['tickers'].keys())
    else:
        df = pd.read_json(session['result'])
        return render_template('Stock-Evaluation.html', tickers=session['tickers'].keys(),
                              result_table=df.to_html(classes='data', header=True, index=False))


@app.route('/get_ticker', methods=['POST'])
def get_ticker():
    session['tickers'][request.form['name']] = True
    session['Is On'] = True
    return redirect(url_for('stock_evaluation'))


@app.route('/ticker_list', methods=['POST'])
def ticker_list():
    if request.form.get('Remove last') == 'Remove last':
        if len(list(session['tickers'].keys()))>0:
            session['tickers'].pop(list(session['tickers'].keys())[-1])
            session['Is On'] = True
            return redirect(url_for('stock_evaluation'))
        else:
            return redirect(url_for('stock_evaluation'))

    elif request.form.get('Clear list') == 'Clear list':
        session['tickers'].clear()
        session['Is On'] = True
        return redirect(url_for('stock_evaluation'))
    elif request.form.get('Import Dow') == 'Import Dow':
        dow = si.tickers_dow()
        for element in dow:
            session['tickers'][element] = True
            session['Is On'] = True
        return redirect(url_for('stock_evaluation'))
    elif request.form.get('Import SP500') == 'Import SP500':
        sp500 = si.tickers_sp500()
        for element in sp500:
            session['tickers'][element] = True
            session['Is On'] = True
        return redirect(url_for('stock_evaluation'))


@app.route('/evaluate', methods=['POST'])
def evaluate():
    instrument_list = [item for item in session['tickers'].keys() if item!='result']
    results = ResultJoin(instrument_list)
    results = results.drop(['Company Summary'], axis=1)
    results.reset_index(drop=True, inplace=True)
    session['result'] = results.to_json()
    return redirect(url_for('stock_evaluation'))


@app.route('/export_to_excel', methods=['POST'])
def export_to_excel():
    df = pd.read_json(session['result'])
    path = os.getcwd() + "/static/results_" + str(date.today()) + '.xlsx'
    df.to_excel(path, index=False)
    return send_file(path, as_attachment=True)


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method=='POST':
        session['Is On'] = True
        f = request.files['file']
        full_name = 'tickers' + secure_filename(f.filename)
        f.save(os.getcwd() + '/static/user_files/' + full_name)
        with open(os.getcwd() + '/static/user_files/' + full_name, newline='') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                session['tickers'][row[0]]=True
        return redirect(url_for('stock_evaluation'))


@app.route('/dividends', methods=['GET','POST'])
def dividends():
    if request.method == 'POST':
        try:
            if 'plot_' + str(date.today()) + '.png' in os.listdir('static/images'):
                os.remove(os.getcwd()+'\\static\\images\\'+'plot_' + str(date.today()) + '.png')
            ticker = request.form['ticker']
            start_date = request.form['date']
            start_date = start_date[-2:] + start_date[4:8] + start_date[:4]
            start_date_as_date = datetime.strptime(start_date, '%d-%m-%Y')
            if start_date_as_date > datetime.now():
                flash('Date from the future. Please pick another!')
                return redirect(url_for('div_history'))
            else:
                data = si.get_dividends(ticker, start_date)
                data = data.reset_index()
                data.columns = ['Date', 'Amount USD', 'Ticker']
                plt.figure()
                plt.plot(data['Date'], data['Amount USD'])
                path = os.getcwd()+'\static\images\plot_' + str(date.today()) + '.png'
                plt.savefig(path)
                plt.clf()
                return render_template('Dividends-History.html', table=data.to_html(classes='data', header=True, index=False), plt = 'images/plot_' + str(date.today()) + '.png')
        except ValueError:
            flash('Invalid ticker!')
            return redirect(url_for('div_history'))
    else:
        return redirect(url_for('div_history'))


@app.route('/prices', methods=['GET', 'POST'])
def prices():
    if request.method=='POST':
        ticker = request.form.get('ticker')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        option = request.form.get('menu')
        if option==0:
            option = '1d'
        elif option==1:
            option = '1mo'
        else:
            option = '1wk'
        start_date = start_date[5:7] + '/' + start_date[-2:] + '/' +start_date[:4]
        end_date = end_date[5:7] + '/' + end_date[-2:] + '/' + end_date[:4]
        price = si.get_data(ticker, start_date=start_date, end_date=end_date, index_as_date=False, interval=option)
        session['prices'] =price.to_json()
        session['option'] = option
        if 'plot_' + str(date.today()) + '.png' in os.listdir('static/images'):
            os.remove(os.getcwd() + '\\static\\images\\' + 'plot_prices' + str(date.today()) + '.png')
        plt.figure()
        plt.plot(price['date'], price['close'])
        path = os.getcwd() + '\static\images\plot_prices' + str(date.today()) + '.png'
        plt.savefig(path)
        plt.clf()
        return render_template('Price-History.html', plt='images/plot_prices' + str(date.today()) + '.png')
    else:
        return redirect(url_for(price_history))


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method=='POST':
        prices = pd.read_json(session['prices'])
        #prices['date'] = prices.index
        #prices.reset_index(drop=True, inplace=True)
        futures = spp.PreditctPrices(prices, session['option'])
        session['futures'] = futures
        if 'plot_prices' + str(date.today()) + '.png' in os.listdir('static/images'):
            os.remove(os.getcwd() + '\\static\\images\\' + 'plot_prices' + str(date.today()) + '.png')
        plt.figure()
        plt.plot(prices['date'], prices['close'], color='blue', label='Actual Price')
        plt.plot(futures[0], futures[1], color='red', label='Future Price')
        plt.title('Prices Chart')
        plt.legend()
        path = os.getcwd() + '\static\images\plot_prices_pred' + str(date.today()) + '.png'
        plt.savefig(path)
        plt.clf()
        return render_template('Price-History.html', plt='images/plot_prices_pred' + str(date.today()) + '.png')
    else:
        return redirect(url_for('price_history'))


@app.route('/report_comp_1', methods=['GET', 'POST'])
def report_comp_1():
    if request.method=='POST':
        try:
            ticker = request.form.get('ticker1')
            session['report_ticker_1'] = ticker
            table, ratios = get_financial_statements(ticker)
            session['fs1'] = table.to_json()
            session['ratios_1'] = ratios.to_json()
            return redirect(url_for('financial_statements'))
        except TypeError:
            flash('Unable to download data. Possible invalid ticker!')
            return redirect(url_for('financial_statements'))


@app.route('/report_comp_2', methods=['GET', 'POST'])
def report_comp_2():
    if request.method == 'POST':
        try:
            ticker = request.form.get('ticker2')
            session['report_ticker_2'] = ticker
            table,ratios = get_financial_statements(ticker)
            session['fs2'] = table.to_json()
            session['ratios_2'] = ratios.to_json()
            return redirect(url_for('financial_statements'))
        except TypeError:
            flash('Unable to download data. Possible invalid ticker!')
            return redirect(url_for('financial_statements'))


@app.route('/plot_reports', methods=['GET', 'POST'])
def plot_reports():
    if request.method == 'POST':
        if 'plot_reports' + str(date.today()) + '.png' in os.listdir('static/images'):
            os.remove(os.getcwd() + '\\static\\images\\' + 'plot_reports' + str(date.today()) + '.png')
        option_dict = {'0':"researchDevelopment", '1':"incomeBeforeTax", '2':"netIncome", '3':"sellingGeneralAdministrative", '4':"grossProfit", '5':"operatingIncome", '6':"interestExpense", '7':"totalRevenue", '8':"costOfRevenue", '9':"grossProfitMargin", '10':"taxPaid", '11':"netRatio", '12':"totalLiab", '13':"totalStockholderEquity", '14':"totalAssets", '15':"commonStock", '16':"otherCurrentAssets", '17':"retainedEarnings", '18':"treasuryStock", '19':"cash", '20':"totalCurrentLiabilities", '21':"shortLongTermDebt", '22':"propertyPlantEquipment", '23':"totalCurrentAssets", '24':"netTangibleAssets", '25':"shortTermInvestments", '26':"netReceivables", '27':"longTermDebt", '28':"inventory", '29':"currentRatio", '30':"debtToESRatio", '31':"longOverShortDebt", '32':"depreciation", '33':"capitalExpenditures", '34':"returnOnShareholdersEquity"}
        option = option_dict[request.form.get('features_menu')]
        ticker_option = request.form.get('ticker_menu')
        plt.figure()
        if ticker_option == '1':
            report1 = pd.read_json(session['fs1'])
            ratios1 = pd.read_json(session['ratios_1'])
            report1 = pd.concat([report1, ratios1])
            x = report1.columns.to_list()[1:]
            y = report1.loc[report1['Breakdown']==option].values.tolist()[0][1:]
            plt.plot(list(reversed(x)), list(reversed(y)), color='blue', label=session['report_ticker_1'])
        elif ticker_option == '2':
            report2 = pd.read_json(session['fs2'])
            ratios2 = pd.read_json(session['ratios_2'])
            report2 = pd.concat([report2, ratios2])
            x = report2.columns.to_list()[1:]
            y = report2.loc[report2['Breakdown']==option].values.tolist()[0][1:]
            plt.plot(list(reversed(x)), list(reversed(y)), color='blue', label=session['report_ticker_2'])
        else:
            report1 = pd.read_json(session['fs1'])
            ratios1 = pd.read_json(session['ratios_1'])
            report1 = pd.concat([report1, ratios1])
            report2 = pd.read_json(session['fs2'])
            ratios2 = pd.read_json(session['ratios_2'])
            report2 = pd.concat([report2, ratios2])
            x = report2.columns.to_list()[1:]
            y1 = report1.loc[report1['Breakdown']==option].values.tolist()[0][1:]
            y2 = report2.loc[report2['Breakdown'] == option].values.tolist()[0][1:]
            plt.plot(list(reversed(x)), list(reversed(y1)), color='blue', label=session['report_ticker_1'])
            plt.plot(list(reversed(x)), list(reversed(y2)), color='red', label=session['report_ticker_2'])
        plt.title('Report Chart')
        plt.legend()
        plt.xlabel('Date')
        plt.ylabel(option)
        path = os.getcwd() + '\static\images\plot_reports' + str(date.today()) + '.png'
        plt.savefig(path)
        plt.clf()
        session['image_report'] = 'images/plot_reports' + str(date.today()) + '.png'
        return redirect(url_for('financial_statements'))


