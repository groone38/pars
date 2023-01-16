import requests
from bs4 import BeautifulSoup

# URL = 'https://krasnodar.hh.ru/search/vacancy?L_save_area=true&text=python&excluded_text=&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=100'
URL = 'https://krasnodar.hh.ru/search/vacancy?L_save_area=true&text=python&excluded_text=&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=100'
headers = {
    # 'Host': 'hh.ru',
    'User-Agent': 'Safari',
    # 'Accept': '*/*',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Connection': 'keep-alive',
}


def extract_max_pages():

    hh_requests = requests.get(URL, headers=headers)

    soup = BeautifulSoup(hh_requests.text, 'html.parser')

    pages = []

    paginator = soup.find_all(
        "span", {'class': 'pager-item-not-in-short-range'})
    for page in paginator:
        pages.append(int(page.find('a').text))

    return pages[-1]


def extreact_job(html, page):
    title = html.find('a').text
    link = html.find('a')['href']
    company = html.find(
        'div', {'class': 'vacancy-serp-item__meta-info-company'}).find('a').text
    company = company.strip()
    location = html.find(
        'div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
    location = location.partition(',')[0]
    return {'title': title, 'company': company, 'location': location, 'link': link, 'page': page}


def extract_hh_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(
            f'{URL}&page={page}&hhtmFrom=vacancy_search_list', headers=headers)
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all(
            "div", {'class': 'serp-item'})
        for result in results:
            job = extreact_job(result, page)
            jobs.append(job)
    return jobs
