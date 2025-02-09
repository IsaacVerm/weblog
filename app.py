from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def show_index():
    return render_template('index.html')

@app.route('/posts/<post_name>/<image_name>')
def get_image_post(post_name, image_name):
    # since this is an API call I use the HTTP verb convention so get_image_post is appropriate
    # this is separate from the show_post function because in that function I don't specify the extension
    # in contrast, for images I want to specify the extension
    # images can be jpg, png, ...
    # while posts can only be HTML
    return send_from_directory(f'posts/{post_name}', image_name)

@app.route('/posts/<post_name>')
def show_post(post_name):
    # using f-string to avoid having to use the complete filename in the url
    # now you don't have to specify the .html extension in the url yourself
    # e.g. /post/first-post instead of /post/first-post.html
    # each post is stored in a folder with the same name as the post
    # for posts without images this is overkill but a folder is necessary for posts with images
    # you don't want images from different posts in the same folder
    # to be consistent for all posts, we use a folder for all posts
    return send_from_directory(f'posts/{post_name}', f'{post_name}.html')