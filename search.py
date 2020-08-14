'''
Conduct inline google search in alfred
'''
import re
import json
import os
from sys import argv, stdout
import urllib
from requests_html import HTMLSession, HTMLResponse


def makeItem(query, url, title, subtitle):
    '''
    Parse input into alfred display item
    '''
    icon = "icon.png"
    item = {
        'uid': url,
        'title': title,
        'subtitle': subtitle,
        'arg': url,
        'autocomplete': query,
        'icon': {
            'path': icon
        }
    }
    return item


def makeReturn(items):
    '''
    Return final list of items
    '''
    out = {'items': items}
    return out


def get_search_results(url: str):
    '''
    Retrieve results from google
    '''
    session = HTMLSession()
    r: HTMLResponse = session.get(url)
    titles = [item.text for item in r.html.xpath("//div[@class='r']/a/h3")]
    links = r.html.xpath("//div[@class='r']/a/@href")
    texts = [item.text for item in r.html.xpath("//span[@class='st']")]
    return titles, links, texts


def main():
    arg_c = len(argv)
    if arg_c <= 1:
        return makeReturn([])
    query = argv[1]
    if not query:
        return makeReturn([])
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    titles, links, texts = get_search_results(url)
    item = [
        makeItem(query, link, title, text)
        for title, link, text in zip(titles, links, texts)
    ]
    out = makeReturn(item)
    return json.dumps(out, indent=4) + '\n'


if __name__ == "__main__":
    results = main()
    stdout.write(results)
