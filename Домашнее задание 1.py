#не получается записать результат в файл

import urllib.request

def request():
    url = 'http://kr-znamya.ru'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'

    req = urllib.request.Request('http://kr-znamya.ru', headers={'User-Agent': user_agent})

    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    return html

import re

def findtitles(html):
    regPostTitle = re.compile('<h2 class="contentheading">.*?</h2>', flags=re.DOTALL)
    titles = regPostTitle.findall(html)
    return titles

def cleantitles(titles):
    new_titles = []
    regTag = re.compile('<.*?>', flags=re.DOTALL)
    regSpace = re.compile('\s{2,}', flags=re.DOTALL)
    regLineBreak = re.compile('\t', flags=re.DOTALL)
    for t in titles:
        clean_t = regSpace.sub("", t)
        clean_t = regTag.sub("", clean_t)
        clean_t = regLineBreak.sub("", clean_t)
        new_titles.append(clean_t)
    for t in new_titles:
        print(t)
    return t

def save_results(t):
    f = open('results.txt', 'w', encoding='utf-8')
    f.write(t)
    f.close()

def main():
    code = request()
    titles = findtitles(code)
    results = cleantitles(titles)
    save_results(results)

if __name__ == '__main__':
    main()
