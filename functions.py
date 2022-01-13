import json
import pprint


def get_data(file):
    with open(file, 'r', encoding='UTF-8') as f:
        return json.load(f)


def get_post_by_pk(pk):
    posts = get_posts_with_comments_count()
    for post in posts:
        if post.get('pk') == pk:
            return post


def get_posts_with_comments_count():
    posts = get_data('data/posts.json')
    comments = get_data('data/comments.json')
    comments_count = {}

    for comment in comments:
        post_id = comment.get('post_id')
        if post_id in comments_count:
            comments_count[post_id] += 1
        else:
            comments_count[post_id] = 1

    for index, post in enumerate(posts):
        pk = post.get('pk')
        if pk in comments_count:
            posts[index]['comments_count'] = comments_count[pk]
            posts[index]['ending'] = set_ending(comments_count[pk])
        else:
            posts[index]['comments_count'] = 0
            posts[index]['ending'] = set_ending(0)

    return posts


def get_post_comments(pk):
    comments = get_data('data/comments.json')
    post_comments = [comment for comment in comments if comment.get('post_id') == pk]
    return post_comments


def set_ending(count):
    if count == 1 or count % 10 == 1 and count % 100 != 11:
        return 'й'
    elif 2 <= count <= 4 or 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 > 20):
        return 'я'
    else:
        return 'ев'


def get_posts_by_word(word):
    posts = get_posts_with_comments_count()
    posts_by_word = [post for post in posts if word.lower() in post.get('content').lower()]
    return posts_by_word


def get_posts_by_user(user):
    posts = get_posts_with_comments_count()
    posts_by_user = [post for post in posts if user.lower() in post.get('poster_name').lower()]
    return posts_by_user

#
# pprint.pprint(get_posts_by_user('leo'))
