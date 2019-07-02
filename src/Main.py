import src.Collector as collector
import src.JsonControl as jsonControl

keywords = ['윤하', '아이유', '연합뉴스']
page_max = 50

# articles = []
# for keyword in keywords:
#     print("Fetching news for: ", keyword)
#     keyword_articles = collector.get_news_list(keyword, page_max, False)
#     print("Got", len(keyword_articles), "article urls from searching", keyword)
#     articles += keyword_articles
#
# jsonControl.push_urls(articles, "data\\queue.json", "data\\completed.json")

url = jsonControl.pop_queue("data\\queue.json")
title, body, sentiment = collector.get_news_contents(url)
a_news = jsonControl.build_contents(title, body, sentiment)
jsonControl.push_to_newsdata(a_news, "data\\newsdata.json")
jsonControl.push_to_completed("data\\completed.json", url)

print(title)
print(body)
print(sentiment)

