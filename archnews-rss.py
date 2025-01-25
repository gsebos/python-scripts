import feedparser
from bs4 import BeautifulSoup
import re
from datetime import datetime


def remove_tags_from_elem(elem):
        elem_no_tags = BeautifulSoup(elem,features="html.parser")
        # True matches all tags
        tags = elem_no_tags.find_all(True)
        for tag in tags:
            tag.unwrap()
        return elem_no_tags.text

def re_format_date(date):
    # Original date string
    date_string = date
    # Parse the original string into a datetime object
    date_obj = datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S +0000")
    # Format the datetime object to your desired format
    # change it to "15-04-2024 06:56"
    formatted_date = date_obj.strftime("%d-%m-%Y %H:%M")
    # Print the formatted date string
    return formatted_date


def main():
    rss = feedparser.parse('https://archlinux.org/feeds/news/')
    for i,item in enumerate(rss.entries[:5]):
        title = remove_tags_from_elem(item.title)
        link = item.link
        description = remove_tags_from_elem(item.description)
        date = remove_tags_from_elem(item.published)

        output = ''
        output += re_format_date(date)
        output += ' - '
        output += title
        output += "\n"
        if i == 0:
            output += "\n"
            output += description
            output += "\n\n"
        output += link
        output += "\n"
        output += "===================================="

        print(output)

if __name__ == "__main__":
    main()
