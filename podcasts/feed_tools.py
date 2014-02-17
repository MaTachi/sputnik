from bs4 import BeautifulSoup
import feedparser
from urllib.request import urlopen


def get_podcast_data(feed):
    feed_xml = urlopen(feed).read()

    feed = feedparser.parse(feed_xml).feed
    soup = BeautifulSoup(feed_xml)
    response = {
        'title': feed.title,
        'description': feed.subtitle,
        'link': feed.link,
        'language': __get_language(feed),
        'tags': __get_tags(feed),
        'image': getattr(getattr(feed, 'image', None), 'href', None),
        'categories': __get_categories(soup),
    }
    return response


def __get_language(feed):
    return feed.language[:2]


def __get_categories(soup):
    categories = {}
    for each in soup.find_all('itunes:category'):
        category = each['text']
        subcategories = []
        for each in each.find_all('itunes:category'):
            subcategory = each['text']
            subcategories.append(subcategory)
        categories.update({category: subcategories})
    return categories


def __get_tags(feed):
    try:
        return [tag.term for tag in feed.tags]
    except AttributeError:
        return []
