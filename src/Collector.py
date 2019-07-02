from urllib import request
import json
import requests
from bs4 import BeautifulSoup
from src.PrintLog import pl
from src.PrintLog import pld


##### Search News List #####
def get_news_list(keyword, page_max, verbose=True):
    article_url_list = []
    for page in range(page_max):
        i = page * 15 + 1
        pl("Fetching page: " + str(page+1) + "...  ", verbose)

        # build query string
        query_url = build_keyword_search_query(keyword, i)

        # get raw html
        query = requests.get(query_url, headers={'User-Agent': 'Mozilla/5.0'}).text
        html = BeautifulSoup(query, "html.parser")

        # get naver news page tags (only naver pages, exclude other publisher pages)
        articles = html.find_all('div', attrs={"class", "news_dsc"})

        # get urls for each tag
        for article in articles:
            if 'm.news' in article.find('a')['href']:
                article_url_list += [article.find('a')['href']]
        pld(verbose)
    return article_url_list


def build_keyword_search_query(keyword, i):
    query_url = 'https://m.search.naver.com/search.naver?where=m_news&query='+keyword+'&start='+str(i)
    return query_url


##### Get News Contents #####
def get_news_contents(url):
    # get html
    html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text

    # get contents
    title = get_news_title(html)
    body = get_news_body(html)
    sentiments = get_news_sentiments(html)

    return title, body, sentiments


def get_news_title(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find('h2', attrs={'class': 'media_end_head_headline'}).text


def get_news_body(html):
    soup = BeautifulSoup(html, 'html.parser')
    ent_or_news = soup.find('div', id='dic_area').text
    if ent_or_news is not None:
        return ent_or_news
    return soup.find('article').text.strip()


def get_news_sentiments(html):
    # get news category (news, entertain, sports)
    data_sid_index = html.find("data-sid")
    news_category = html[data_sid_index: data_sid_index+20].split('"')[1]

    # get cid
    data_cid_index = html.find("data-cid")
    cid = html[data_cid_index: data_cid_index+30].split('"')[1]

    # build query
    query = build_query(news_category, cid)

    # get json from query
    f = request.urlopen(query)
    jsons = f.read().decode('utf8')
    f.close()

    page_json = json.loads(jsons)

    # get sentiments into a dict and return
    sentiment_list = {"like": 0, "sad": 0, "warm": 0, "angry": 0, "want": 0}
    for reaction in page_json['contents'][0]['reactions']:
        sentiment_list[reaction['reactionType']] = reaction['count']
    return sentiment_list


def build_query(news_category, cid):
    if news_category in 'SPORTS':
        return 'https://sports.like.naver.com/v1/search/contents?q=SPORTS%5B' + cid + '%5D%7CSPORTS_MAIN'
    if news_category in 'ENTERTAIN':
        return 'https://news.like.naver.com/v1/search/contents?q=ENTERTAIN%5B' + cid + '%5D%7CENTERTAIN_MAIN'
    if news_category in 'NEWS':
        return 'https://news.like.naver.com/v1/search/contents?q=NEWS%5B' + cid + '%5D%7CNEWS_SUMMARY'

