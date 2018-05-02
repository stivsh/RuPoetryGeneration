import requests
from bs4 import BeautifulSoup
import multiprocessing
import pickle
from tqdm import tqdm

def load_poem(link):
    poem_html = requests.get(link).text
    poem_soup = BeautifulSoup(poem_html, 'html.parser')
    poem_text = poem_soup.find('div', class_='poem-text').text.replace('\r','')
    poem_sourse = poem_soup.find('div', class_='poemsource')
    if poem_sourse:
        poem_sourse = poem_sourse.text.replace('\n','').replace('\r','')
    else:
        poem_sourse = None
    name = poem_soup.find('h1', class_='poemtitle').text.replace('\n','').replace('\r','')

    return {
        'name':name,
        'source':poem_sourse,
        'text':poem_text
    }

def load_data():
    html_doc=requests.get('http://rupoem.ru/love.aspx').text
    html_doc = html_doc.replace('\r\n',' ')

    soup = BeautifulSoup(html_doc, 'html.parser')
    author_urls = [ 'http://rupoem.ru'+link.get('href') for link in soup.find_all('a')[5:-47] ]

    links_to_poems = []
    for auth_url in tqdm(author_urls):
        auth_doc=requests.get(auth_url).text
        auth_soup = BeautifulSoup(auth_doc, 'html.parser')
        poetry_table = auth_soup.find_all('table', class_ = 'catlink')
        if poetry_table:
            for link in poetry_table[0].find_all('a'):
                links_to_poems.append('http://rupoem.ru'+link.get('href'))


    pool = multiprocessing.Pool()
    poems = pool.map(load_poem, links_to_poems)

    with open('data/poems.pkl', 'wb') as f:
        pickle.dump(poems, f)
      
    print("Words loaded: ", sum([ len(p['text'].split()) for p in poems ]) )
        
if __name__ == "__main__":        
    load_data()