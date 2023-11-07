import pandas as pd


SP500 = pd.read_csv(r'Option price modelling/SP500.csv')
SP500['daily_return'] = (SP500['close']/ SP500['close'].shift(1)) -1

SP500.dropna(inplace = True)

SP_mean = SP500['daily_return'].mean()
SP_std = SP500['daily_return'].std()

# How many records have return further than 10 std dev
std10 = SP_std * 10
bad_days_10 = SP500.loc[SP500['daily_return'] < SP_mean - std10]
empirical_prob_10 = len(bad_days_10) / len(SP500)

import scipy
theoretical_prob_10 = scipy.stats.norm.cdf(-10)

# How many records have return further than 1 std dev
bad_days_1 = SP500.loc[SP500['daily_return'] < SP_mean - SP_std]
empirical_prob_1 = len(bad_days_1) / len(SP500)
theoretical_prob_1 = scipy.stats.norm.cdf(-1)

result_df = pd.DataFrame(columns=['Std_dev_multiplier', 'Empirical prob', 'Theoretical prob'])
for i in range(1, 11):
    std_x = SP_std * i
    bad_days_x = SP500.loc[SP500['daily_return'] < SP_mean - std_x]
    empirical_prob_x = len(bad_days_x) / len(SP500)
    theoretical_prob_x = scipy.stats.norm.cdf(-i)
    result_df.loc[len(result_df)] = [i, empirical_prob_x, theoretical_prob_x]

# Does not look like a normal distribution
shap = scipy.stats.shapiro(SP500['daily_return'].sample(4000))
print(shap.statistic)
print(shap.pvalue)
# Not gaussian
