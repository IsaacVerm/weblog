import os

def ask_for_post_name():
    os.system('clear') # if not the terminal will be cluttered with the previous steps
    print("* STEP 0: what's the name of your post?")
    print("")
    post_name_natural = input("Type the name of your post:\n\n")
    post_name_kebab_case = post_name_natural.lower().replace(" ", "-")
    post_names = {'natural_language': post_name_natural, 'kebab_case': post_name_kebab_case}
    return post_names

def create_post_in_obsidian(post_name_kebab_case, post_name_natural):
    os.system('clear')
    print("* STEP 1: create post in Obsidian")
    print("")
    print("CHECKLIST:")
    print(f"- post is kept at /static/posts/{post_name_natural}.md (.md added automatically by Obsidian) in the Obsidian vault")
    print(f"- images are kept in the /static/images/posts/{post_name_kebab_case} folder in the Obsidian vault")
    print("- there's a newline after each header")
    print("- there's a newline before starting a list")
    print(f"- images are added as ![](/static/images/posts/{post_name_kebab_case}/{{image_name}}.{{extension}})")
    print("")
    print("Make sure to use /static and not static or the post and images won't load in the web app later on.")
    print("")
    input("Press Enter when you have created the post in Obsidian...")
    
def copy_obsidian_post_to_weblog_repo(post_name_kebab_case):
    os.system('clear')
    print("* STEP 2: copy Obsidian post (and images used in the post) to weblog repo")
    print("")
    print("CHECKLIST:")
    print("- Markdown post should be copied to the posts folder")
    print(f"- images should be copied to the static/images/posts/{post_name_kebab_case} folder")
    print("")
    input("Press Enter when you have copied the post to the weblog repo...")
    
def convert_markdown_post_to_html(post_name_kebab_case):
    os.system('clear')
    print("* STEP 3: convert Markdown post to html")
    print("")
    print("(assuming you're in the root of the weblog repo)")
    print(f"COMMAND: pandoc posts/{post_name_kebab_case}.md -o posts/{post_name_kebab_case}.html")
    print("")
    print("After running the command a HTML file of the Markdown post should be created in the posts folder.")
    print("")
    input("Press Enter when you have converted the Markdown post to HTML...")
    
def add_toc_to_html_post():
    os.system('clear')
    print("* STEP 4: add table of contents to HTML post")
    print("")
    print("- open LibreChat")
    print("- copy the HTML of the post into LibreChat")
    print("- run this prompt: Create a HTML table of contents for the HTML above. Returning nothing else but the HTML.")
    print("- add HTML returned by LLM after <h1> tag in HTML post")
    print("")
    input("Press Enter when you have added the table of contents to the HTML post...")
    
def check_post_served_by_web_server(post_name_kebab_case):
    os.system('clear')
    print("* STEP 5: run web server in Docker")
    print("")
    print("(assuming you have Docker installed and running)")
    print("COMMAND: docker build -t weblog .")
    print("COMMAND: docker run -p 8000:8000 weblog")
    print("")
    print(f"Open http://0.0.0.0:8000/posts/{post_name_kebab_case} in your browser to check if the post is displayed correctly.")
    print("")
    print("CHECKLIST:")
    print("- post visible in the browser")
    print("- images displayed correctly")
    print("- table of contents displayed correctly")
    print("- no major layout issues")
    print("")
    input("Press Enter when you have run the web server and checked the post in the browser...")
    
def commit_post_to_github(post_name_natural_language):
    os.system('clear')
    print("* STEP 6: commit post to GitHub")
    print("")
    print("Don't create a separate issue/merge request for adding a post. Just commit it directly to the main branch.")
    print("")
    print("(assuming you're on the main branch)")
    print("COMMAND: git add -a")
    print(f"COMMAND: git commit -m 'add post {post_name_natural_language}'")
    print("COMMAND: git push")
    print("")
    print("The commit of the post should be visible on the weblog repo page on GitHub.")
    print("")
    input("Press Enter when you have committed the post to GitHub...")
          
def main():
    # run steps in sequence
    post_names = ask_for_post_name()
    create_post_in_obsidian(post_names['kebab_case'], post_names['natural_language'])
    copy_obsidian_post_to_weblog_repo(post_names['kebab_case'])
    convert_markdown_post_to_html(post_names['kebab_case'])
    add_toc_to_html_post()
    check_post_served_by_web_server(post_names['kebab_case'])
    commit_post_to_github(post_names['natural_language'])
    
    os.system('clear')
    
    print("Post has been added.")

if __name__ == "__main__":
    main()