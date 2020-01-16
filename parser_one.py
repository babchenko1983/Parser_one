import requests
import csv
from bs4 import BeautifulSoup as bs

base_url = 'https://www.work.ua/jobs-python//'


def parse(base_url):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url)
    if request.status_code == 200:
        request = session.get(base_url)
        soup = bs(request.content, 'html.parser')
        try:
            pag = soup.find('ul', class_='pagination hidden-xs')
            pig = pag.find_all('li')
            count = int(pig[-2].text)
            for i in range(count):
                url = f'https://www.work.ua/jobs-python/3/?page={i+1}'
                urls.append(url)
                # if url not in urls:

        except:
            pass
    for url in urls:
        request = session.get(url)
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', class_='card card-hover card-visited wordwrap job-link')
        for div in divs:
            title = (div.a['title'])
            href = 'https://work.ua' + (div.a['href'])
            company = div.span.text
            disc = div.p.text
            jobs.append({'title': title,
                         'href': href,
                         'company': company,
                         'disc': disc})


    else:
        print('ERROR or DONE. Status_code =' + str(request.status_code))

        return jobs

def files_writer(jobs):
    with open('parsed_jobs.csv', 'w', encoding='utf-8') as file:
        pen = csv.writer(file)
        pen.writerow(('Название вакансии', 'URL', 'Название компании', 'Описание'))
        for i in jobs:
            pen.writerow((i['title'], i['href'], i['company'], i["disc"]))


jobs = parse(base_url)
files_writer(jobs)
