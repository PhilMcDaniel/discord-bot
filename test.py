import random
with open("insults.txt") as file_object:
    lines = file_object.readlines()
for line in lines:
    print(line.rstrip())
response = random.choice(lines)

print(response)