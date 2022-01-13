from flask import Flask, request, render_template
from functions import *
app = Flask(__name__)


@app.route('/',)
def page_index():
    posts = get_posts_with_comments_count()
    return render_template('index.html', posts=posts)


@app.route('/posts/<int:pk>',)
def page_post(pk):
    post = get_post_by_pk(pk)
    comments = get_post_comments(pk)
    return render_template('post.html', post=post, comments=comments)


@app.route('/search/', methods=["GET", "POST"])
def page_search():
    if request.method == "POST":
        search = request.form.get('search')
    elif request.method == "GET":
        search = request.args.get('s')
    if search:
        found_posts = get_posts_by_word(search)
        if len(found_posts) <= 10:
            count = len(found_posts)
        else:
            count = 10
            found_posts = found_posts[:10]
        return render_template('search.html', found_posts=found_posts, count=count, search=search)
    return 'Вы не ввели запрос'


@app.route('/users/<username>',)
def page_user(username):
    posts = get_posts_by_user(username)
    return render_template('user-feed.html', posts=posts, username=username)


if __name__ == "__main__":
    app.run(debug=True)
