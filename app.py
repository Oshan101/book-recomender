from flask import Flask, render_template, request
import pickle
import numpy as np
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           authors=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           no_of_votes=list(popular_df['num_ratings'].values),
                           ratings=list(popular_df['avg_ratings'].values)
                           )
@app.route('/recommend')
def recommend():
    return render_template('recommend.html',

                           )

@app.route('/recommend_books',methods=['POST'])
def recommend_books():
    book_name = request.form.get('book_name')
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:9]
    data = []
    for d in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[d[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return render_template('recommend.html',data=data)
if __name__ == '__main__':
    app.run()