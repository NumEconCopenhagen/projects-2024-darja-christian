from collections import Counter
import matplotlib.pyplot as plt

def interactive_figure(data1, data2, country):
    """
    Plot the time series of GDP growth and debt for a selected country.

    Parameters:
    - data1: DataFrame containing GDP growth data with columns 'year', 'Countries', and 'annual_gdp_growth'.
    - data2: DataFrame containing debt data with columns 'year', 'Countries', and 'debt'.
    - country: Name of the country for which to plot the time series.

    Returns:
    - None
    """
    # Create a figure
    fig = plt.figure(frameon=True, figsize=(30, 12), dpi=100)

    # Plot GDP growth
    ax = fig.add_subplot(1, 2, 1)
    selected_country_data1 = data1[data1['Countries'] == country]
    ax.plot(selected_country_data1['year'], selected_country_data1['annual_gdp_growth'])
    ax.set_xlabel('Year')
    ax.set_ylabel('Annual GDP Growth (%)')
    ax.set_title("Time Series of GDP Growth for {}".format(country))
    plt.xticks(rotation=45)

    # Plot debt
    az = fig.add_subplot(1, 2, 2)
    selected_country_data2 = data2[data2['Countries'] == country]
    az.plot(selected_country_data2['year'], selected_country_data2['debt'])
    az.set_xlabel('Year')
    az.set_ylabel('Debt')
    az.set_title("Time Series of Debt for {}".format(country))
    plt.xticks(rotation=45)

    # Show the plot
    plt.show()




def find_country_with_extreme_value_per_year(data, column_name):
    """
    Find the country with the highest and lowest value for the specified column for each year in the given DataFrame.
    Also count how often each country appears as the country with the minimum and maximum value over the last 22 years.

    Parameters:
    - data: DataFrame containing 'year', 'Countries', and the specified column.
    - column_name: Name of the column for which to find extreme values ('debt' or 'annual_gdp_growth').

    Returns:
    - DataFrame with the country with the highest and lowest value for the specified column for each year.
    - Counter objects for the occurrence of each country as the country with the minimum and maximum value.
    """
    # Find the index of the row with the lowest value for each year
    min_value_per_year_idx = data.groupby('year')[column_name].idxmin()
    # Find the index of the row with the highest value for each year
    max_value_per_year_idx = data.groupby('year')[column_name].idxmax()

    # Extract the specific country for each year with the lowest value
    countries_with_min_value_per_year = data.loc[min_value_per_year_idx, ['year', 'Countries', column_name]]
    # Extract the specific country for each year with the highest value
    countries_with_max_value_per_year = data.loc[max_value_per_year_idx, ['year', 'Countries', column_name]]

    # Merge the two DataFrames
    result = countries_with_min_value_per_year.merge(countries_with_max_value_per_year, on='year', suffixes=('_min', '_max'))

    # Count how often each country appears as the country with the minimum and maximum value
    min_counter = Counter(countries_with_min_value_per_year['Countries'])
    max_counter = Counter(countries_with_max_value_per_year['Countries'])
    return result, min_counter, max_counter
