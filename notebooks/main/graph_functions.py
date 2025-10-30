import matplotlib.pyplot as plt
import seaborn as sns

def price_airline(df):

    plt.figure(figsize=(10,6))
    sns.boxplot(data=df, x='airline', y='price')
    plt.xticks(rotation=45)
    plt.title('Price Distribution by Airline (Detecting Outliers)')
    plt.show()

def detect_outliers_iqr(group):
    Q1 = group['price'].quantile(0.25)
    Q3 = group['price'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return group[(group['price'] < lower_bound) | (group['price'] > upper_bound)]


def avg_price(df):
    plt.figure(figsize=(10, 6))
    avg_price.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Average Ticket Prices by Airline')
    plt.xlabel('Airline')
    plt.ylabel('Average Price')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
