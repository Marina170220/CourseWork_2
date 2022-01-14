import json


def get_data(file):
    """
    Получает данные из json файла.
    :param file: файл с данными.
    :return:  данные в json формате.
    """
    with open(file, 'r', encoding='UTF-8') as f:
        return json.load(f)


def get_posts_with_comments_count():
    """
    На основе списков постов и комментариев добавляет количество комментариев для каждого поста.
    :return: список постов с числом комментариев.
    """
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


def get_post_by_pk(pk):
    """
    Находит пост по его id.
    :param pk: id поста.
    :return: соответсвующий пост.
    """
    posts = get_posts_with_comments_count()
    for post in posts:
        if post.get('pk') == pk:
            post['content'] = replace_hashtags_with_links(post['content'])
            return post


def get_post_comments(pk):
    """
    Формирует список комментариев к посту.
    :param pk: id поста.
    :return: список комментариев к этому посту.
    """
    comments = get_data('data/comments.json')
    post_comments = [comment for comment in comments if comment.get('post_id') == pk]
    return post_comments


def set_ending(count):
    """
    Возвращает окончание слова в нужном склонении в зависимости от количества комментариев.
    Предназначен для корректного отображения числа комментариев к посту на странице.
    :param count: количество комментариев.
    :return: окончание слова "комментарий".
    """
    if count == 1 or count % 10 == 1 and count % 100 != 11:
        return 'й'
    elif 2 <= count <= 4 or 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 > 20):
        return 'я'
    else:
        return 'ев'


def get_posts_by_word(word):
    """
    Находит посты по вхождению ключевого слова.
    :param word: ключевое слово для поиска.
    :return: список постов, содержащих ключевое слово.
    """
    posts = get_posts_with_comments_count()
    posts_by_word = [post for post in posts if word.lower() in post.get('content').lower()]
    return posts_by_word


def get_posts_by_tag(tag):
    """
    Формирует список постов по выбранному тегу.
    :param tag: выбранный тег.
    :return: список найденных постов.
    """
    posts = get_posts_with_comments_count()
    return [post for post in posts if f'#{tag}' in post['content']]


def get_posts_by_user(user):
    """
    Находит посты, опубликованные определённым пользователем.
    :param user: имя пользователя.
    :return: список постов искомого пользователя.
    """
    posts = get_posts_with_comments_count()
    posts_by_user = [post for post in posts if user.lower() in post.get('poster_name').lower()]
    return posts_by_user


def replace_hashtags_with_links(content):
    """
    Заменяет хештеги в посте ссылками.
    :param content: текст поста.
    :return: текст поста с кликабельными хештегами.
    """
    words_in_post = content.split(' ')
    for index, word in enumerate(words_in_post):
        if word.startswith('#'):
            tag = word[1:]
            words_in_post[index] = f"<a href='/tag/{tag}'>{word}</a>"
    return " ".join(words_in_post)


def add_bookmark(pk):
    """
    Добавляет пост в закладки.
    :param pk: id добавляемого поста.
    """
    bookmarks = get_data('data/bookmarks.json')

    posts = get_posts_with_comments_count()
    for post in posts:
        if pk == post.get('pk'):
            if not is_post_in_list_check(pk, bookmarks):
                bookmarks.append(post)

    with open('data/bookmarks.json', 'w', encoding='UTF-8') as f:
        json.dump(bookmarks, f, ensure_ascii=False, indent=4)


def remove_bookmark(pk):
    """
    Удаляет пост из закладок.
    :param pk: id удаляемого поста.
    """
    bookmarks = get_data('data/bookmarks.json')

    if bookmarks:
        for post in bookmarks:
            if pk == post.get('pk'):
                bookmarks.remove(post)

    with open('data/bookmarks.json', 'w', encoding='UTF-8') as f:
        json.dump(bookmarks, f, ensure_ascii=False, indent=4)


def is_post_in_list_check(id_, list_):
    """
    Проверяет, находится ли пост в списке
    :param id_: id поста
    :param list_: список постов
    :return: True, если искомый пост есть в списке, иначе False
    """
    for post in list_:
        if id_ == post.get('pk'):
            return True
    return False


def add_new_comment(name, text, id_):
    """
    Добавляет новый комментарий к списку комментариев.
    :param name: имя пользователя, добавившего комментарий.
    :param text: текст нового комментария.
    :param id_: id поста, к которому добавлен комментарий.
    """
    comments = get_data('data/comments.json')
    new_comment = {'post_id': id_,
                   'commenter_name': name,
                   'comment': text,
                   'pk': (len(comments) + 1),
                   }
    comments.append(new_comment)

    with open('data/comments.json', 'w', encoding='UTF-8') as f:
        json.dump(comments, f, ensure_ascii=False, indent=4)
