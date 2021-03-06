import html2text
import os
import re

def find_matches():

    with open('words.txt', 'r', encoding='utf-8') as f_words:
        words = set(line.strip() for line in f_words)

    with open('adyg.html', 'r', encoding='utf-8') as f_news:
        text_words = set()

        h = html2text.HTML2Text() #clean html
        h.ignore_links = True

        text = h.handle(f_news.read())

        for word in text.split():
            text_words.add(word)

    words_list = words & set(text_words)

    with open('wordlist.txt', 'w', encoding='utf-8') as f_result:
        for word in words_list:
            f_result.write(word + '\n')

def rus_nouns():
    inp = '/Users/nata/Desktop/'
    os.system(r'/Users/nata/Desktop/mystem ' + inp + 'wordlist.txt' + ' ' + 'rus.txt' + ' -ind')
    with open('rus.txt', 'r', encoding='utf-8') as f:
        rus_words = set()

        for line in f:
            m = re.search(r'=S,[^=]+=им,ед', line)
            if m:
                m_word = re.search(r'^[^\{]+', line)
                if m_word:
                    rus_words.add(m_word.group(0))

    with open('rus_nouns.txt', 'w', encoding='utf-8') as f:
        f.writelines(['%s\n' % word for word in rus_words])
                    
    

def main():
    find_matches()
    rus_nouns()

if __name__ == '__main__':
    main()
