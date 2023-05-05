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




@app.route('/analysis')
def analysis( ):
    
    data = sheet.get_all_values()

    #  create a Pandas DataFrame from the data
    df = pd.DataFrame(data[1:], columns=data[0])

    df['status'] = df['status'].astype(int) - 1

    # convert 'status' column to integer values
    df['status'] = df['status'].astype(int)

    # group by date and calculate the number of correct and incorrect questions
    grouped = df.groupby('date')['status'].agg(correct='sum', incorrect='count') 

    # calculate the total number of questions per date
    grouped['total_questions'] = grouped['correct'] + grouped['incorrect']
    
    grouped1 = grouped.reset_index()
    ax = grouped1.plot.bar(x='date', y=['correct', 'incorrect'], stacked=True, width= 0.1 ,  color=['#03fc30', '#fc1303'])


    # add labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Questions')
    ax.set_title('Correct and Incorrect Questions by Date')



    ax.set_facecolor('#fffade')
    
    plt.title('Line Plot')
    plt.plot(grouped1['date'] , grouped1['total_questions'] , color = 'black')
    plt.scatter(grouped1['date'] , grouped1['total_questions'] , color='black')
    plt.tight_layout()
    plt.savefig("static/images/plot1.png")
    # x = np.arange(0, 10, 0.1)
    # y = np.sin(x)
    # plt.plot(x, y)
    # plt.title('Line Plot')
    # plt.xlabel('x')
    # plt.ylabel('y')
    # # plt.grid(grid = True)
    # plt.tight_layout()
    # # Save the plot to a PNG image file and return the file path
    # plt.savefig("static/images/line_plot.png")
    
    
    plt.title("new Plot")
    plt.figure(facecolor= '#fffade')

    plt.scatter(grouped1['date'], 100*(grouped1['correct']/grouped1['incorrect']))
    plt.plot(grouped1['date'], 100*(grouped1['correct']/grouped1['incorrect']))
    plt.xlabel("dates along -> ")
    plt.ylabel("(%) accuracy on daily basis")
    
    plt.savefig("static/images/plot2.png")
    
    # third plot 
    
# Create a dictionary to store the frequency of correct and incorrect letters
    letter_freq = {}
    
    # Iterate over each row of the DataFrame and count the frequency of correct and incorrect letters
    for index, row in df.iterrows():
        letter = row['letter']
        incorrect_data = row['incorrectdata']
        incorrect_data_list = eval(incorrect_data) # convert string to list
        correct = sum(incorrect_data_list)
        incorrect = len(incorrect_data_list) - correct
        
        if letter not in letter_freq:
            letter_freq[letter] = {'correct': 0, 'incorrect': 0}
        
        letter_freq[letter]['correct'] += correct
        letter_freq[letter]['incorrect'] += incorrect


    # Use the matplotlib library to plot the horizontal bars for each letter
    fig, ax = plt.subplots(figsize=(10, 5))

    x_ticks = []
    y_values_correct = []
    y_values_incorrect = []

    for letter, freq in letter_freq.items():
        x_ticks.append(letter)
        y_values_correct.append(freq['correct'])
        y_values_incorrect.append(freq['incorrect'])
        

    ax.barh(x_ticks, y_values_correct, label='Correct' , color ='green')
    ax.barh(x_ticks, y_values_incorrect, label='Incorrect', left=y_values_correct , color= 'red')

    x_ticks.sort(reverse=True)
    plt.xlabel('Frequency')
    plt.ylabel('Letters')
    plt.legend()
    plt.savefig("static/images/plot3.png")

        
    return render_template('analysis.html')

if(__name__ == "__main__"):
    app.run(debug=True)




