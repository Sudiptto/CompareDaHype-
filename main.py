import requests
from flask import Flask, render_template, request, flash, redirect, url_for
from password import *
import os
# NOTEE:
# DO npm install chart.js
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_PASSWORD')
@app.route('/', methods=['GET', 'POST'])
def home():
      # Replace with your API key
    
    # Make the API call to get the latest headlines
    url = f"https://newsapi.org/v2/top-headlines/sources?apiKey={api_key}"
    news_data = requests.get(url).json()
    
    #print(news_data['sources'][0]['id'])

    sources = []
    for i in news_data['sources']:
        sources.append(i['name'] + '-  Language: ' + i['language'])


    if request.method == 'POST':
        topic_1 = request.form.get('Topic')
        topic_2 = request.form.get('Topic2')
        if len(topic_1) == 0 or len(topic_2) == 0:
            flash('Fill out the two fields', category='error')
        elif topic_1 == topic_2:
            flash('These topics are the same make them diferent!', category='error')
        else:
            url2  = f'https://newsapi.org/v2/everything?q={topic_1}&apiKey={api_key}' # first topic the user gave
            popularity = requests.get(url2).json()
            #print(popularity['totalResults']) # total result for the first field

            url3  = f'https://newsapi.org/v2/everything?q={topic_2}&apiKey={api_key}' # second topic the user gave
            popularity2 = requests.get(url3).json()
            #print(popularity2['totalResults']) # total result for the first field
            # total results for each field
            first_topic = int(popularity['totalResults'])
            second_topic = int(popularity2['totalResults'])
            if first_topic > second_topic:
                flash(topic_1 + " recieved: " + str(first_topic) + " results! (Scroll Down For Graph)", category='success')
                flash(topic_2 + " recieved: " + str(second_topic) + " results! ", category='success')
                flash(topic_1 + " Has more RESULTS!", category='success')
                return render_template('home.html', topic_1=topic_1, topic_2=topic_2, second_topic=second_topic, first_topic=first_topic)
            elif first_topic == second_topic:
                flash(f'Both topics ({topic_1} + {topic_2}) are equal! Each recieving: ' + str(second_topic) + ' results!', category='success')
                return render_template('home.html', topic_1=topic_1, topic_2=topic_2, second_topic=second_topic, first_topic=first_topic)
            else: 
                flash(topic_1 + " recieved: " + str(first_topic) + " results! (Scroll Down For Graph)", category='success')
                flash(topic_2 + " recieved: " + str(second_topic) + " results! ", category='success')
                flash(topic_2 + " Has more RESULTS!", category='success')
                return render_template('home.html', topic_1=topic_1, topic_2=topic_2, second_topic=second_topic, first_topic=first_topic)

                #return popularity2

        
        


            


            
            



    return render_template("home.html", sources=sources)



if __name__ == '__main__':
    app.run(debug=True)