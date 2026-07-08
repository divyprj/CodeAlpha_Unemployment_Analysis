import pandas as pd
import numpy as np
import os

def clean_dataset(df):
    """
    Cleans the dataframe by stripping whitespace from column names,
    converting Date to datetime, dropping NaN rows, and sorting.
    """
    # Strip whitespace from column names
    df.columns = [col.strip() for col in df.columns]
    
    # Drop rows that are completely empty
    df = df.dropna(how='all').copy()
    
    # Strip string values
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
        
    # Convert date column
    if 'Date' in df.columns:
        # The date might be formatted like '31-05-2019' or '31-08-2020'
        # Let's parse it flexibly, handling spaces
        df['Date'] = df['Date'].str.strip()
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
        
        # Drop rows where Date could not be parsed
        df = df.dropna(subset=['Date'])
        
        # Sort by date
        df = df.sort_values('Date').reset_index(drop=True)
        
        # Extract features
        df['Year'] = df['Date'].dt.year
        df['Month_Num'] = df['Date'].dt.month
        df['Month'] = df['Date'].dt.strftime('%b')
        df['Year_Month'] = df['Date'].dt.strftime('%Y-%m')
        
    # Standardize numeric columns
    numeric_cols = [
        'Estimated Unemployment Rate (%)', 
        'Estimated Employed', 
        'Estimated Labour Participation Rate (%)'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Drop rows with NaN in key fields
    df = df.dropna(subset=['Estimated Unemployment Rate (%)'])
    
    return df

def load_data():
    """
    Loads and cleans both datasets if available.
    """
    data_dir = "data"
    file1_path = os.path.join(data_dir, "Unemployment in India.csv")
    file2_path = os.path.join(data_dir, "Unemployment_Rate_upto_11_2020.csv")
    
    df_india = None
    df_upto_2020 = None
    
    if os.path.exists(file1_path):
        try:
            raw_df = pd.read_csv(file1_path)
            df_india = clean_dataset(raw_df)
            print(f"Loaded 'Unemployment in India.csv' with {len(df_india)} rows.")
        except Exception as e:
            print(f"Error loading {file1_path}: {e}")
            
    if os.path.exists(file2_path):
        try:
            raw_df = pd.read_csv(file2_path)
            df_upto_2020 = clean_dataset(raw_df)
            print(f"Loaded 'Unemployment_Rate_upto_11_2020.csv' with {len(df_upto_2020)} rows.")
        except Exception as e:
            print(f"Error loading {file2_path}: {e}")
            
    return df_india, df_upto_2020

def analyze_covid_impact(df):
    """
    Analyzes the impact of COVID-19 on unemployment rates.
    In India, the strict lockdown was implemented in March 2020.
    We'll compare:
    - Pre-COVID: Before April 2020 (e.g. up to March 2020)
    - Lockdown / Peak COVID: April 2020 to October 2020
    """
    if df is None or 'Date' not in df.columns:
        return None
        
    # Add Period classification
    df = df.copy()
    
    # Define lockdown period start
    lockdown_start = pd.to_datetime('2020-04-01')
    
    df['Period'] = np.where(df['Date'] < lockdown_start, 'Pre-Lockdown (Before Apr 2020)', 'Lockdown Period (Apr-Oct 2020)')
    
    # Calculate aggregate stats
    impact = df.groupby('Period').agg({
        'Estimated Unemployment Rate (%)': ['mean', 'min', 'max', 'std'],
        'Estimated Employed': ['mean', 'sum'],
        'Estimated Labour Participation Rate (%)': ['mean']
    }).reset_index()
    
    # Flatten columns
    impact.columns = [
        'Period', 
        'Avg Unemployment Rate (%)', 'Min Unemployment Rate (%)', 'Max Unemployment Rate (%)', 'Std Dev Unemployment',
        'Avg Employed', 'Total Employed (Sum)',
        'Avg Labour Participation Rate (%)'
    ]
    
    return df, impact

def get_statewise_comparison(df):
    """
    Computes state-wise mean unemployment pre and post lockdown.
    """
    if df is None or 'Region' not in df.columns:
        return None
        
    df = df.copy()
    lockdown_start = pd.to_datetime('2020-04-01')
    df['Period'] = np.where(df['Date'] < lockdown_start, 'Pre-Lockdown', 'Lockdown Period')
    
    state_perf = df.groupby(['Region', 'Period'])['Estimated Unemployment Rate (%)'].mean().unstack().reset_index()
    
    # Calculate the absolute and relative increase
    if 'Pre-Lockdown' in state_perf.columns and 'Lockdown Period' in state_perf.columns:
        state_perf['Absolute Increase (%)'] = state_perf['Lockdown Period'] - state_perf['Pre-Lockdown']
        state_perf['Relative Increase (%)'] = (state_perf['Absolute Increase (%)'] / state_perf['Pre-Lockdown']) * 100
        state_perf = state_perf.sort_values(by='Absolute Increase (%)', ascending=False)
        
    return state_perf
