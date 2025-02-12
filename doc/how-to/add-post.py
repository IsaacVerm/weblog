import os

def ask_for_post_name():
    os.system('clear') # if not the terminal will be cluttered with the previous steps
    print("* step 0: what's the name of your post?")
    print("")
    post_name_natural = input("Type the name of your post.")
    post_name_kebab_case = post_name_natural.lower().replace(" ", "-")
    post_names = {'natural language': post_name_natural, 'kebab_case': post_name_kebab_case}
    return post_names

def create_post_in_obsidian(post_name_kebab_case):
    os.system('clear')
    print("* step 1: create post in Obsidian")
    print("")
    print("checklist:")
    print("- post should be kept in posts folder")
    print("- there's a newline after each header")
    print("- there's a newline before starting a list")
    print(f"- images are added as ![](/static/images/posts/{post_name_kebab_case}/{{image_name}}.{{extension}})")
    print("    make sure you use /static and not static or the images won't load in the web app later on")
    print("")
    input("Press Enter when you have created the post in Obsidian...")
    
def copy_obsidian_post_to_weblog_repo():
    os.system('clear')
    print("* step 2: copy Obsidian post (and images used in the post) to weblog repo")
    print("")
    print("checklist:")
    print("- Markdown post should be copied to the posts folder")
    print("- images should be copied to the static/images/posts/{postNameDashes} folder")
    print("")
    input("Press Enter when you have copied the post to the weblog repo...")
    
def convert_markdown_post_to_html():
    os.system('clear')
    print("* step 3: convert Markdown post to html")
    print("")
    print("(assuming you're in the root of the weblog repo)")
    print("command: pandoc posts/{postNameDashes}.md -o posts/{postNameDashes}.html")
    print("After running the command a HTML file of the Markdown post should be created in the posts folder.")
    input("Press Enter when you have converted the Markdown post to HTML...")
    
def add_toc_to_html_post():
    os.system('clear')
    print("* step 4: add table of contents to HTML post")
    print("")
    print("open LibreChat")
    print("copy the HTML of the post into LibreChat")
    print("run this prompt:")
    print("Create a HTML table of contents for the HTML above. Returning nothing else but the HTML.")
    print("add HTML returned by LLM after <h1> tag in HTML post")
    input("Press Enter when you have added the table of contents to the HTML post...")
    
def check_post_served_by_web_server():
    os.system('clear')
    print("* step 5: run web server in Docker")
    print("")
    print("command: docker build -t weblog .")
    print("command: docker run -p 8000:8000 weblog")
    print("open http://0.0.0.0:8000/posts/{postNameDashes} in your browser")
    print("checklist:")
    print("- post visible in the browser")
    print("- images displayed correctly")
    print("- table of contents displayed correctly")
    print("- no major layout issues")
    
    input("Press Enter when you have run the web server and checked the post in the browser...")

def main():
    # run steps in sequence
    post_names = ask_for_post_name()
    create_post_in_obsidian(post_names['kebab_case'])
    copy_obsidian_post_to_weblog_repo()
    convert_markdown_post_to_html()
    add_toc_to_html_post()
    check_post_served_by_web_server()
    
    os.system('clear')

if __name__ == "__main__":
    main()