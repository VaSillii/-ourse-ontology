import requests
import json
from pathlib import Path
from bs4 import BeautifulSoup


def get_html(url: str):
    """
    Function get html file
    :param url: URL- site
    :return: HTML-frile
    """
    req = requests.get(url)
    return req.text


def get_main_info_book(base_url: str, book_item: object):
    """
    Function get data from book item
    :param base_url: Base url
    :param book_item: BeautifulSoup object
    :return: Dictionary with data from BeautifulSoup object
    """
    data = {}
    a = book_item.find('h4').find('a')
    author_a = book_item.find('p', class_='author-wr').find('a', class_='author')
    data['title'] = a.text
    data['author'] = {
        'author_name': author_a.text,
        'author_page': base_url + author_a.get('href')
    }
    data['book_url'] = base_url + a.get('href')
    tags = book_item.find('p', class_='tags-wr').find_all('a')
    data['book_tags'] = [tag.text for tag in tags]
    return data


def get_rating_book(meta_info: object):
    """
    Function get rating book
    :param meta_info: BeautifulSoup object
    :return: Rating book
    """
    p = meta_info.find('p')
    return int(p.text.split()[2])


def get_data_from_url(base_url: str, html: str):
    """
    Get all links from page
    :param base_url: Base url
    :param html: Html file
    :return: List links
    """
    soup = BeautifulSoup(html, 'lxml')
    book_items = soup.find('div', class_='content').find_all('div', class_='row book-item')
    data = []

    for book_item in book_items:
        main_info = book_item.find('div', class_='col-xs-7')
        book_info = get_main_info_book(base_url, main_info)
        book_info['rating'] = get_rating_book(book_item.find('div', class_='col-xs-3 meta-info'))
        data.append(book_info)
    return data


def save_json(path: str, books: list):
    """
    Save data in JSON file
    :param path: Path to save
    :param books: List books data
    """
    with open(path, 'w', encoding='utf-8') as fout:
        json.dump(books, fout, ensure_ascii=False)

