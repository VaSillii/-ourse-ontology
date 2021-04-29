from pathlib import Path
from Parser.parser import get_data_from_url, save_json, get_html


if __name__ == '__main__':
    url = r'https://litnet.com/ru/top/all?alias=all&page=2'
    url = r'https://litnet.com/ru/top/detektivy'
    url = r'https://litnet.com/ru/top/fantastika'
    data = get_data_from_url('https://litnet.com/', get_html(url))
    save_json(Path(__file__).parent.absolute().joinpath('File\\data.json'), data)