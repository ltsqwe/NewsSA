import src.Collector as collector
import src.JsonControl as jsonControl


# variables
keywords = ['윤하', '아이유', '연합뉴스']
page_max = 10

# get article urls
articles = []
for keyword in keywords:
    print("Fetching news for: ", keyword)
    keyword_articles = collector.get_news_list(keyword, page_max, False)
    print("Got", len(keyword_articles), "article urls from searching", keyword)
    articles += keyword_articles

# push to queue file
jsonControl.push_urls(articles, "data\\queue.json", "data\\completed.json")

# pop queue file til it's empty
total = len(jsonControl.open_json("data\\queue.json")['url'])
i = 1
print("Processing:", str(0), "/", str(total))
while jsonControl.first("data\\queue.json", False) is not None:
    try:
        if i % 10 == 0 or i == total:
            print("Processing:", str(i), "/", str(total))
        url = jsonControl.pop_queue("data\\queue.json", False)
        title, body, sentiment = collector.get_news_contents(url)
        a_news = jsonControl.build_contents(url, title, body, sentiment)
        jsonControl.push_to_newsdata(a_news, "data\\newsdata.json", False)
        jsonControl.push_to_completed("data\\completed.json", url, False)
        i += 1
    except Exception:
        i += 1
        continue
