class DCCF {
    constructor(
        operating_income_after_tax,
        net_capital_expenditures,
        change_in_working_capital,
        return_on_capital,
        risk_free_rate,
        beta,
        erp,
        default_spread,
        marginal_tax_rate,
        market_value,
        debt,
        number_of_years,
        cash,
        management_options,
        number_of_shares,

    ) {
        this.operating_income_after_tax = operating_income_after_tax;
        this.net_capital_expenditures = net_capital_expenditures;
        this.change_in_working_capital = change_in_working_capital;
        this.return_on_capital = return_on_capital;
        this.risk_free_rate = risk_free_rate;
        this.beta = beta;
        this.erp = erp;
        this.default_spread = default_spread;
        this.marginal_tax_rate = marginal_tax_rate;
        this.market_value = market_value;
        this.debt = debt;
        this.number_of_years = number_of_years;
        this.cash = cash;
        this.management_options = management_options;
        this.future_growth = 0;
        this.future_cost_of_capital = 0;
        this.number_of_shares = number_of_shares;
        this.results = {
            fcff: 0,
            reinvestment_rate: 0,
            growth: 0,
            cost_of_equity: 0,
            cost_of_debt: 0,
            cost_of_capital: 0,
            terminal_value: 0,
            reinvestment_rate_stable_growth: 0,
            operating_assets_value: 0,
            equity_value: 0,
            value_per_share: 0
        }
    }
    calculateCostOfCapital() {
        // Results
        this.results.fcff = this.operating_income_after_tax - this.net_capital_expenditures - this.change_in_working_capital;
        this.results.reinvestment_rate = (this.net_capital_expenditures + this.change_in_working_capital) / this.operating_income_after_tax;
        this.results.growth = this.results.reinvestment_rate * this.return_on_capital;
        this.results.cost_of_equity = this.risk_free_rate + this.beta * this.erp;
        this.results.cost_of_debt = (this.risk_free_rate + this.default_spread) * (1 - this.marginal_tax_rate);
        this.results.cost_of_capital = this.results.cost_of_equity * this.market_value / (this.debt + this.market_value) + this.results.cost_of_debt * this.debt / (this.debt + this.market_value);
    }
    setFutureGrowthCostOfCapital(future_growth, future_cost_of_capital) {
        this.future_growth = future_growth;
        this.future_cost_of_capital = future_cost_of_capital;
    }
    calculateStockPrice() {
        this.results.operating_assets_value = 0;
        this.results.reinvestment_rate_stable_growth = this.future_growth / this.future_cost_of_capital;
        this.results.terminal_value = this.operating_income_after_tax * (1 + this.results.growth) ** (this.number_of_years) * (1 + this.future_growth) * (1 - this.results.reinvestment_rate_stable_growth) / (this.future_cost_of_capital - this.future_growth);
        for (let year = 0; year < this.number_of_years; year++) {
            if (year + 1 != this.number_of_years) {
                this.results.operating_assets_value = this.results.operating_assets_value + this.operating_income_after_tax * (1 + this.results.growth) ** (year + 1) * (1 - this.results.reinvestment_rate) / ((1 + this.results.cost_of_capital) ** (year + 1));
            }
            else {
                this.results.operating_assets_value = this.results.operating_assets_value + (this.operating_income_after_tax * (1 + this.results.growth) ** (year + 1) * (1 - this.results.reinvestment_rate) + this.results.terminal_value) / ((1 + this.results.cost_of_capital) ** (year + 1));
            }
        }
        this.results.equity_value = this.results.operating_assets_value + this.cash - this.debt - this.management_options
        this.results.value_per_share = this.results.equity_value / this.number_of_shares
    }
}

export default DCCF;



