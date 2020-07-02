import requests
import click
import csv
from bs4 import BeautifulSoup

@click.command()
@click.option("--url", help="URL of the newsletter")
@click.option("--csv_file", default="out.csv", help="CSV where data will be stored")
def main(url, csv_file):
    click.echo(f"Getting data from {url}")
    req = requests.get(url)
    if (req.status_code != 200):
        print(f"Error on requests with URL {url} - {req.status_code}")
        quit()

    links = parse_all_links(req.text)
    title = parse_img(req.text)
    print(f"Title: {title}")
    with open(csv_file, 'w', newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for link in links:
            csv_writer.writerow([
                title,
                link.get('book_title'),
                link.get('href'),
                link.get('tag')
            ])

    print(f"File: {csv_file} with {len(links)} links")

def parse_img(html):
    soup = BeautifulSoup(html, 'html.parser')
    first_image = soup.find_all("img", alt=True)[0]
    return first_image["alt"]

def get_all_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('a')

def parse_all_links(html):
    books = []
    all_links = get_all_links(html)
    for link in all_links:
        l = requests.get(link.get('href'))
        if ('amazon.com.br') in l.url:
            print(f'Request to {l.url}')
            url_split = l.url.split("&tag=")
            tag = '' if ('http' in url_split[-1]) else url_split[-1] 
            book = {
                'href': l.url, 
                'book_title': link.get('title').encode('utf8').decode('utf8'),
                'tag': tag
            }
            print(book)
            books.append(book)

    return books

if __name__ == "__main__":
    main()
