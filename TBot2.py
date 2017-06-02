import pymorphy2
from pymorphy2 import MorphAnalyzer
import re
import random
import telebot
import conf

morph = MorphAnalyzer()

def words():
    with open('all_words.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        all_words = []
        for line in lines:
            line = line.replace('\n', '')
            all_words.append(line.split('\t')[1])

    return all_words

def lemmas(all_words):
    all_ana = []

    for word in all_words:
        ana = morph.parse(word)
        all_ana.append(ana[0])
    return all_ana

d = {}

def nouns(all_ana):
    for ana in all_ana:
        if ana.tag.POS == 'NOUN':
            if ana.tag.POS not in d:
                d[ana.tag.POS] = {}
                continue

            if ana.tag.animacy not in d[ana.tag.POS]:
                d[ana.tag.POS][ana.tag.animacy] = {}
                continue

            if ana.tag.gender not in d[ana.tag.POS][ana.tag.animacy]:
                d[ana.tag.POS][ana.tag.animacy][ana.tag.gender] = []
                d[ana.tag.POS][ana.tag.animacy][ana.tag.gender].append(ana.normal_form)
            else:
                d[ana.tag.POS][ana.tag.animacy][ana.tag.gender].append(ana.normal_form)

def pronouns(all_ana):
    for ana in all_ana:
        if ana.tag.POS == 'NPRO':
            if ana.tag.POS not in d:
                d[ana.tag.POS] = {}
                continue

            if ana.tag.person not in d[ana.tag.POS]:
                d[ana.tag.POS][ana.tag.person] = []
                d[ana.tag.POS][ana.tag.person].append(ana.normal_form)
            else:
                d[ana.tag.POS][ana.tag.person].append(ana.normal_form)
 
def verbs(all_ana):
    for ana in all_ana:
        if ana.tag.POS == 'VERB':
            if ana.tag.POS not in d:
                d[ana.tag.POS] = {}
                continue

            if ana.tag.aspect not in d[ana.tag.POS]:
                d[ana.tag.POS][ana.tag.aspect] = {}
                continue

            if ana.tag.transitivity not in d[ana.tag.POS][ana.tag.aspect]:
                d[ana.tag.POS][ana.tag.aspect][ana.tag.transitivity] = []
                d[ana.tag.POS][ana.tag.aspect][ana.tag.transitivity].append(ana.normal_form)
            else:
                d[ana.tag.POS][ana.tag.aspect][ana.tag.transitivity].append(ana.normal_form)

def others(all_ana):
    for ana in all_ana:
        if ana.tag.POS != 'NOUN' and ana.tag.POS != 'NPRO' and ana.tag.POS != 'VERB':
            if ana.tag.POS not in d:
                d[ana.tag.POS] = []
                d[ana.tag.POS].append(ana.normal_form)

            else:
                d[ana.tag.POS].append(ana.normal_form)
    
    # print(d)

def normalforms(all_ana):
    all_normalforms = []

    for ana in all_ana:
        all_normalforms.append(ana.normal_form)

    return all_normalforms

umessage = input('Введите ваше сообщение: ')

def parse_umessage(umessage):
    all_umes_ana = []
    umessage = umessage.split()
    for mes in umessage:
        umes_ana = morph.parse(mes)
        umes_ana = umes_ana[0]
        
        all_umes_ana.append(umes_ana.tag)

    # print(all_umes_ana)
    return all_umes_ana

def chars(all_umes_ana, all_normalforms):
    all_rand = []

    for_answ = False # значение логического типа; поможет выбрать слово, удовлетворяющее всем необходимым параметрам

    for umes in all_umes_ana:
        while True:
            randword = random.choice(all_normalforms) # выбираем случайную лемму из массива всех лемм
            randword_ana = morph.parse(randword)[0]
            randword_ana = randword_ana.tag

            # print(randword)

            if randword_ana.POS == umes.POS:
                for_answ = True
                if randword_ana.POS == 'NOUN':
                    for_answ = (randword_ana.animacy == umes.animacy and randword_ana.gender == umes.gender)

                elif randword_ana.POS == 'NPRO':
                    for_answ = (randword_ana.person == umes.person)

                elif randword_ana.POS == 'VERB': #or randword_ana.tag.POS == 'GRND':
                    for_answ = (randword_ana.aspect == umes.aspect and randword_ana.transitivity == umes.transitivity)

                if for_answ:
                    all_rand.append(randword)
                    break

    # print(all_rand)
    return all_rand

def send_answer(all_umes_ana, all_rand):
    bot_answer_ana = []

    for ana in all_umes_ana:
        ana = re.findall(r"[\w']+", str(ana))

        # print(ana)

    for randomword in all_rand:
        rand_ana = morph.parse(randomword)[0]
        bot_answer_ana.append(rand_ana)

        print(bot_answer_ana)

    ana_answer = zip(ana, bot_answer_ana)
    bot_answer = []
    for an, ans in ana_answer:
        answer = str(ans.inflect(set(an)))

        # prin(answer)
        bot_answer.append(answer[2])

    bot_ans = ' '.join(bot_answer)
    print(bot_ans)


def main():
    get_words = words()
    get_lemmas = lemmas(get_words)
    get_nouns = nouns(get_lemmas)
    get_pronouns = pronouns(get_lemmas)
    get_verbs = verbs (get_lemmas)
    get_others = others(get_lemmas)
    get_normalforms = normalforms(get_lemmas)
    get_message = parse_umessage(umessage)
    get_chars = chars(get_message, get_normalforms)
    send_answer(get_message, get_chars)
  
if __name__ == '__main__':
    main()
