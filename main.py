from pathlib import Path
from Parser.parser import save_json, get_html, get_list_genre, get_data_from_site


if __name__ == '__main__':
    # print(get_list_genre('https://litnet.com'))
    data = get_data_from_site('https://litnet.com')
    save_json(Path(__file__).parent.absolute().joinpath('File/data.json'), data)
