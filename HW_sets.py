import re
import urllib.request
import html
import collections

def download_page_1():
    url = 'http://izvestia.ru/news/648539'
    with urllib.request.urlopen(url) as response:
        html_1 = response.read().decode('utf-8')
        
    return html_1
    
def find_clean_text_1(html_1):
    regPostText = re.compile('<p>(.*?)</article>', flags=re.U | re.DOTALL)
    text = regPostText.findall(html_1)
    regTag = re.compile('<.*?>')
    regSpace = re.compile(r'[\s\xa0]{1,}')

    new_text = []
    for tx in text:
        tx = html.unescape(tx)
        tx = regSpace.sub(" ", tx)
        tx = regTag.sub(" ", tx)
        
        new_text.extend(tx.split(' '))

    text_1 = []
    for t in new_text:
        t = t.strip('.,!?;:«»"\'(){}[]\\/—')
        t = t.lower()
        if t:
            text_1.append(t)
            
    return text_1

def set_1(text_1):
    set_1 = set(text_1)

    return set_1

def download_page_2():
    url = 'https://indicator.ru/news/2016/11/30/podtverzhdeny-nazvaniya-chetyreh-novyh-himicheskih-elementov/'
    with urllib.request.urlopen(url) as response:
        html_2 = response.read().decode('utf-8')
        
    return html_2

def find_clean_text_2(html_2):
    regPostText = re.compile('<div class="typo"><p>(.*?)</div>', flags=re.U | re.DOTALL)
    text = regPostText.findall(html_2)
    new_text = []
    regTag = re.compile('<.*?>')
    regSpace = re.compile(r'[\s\xa0]{1,}')

    new_text = []
    for tx in text:
        tx = html.unescape(tx)
        tx = regSpace.sub(" ", tx)
        tx = regTag.sub(" ", tx)

        new_text.extend(tx.split(' '))

    text_2 = []
    for t in new_text:
        t = t.strip('.,!?;:«»"\'(){}[]\\/—')
        t = t.lower()
        if t:
            text_2.append(t)
            
    return text_2

def set_2(text_2):
    set_2 = set(text_2)

    return set_2

def download_page_3():
    url = 'http://tass.ru/moskovskaya-oblast/3827291'
    with urllib.request.urlopen(url) as response:
        html_3 = response.read().decode('utf-8')
        
    return html_3

def find_clean_text_3(html_3):
    regPostText = re.compile('<div class="b-material-text__l js-mediator-article">(.*?)<p><strong>', flags=re.U | re.DOTALL)
    text = regPostText.findall(html_3)
    new_text = []
    regTag = re.compile('<.*?>')
    regSpace = re.compile(r'[\s\xa0]{1,}')

    new_text = []
    for tx in text:
        tx = html.unescape(tx)
        tx = regSpace.sub(" ", tx)
        tx = regTag.sub(" ", tx)
        
        new_text.extend(tx.split(' '))

    text_3 = []
    for t in new_text:
        t = t.strip('.,!?;:«»-"\'(){}[]\\/—')
        t = t.lower()
        if t:
            text_3.append(t)
            
    return text_3

def set_3(text_3):
    set_3 = set(text_3)

    return set_3

def download_page_4():
    url = 'http://ufacitynews.ru/news/2016/12/01/v-tablice-mendeleeva-oficialno-poyavilis-novye-elementy/'
    with urllib.request.urlopen(url) as response:
        html_4 = response.read().decode('utf-8')
        
    return html_4

def find_clean_text_4(html_4):
    regPostText = re.compile('<div class="b-post__text">(.*?)<div class="b-post__author">', flags=re.U | re.DOTALL)
    text = regPostText.findall(html_4)
    new_text = []
    regTag = re.compile('<.*?>')
    regSpace = re.compile(r'[\s\xa0]{1,}')

    new_text = []
    for tx in text:
        tx = html.unescape(tx)
        tx = regSpace.sub(" ", tx)
        tx = regTag.sub(" ", tx)
        
        new_text.extend(tx.split(' '))

    text_4 = []
    for t in new_text:
        t = t.strip('.,!?;:«»–"\'(){}[]\\/—')
        t = t.lower()
        if t:
            text_4.append(t)
        
    return text_4

def set_4(text_4):
    set_4 = set(text_4)

    return set_4

def find_inter(set_1, set_2, set_3, set_4):
    intersection = set_1 & set_2 & set_3 & set_4
    f = open('results.txt', 'w', encoding='utf-8')
    f.write('Пересечение:' + '\n')
    for word in sorted(intersection):
        f = open('results.txt', 'a', encoding='utf-8')
        f.write(word + '\n')
        f.close()

def find_difference(set_1, set_2, set_3, set_4):
    difference = set_1 ^ set_2 ^ set_3 ^ set_4
    f = open('results.txt', 'a', encoding='utf-8')
    f.write('Симметрическая разность:' + '\n')
    for word in sorted(difference):
        f = open('results.txt', 'a', encoding='utf-8')
        f.write(word + '\n')
        f.close()

    return difference

def freq_difference(difference, text_1, text_2, text_3, text_4):
    texts = text_1 + text_2 + text_3 + text_4
    count = collections.Counter(texts) # count the occurrences of a particular item in array
    frequency = []
    for word, quantity in count.items():
        if quantity > 1:
            frequency.append(word)

    freq_set = set(frequency)
    inter = freq_set & difference
    
    for word in sorted(inter):
        f = open('frequency.txt', 'a', encoding='utf-8')
        f.write(word + ' ' + str(count[word]) + '\n')
        f.close()

def main():
    html_1 = download_page_1()
    text_1 = find_clean_text_1(html_1)
    set1 = set_1(text_1)
    html_2 = download_page_2()
    text_2 = find_clean_text_2(html_2)
    set2 = set_2(text_2)
    html_3 = download_page_3()
    text_3 = find_clean_text_3(html_3)
    set3 = set_3(text_3)
    html_4 = download_page_4()
    text_4 = find_clean_text_4(html_4)
    set4 = set_4(text_4)
    inter = find_inter(set1, set2, set3, set4)
    difference = find_difference(set1, set2, set3, set4)
    freq_difference(difference, text_1, text_2, text_3, text_4)

if __name__ == '__main__':
    main()

