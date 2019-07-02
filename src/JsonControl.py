import json
import os
from .PrintLog import pl
from .PrintLog import pld


##### build format #####
def build_contents(url, title_words, body_words, sentiments):
    a_news = {
        'url': url,
        'title': title_words,
        'body': body_words,
        'sentiments': sentiments,
    }
    return [a_news]


def build_urls(urls):
    urls = {
        'url': urls
    }
    return urls


def check_file_paths(data_folder_path, q_path, c_path, verbose=True):
    pl('Checking paths...\n', verbose)
    # check if data folder exist (create one if not present)
    if not os.path.exists(data_folder_path):
        os.makedirs(data_folder_path)

    # check if queue file exist (create one if not present)
    if not os.path.exists(q_path):
        pl('No queue file found. Creating one... ', verbose)
        with open(q_path, 'w', encoding='utf-8') as out:
            json.dump(build_urls([]), out, ensure_ascii=False, indent=2)
        pld(verbose)

    # check if completed file exist (create one if not present)
    if not os.path.exists(c_path):
        pl('No completed file cound. Creating one... ', verbose)
        with open(c_path, 'w', encoding='utf-8') as out:
            json.dump(build_urls([]), out, ensure_ascii=False, indent=2)
        pld(verbose)
    pl('Path checking Done!\n', verbose)


##### To Queue #####
def push_urls(urls, q_path, c_path, verbose=True):
    data_folder = "data\\"

    # check for path validity
    pl("Checking path validity... ", verbose)
    check_file_paths(data_folder, q_path, c_path)
    pld(verbose)

    # add valid urls to existing json urls
    pl("Adding new urls... ", verbose)
    queue_json = open_json(q_path)
    queue_json['url'] += get_valid_urls(q_path, c_path, urls)

    # overwrite with new queue
    with open(q_path, 'w', encoding='utf-8') as outfile:
        json.dump(queue_json, outfile, ensure_ascii=False, indent=2)
    pld(verbose)


def get_valid_urls(q_path, c_path, urls, verbose=True):
    pl('Extracting new urls...\n', verbose)
    # read from queue and completed
    queue_json = open_json(q_path)
    completed_json = open_json(c_path)

    # push to 'to be added' if not in both queue and completed
    valid_urls = []

    # check if url's already listed
    total = len(urls)
    i = 1
    for url in urls:
        if i % 100 == 0 or i == total:
            pl('Checking url   ' + str(i) + '/' + str(total) + "\n", verbose)
        if url not in queue_json['url'] and url not in completed_json['url']:
            valid_urls += [url]
        i += 1

    pl('Total new urls to be added: ' + str(len(valid_urls)) + "\n", verbose)

    # return valid urls only
    return valid_urls


##### To newsData & completed #####
def pop_queue(q_path, verbose=True):
    top = first(q_path, False)

    pl("Popping the first element in queue... ", verbose)
    if top is None:
        pl("The queue is Empty! Nothing to pop.\n", verbose)
        return
    remove_url(q_path, top, verbose)
    pld(verbose)
    return top


def remove_url(q_path, url, verbose=True):
    jo = open_json(q_path)
    pl("Removing url... ", verbose)
    if jo['url'] == []:
        pl("No url to remove from file: " + q_path + "\n", verbose)
        return
    new_urls = []

    for element in jo['url']:
        if element != url:
            new_urls += [element]
    jo['url'] = new_urls

    with open(q_path, 'w', encoding='utf-8') as outfile:
        json.dump(jo, outfile, ensure_ascii=False, indent=2)
    pld(verbose)


def push_to_newsdata(news, n_path, verbose=True):
    # check for destination json file
    if not os.path.exists(n_path):
        pl('No newsdata file found. Creating one... ', verbose)
        with open(n_path, 'w', encoding='utf-8') as out:
            news_json = {'news': []}
            json.dump(news_json, out, ensure_ascii=False, indent=2)
        pld(verbose)

    # add news data
    newsdata_json = open_json(n_path)
    newsdata_json['news'] += news

    with open(n_path, 'w', encoding='utf-8') as outfile:
        json.dump(newsdata_json, outfile, ensure_ascii=False, indent=2)


def push_to_completed(c_path, url, verbose=True):
    pl('Pushing to completed: ' + url + '...', verbose)
    completed_json = open_json(c_path)
    completed_json['url'] += [url]

    with open(c_path, 'w', encoding='utf-8') as outfile:
        json.dump(completed_json, outfile, ensure_ascii=False, indent=2)
    pld(verbose)

##### misc #####
def first(file_path, verbose=True):
    pl("Opening file...", verbose)
    jo = open_json(file_path)
    pld(verbose)
    pl("Getting first url in list...", verbose)
    if not jo['url'] == []:
        url = jo['url'][0]
        pl(url + "   ", verbose)
        pld(verbose)
        return jo['url'][0]
    else:
        pl("Url list is empty. Nothing the fetch!\n", verbose)



def open_json(file_path):        # return dict
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)