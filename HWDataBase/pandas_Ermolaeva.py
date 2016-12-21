import os
import re

def open_file():
    f = open('pandas.txt', 'r', encoding='utf-8')
    string = f.read()
    words = string.split()
    f.close()

    # for indx, let in enumerate(words):
    #     words[indx] = let.lower() # на всякий случай, если вдруг понадобится

    return words

def insert_ino_table_1(words):
    right = []
    left = []

    a = ''
    for i in range(0, len(words)):
        right.append('')
        left.append('')

        if a:
            left[i] = a.group(0)
            a = ''

        a = re.search('[.|,|!|?|:|;]', words[i]) # список знаков можно расширить
        if a:
            words[i] = re.sub('[.|,|!|?|:|;]', '', words[i]) # список знаков можно расширить
            right[i] = a.group(0)

    with open('pandas_sql.txt', 'a', encoding='utf-8') as f:
        f.write('Таблица №1' + '\n')
        for i in range(0, len(words)):
            f.write('INSERT INTO Pandas (id, token, left_punct, right_punct, token_id, sent_num) VALUES (' + str(i+1) + ', \'' + words[i] + '\', \'' + left[i] + '\', \'' + right[i] + '\', ' + '0' + ', ' + str(i+1) + ');' + '\n')

def mystem():
    inp = '/Users/nata/Desktop/'
    os.system(r'/Users/nata/Desktop/mystem ' + inp + 'pandas.txt' + ' ' + 'output.txt' + ' -nd')

    text = []

    with open('output.txt', 'r', encoding='utf-8') as f:
        for line in f:
            text.append(line)

    low_text = [x.lower() for x in text]
    set_text = set(low_text)
    make_search = ''.join(set_text)

    regToken = re.compile('{.*?}', flags=re.U | re.DOTALL)
    regSpace = re.compile('\n',  flags=re.U | re.DOTALL)

    tokens = []
    for token in set_text:
        token = regToken.sub('', token)
        token = regSpace.sub('', token)
        tokens.append(token)

    regLemma = re.compile('{(.*?)}', flags=re.U | re.DOTALL)
    lemmas = regLemma.findall(make_search)

    return tokens, lemmas

def insert_into_table_2(tokens, lemmas):
    with open('pandas_sql.txt', 'a', encoding='utf-8') as f:
        f.write('Таблица №2' + '\n')  
        for i in range(0, len(tokens)):
            f.write('INSERT INTO TokensPandas (id, token, lemma) VALUES (' + str(i+1) + ', \''  + tokens[i] + '\', \'' + lemmas[i] + '\');' + '\n')

def main():
    read = open_file()
    table_1 = insert_ino_table_1(read)
    tok, lem = mystem()
    table_2 = insert_into_table_2(tok, lem)

if __name__ == '__main__':
    main()


