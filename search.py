'''
Conduct inline google search in alfred
'''
import re
import json
import os
from sys import argv, stdout
import urllib
import asyncio
from itertools import chain
import concurrent.futures as cf
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
    '''
    Main function to produce output for alfred workflow
    '''
    arg_c = len(argv)
    if arg_c <= 1:
        return makeReturn([])
    query = argv[1]
    if not query:
        return makeReturn([])
    encoded_query = urllib.parse.quote(query)
    pages = range(0, 50, 10)
    urls = [
        f"https://www.google.com/search?q={encoded_query}&start={page}"
        for page in pages
    ]

    async def search():
        '''
        async function to gather search results
        '''
        with cf.ThreadPoolExecutor(max_workers=8) as executor:
            loop = asyncio.get_event_loop()
            futures = (loop.run_in_executor(executor, get_search_results, url)
                       for url in urls)
            async_results = await asyncio.gather(*futures)
            titles = [title for item in async_results for title in item[0]]
            links = [link for item in async_results for link in item[1]]
            texts = [text for item in async_results for text in item[2]]
        return titles, links, texts

    loop = asyncio.get_event_loop()
    titles, links, texts = loop.run_until_complete(search())
    item = [
        makeItem(query, link, title, text)
        for title, link, text in zip(titles, links, texts)
    ]
    out = makeReturn(item)
    return json.dumps(out, indent=4) + '\n'


if __name__ == "__main__":
    results = main()
    stdout.write(results)
