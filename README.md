# Market-efficiency-test
The code analyzes the market efficiency and stationarity of a list of 90 stocks. It first defines two functions:

marketEfficency_df calculates the market efficiency of a given stock ticker by performing the following steps:
Creating a pandas DataFrame with Open, High, Low, Close, Adj Close, and Volume columns.
Calculating the daily percentage change, mean, and sigma.
Generating a simulation of the probable price path using a random walk simulation.
Computing the F-value and p-value of the ANOVA test on the simulation data to determine market efficiency.
Returning the p-value of the ANOVA test.

dickyfullermethod tests for stationarity of a given stock ticker by performing the following steps:
Creating a pandas DataFrame with the Adj Close column.
Replacing infinity and NaN values with 0.
Computing the log of the Adj Close column.
Running the Augmented Dickey-Fuller (ADF) test to check for stationarity of the stock.
Printing out the ADF statistic, p-value, and critical values.
Returning the ADF statistic.

After defining the two functions, the code reads a CSV file that contains a list of 90 stock tickers. It then loops over each ticker in the list and calls the marketEfficency_df function to calculate its market efficiency. The code prints out the F-value, p-value, and ticker symbol for each stock.

Next, the code loops over each ticker in the list again and calls the dickyfullermethod function to test for stationarity using the ADF test. The code prints out the ADF statistic, p-value, and ticker symbol for each stock.

Finally, the code creates a pandas DataFrame Dickyfullerresults to store the ADF statistic for each stock. However, this part of the code is commented out so the DataFrame is not actually created.

Overall, the code provides an analysis of the market efficiency and stationarity of a list of 90 stocks, which can be useful for investment and trading strategies.
