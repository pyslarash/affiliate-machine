def surferseo_fit():
    min_words = int(input("What is the MIN amount of words do you need? "))
    max_words = int(input("What is the MAX amount of words do you need? "))
    min_headings = int(input("What is the MIN amount of headings do you need? "))
    max_headings = int(input("What is the MAX amount of headings do you need? "))
    min_paragraphs = int(input("What is the MIN amount of paragraphs do you need? "))
    post_title = input("What is the post title name? ")
    directory_name = input("Please, provide the name of the directory in 'inputs' directory: ")
    return min_words, max_words, min_headings, max_headings, min_paragraphs, post_title, directory_name

def main():
    (min_words, max_words, min_headings, max_headings, min_paragraphs, post_title, directory_name) = surferseo_fit()

# If this script is being executed as the main program, run the main function
if __name__ == "__main__":
    main()