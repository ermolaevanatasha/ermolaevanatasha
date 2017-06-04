import pymorphy2
from pymorphy2 import MorphAnalyzer
import re
import random

morph = MorphAnalyzer()

def words():
    with open('text.txt', 'r', encoding='utf-8') as f:
        lines = f.read()
        cl_lines = re.sub(r'[.,!?;:\u2013\u2014«»"@№#&$%^*()<>+=\/|\\]+\ *', ' ', lines)
        all_words = cl_lines.split()
        
    return all_words

    # для списка слов из НКРЯ:
    #     all_words = []
    #     for line in lines:
    #         line = line.replace('\n', '')
    #         # all_words.append(line.split('\t')[1])
    # return all_words

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
        if ana.tag.POS == 'VERB' or ana.tag.POS == 'INFN':
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
        if ana.tag.POS != 'NOUN' and ana.tag.POS != 'NPRO' and ana.tag.POS != 'VERB' and ana.tag.POS != 'INFN':
            if ana.tag.POS not in d:
                d[ana.tag.POS] = []
                d[ana.tag.POS].append(ana.normal_form)
            else:
                d[ana.tag.POS].append(ana.normal_form)

umessage = input('Введите ваше сообщение: ')

def parse_umessage(umessage):
    all_umes_ana = []
    umessage = re.sub(r'[^\w\s]', '', umessage)
    umessage = umessage.split()
    first = umessage[0]
    for mes in umessage:
        umes_ana = morph.parse(mes)
        umes_ana = umes_ana[0]
        print(umes_ana)
        
        all_umes_ana.append(umes_ana.tag)

    return all_umes_ana, first

def check_all(all_umes_ana, d, all_ana):
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

            elif uana.POS == 'VERB' or uana.POS == 'INFN':
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
                answer_word = random.choice(d[uana.POS])
                make_infl(answer_word, p_ana)

def make_infl(answer_word, p_ana):
    rand_ana = []
    cl_word = []
    answer_word_ana = morph.parse(answer_word)[0]
    print(answer_word_ana)
    rand_ana.append(answer_word_ana)
    for ans in rand_ana:
        infl_ana = str(ans.inflect(set(p_ana)))

        if 'Parse' in infl_ana:
            infl_ana = re.findall(r"\w+", infl_ana)
            cl_word.append(infl_ana[2])

        elif infl_ana == 'None':
            cl_ans = re.findall(r"\w+", str(ans))
            cl_word.append(ans[2])

    s_ans = ' '.join(cl_word)
    print(s_ans)

def main():
    get_words = words()
    get_lemmas = lemmas(get_words)
    get_nouns = nouns(get_lemmas)
    get_pronouns = pronouns(get_lemmas)
    get_verbs = verbs(get_lemmas)
    get_others = others(get_lemmas)
    get_message, get_first = parse_umessage(umessage)
    check_all(get_message, d, get_lemmas)

    # check_nouns(get_message, d, get_lemmas)
    # check_verbs(get_message, d, get_lemmas)
    # check_pronouns(get_message, d, get_lemmas)
    # check_others(get_message, d, get_lemmas)
  
if __name__ == '__main__':
    main()
