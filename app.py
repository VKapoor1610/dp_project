from flask import Flask , render_template , jsonify

import pandas as pd 
from connect import sheet
import numpy as np
import matplotlib.pyplot as plt 


app = Flask(__name__)


@app.route('/')
def home():
    # return jsonify(grouped )
    return render_template('home.html')


@app.route('/analysis2')
def analysis2():

    data = sheet.get_all_values()

    # Create a Pandas DataFrame from the data
    df = pd.DataFrame(data[1:], columns=data[0])

    # Convert 'status' column to integer
    df['status'] = df['status'].astype(int)

    # Filter the data based on 'mode' column and status values
    filtered_data = df[(df['mode'] == 'wp') & (df['status'].isin([1, 2]))]

    # Convert 'date' column to datetime
    filtered_data['date'] = pd.to_datetime(filtered_data['date'])

    # Group the filtered data based on 'date' and 'status'
    grouped = filtered_data.groupby(['date', 'status']).size().unstack(fill_value=0)

    # Reset the index to make 'date' the new index
    grouped = grouped.reset_index().set_index('date')

    # Plot the stacked bar chart
    ax = grouped.plot(kind='bar', stacked=True, color=['red', 'green'], width=0.2)
    ax.set_xticklabels(grouped.index.strftime('%d-%m-%y'), rotation=0)

    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title('Number of Correct and Incorrect Attempts in Word Practice Mode')
    plt.legend(['Incorrect', 'Correct'])
    plt.tight_layout()
    plt.savefig("static/images/plot4.png")

    plt.figure()

    grouped['accuracy'] = (grouped[2] / (grouped[1] + grouped[2])) * 100

    # Plot the bar chart
    ax = grouped['accuracy'].plot.bar(color='#03fc30', width=0.2)
    plt.xticks(rotation=0)

    # Add labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Accuracy (%)')
    ax.set_title('Accuracy Percentage by Date')

    # Add dots and lines
    for i, v in enumerate(grouped['accuracy']):
        ax.text(i, v, f"{v:.2f}%", ha='center', va='bottom', color='black')
        ax.plot([i-0.15, i+0.15], [v, v], color='black')

    plt.tight_layout()

    plt.savefig("static/images/plot5.png")




    return render_template('word_analysis.html')


@app.route('/analysis')
def analysis():
    data = sheet.get_all_values()

    # Create a Pandas DataFrame from the data
    df = pd.DataFrame(data[1:], columns=data[0])

    df_plot1 = pd.DataFrame(data[1:], columns=data[0])

    # Convert columns to appropriate data types
    df_plot1['status'] = df_plot1['status'].astype(int)
    df_plot1['incorrect'] = df_plot1['incorrect'].astype(int)

    # Filter the DataFrame based on mode = 'lp'
    filtered_df = df_plot1[df_plot1['mode'] == 'lp']

    # Group by date and calculate the number of correct and incorrect questions
    grouped = filtered_df.groupby('date')['status'].value_counts().unstack().fillna(0)

    # Plot the stacked bar chart
    ax = grouped.plot.bar(stacked=True, color=['#fc1303', '#03fc30'], width=0.3)

    # Add labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Frequency')
    ax.set_title('Frequency of Correct and Incorrect Attempts by Date')

    # Add legend
    ax.legend(['Incorrect', 'Correct'], loc='upper left')

    # Show the plot
    plt.tight_layout()
    plt.savefig("static/images/plot1.png")
    
    
    plt.figure()
    
    
    grouped['accuracy'] = (grouped[2] / (grouped[1] + grouped[2]) )* 100
    
    # f = open('op.txt' , 'w')
    # f.write(str(grouped))

    # Plot the accuracy percentage
    
    ax = grouped['accuracy'].plot.bar(color='#03fc30', width=0.3)
    plt.xticks(rotation=0)

    # Add labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Accuracy (%)')
    ax.set_title('Accuracy Percentage by Date')
    # plt.scatter(grouped['date'] , )
    x_coords = grouped.index
    y_coords = grouped['accuracy']

    # Draw lines and dots to join the tops of the bars
    for i in range(len(x_coords)):
        x = x_coords[i]
        y = y_coords[i]
        plt.plot([x, x], [100, y], color='black', linestyle=':', linewidth=1)  # Draw vertical line
        plt.plot(x, y, marker='o', markersize=5, color='black')  # Draw dot
        if i > 0:
            prev_x = x_coords[i-1]
            prev_y = y_coords[i-1]
            plt.plot([prev_x, x], [prev_y, y], color='black', linestyle='-', linewidth=1)  # Draw connecting line

    plt.savefig("static/images/plot2.png")
    
    
    # plotted the accuracy curve 
    
    letter_freq = {}

    # Iterate over each row of the DataFrame and count the frequency of correct and incorrect letters
    for index, row in df[df['mode'] == 'lp'].iterrows():
        letter = row['letter']
        incorrect_data = row['incorrectdata']
        incorrect_data_list = eval(incorrect_data)  # convert string to list
        correct = incorrect_data_list.count(1)
        incorrect = len(incorrect_data_list) - correct

        if letter not in letter_freq:
            letter_freq[letter] = {'correct': 0, 'incorrect': 0, 'total': 0}

        letter_freq[letter]['correct'] += correct
        letter_freq[letter]['incorrect'] += incorrect
        letter_freq[letter]['total'] += (correct + incorrect)

    # Use the matplotlib library to plot the horizontal bars for each letter
    fig, ax = plt.subplots(figsize=(10, 5))

    x_ticks = []
    y_values = []
    
    f = open('op.txt' , 'w')

    for letter, freq in letter_freq.items():
        total_attempts = freq['total']/6
        
        f.write( str(letter) + '  ' + str(total_attempts) + '\n')
        if total_attempts <= 5:
            completion_percentage = 0
       
        else:
            # logic 60% completion over time is marked with 100% completions and calculated if attempts more that equal to 5
            completion_percentage = min( 100 , 100*(freq['correct'] * 100 ) / (freq['correct'] + freq['incorrect'] * 60  ))

        x_ticks.append(letter)
        y_values.append(completion_percentage)

    sorted_indices = sorted(range(len(x_ticks)), key=lambda x: x_ticks[x])
    sorted_list1 = [x_ticks[i] for i in sorted_indices]
    sorted_list2 = [y_values[i] for i in sorted_indices] 
    
    ax.barh(sorted_list1, sorted_list2, color='green' , height = 0.9)

    y_values.sort(reverse=True)
    plt.xlabel('Completion Percentage')
    plt.ylabel('Letters')
    plt.title('Letter Completion Percentage')
    plt.savefig("static/images/plot3.png")

    return render_template('analysis.html')

@app.route('/team')
def team():
    return render_template('team.html')

if(__name__ == "__main__"):
    app.run(debug=True)




