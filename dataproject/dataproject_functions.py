from collections import Counter
import matplotlib.pyplot as plt

# This function tells the widget how the plot should look at a specific parametrization 
def interactive_figure(data1, data2, country):
    # Create a figure
    fig = plt.figure(frameon=True,figsize=(30,12), dpi=100)
    ax = fig.add_subplot(1,2,1)
    
    # Plot the selected country's GDP growth time series
    selected_country_data = data1[data1['Countries'] == country]
    ax.plot(selected_country_data['year'], selected_country_data['annual_gdp_growth'])
    
    # Set the title
    ax.set_xlabel('year')
    plt.xticks(rotation=45)
    ax.set_ylabel('annual gdp growth (in %)')
    ax.set_title("Time Series of GDP Growth for {}".format(country))


    az = fig.add_subplot(1,2,2)
    
    # Plot the selected country's debt time series
    selected_country_data = data2[data2['Countries'] == country]
    az.plot(selected_country_data['year'], selected_country_data['debt'])
    
    # Set the title
    az.set_xlabel('year')
    plt.xticks(rotation=45)
    az.set_ylabel('annual gdp growth (in %)')
    az.set_title("Time Series of debt for {}".format(country))
    
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
