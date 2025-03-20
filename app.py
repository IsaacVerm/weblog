from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def show_index():
    return send_from_directory('static/pages', 'posts_overview_public.html')

@app.route('/linkfest')
def show_linkfest():
    return send_from_directory('static/pages', 'linkfest.html')

@app.route('/posts/<post_name>')
def show_post(post_name):
    # using f-string to avoid having to use the complete filename in the url
    # now you don't have to specify the .html extension in the url yourself
    # e.g. /posts/first-post instead of /posts/first-post.html
    return send_from_directory('static/posts', f'{post_name}.html')

@app.route('/data/<filename>')
def get_data(filename):
    return send_from_directory('static/data', f'{filename}.json', mimetype='application/json')