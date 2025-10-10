import requests
from bs4 import BeautifulSoup
import random
import argparse

def get_from_file(file):
    poem_string = ""
    with open(file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

        poems = soup.find_all('p',class_='grommetux-paragraph grommetux-paragraph--large grommetux-paragraph--margin-medium')
        poem_arr = [poem for poem in poems]
        
        for line in random.choice(poem_arr):
            poem_string += (line.text + "\n")
    
    return poem_string

def get_from_website(URL):
    poem_string = ""
    try:
        response = requests.get(URL)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        exit()

    if response.status_code == 200:
        html = response.content
        soup = BeautifulSoup(html,features="html.parser")
        poems = soup.find_all('p',class_='grommetux-paragraph grommetux-paragraph--large grommetux-paragraph--margin-medium')

        # Save code here optionally

        for line in random.choice(poems):
            poem_string += (line.text + "\n")

    else:
        print(f"Error, response status code {response.status_code}")
    
    return poem_string

def main():

    parser = argparse.ArgumentParser(
    prog="Havamal poem picker",
    description="outputs a random poem from Havamal"
    )
    
    parser.add_argument("--url", type = str , default = "https://havamal.se/")
    parser.add_argument("--file", type = str , default = "/home/seb/python-scripts/havamal.html")
    parser.add_argument("--web",action='store_true')
    parser.set_defaults(web=False)
    args = parser.parse_args()

    if args.web:
        poem = get_from_website(args.url)
    else:
        poem = get_from_file(args.file)

    print(poem)

if __name__ == "__main__":
    main()


### Notes

        # Save as html
        
        # with open('havamal.html', 'w', encoding='utf-8') as f:
        #     for poem in poems:
        #         f.write(str(poem) + "\n")

        # can be recovered with

        # with open("result.html", "r", encoding="utf-8") as f:
        #     soup = BeautifulSoup(f, "html.parser")
        #     result_set = soup.find_all("tagname") 


        # Write out the whole text to file with line breaks 

        # with open('havamal.txt', 'w', encoding='utf-8') as f:
        #     for poem in poem_arr:
        #         for line in poem:
        #             f.write(line.text + '\n')
        #         f.write('\n')