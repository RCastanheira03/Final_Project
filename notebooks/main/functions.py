import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import re

import scipy.stats as st
from scipy.stats import shapiro, levene, kruskal, f_oneway, spearmanr, pearsonr
from datetime import datetime, timedelta

import yaml

try:
    with open("../../config.yaml", "r") as file:
        config = yaml.safe_load(file)

    df = pd.read_csv(config['data']['clean_data']['full_clean'], sep=";")

except:
    print("Yaml configuration file not found!")


def convert_decimal_to_hhmmss(decimal_hours):
    try:
        decimal_hours = float(decimal_hours)
    except (ValueError, TypeError):
        return None
    
    hours = int(decimal_hours)
    minutes = int((decimal_hours - hours) * 60)
    seconds = int(round(((decimal_hours - hours) * 60 - minutes) * 60))
    
    if seconds == 60:
        seconds = 0
        minutes += 1
    if minutes == 60:
        minutes = 0
        hours += 1
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"



def normalize_time_string(time_str):
    try:
        parts = str(time_str).split(':')
        if len(parts) < 2:
            return None  # Invalid format
        
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2]) if len(parts) > 2 else 0
        
        total_minutes = hours * 60 + minutes + seconds / 60
        norm_hours = int(total_minutes // 60)
        norm_minutes = int(total_minutes % 60)
        norm_seconds = int(round((total_minutes * 60) % 60))
        
        if norm_seconds == 60:
            norm_seconds = 0
            norm_minutes += 1
        if norm_minutes == 60:
            norm_minutes = 0
            norm_hours += 1

        return f"{norm_hours:02d}:{norm_minutes:02d}:{norm_seconds:02d}"
    except Exception:
        return None


def convert_hm_to_hhmmss(duration_str):
    try:
        s = str(duration_str).strip().lower()
        
        match = re.search(r'(\d+)\s*h\s*(\d+)\s*m', s)
        if not match:
            return None
        
        hours = int(match.group(1))
        minutes = int(match.group(2))
        
        total_minutes = hours * 60 + minutes
        norm_hours = total_minutes // 60
        norm_minutes = total_minutes % 60
        
        return f"{norm_hours:02d}:{norm_minutes:02d}:00"
    except Exception:
        return None



def detect_outliers_iqr(group):
    Q1 = group['price'].quantile(0.25)
    Q3 = group['price'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return group[(group['price'] < lower_bound) | (group['price'] > upper_bound)]



def price_airline(df):
    plt.figure(figsize=(10,6))
    sns.boxplot(data=df, x='airline', y='price')
    plt.xticks(rotation=45)
    plt.title('Price Distribution by Airline (Detecting Outliers)')
    plt.show()



def shapiro_by_airline(df, group_col='airline', value_col='price'):
    results = {}
    for group_name, group in df.groupby(group_col):
        stat, p_value = shapiro(group[value_col])
        results[group_name] = (stat, p_value)
        print(f"{group_name}: W = {stat:.4f}, p-value = {p_value:.4f}")
    return results

    

def plot_airline_means(summary_df, h, palette_name="Set3"):

    palette = h.sns.color_palette(palette_name, len(summary_df))

    h.plt.errorbar(
        summary_df['airline'],
        summary_df['mean'],
        yerr=summary_df['error'],
        fmt='o',
        color='black',
        elinewidth=3,
        capthick=3,
        errorevery=1,
        alpha=1,
        ms=4,
        capsize=5
    )

    h.plt.bar(
        summary_df['airline'],
        summary_df['mean'],
        color=palette,
        tick_label=summary_df['airline']
    )

    h.plt.xlabel("Airline")
    h.plt.ylabel("Mean Delay Log + CI")
    h.plt.yscale('log')
    h.plt.tight_layout()
    h.plt.show()



def plot_mean_price_by_airline(df, h, palette='viridis', sort_desc=True):
    mean_prices = df.groupby('airline')['price'].mean().reset_index()

    if sort_desc:
        mean_prices = mean_prices.sort_values('price', ascending=False)

    h.plt.figure(figsize=(10, 6))
    h.sns.barplot(data=mean_prices, x='airline', y='price', palette=palette)

    h.plt.title('Mean Ticket Price by Airline')
    h.plt.xlabel('Airline')
    h.plt.ylabel('Mean Price')
    h.plt.xticks(rotation=45)
    h.plt.tight_layout()
    h.plt.show()

    return mean_prices



def kruskal_by_airline(df, h, group_col='airline', value_col='price'):

    groups = [df[df[group_col] == g][value_col] for g in df[group_col].unique()]

    stat, p_value = h.kruskal(*groups)

    print(f"Kruskal–Wallis H-statistic: {stat:.4f}")
    print(f"p-value: {p_value:.4e}")

    return stat, p_value



def plot_price_trend_by_lead_time(df, h, x_col='lead_time_days', y_col='price', hue_col='airline',
                                  palette='husl', height=6, aspect=1.5):

    h.plt.figure(figsize=(10, 6))

    h.sns.lmplot(
        data=df,
        x=x_col,
        y=y_col,
        hue=hue_col,
        lowess=True,
        height=height,
        aspect=aspect,
        scatter=False,
        palette=palette
    )

    h.plt.title('Average Price Trend by Lead Time')
    h.plt.xlabel('Lead Time (days)')
    h.plt.ylabel('Ticket Price')
    h.plt.tight_layout()
    h.plt.show()



def plot_price_vs_duration(h, df, x_col='duration', y_col='price',
                           gridsize=50, cmap='viridis', bins='log'):

    h.plt.figure(figsize=(8, 6))

    hb = h.plt.hexbin(
        df[x_col],
        df[y_col],
        gridsize=gridsize,
        cmap=cmap,
        bins=bins
    )

    h.plt.colorbar(hb, label='log10(Number of flights)')
    h.plt.title("Price vs Duration")
    h.plt.xlabel("Duration (minutes)")
    h.plt.ylabel("Price (INR)")
    h.plt.tight_layout()
    h.plt.show()



def plot_price_by_stops(df, h, x_col='stops', y_col='price', palette='Set2'):
    h.plt.figure(figsize=(7, 5))

    h.sns.boxplot(
        data=df,
        x=x_col,
        y=y_col,
        palette=palette
    )

    h.plt.title("Ticket Prices by Number of Stops")
    h.plt.xlabel("Number of Stops")
    h.plt.ylabel("Price")
    h.plt.tight_layout()
    h.plt.show()



def plot_avg_price_by_stops(df, h, x_col='flight_type', y_col='price',
                            ci=95, capsize=0.2, palette='Set2'):
    
    h.plt.figure(figsize=(7, 5))

    h.sns.barplot(
        data=df,
        x=x_col,
        y=y_col,
        ci=ci,
        capsize=capsize,
        palette=palette
    )

    h.plt.title("Average Ticket Price by Number of Stops (95% CI)")
    h.plt.xlabel("Number of Stops")
    h.plt.ylabel("Average Price")
    h.plt.tight_layout()
    h.plt.show()



def plot_price_by_class(df, h, x_col='class', y_col='price', palette='Set3'):

    h.plt.figure(figsize=(6, 5))

    h.sns.boxplot(
        data=df,
        x=x_col,
        y=y_col,
        palette=palette
    )

    h.plt.title("Ticket Price by Travel Class")
    h.plt.xlabel("Class")
    h.plt.ylabel("Price (INR)")
    h.plt.tight_layout()
    h.plt.show()



def plot_avg_price_by_class(df, h, x_col='class', y_col='price',
                            ci=95, palette='pastel', capsize=0.2):

    h.plt.figure(figsize=(7, 5))

    h.sns.barplot(
        data=df,
        x=x_col,
        y=y_col,
        ci=ci,
        palette=palette,
        capsize=capsize
    )

    h.plt.title("Average Price by Class (with 95% CI)")
    h.plt.xlabel("Travel Class")
    h.plt.ylabel("Mean Price (INR)")
    h.plt.tight_layout()
    h.plt.show()


def plot_price_distribution_by_class(df, h, class_col='class', price_col='price', classes=None, palette='pastel'):

    if classes is None:
        classes = df[class_col].unique()

    colors = h.sns.color_palette(palette, len(classes))

    h.plt.figure(figsize=(8, 5))

    for cls, color in zip(classes, colors):
        subset = df[df[class_col] == cls][price_col]
        h.sns.kdeplot(subset, label=cls, fill=True, color=color)

    h.plt.title("Distribution of Ticket Prices by Class")
    h.plt.xlabel("Price (INR)")
    h.plt.ylabel("Density")
    h.plt.legend(title="Class")
    h.plt.tight_layout()
    h.plt.show()



def plot_price_density_by_stops(df, f, stops_col='stops', price_col='price', palette='viridis'):

    stop_values = sorted(df[stops_col].unique())
    colors = f.sns.color_palette(palette, len(stop_values))

    f.plt.figure(figsize=(7, 5))

    for stops, color in zip(stop_values, colors):
        subset = df[df[stops_col] == stops][price_col]
        f.sns.kdeplot(subset, label=f'{int(stops)} stop(s)', fill=True, color=color)

    f.plt.title("Price Density by Number of Stops")
    f.plt.xlabel("Ticket Price")
    f.plt.ylabel("Density")
    f.plt.legend(title="Stops")
    f.plt.tight_layout()
    f.plt.show()
