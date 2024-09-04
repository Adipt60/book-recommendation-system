

from flask import Flask, render_template, request
import pickle
import numpy as np


popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                            book_name = popular_df['Book-Title'].to_list(),
                            author = popular_df['Book-Author'].to_list(),
                            image = list(popular_df['Image-URL-M']),
                            votes = popular_df['num_ratings'].to_list(),
                            rating = popular_df['avg_rating'].to_list(),
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    idx = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[idx])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].to_list()))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].to_list()))
        data.append(item)

    print(data)
    return render_template('recommend.html', data=data)



if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')