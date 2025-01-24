import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = r'C:\Users\admin\Downloads\UberDataset_with_payment.csv'
data = pd.read_csv(file_path)

# Data preprocessing
data['START_DATE'] = pd.to_datetime(data['START_DATE'], errors='coerce')
data['END_DATE'] = pd.to_datetime(data['END_DATE'], errors='coerce')

# Handle missing values by dropping rows & Extract additional time features
data.dropna(subset=['START', 'STOP', 'START_DATE', 'END_DATE'], inplace=True)

data['Day'] = data['START_DATE'].dt.day_name()
data['Hour'] = data['START_DATE'].dt.hour
data['Month'] = data['START_DATE'].dt.month_name()

# 1. Identify peak demand hours and days
plt.figure(figsize=(14, 6))
sns.countplot(x='Hour', data=data, palette='Reds')
plt.title('Peak Demand Hours')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Rides')
plt.show()

plt.figure(figsize=(14, 6))
sns.countplot(x='Day', data=data, order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], palette='viridis')
plt.title('Rides by Day of the Week')
plt.xlabel('Day')
plt.ylabel('Number of Rides')
plt.show()

# 2. Analyze high-demand pickup and drop-off locations
top_start_locations = data['START'].value_counts().head(10)
top_stop_locations = data['STOP'].value_counts().head(10)

print("Top 10 Pickup Locations:")
print(top_start_locations)

plt.figure(figsize=(14, 6))
top_start_locations.plot(kind='bar', color='darkblue')
plt.title('Top 10 Pickup Locations')
plt.xlabel('Pickup Location')
plt.ylabel('Number of Rides')
plt.show()

print("\nTop 10 Drop-off Locations:")
print(top_stop_locations)

plt.figure(figsize=(14, 6))
top_stop_locations.plot(kind='bar', color='#A40000')
plt.title('Top 10 Drop-off Locations')
plt.xlabel('Drop-off Location')
plt.ylabel('Number of Rides')
plt.show()

# 3. Trends in ride volumes over time
rides_per_day = data.groupby(data['START_DATE'].dt.date).size()

plt.figure(figsize=(14, 6))
rides_per_day.plot()
plt.title('Ride Volumes Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Rides')
plt.show()

# 4. Analyze Trip Durations
data['Trip_Duration'] = (data['END_DATE'] - data['START_DATE']).dt.total_seconds() / 60  # Trip duration in minutes

# Average trip duration by hour
avg_duration_hour = data.groupby('Hour')['Trip_Duration'].mean()

plt.figure(figsize=(14, 6))
avg_duration_hour.plot(kind='bar', color='teal')
plt.title('Average Trip Duration by Hour of the Day')
plt.xlabel('Hour of the Day')
plt.ylabel('Average Duration (minutes)')
plt.show()

# Average trip duration by day
avg_duration_day = data.groupby('Day')['Trip_Duration'].mean().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)

plt.figure(figsize=(14, 6))
avg_duration_day.plot(kind='bar', color='orange')
plt.title('Average Trip Duration by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Average Duration (minutes)')
plt.show()

# Zones with unusual trip durations
avg_duration_zone = data.groupby('START')['Trip_Duration'].mean().sort_values(ascending=False).head(10)

print("\nZones with Longest Average Trip Durations:")
print(avg_duration_zone)

plt.figure(figsize=(14, 6))
avg_duration_zone.plot(kind='bar', color='darkgreen')
plt.title('Zones with Longest Average Trip Durations')
plt.xlabel('Pickup Zone')
plt.ylabel('Average Trip Duration (minutes)')
plt.show()

# 5. Analyze Payment Methods
if 'payment' in data.columns:
    payment_counts = data['payment'].value_counts()

    plt.figure(figsize=(14, 6))
    payment_counts.plot(kind='bar', color='purple')
    plt.title('Distribution of Payment Methods')
    plt.xlabel('Payment Method')
    plt.ylabel('Count')
    plt.show()

    # Payment method preference by zone
    payment_zone = data.groupby(['START', 'payment']).size().unstack().fillna(0)

    print("\nPayment Preferences by Zone:")
    print(payment_zone.head(10))

    # Visualize payment preferences in top pickup zones
    payment_zone_top = payment_zone.loc[top_start_locations.index]

    payment_zone_top.plot(kind='bar', stacked=True, figsize=(14, 6), colormap='Spectral')
    plt.title('Payment Preferences in Top Pickup Zones')
    plt.xlabel('Pickup Zone')
    plt.ylabel('Count')
    plt.show()
else:
    print("No payment column found in the dataset.")
