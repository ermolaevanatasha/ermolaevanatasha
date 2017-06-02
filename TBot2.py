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

umessage = input('Введите ваше сообщение: ')

def parse_umessage(umessage):
    all_umes_ana = []
    umessage = umessage.split()
    for mes in umessage:
        umes_ana = morph.parse(mes)
        umes_ana = umes_ana[0]
        
        all_umes_ana.append(umes_ana.tag)

    return all_umes_ana

def check_base(all_umes_ana, d, all_ana):
    for uana in all_umes_ana:
        p_ana = re.findall(r"[\w']+", str(uana))
        if uana.POS in d:
            if uana.POS == 'NOUN':
                if uana.animacy == 'anim':
                    if uana.gender == 'masc':
                        answer_word = random.choice(d['NOUN']['anim']['masc'])
                        make_infl(answer_word, p_ana)
                    elif uana.gender == 'femn':
                        answer_word = random.choice(d['NOUN']['anim']['femn'])
                        make_infl(answer_word, p_ana)
                    else:
                        answer_word = random.choice(d['NOUN']['anim']['neut'])
                        make_infl(answer_word, p_ana)

                else:
                    if uana.gender == 'masc':
                        answer_word = random.choice(d['NOUN']['inan']['masc'])
                        make_infl(answer_word, p_ana)
                    elif uana.gender == 'femn':
                        answer_word = random.choice(d['NOUN']['inan']['femn'])
                        make_infl(answer_word, p_ana)
                    else:
                        answer_word = random.choice(d['NOUN']['inan']['neut'])
                        make_infl(answer_word, p_ana)

            elif uana.POS == 'VERB':
                if uana.aspect == 'perf':
                    if uana.transitivity == 'tran':
                        answer_word = random.choice(d['VERB']['perf']['tran'])
                        make_infl(answer_word, p_ana)
                    else:
                        answer_word = random.choice(d['VERB']['perf']['intr'])
                        make_infl(answer_word, p_ana)
                else:
                    if uana.transitivity == 'tran':
                        answer_word = random.choice(d['VERB']['impf']['tran'])
                        make_infl(answer_word, p_ana)
                    else:
                        answer_word = random.choice(d['VERB']['impf']['intr'])
                        make_infl(answer_word, p_ana)

            elif uana.POS == 'NPRO':
                if uana.person == '1per':
                    answer_word = random.choice(d['NPRO']['1per'])
                    make_infl(answer_word, p_ana)
                elif uana.person == '2per':
                    answer_word = random.choice(d['NPRO']['2per'])
                    make_infl(answer_word, p_ana)
                else:
                    answer_word = random.choice(d['NPRO']['3per'])
                    make_infl(answer_word, p_ana)

            else:
                for ana in all_ana:
                    answer_word = random.choice(d[ana.tag.POS][ana.normal_form])
                    make_infl(answer_word, p_ana)

def make_infl(answer_word, p_ana):
    rand_ana = []
    cl_word = []
    answer_word_ana = morph.parse(answer_word)[0]
    rand_ana.append(answer_word_ana)
    for ans in rand_ana:
        infl_ana = str(ans.inflect(set(p_ana)))

        if 'Parse' in infl_ana:
            infl_ana = re.findall(r"\w+", infl_ana)
            cl_word.append(infl_ana[2])

    s_ans = ''.join(cl_word)
    print(s_ans)

def main():
    get_words = words()
    get_lemmas = lemmas(get_words)
    get_nouns = nouns(get_lemmas)
    get_pronouns = pronouns(get_lemmas)
    get_verbs = verbs(get_lemmas)
    get_others = others(get_lemmas)
    get_message = parse_umessage(umessage)
    check_base(get_message, d, get_lemmas)
  
if __name__ == '__main__':
    main()
