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


def get_soup(url: str):
    """
    Get object BeautifulSoup
    :param url: Url page
    :return: BeautifulSoup object
    """
    return BeautifulSoup(get_html(url), 'lxml')


def get_main_info_book(base_url: str, book_item: object):
    """
    Function get data from book item
    :param base_url: Base url
    :param book_item: BeautifulSoup object
    :return: Dictionary with data from BeautifulSoup object
    """
    data = {}
    a = book_item.find('h4').find('a')
    data_main = book_item.find('p', class_='author-wr')
    authors_a = data_main.find_all('a', class_='author')
    data['title'] = a.text
    data['author'] = [{
        'author_name': author_a.text,
        'author_page': base_url + author_a.get('href')
    } for author_a in authors_a]
    data['book_url'] = base_url + a.get('href')
    data['description'] = book_item.text
    data['number_pages'] = int((book_item.find('span', class_='book-status').find('span').text).split()[0])
    tags = book_item.find('p', class_='tags-wr').find_all('a')
    data['book_tags'] = [tag.text for tag in tags]
    data['views'] = int(book_item.find('span', class_='count-views').text)
    data['favourites'] = int(book_item.find('span', class_='count-favourites').text)
    return data


def get_rating_book(meta_info: object):
    """
    Function get rating book
    :param meta_info: BeautifulSoup object
    :return: Rating book
    """
    p = meta_info.find('p')
    return int(p.text.split()[2])


def get_data_from_url(base_url: str, url_page: str, genre: str, type_book: str):
    """
    Get all links from page
    :param base_url: Base url
    :param url_page: Url current page
    :param genre: Genre book
    :param type_book: Type book
    :return: List links
    """
    soup = get_soup(url_page)
    book_items = soup.find('div', class_='content').find_all('div', class_='row book-item')
    data = []

    for book_item in book_items:
        try:
            main_info = book_item.find('div', class_='col-xs-7')
            book_info = get_main_info_book(base_url, main_info)
            book_info['rating'] = get_rating_book(book_item.find('div', class_='col-xs-3 meta-info'))
            book_info['genre'] = genre
            book_info['type_book'] = type_book
            data.append(book_info)
        except Exception as exp:
            print(url_page)

            continue
    return data


def get_data_from_site(base_url: str):
    genres = get_list_genre(base_url)
    data = []
    for genre in genres:
        for page_number in range(1, 10):
            data += get_data_from_url(base_url, genres[genre] + f'?page={page_number}', genre, 'Entertainment_book')
    return data


def get_list_genre(base_url: str):
    """
    Function get dictionary genre with url
    :param base_url: Base url
    :return: Dictionary with url
    """
    genre = {}
    soup = get_soup(base_url)
    genres_a = soup.find('div', class_='ln_topbar_genres_list').find_all('a')
    for a in genres_a:
        genre[a.text] = base_url + a.get('href')
    if 'Все жанры' in genre:
        del genre['Все жанры']
    return genre


def save_json(path: Path, books: list):
    """
    Save data in JSON file
    :param path: Path to save
    :param books: List books data
    """
    with open(path, 'w', encoding='utf-8') as fout:
        json.dump(books, fout, ensure_ascii=False)

