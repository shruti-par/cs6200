import os, requests
from time import sleep

input_file = input("Enter the name of the file containing links: ")
f_in = open(input_file, 'r')

if not os.path.exists("./HTML_Docs"):
    os.makedirs("./HTML_Docs")

for url in f_in:
    sleep(1)
    url = url.rstrip('\n')
    title = url[30:]
    with open("./HTML_Docs/" + title, 'w+') as f_out:
        f_out.write(str(requests.get(url).text.encode("utf-8")))

f_in.close()
