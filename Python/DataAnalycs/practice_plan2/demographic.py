import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def demographic(df):
    state_dict = {}
    full_dict = {'state': [], 'avg': [], 'max': [], 'min': []}
    
    for index, row in df.iterrows():
        state = row['State']
        male_population = row['Male Population']
        female_population = row['Female Population']
        
        if f'{state}_Male' not in state_dict:
            state_dict[f'{state}_Male'] = []
        state_dict[f'{state}_Male'].append(male_population)
        
        if f'{state}_Female' not in state_dict:
            state_dict[f'{state}_Female'] = []
        state_dict[f'{state}_Female'].append(female_population)
    
    # Calculate the average, max, and min for each month
    try:
        for country, populations in state_dict.items():
            state = country.split('_')[0]
            avg_population = round(np.mean(populations), 2)
            max_population = round(np.max(populations), 2)
            min_population = round(np.min(populations), 2)

            # Append the results to the full_dict
            full_dict['state'].append(state)
            full_dict['avg'].append(avg_population)
            full_dict['max'].append(max_population)
            full_dict['min'].append(min_population)
        return full_dict
    except Exception as e:
        print(f"Error calculating averages: {e}")#        

def plot_graph_graphic(full_dict, graph_name, path):
    state = full_dict['state']
    avg_population = full_dict['avg']
    max_population = full_dict['max']
    min_population = full_dict['min']
    
    try:
        plt.figure(figsize=(10, 6))
        # make the pie chart
        plt.pie(graph_name, state, avg_population, max_population, min_population)
        
        
        # Title and labels
        plt.title('Population by State')
        plt.xlabel('State')
        plt.ylabel('Population')
        
        plt.legend()
        plt.tight_layout()
        plt.xticks(rotation=45)  # Rotate month labels for better readability
        plt.savefig(f'{path}\save_png\{graph_name}.jpg')
        plt.close()
    except Exception as e:
        print(f"Error plotting graph: {e}")