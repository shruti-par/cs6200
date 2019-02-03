# Program to count the number of duplicate links encountered during focused BFS
input_file = open("Duplicate_links_Task2.txt", 'r')

c = sum(1 for line in input_file)
print("Number of duplicate links encountered: ", c)
