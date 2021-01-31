import string

escapedlist = []
with open("jokes.txt",encoding="utf8") as file_object:
    lines = file_object.readlines()
    #lines
for line in lines:
    line = line.rstrip()
    line = line.replace('\\n', '\n')
    escapedlist.append(line)
    
lines
escapedlist