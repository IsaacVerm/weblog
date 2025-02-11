import os

def create_post_in_obsidian():
    print("* step 1: create post in Obsidian")
    print("")
    print("checklist:")
    print("- post should be kept in posts folder")
    print("- there's a newline after each header")
    print("- there's a newline before starting a list")
    print("- images are added as ![](/static/images/posts/{postNameDashes}/{imageName}.{extension})")
    print("    example postNameDashes: how-to-use-llms-for-learning-a-language-fr")
    print("    make sure you use /static and not static or the images won't load in the web app later on")
    print("")
    input("Press Enter when you have created the post in Obsidian...")
    
def copy_obsidian_post_to_weblog_repo():
    os.system('clear') # if not the terminal will be cluttered with the previous steps
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

def main():
    # run steps in sequence
    create_post_in_obsidian()
    copy_obsidian_post_to_weblog_repo()
    convert_markdown_post_to_html()
    
    os.system('clear')

if __name__ == "__main__":
    main()