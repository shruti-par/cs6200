# Program to compare BFS and DFS and print the number of overlapping links
bfs_file = open('Task1_BFS.txt', 'r')
dfs_file = open('Task1_DFS.txt', 'r')

bfs_links = {}

for link in bfs_file:
    bfs_links[link] = True

common_links = 0

for link in dfs_file:
    if link in bfs_links:
        common_links += 1

print("Overlapping links in BFS and DFS outputs: ", common_links)

bfs_file.close()
dfs_file.close()
