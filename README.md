# UR-SQLAlchemy-Challenge
Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with your trip planning, you need to do some climate analysis on the area. The following outlines what you need to do.


## Step 1 - Climate Analysis and Exploration

To begin, use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.


### Precipitation Analysis
*Start by finding the most recent date in the data set.

*Using this date, retrieve the last 12 months of precipitation data by querying the 12 preceding months of data. Note you do not pass in the date as a variable to your query.

*Select only the date and prcp values.

*Load the query results into a Pandas DataFrame and set the index to the date column.

*Sort the DataFrame values by date.

*Plot the results 

*Use Pandas to print the summary statistics for the precipitation data.


### Station Analysis

*Design a query to calculate the total number of stations in the dataset.

*Design a query to find the most active stations (i.e. which stations have the most rows?).

*List the stations and observation counts in descending order.

*Which station id has the highest number of observations?

*Using the most active station id, calculate the lowest, highest, and average temperature.

*Design a query to retrieve the last 12 months of temperature observation data (TOBS).

*Filter by the station with the highest number of observations.

*Query the last 12 months of temperature observation data for this station.

*Plot the results as a histogram with bins=12.


## Step 2 - Climate App

Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.


# Bonus: Other Recommended Analyses


###Temperature Analysis I

Hawaii is reputed to enjoy mild weather all year. Is there a meaningful difference between the temperature in, for example, June and December?

*Convert the date column format from string to datetime.

*Set the date column as the DataFrame index

*Identify the average temperature in June at all stations across all available years in the dataset. Do the same for December temperature.

*Use the t-test to determine whether the difference in the means, if any, is statistically significant. Will you use a paired t-test, or an unpaired t-test? Why?