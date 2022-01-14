from flask import Flask, request, render_template, redirect
from functions import *
app = Flask(__name__)


@app.route('/')
def page_index():
    posts = get_posts_with_comments_count()
    bookmarks = get_data('data/bookmarks.json')
    bookmarks_count = len(bookmarks)
    return render_template('index.html', posts=posts, bookmarks_count=bookmarks_count)


@app.route('/posts/<int:pk>',)
def page_post(pk):
    post = get_post_by_pk(pk)
    comments = get_post_comments(pk)
    return render_template('post.html', post=post, comments=comments)


@app.route('/search/', methods=["GET", "POST"])
def page_search():
    if request.method == "GET":
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


@app.route('/users/<username>')
def page_user(username):
    posts = get_posts_by_user(username)
    return render_template('user-feed.html', posts=posts, username=username)


@app.route('/tag/<tagname>')
def page_tag(tagname):
    posts = get_posts_by_tag(tagname)
    return render_template('tag.html', posts=posts, tagname=tagname)


@app.route('/bookmarks/add/<int:postid>')
def page_bookmarks_add(postid):
    add_bookmark(postid)
    return redirect("/", code=302)


@app.route('/bookmarks/remove/<int:postid>')
def page_bookmarks_remove(postid):
    remove_bookmark(postid)
    return redirect("/", code=302)
    # posts = get_posts_with_hashtags()
    # return render_template('index.html', posts=posts)


@app.route('/bookmarks/')
def page_bookmarks():
    posts = get_data('data/bookmarks.json')
    count = len(posts)
    if posts:
        return render_template('bookmarks.html', posts=posts, count=count)
    return "В закладках пока нет ни одного поста"


# @app.route("/tag")
# def page_tag():
#     tag = request.args.get('tag')
#     if tag:
#         posts = get_posts_by_tag(read_json(POST_PATH), tag)
#         return render_template("post_by_tag.html", posts=posts, tag=tag)
#     return abort(400, "Вы не выбрали ни одного тега :(")


if __name__ == "__main__":
    app.run(debug=True)
