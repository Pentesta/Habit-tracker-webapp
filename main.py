import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Load existing data or create a new dataframe
try:
    df = pd.read_csv('habits.csv')
except FileNotFoundError:
    df = pd.DataFrame(columns=['Date', 'Exercise', 'Reading', 'Coding'])

# Function to add a new habit entry
def add_habit(date, exercise, reading, coding):
    new_data = {'Date': date, 'Exercise': exercise, 'Reading': reading, 'Coding': coding}
    df.loc[len(df)] = new_data
    df.to_csv('habits.csv', index=False)
    print("Habit added successfully!")

# Function to visualize habit data
def visualize_habits():
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df.plot(figsize=(10, 5))
    plt.title('Habit Tracking Progress')
    plt.xlabel('Date')
    plt.ylabel('Habit Completed (1 = Yes, 0 = No)')
    plt.show()

# Example usage
today = datetime.now().strftime('%Y-%m-%d')
add_habit(today, 1, 1, 0)
visualize_habits()
