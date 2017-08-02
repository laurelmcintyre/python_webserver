import cgi
import sqlite3

form = b'''
    <html>
    <head>
    <title>Translation</title>
    </head>
    <body>
    <form method="post" action="">
    <label>Translate</label>
    <input type="text" name="textinput">
    <input type="submit" value="Go">
    </form>
    </body>
    </html>
    '''


def app(environ, start_response):
    html = form

    if environ['REQUEST_METHOD'] == 'POST':
        post_env = environ.copy()
        post_env['QUERY_STRING'] = ''
        post = cgi.FieldStorage(
                                fp=environ['wsgi.input'],
                                environ=post_env,
                                keep_blank_values=True
                                )
        query = "SELECT english || ' ' || spanish FROM Translation \
        WHERE english=?;"
        connection = sqlite3.connect('translation.db')
        connection.text_factory = str
        cursor = connection.cursor()
        input_text = post.getlist("textinput")
        cursor.execute(query, input_text)
        results = [r[0] for r in cursor.fetchall()]
        cursor.close()
        connection.close()
        html = b'Translate, ' + str(results) + '.'
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [html]


if __name__ == '__main__':
    try:
        from wsgiref.simple_server import make_server
        httpd = make_server('', 8080, app)
        print('Serving on port 8080...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Goodbye.')
