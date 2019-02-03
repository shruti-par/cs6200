"""
 Program definition -
    To create a web crawler to crawl the web using three techniques - breadth first search, depth first search and
    focused breadth first search.
"""

# Importing required libraries
import re, requests
from bs4 import BeautifulSoup as bsoup
from time import sleep

# Base Wikipedia url
base_url = 'https://en.wikipedia.org'

# Start of class WebCrawler
class WebCrawler(object):

    # Defining instance attributes
    def __init__(self, seed_url, keywords=None, max=1000, max_depth=6, wait_time=1):
        self.seed_url = seed_url    # Assigning seed url to start the crawl
        self.keywords = [kw.lower() for kw in keywords] if keywords else None   # Value is None for simple BFS and DFS
        # And list of keywords provided by the user for focused BFS
        self.max = max  # Maximum number of url
        self.max_depth = max_depth  # Maximum depth to search
        self.wait_time = wait_time  # Wait time of 1 second to respect politeness policy

    # Extracting urls, appending them to the base url and adding them to the list of urls
    def get_urls(self, url):
        sleep(self.wait_time)
        reqs = requests.get(url)

        # Checking for status codes which are not ok and for redirected pages
        if reqs.status_code != requests.codes.ok or reqs.is_redirect:
            return []

        # Extracting body content in html form
        body_con = bsoup(reqs.content, "html.parser").find(id="bodyContent")
        urls = []

        # Parsing all anchor tags and extracting the url if the link is not empty or a link to the main page or an
        # administrative link or a link to another section on the same page
        for ref in body_con.find_all("a"):
            link = ref.get("href")

            if link and re.match('/wiki/.*', link) is not None and re.match('/wiki/Main_Page', link) is None \
                    and re.match('/wiki/(.*)#(.*)', link) is None and re.match('/wiki/(.*):(.*)', link) is None:

                # Applicable for focused BFS, where the link is appended only if it contains a keyword from the list
                if self.keywords is not None and not self.contains_keyword(link, ref.string):
                    continue

                urls.append(base_url + link)    # Appending link to base url

        return urls

    # Checking if the url contains a word from the keyword list provided by the user
    def contains_keyword(self, url, text):

        for kw in self.keywords:

            if kw.find(" ") != -1:
                self.keywords[self.keywords.index(kw)] = kw.replace(" ", "_")

            if url.lower().find(kw) != -1 or (text and text.lower().find(kw) != -1):
                return True

        return False

    # Conducting a breadth first search and adding the urls to the output list
    def breadth_first(self):

        link_num = 1
        self.output = [self.seed_url]   # Initializing the output list
        self.duplicate = {}
        depth = {self.seed_url: 1}
        for url in self.output:

            # Checking if max depth of 6 is reached before finding a 1000 urls
            if depth[url] > self.max_depth:
                print("Maximum depth reached: ", self.max_depth)
                return

            # Extracting the urls using the get_urls() function and receiving a list of urls
            links = self.get_urls(url)
            for link in links:

                # Encountering a new link
                if link not in depth:
                    depth[link] = depth[url] + 1    # Incrementing the depth searched
                    self.output.append(link)
                    link_num += 1

                    # Checking if the max number of links to be found has crossed
                    if link_num >= self.max:
                        print("Maximum depth reached: ", depth[link])
                        return

                # Encountering a duplicate link
                if link in depth:
                    if link in self.duplicate:
                        self.duplicate[link] = self.duplicate[link] + 1

                    else:
                        self.duplicate[link] = 1

    # Conducting a depth first search and adding the urls to the output list
    def depth_first(self):

        self.output = []    # Initializing the output list
        self.visited = {self.seed_url: True}
        self.maxdep = 1
        self.depth_first_rec(self.seed_url, 1)
        print("Maximum depth reached: ", self.maxdep)

    # Implementation of DFS till a depth of 6 is reached and 1000 urls have been found
    def depth_first_rec(self, url, depth):
        self.maxdep = max(depth, self.maxdep)
        self.output.append(url)
        self.visited[url] = True

        # Control finally returns to depth_first() when 1000 urls have been found
        if len(self.output) >= self.max:
            return

        # Checking if maximum depth of 6 is reached
        if depth < self.max_depth:

            for link in self.get_urls(url):

                # Checking if 1000 urls haven't been found and and url has not been visited before
                if len(self.output) < self.max and link not in self.visited:
                    # Recursively calling function with new link and incremented depth
                    self.depth_first_rec(link, depth+1)

    # Writing the list of urls found on to the output file
    def save_output(self, file_name):
        file = open(file_name, "w")     # Opening file in write mode

        for url in self.output:
            file.write(url + "\n")

        file.close()


# Main body of code
if __name__ == "__main__":

    # Seed url to start crawling
    seed = 'https://en.wikipedia.org/wiki/Space_exploration'
    print("Seed Url: ", seed)

    # Accepting keyword list from user to conduct focused BFS
    keyword_list = input("\nPlease enter keywords to be used for focused crawling (separated by a pipe (|) ): ").split('|')
    # Martian|Rover|Orbit|Pathfinder|Mars Mission|Mars Exploration|Red Planet

    # Initiating the crawl using the seed url
    web_crawler = WebCrawler(seed)

    print("\nTask 1 Breadth First Search: ")
    web_crawler.breadth_first()
    web_crawler.save_output("Task1_BFS.txt")

    print("\nTask 1 Depth First Search: ")
    web_crawler.depth_first()
    web_crawler.save_output("Task1_DFS.txt")

    # Using the keyword list provided by the user for focused BFS
    print("\nFocused Breadth First Search using the following keywords: \n", keyword_list, ": \n")
    focused_crawler = WebCrawler(seed, keywords=keyword_list)
    focused_crawler.breadth_first()
    focused_crawler.save_output("Task2_BFS.txt")
    # Writing the duplicate links to a separte file
    dup_file = open("Duplicate_links_Task2.txt", "w")
    for url in focused_crawler.duplicate:
        # print(url, "\t", focused_crawler.duplicate[url])
        dup_file.write(url + "\t" + str(focused_crawler.duplicate[url]) + "\n")

    dup_file.close()
