import re

regex = r'<a href="(.*)">'
pattern = re.compile(regex)

exhibitors = []

with open("exhibitor list.html") as f:
    for line in f.readlines():
        m = pattern.search(line)
        if m:
            exhibitors.append(m.group(1) + '\n')

with open("exhibitor_urls.txt", 'w') as f:
    f.writelines(exhibitors)

