import os

def create_post_in_obsidian():
    print("* step 1: create post in Obsidian")
    print("")
    print("checklist:")
    print("- post should be kept in posts folder")
    print("- there's a newline after each header")
    print("- there's a newline before starting a list")
    print("- images are added as ![](/static/images/posts/{postName}/{imageName}.{extension})")
    print("    the postname has dashes instead of spaces")
    print("    make sure you use /static and not static or the images won't load in the web app later on")
    print("")
    input("Press Enter when you have created the post in Obsidian...")
    
def copy_obsidian_post_to_weblog_repo():
    os.system('clear') # if not the terminal will be cluttered with the previous steps
    print("* step 2: copy Obsidian post (and images used in the post) to weblog repo")
    print("")
    print("checklist:")
    print("- Markdown post should be copied to the posts folder")
    print("- images should be copied to the static/images/posts/{postName} folder")
    print("")
    input("Press Enter when you have copied the post to the weblog repo...")

def main():
    # run steps in sequence
    create_post_in_obsidian()
    copy_obsidian_post_to_weblog_repo()
    
    os.system('clear')

if __name__ == "__main__":
    main()