import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calc_price(df, str):
    # Initialize necessary variables
    monthly_data = {}  # Dictionary to store data by month
    full_dict = {'month': [], 'avg': [], 'max': [], 'min': []}
    
    # Loop through the rows in the dataframe
    try:
        for index, row in df.iterrows():
        # Select price based on input string
            if str == 'open':
                price = row['Open Price']
            elif str == 'high':
                price = row['High Price']
            elif str == 'low':
                price = row['Low Price']
            elif str == 'close':
                price = row['Close Price']  

            month = row['Date'][:-6] # Extract the month from the 'Date' column
            
            # Add the price to the corresponding month in the dictionary
            if month not in monthly_data:
                monthly_data[month] = []
            monthly_data[month].append(price)
    except Exception as e:
        print(f"Error processing data: {e}")
    
    # Calculate the average, max, and min for each month
    try:
        for month, prices in monthly_data.items():
            avg_price = round(np.mean(prices), 2)
            max_price = round(np.max(prices), 2)
            min_price = round(np.min(prices), 2)
            
            # Append the results to the full_dict
            full_dict['month'].append(month)
            full_dict['avg'].append(avg_price)
            full_dict['max'].append(max_price)
            full_dict['min'].append(min_price)
        return full_dict
    except Exception as e:
        print(f"Error calculating average, max, min: {e}")


def plot_graph(full_dict, graph_name, path, cur):
    # Extract data for plotting
    # Create a table if it doers not exist
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS price_trends_{} (month VARCHAR(10), avg_price FLOAT, max_price FLOAT, min_price FLOAT)".format(graph_name))
    except Exception as e:
        print(f"Error creating table: {e}")
    
    months = full_dict['month']
    avg_prices = full_dict['avg']
    max_prices = full_dict['max']
    min_prices = full_dict['min']
    
    # Plot average, max, and min
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(months, avg_prices, label='Average Price', color='blue', marker='o')
        plt.plot(months, max_prices, label='Maximum Price', color='red', linestyle='--', marker='x')
        plt.plot(months, min_prices, label='Minimum Price', color='green', linestyle=':', marker='s')
        
        # Title and labels
        plt.title('Monthly Price Trends')
        plt.xlabel('Month')
        plt.ylabel('Price')
        
        plt.legend()
        plt.tight_layout()
        plt.xticks(rotation=45)  # Rotate month labels for better readability
        plt.savefig(f'{path}\save_png\{graph_name}.jpg')
        plt.close()
    except Exception as e:
        print(f"Error plotting graph: {e}")