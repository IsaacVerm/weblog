from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS 
import json
import os

app = Flask(__name__)

CORS(app)

LINKS_JSON_PATH = os.path.expanduser("~/Documents/index/projects/weblog/static/data/links.json")

@app.route('/add-link', methods=['POST'])
def add_link():
    # if anything goes wrong, just return the error so you can debug it
    try:
        # get the link data from the request
        link_data = request.json
        
        # read the existing links.json file
        with open(LINKS_JSON_PATH, 'r', encoding='utf-8') as file:
            links = json.load(file)
        
        # add the new link to the beginning of the list
        links.insert(0, link_data)
        
        # write back to links.json
        # indent=4 for better readability, that's also how the file is formatted when you format it in VSCode
        # ensure_ascii=False makes sure non-English text isn't converted
        with open(LINKS_JSON_PATH, 'w', encoding='utf-8') as file:
            json.dump(links, file, indent=4, ensure_ascii=False)
        
        return jsonify({'success': True, 'message': 'Link added successfully'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/')
def show_index():
    return send_from_directory('static/pages', 'posts_overview_public.html')

@app.route('/private')
def show_private_index():
    return send_from_directory('static/pages', 'posts_overview_private.html')

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