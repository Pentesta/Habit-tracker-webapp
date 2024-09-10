from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import os

app = Flask(__name__)

# Load existing data or create a new dataframe
data_file = 'habits.csv'
if os.path.exists(data_file):
    df = pd.read_csv(data_file)
else:
    df = pd.DataFrame(columns=['Date', 'Exercise', 'Reading', 'Coding'])

# Home route to display the form and table
@app.route('/')
def index():
    return render_template('index.html', habits=df.to_dict(orient='records'))

# Route to handle form submission
@app.route('/add', methods=['POST'])
def add_habit():
    date = datetime.now().strftime('%Y-%m-%d')
    exercise = int(request.form.get('exercise', 0))
    reading = int(request.form.get('reading', 0))
    coding = int(request.form.get('coding', 0))

    # Create a new DataFrame for the new data
    new_data = pd.DataFrame({'Date': [date], 'Exercise': [exercise], 'Reading': [reading], 'Coding': [coding]})
    
    # Concatenate the new row to the existing dataframe
    global df
    df = pd.concat([df, new_data], ignore_index=True)

    # Save the updated dataframe to the CSV file
    df.to_csv(data_file, index=False)

    return redirect(url_for('index'))


# Route to visualize habits
@app.route('/visualize')
def visualize_habits():
    global df  # Declare that we're using the global df variable
    
    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Remove duplicate dates, keeping the first occurrence
    df.drop_duplicates(subset='Date', keep='first', inplace=True)
    
    # Set 'Date' column as index
    df.set_index('Date', inplace=True)
    
    # Resample data to fill missing dates with NaN
    # df = df.resample('D').asfreq()
    
    # Plot the habits
    plt.figure(figsize=(10, 5))
    df.plot(marker='o')  # Use marker='o' to show actual data points
    plt.title('Habit Tracking Progress')
    plt.xlabel('Date')
    plt.ylabel('Habit Completed (1 = Yes, 0 = No)')
    
    # Save the chart as an image
    plt.savefig('static/habit_progress.png')
    plt.close()
    
    return render_template('visualize.html', image='static/habit_progress.png')
    
    # Plot the habits
    plt.figure(figsize=(10, 5))
    df.plot(kind='bar', figsize=(10, 5))  # Use marker='o' to show actual data points
    plt.title('Habit Tracking Progress')
    plt.xlabel('Date')
    plt.ylabel('Habit Completed (1 = Yes, 0 = No)')
    
    # Save the chart as an image
    plt.savefig('static/habit_progress.png')
    plt.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
