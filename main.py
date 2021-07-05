import datetime
import json

import requests
from bs4 import BeautifulSoup

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

r = requests.get('https://www.trustpilot.com/categories/financial_consultant', headers=headers)

soup = BeautifulSoup(r.text, 'lxml')

results_amount = int(soup.find('b', class_='styles_categoryFilteredResultsBold__7x0f4').text.split(' ')[3])

pages_amount = results_amount // 20

last_page_tail = results_amount % 20


def main():
    result = []
    for i in range(1, pages_amount + 1):
        page_url = f'https://www.trustpilot.com/categories/financial_consultant?page={i}'
        req = requests.get(page_url, headers)
        soup = BeautifulSoup(req.text, 'lxml')
        tags = soup.find_all('a', class_='link_internal__YpiJI link_wrapper__LEdx5')
        for tag in tags:
            if 'https:' not in tag.get('href'):
                url = f'https://www.trustpilot.com/{tag.get("href")}'
                req = requests.get(url, headers)
                soup = BeautifulSoup(req.text, 'lxml')
                domain_part1 = soup.find('span', class_='smart-ellipsis__prefix')
                domain_part2 = soup.find('span', class_='smart-ellipsis__suffix')
                domain = domain_part1.text + domain_part2.text
                name = soup.find('span', class_='multi-size-header__big').text.replace('  ', '').replace('\n', '')
                rating = soup.find('p', class_='header_trustscore').text
                obj_dict = {
                    'domain': domain,
                    'name': name,
                    'rating': rating
                }
                result.append(obj_dict)
        print(f'LOG[INFO]: {i}/{pages_amount+1} pages passed')

    if last_page_tail != 0:
        page_url = f'https://www.trustpilot.com/categories/financial_consultant?page={pages_amount + 1}'
        req = requests.get(page_url, headers)
        soup = BeautifulSoup(req.text, 'lxml')
        tags = soup.find_all('a', class_='link_internal__YpiJI link_wrapper__LEdx5')
        for i in range(last_page_tail):
            if 'https:' not in tags[i].get('href'):
                url = f'https://www.trustpilot.com/{tags[i].get("href")}'
                req = requests.get(url, headers)
                soup = BeautifulSoup(req.text, 'lxml')
                domain_part1 = soup.find('span', class_='smart-ellipsis__prefix')
                domain_part2 = soup.find('span', class_='smart-ellipsis__suffix')
                domain = domain_part1.text + domain_part2.text
                name = soup.find('span', class_='multi-size-header__big').text.replace('  ', '').replace('\n', '')
                rating = soup.find('p', class_='header_trustscore').text
                obj_dict = {
                    'domain': domain,
                    'name': name,
                    'rating': rating
                }
                result.append(obj_dict)
        print(f'LOG[INFO]: {pages_amount + 1}/{pages_amount+1} pages passed')

    current_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    with open(f'data_{current_time}.json', 'a') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()