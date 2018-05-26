# financial_stock_modeling
financial stock modeling tool

Abstract

The current project is a computer programme, written in Python 3, that allows its end user to
retrieve, analyse and model stock times-series data. This report is the user’s guide for the specific
programme and its main aim is to present the programme’s features in a short but detailed manner.

Introduction

This programme combines a series of processes that target to facilitate the end user to extract
useful insights from stock market data. The entire process was designed and implemented in such a
way that serves three main functions:
1. Provides a robust tool to aid in the investor’s capital and investment planning
procedure.
2. Allows the user to alter or adjust specific programme’s features by incorporating a
higher level of flexibility.
3. Does not require any specialized technical knowledge from the end user and provides
an intuitive and fairly easy to understand structure.

Overview

The data that were used for this programme were imported from NASDAQ stock exchange and
Google financial history database. The relevant company datasets were downloaded from Google
finance and were processed before being actually used in the programme. Columns were converted
to numeric and date types and non-numeric values were denoted as NaN.
In order to give a general overview of the programme’s structure and capabilities we shall divide
its structure in three distinct, yet fully interactive, parts. The initial part involves the data loading
process and a welcome message, the second part allows the user to select company and data frame
and the third part is the analysis part along with the methods and tools used. All the above are
considered through the lens of increased flexibility without though any sacrifice in the programme’s
usability. For instance, throughout the programme the user may press the ‘Enter’ button once to
return to the last section. Subsequently, when the user decides that he / she wants to entirely exit
the programme, the ‘Enter’ button may be pressed successively.
When the programme gets initialised, in terms of what the user sees, a welcome message and a
short introduction to the programme are provided and at the same time the data are loading.
Furthermore, a second optional level has been created, asking the user whether he want some
further details that serve as the programme’s guidelines.
Next the programme proceeds to the company selection by allowing the user to define the
relevant name or symbol. The company selection process is designed to be fairly flexible, giving the
user the ability to customize the search and simultaneously allowing him to retry in case of an invalid
output. In this case the programme doesn’t terminate but gives the user a second opportunity to
modify its input and proceed normally to the following step.
When the user has successfully defined the desired company, the relevant data are being
loaded. In case the relevant data are unavailable, the programme allows user to enter another
company symbol. Generally, throughout the company selection process the user is given flexibility to
adjust his / her search based on the name, the symbol, the sector or the industry. If the user does
not specify the exact name or symbol, a list of possible matches is being generated to assist
throughout the process.
At this level, in order to avoid possible information overload, an optional step has been created
that allows the display of a maximum of 20 companies. If the user wishes to see all possible relevant
recommendations he / she is allowed to proceed to a second list that displays the remaining
relevant results. Otherwise he / she can proceed to the next step.
The next step includes the definition of a specific time period for which the relevant data will be
gathered and analysed. The user can make a choice between preselected (default) dates or specify adesired time frame. In the latter case, the possibility to alter this decision and ultimately proceed
with the predefined set of dates has been provided.
After the company and time period have been defined the programme enters its analysis phase.
The user is prompted to select if he / she wishes to proceed with statistical, technical or regression
analysis. Whenever one selection has been made, the user can select the other two types of analysis
as many times as he / she wishes. There is no limitation in the number or the order of the analysis
section.
Three main categories have been defined in this section of the code. Descriptive statistics that
include a table with the mean, sample standard deviation, relative standard deviation, minimum and
maximum values of the selected data along with a correlation matrix. We decided to incorporate
some visualization in the descriptive statistics category since we believe that it leads to a more
interactive and engaging user experience.
In the next part of the programme, visualization tools have been heavily employed in order to
give the user the ability to make sense of the data and turn them into meaningful insights. Technical
indicators, including moving averages and time series amongst others, were employed so that the
end user is able to recognize insightful and easy to interpret data patterns and ultimately gain added
conviction.
The last part of the programme, gives the user the ability to perform regression analysis in order
to model the stock market price value for a specific number of days; currently this is set to 10 days.
Polynomial regression analysis was chosen, as an effort to better model non-linear phenomena and
to increase the accuracy of the prediction itself.
#
