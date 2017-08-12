# Scrapes transcripts of each episode from the Phineas and Ferb wiki.
# Looks for the urls in 'transcripts/season_X_urls.txt'

# Import things
from bs4 import BeautifulSoup
import requests


def get_html_page(url):
    r = requests.get(url)
    return r.text

def isolate_script(script_file, html_file):
    soup = BeautifulSoup(html_file, 'html.parser')
    f = open(script_file, 'w')
    script_html = soup.find(id='mw-content-text')
    f.write(script_html.get_text())
    f.close()
    return script_file

def scrape(season_number):
    urls_file = open('transcripts/season_' + str(season_number) + '_urls.txt', 'r')
    episode = 1
    for line in urls_file:
        script_file = 'transcripts/season_' + str(season_number) + '/episode' + str(episode) + '.txt'
        url = line.rstrip() + '/Transcript'
        isolate_script(script_file, get_html_page(url))
        print('downloaded ' + script_file)
        episode += 1
    urls_file.close()

for season_number in range(1, 5):
    scrape(season_number)
