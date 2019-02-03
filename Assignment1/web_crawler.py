# Program definition

# Importing required libraries
import re, requests
from bs4 import BeautifulSoup as bsoup
from time import sleep

base_url = 'https://en.wikipedia.org'

class WebCrawler(object):
    def __init__(self, seedUrl, keywords=None, max=1000, maxDepth=6, waitTime=1):
        self.seedUrl = seedUrl
        self.keywords = [kw.lower() for kw in keywords] if keywords else None
        self.max = max
        self.maxDepth = maxDepth
        self.waitTime = waitTime

    def get_urls(self, url):
        sleep(self.waitTime)
        reqs = requests.get(url)
        if reqs.status_code != requests.codes.ok or reqs.is_redirect:
            return []

        bodyCon = bsoup(reqs.content, "html.parser").find(id = "bodyContent")
        urls = []

        for ref in bodyCon.find_all("a"):
            link = ref.get("href")

            if link and re.match('/wiki/.*', link) is not None and re.match('/wiki/Main_Page', link) is None \
                    and re.match('/wiki/(.*)#(.*)', link) is None and re.match('/wiki/(.*):(.*)', link) is None:

                if self.keywords is not None and not self.contains_keyword(link, ref.string):
                    continue

                urls.append(base_url + link)

        return urls

    def contains_keyword(self, url, text):

        for kw in self.keywords:
            if url.lower().find(kw) != -1 or (text and text.lower().find(kw) != -1):
                return True
        return False

    def breadth_first(self):

        link_num = 1
        self.output = [self.seedUrl]
        depth = {self.seedUrl: 1}
        for url in self.output:

            if depth[url] > self.maxDepth:
                print("Maximum depth reached: ", self.maxDepth)
                return

            links = self.get_urls(url)
            for link in links:

                if link not in depth:
                    depth[link] = depth[url] + 1
                    self.output.append(link)
                    link_num += 1

                    if link_num >= self.max:
                        print("Maximum depth reached: ", depth[link])
                        return

    def depth_first_imp(self, url, depth):
        self.maxdep = max(depth, self.maxdep)
        self.output.append(url)
        self.visited[url] = True

        if len(self.output) >= self.max:
            return

        if depth < self.maxDepth:

            for link in self.get_urls(url):

                if len(self.output) < self.max and link not in self.visited:
                    self.depth_first_imp(link, depth+1)

    def depth_first(self):

        self.output = []
        self.visited = {self.seedUrl: True}
        self.maxdep = 1
        self.depth_first_imp(self.seedUrl, 1)
        print("Maximum depth reached: ", self.maxdep)

    def save_output(self, file_name):
        file = open(file_name, "w")

        for url in self.output:
            file.write(url + "\n")

        file.close()

if __name__ == "__main__":

    seed_url = 'https://en.wikipedia.org/wiki/Space_exploration'
    print("Seed Url: ", seed_url)
    keywords = input("\nPlease enter keywords to be used for focused crawling (separated by a space): ").split(', ')
# Mars, Rover, Orbiter, Pathfinder, Mars Mission, Mars Exploration
    web_crawler = WebCrawler(seed_url)

    print("\nTask 1 Breadth First Search: ")
    web_crawler.breadth_first()
    web_crawler.save_output("Task1_BFS.txt")

    print("\nTask 1 Depth First Search: ")
    web_crawler.depth_first()
    web_crawler.save_output("Task1_DFS.txt")

    print("\nFocused Breadth First Search using the following keywords: \n", keywords, ": \n")
    focused_crawler = WebCrawler(seed_url, keywords=keywords)
    focused_crawler.breadth_first()
    focused_crawler.save_output("Task2_BFS.txt")















