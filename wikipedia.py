import json
import urllib.request
import sys
import time
import os


class Wikipedia:

    def __init__(self, subdomain="en", summary=True):
        self.subdomain = subdomain
        self.summary = summary

    def random_article_titles(self, num_of_articles=20):
        ''' Returns titles of random Wikipedia articles '''

        url = "https://"+self.subdomain + \
            ".wikipedia.org/w/api.php?format=json&action=query&list=random&rnnamespace=0&rnlimit=" + \
            str(num_of_articles)
        json_doc = urllib.request.urlopen(url).read().decode(
            encoding="utf-8", errors="ignore")
        parsed = json.loads(json_doc)
        titles = []
        for article in parsed["query"]["random"]:
            titles.append(article["title"])
        return titles

    def get(self, titles):
        ''' Returns full or summarized Wikipedia articles specified by their titles '''

        if titles == None or len(titles) < 1:
            return None

        articles_dict = dict()

        if self.summary:
            titles_string = "|".join(titles)
            url = "https://"+self.subdomain+".wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exlimit=max&explaintext&redirects&exintro&titles=" + \
                urllib.parse.quote_plus(titles_string)
            json_doc = urllib.request.urlopen(url).read().decode(
                encoding="utf-8", errors="ignore")
            parsed = json.loads(json_doc)
            pages = parsed["query"]["pages"]

            for i in pages:
                page = pages[i]
                title = page["title"].encode(
                    encoding="utf-8", errors="ignore").decode(encoding="utf-8")
                content = page["extract"].encode(
                    encoding="utf-8", errors="ignore").decode(encoding="utf-8")
                articles_dict[title] = content

        else:
            for title in titles:
                url = "https://"+self.subdomain + \
                    ".wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exlimit=max&explaintext&redirects&titles=" + \
                    urllib.parse.quote_plus(title)
                json_doc = urllib.request.urlopen(
                    url).read().decode("utf-8", errors="ignore")
                parsed = json.loads(json_doc)
                pages = parsed["query"]["pages"]

                for i in pages:
                    page = pages[i]
                    title = page["title"].encode(
                        encoding="utf-8", errors="ignore").decode(encoding="utf-8")
                    content = page["extract"].encode(
                        encoding="utf-8", errors="ignore").decode(encoding="utf-8")
                    articles_dict[title] = content

        return articles_dict

    def crawl(self, single_fetch=20, count=1000, minimum_length=10240):
        ''' Crawls Wikipedia until it get count number of article having
                minimum length while fethcing single fetch_size number of
                                articles at a time '''
        try:
            os.mkdir("./data/")
        except FileExistsError:
            pass
        cnt = 0
        while cnt < count:
            titles = self.random_article_titles(single_fetch)
            articles = self.get(titles)
            for title in articles:
                print(len(articles[title]))
                if len(articles[title]) < minimum_length:
                    continue
                cnt += 1
                clean_title = "".join(c for c in title if c.isalnum())
                print("saving:::"+clean_title)
                path = "./data/"+clean_title+".txt"
                if os.path.exists(path):
                    continue

                with open(path, "wt", encoding="utf-8") as f:
                    f.write(articles[title])
