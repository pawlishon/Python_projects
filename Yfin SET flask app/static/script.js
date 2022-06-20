import DCCF from "./DCCF.js";

const main = document.querySelector("main")
const new_article = document.createElement("article")

main.append(new_article)

function create_new_DCCF(evt) {
    evt.preventDefault();
    let operating_income_after_tax = parseFloat(document.getElementById("operating_income_after_tax").value);
    let net_capital_expenditures = parseFloat(document.getElementById("net_capital_expenditures").value);
    let change_in_working_capital = parseFloat(document.getElementById("change_in_working_capital").value);
    let return_on_capital = parseFloat(document.getElementById("return_on_capital").value);
    let risk_free_rate = parseFloat(document.getElementById("risk_free_rate").value);
    let beta = parseFloat(document.getElementById("beta").value);
    let erp = parseFloat(document.getElementById("erp").value);
    let default_spread = parseFloat(document.getElementById("default_spread").value);
    let marginal_tax_rate = parseFloat(document.getElementById("marginal_tax_rate").value);
    let market_value = parseFloat(document.getElementById("market_value").value);
    let debt = parseFloat(document.getElementById("debt").value);
    let number_of_years = parseFloat(document.getElementById("number_of_years").value);
    let cash = parseFloat(document.getElementById("cash").value);
    let management_options = parseFloat(document.getElementById("management_options").value);
    let number_of_shares = parseFloat(document.getElementById("number_of_shares").value);
    current_DCCF = new DCCF(operating_income_after_tax, net_capital_expenditures, change_in_working_capital, return_on_capital,
        risk_free_rate, beta, erp, default_spread, marginal_tax_rate, market_value, debt, number_of_years, cash, management_options, number_of_shares)
    current_DCCF.calculateCostOfCapital()
    console.log('After input data:')
    console.log(current_DCCF)
    create_results()
    if (document.getElementsByClassName('future-form').length == 0) {
        create_future_form()
    }
}

function create_results() {
    var resultDict = {
        'FCFF': current_DCCF.results.fcff, 'Reinvestment Rate': current_DCCF.results.reinvestment_rate, 'Growth': current_DCCF.results.growth,
        'Cost of equity': current_DCCF.results.cost_of_capital, 'Cost of debt': current_DCCF.results.cost_of_debt, 'Cost of capital': current_DCCF.results.cost_of_capital
    };
    let result_id = 0
    if (document.getElementById('0') == null) {
        let ResultDiv = document.createElement('div');
        ResultDiv.setAttribute('id', 'prel-results')

        for (var key in resultDict) {
            let paragraph = document.createElement("p");
            paragraph.setAttribute('id', result_id)
            result_id = result_id + 1
            paragraph.innerHTML = `${key}: <span>${resultDict[key]}</span>`
            ResultDiv.append(paragraph)
        }
        let paragraph = document.createElement("p");
        paragraph.innerHTML = `Using preliminary results from above please try to estimate company growth and cost of capital in next ${current_DCCF.number_of_years} years:`
        ResultDiv.append(paragraph)
        new_article.append(ResultDiv)
    }
    else {
        for (var key in resultDict) {
            document.getElementById(result_id).querySelector("span").innerHTML = resultDict[key];
            result_id = result_id + 1;
        }
    }
}

function create_future_form() {
    var future_form = document.createElement("form")
    future_form.classList.add('future-form')
    future_form.innerHTML = '<label for="future_growth">Future Growth:</label><br><input type="number", id="future_growth", name="future_growth" step="0.01" style= "color:black"><br>' +
        '<label for="future_cost_of_capital">Future Cost Of Capital:</label><br><input type="number", id="future_cost_of_capital", name="future_cost_of_capital" step="0.01" style= "color:black" required><br>' +
        '<br><input type="submit" value="Calculate Stock Price" id="submit_future" style= "color:black">'
    new_article.append(future_form)
    future_form.addEventListener('submit', valuate)
}


function valuate(evt1) {
    evt1.preventDefault();
    let future_growth = parseFloat(document.getElementById("future_growth").value);
    let future_cost_of_capital = parseFloat(document.getElementById("future_cost_of_capital").value);
    current_DCCF.setFutureGrowthCostOfCapital(future_growth, future_cost_of_capital)
    current_DCCF.calculateStockPrice()
    if (document.getElementById('result') == null) {
        let paragraph = document.createElement("p")
        paragraph.setAttribute('id', 'result')
        paragraph.innerHTML = `Stock price from valuation: <span>${current_DCCF.results.value_per_share}</span>`
        new_article.append(paragraph)
    }
    else {
        document.getElementById('result').querySelector('span').innerHTML = current_DCCF.results.value_per_share
    }
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

var current_DCCF = new DCCF(7112400, -2072500, 3066500, 0.1442, 0.0284, 0.61, 0.055, 0.0159, 0.4, 180770000, 49349100, 5, 4709200, 0, 748000)

var input_form = document.createElement("form")
var feature_array = Object.keys(current_DCCF)
feature_array = feature_array.filter(e => !["results", "future_growth", "future_cost_of_capital"].includes(e))
console.log(feature_array)

feature_array.forEach(function (item) {
    if (item != 'results') {
        input_form.innerHTML = input_form.innerHTML + `<label for="${item}">${capitalizeFirstLetter(item.replaceAll('_', ' '))}:</label><br><input type="number", id="${item}", name="${item}" step="0.0001" style= "color:black" required><br>`
    }
})
input_form.innerHTML = input_form.innerHTML + '<br><input type="submit" value="Submit" id="submit" style= "color:black">'
new_article.append(input_form)

const form = document.querySelector('form')

FillOutMCDData()
form.addEventListener('submit', create_new_DCCF)

function FillOutMCDData() {
    document.getElementById("operating_income_after_tax").value = 7112400;
    document.getElementById("net_capital_expenditures").value = -2072500;
    document.getElementById("change_in_working_capital").value = 3066500;
    document.getElementById("return_on_capital").value = 0.1442;
    document.getElementById("risk_free_rate").value = 0.0284;
    document.getElementById("beta").value = 0.61;
    document.getElementById("erp").value = 0.055;
    document.getElementById("default_spread").value = 0.0159;
    document.getElementById("marginal_tax_rate").value = 0.4;
    document.getElementById("market_value").value = 180770000;
    document.getElementById("debt").value = 49349100;
    document.getElementById("number_of_years").value = 5;
    document.getElementById("cash").value = 4709200;
    document.getElementById("management_options").value = 0;
    document.getElementById("number_of_shares").value = 748000;
}

