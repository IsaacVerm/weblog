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
    input("Press Enter when you have created the post in Obsidian...")

def main():
    print("Starting weblog post process...")
    
    # Run steps in sequence
    create_post_in_obsidian()
    
    print("Process completed!")

if __name__ == "__main__":
    main()