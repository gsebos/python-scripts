import requests
from bs4 import BeautifulSoup
import re
import random
import tkinter as tk
from tkinter import ttk
import argparse

class Quote:
    def __init__(self, gui:bool):
        self.gui = gui
        if self.gui:
            self.root = tk.Tk()
            self.title = self.root.title("linus_quotes")
            self.root.wait_visibility(self.root)
            self.root.attributes("-alpha", 0.9)
            self.label = ttk.Label(self.root,text=self.get_rand_quote(),wraplength=500,justify="left",font=("JetBrainsMonoNL NFP SemiBold",12))
            self.label.pack(padx=50,pady=50)
            self.root.after(15000,self.update_quote)
            self.root.mainloop()
        self.get_rand_quote()

    def get_rand_quote(self):
        quotes = []
        random_page = random.randint(1,9)
        URL = f"https://www.azquotes.com/author/14737-Linus_Torvalds?p={random_page}"
        request = requests.get(URL)
        html = request.content
        soup = BeautifulSoup(html,features="html.parser")
        links = soup.find_all("a",id = re.compile("title_quote_link*"))

        for link in links:
            quotes.append(link.string)

        quote_text = quotes[random.randrange(0,len(quotes))]

        if self.gui:
            return quote_text
        else:
            print(quote_text)


    def update_quote(self):
        quote_text = self.get_rand_quote()
        self.label.config(text=str(quote_text))
        self.root.after(15000, self.update_quote)  



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gui",action='store_true')
    parser.add_argument("--no-gui",dest='gui',action='store_false')
    parser.set_defaults(gui=True)
    args = parser.parse_args()
    gui = args.gui

    programme = Quote(gui)

if __name__ == "__main__":
    main()