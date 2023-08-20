import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the csv file
df = pd.read_csv('posts.csv')

# Data has the following columns:
# Title, URL, Date, Category

# The column titles aren't stored in the data, so we need to add them
df.columns = ['title', 'url', 'date', 'category']

df['date'] = pd.to_datetime(df['date'])


grouped = df.groupby(pd.Grouper(key='date', freq='M')).size()

accepted_df = df[df['category'] == 'Accepted']
denied_df = df[df['category'] == 'Denied']
abuse_df = df[df['category'] == 'Report Abuse']

grouped_accepted = accepted_df.groupby(pd.Grouper(key='date', freq='M')).size()
grouped_denied = denied_df.groupby(pd.Grouper(key='date', freq='M')).size()
grouped_abuse = abuse_df.groupby(pd.Grouper(key='date', freq='M')).size()

plt.figure(figsize=(10, 6))
plt.plot(grouped.index, grouped.values, linestyle='-', label='Total Posts')
plt.plot(grouped_accepted.index, grouped_accepted.values, linestyle='-', color='green', label='Accepted Posts')
plt.plot(grouped_denied.index, grouped_denied.values, linestyle='-', color='red', label='Denied Posts')
plt.plot(grouped_abuse.index, grouped_abuse.values, linestyle='-', label='Report Abuse Posts')
plt.xlabel('Time')
plt.ylabel('Post Count')
plt.title('Monthly Post Count by Category')
plt.xticks(rotation=45)
plt.legend()  # Display legend
plt.grid(True, alpha=0.3)  # Display grid
plt.tight_layout()
plt.show()
