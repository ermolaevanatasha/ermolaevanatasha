import pymorphy2
from pymorphy2 import MorphAnalyzer
import re
import random
import string

morph = MorphAnalyzer()

def words():
    with open('awords.txt', 'r', encoding='utf-8') as f:

    # для обычного текста:
    #     lines = f.read()
    #     cl_lines = re.sub(r'[.,!?;:\u2013\u2014«»"@№#&$%^*()<>+=\/|\\]+\ *', ' ', lines)
    #     all_words = cl_lines.split()

    # return all_words

    # для списка слов из НКРЯ:
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
                d[ana.tag.POS][ana.tag.person] = {}
                continue

            if ana.tag.number not in d[ana.tag.POS][ana.tag.person]:
                d[ana.tag.POS][ana.tag.person][ana.tag.number] = []
                d[ana.tag.POS][ana.tag.person][ana.tag.number].append(ana.normal_form)
            else:
                d[ana.tag.POS][ana.tag.person][ana.tag.number].append(ana.normal_form)

def verbs(all_ana):
    for ana in all_ana:
        if ana.tag.POS == 'VERB' or ana.tag.POS == 'INFN' or ana.tag.POS == 'GRND':
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

def adjs(all_ana):
    for ana in all_ana:
        if ana.tag.POS == 'ADJS':
            if ana.tag.POS not in d:
                d[ana.tag.POS] = {}
                continue

            if ana.tag.number not in d[ana.tag.POS]:
                d[ana.tag.POS][ana.tag.number] = {}
                continue

            if ana.tag.gender not in d[ana.tag.POS][ana.tag.number]:
                d[ana.tag.POS][ana.tag.number][ana.tag.gender] = []
                d[ana.tag.POS][ana.tag.number][ana.tag.gender].append(ana.normal_form)
            else:
                d[ana.tag.POS][ana.tag.number][ana.tag.gender].append(ana.normal_form)

def others(all_ana):
    for ana in all_ana:
        if ana.tag.POS != 'NOUN' and ana.tag.POS != 'NPRO' and ana.tag.POS != 'VERB' and ana.tag.POS != 'INFN' and ana.tag.POS != 'GRND' and ana.tag.POS != 'ADJS':
            if ana.tag.POS not in d:
                d[ana.tag.POS] = []
                d[ana.tag.POS].append(ana.normal_form)
            else:
                d[ana.tag.POS].append(ana.normal_form)

umessage = input('Введите ваше сообщение: ')

def parse_umessage(umessage):
    all_umes_ana = []
    # umes_word = []
    umessage = re.sub(r'[^\w\s]', '', umessage)
    umessage = umessage.split()
    for mes in umessage:
        umes_ana = morph.parse(mes)
        umes_ana = umes_ana[0]
        # print(umes_ana)
        
        all_umes_ana.append(umes_ana.tag)
        # umes_word.append(umes_ana)

    return all_umes_ana # umes_word

def check_all(all_umes_ana, d, all_ana): # umes_word
    for uana in all_umes_ana:
        p_ana = re.findall(r"[\w']+", str(uana))
        if uana.POS in d:
            if uana.POS == 'NOUN':
                check_nouns(uana, p_ana)

            elif uana.POS == 'VERB':
                check_verbs(uana, p_ana)

            elif uana.POS == 'INFN':
                check_infns(uana, p_ana)

            elif uana.POS == 'GRND':
                check_grnds(uana, p_ana)

            elif uana.POS == 'NPRO':
                check_pronouns(uana, p_ana)

            elif uana.POS == 'ADJS':
                check_adjshs(uana, p_ana)

            else:
                answer_word = random.choice(d[uana.POS])
                make_infl(answer_word, p_ana)

            # else:
            #     if uana.POS not in d:
            #         for uw in umes_word:
            #             answer_word = uw.word

def check_nouns(uana, p_ana):
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

def check_verbs(uana, p_ana):
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

def check_infns(uana, p_ana):
    if uana.aspect == 'perf':
        if uana.transitivity == 'tran':
            answer_word = random.choice(d['INFN']['perf']['tran'])
            make_infl(answer_word, p_ana)
        else:
            answer_word = random.choice(d['INFN']['perf']['intr'])
            make_infl(answer_word, p_ana)
    
    else:
        if uana.transitivity == 'tran':
            answer_word = random.choice(d['INFN']['impf']['tran'])
            make_infl(answer_word, p_ana)
        else:
            answer_word = random.choice(d['INFN']['impf']['intr'])
            make_infl(answer_word, p_ana)

def check_grnds(uana, p_ana):
    if uana.aspect == 'perf':
        if uana.transitivity == 'tran':
            answer_word = random.choice(d['GRND']['perf']['tran'])
            make_infl(answer_word, p_ana)
        else:
            answer_word = random.choice(d['GRND']['perf']['intr'])
            make_infl(answer_word, p_ana)
            
    else:
        if uana.transitivity == 'tran':
            answer_word = random.choice(d['GRND']['impf']['tran'])
            make_infl(answer_word, p_ana)
        else:
            answer_word = random.choice(d['GRND']['impf']['intr'])
            make_infl(answer_word, p_ana)

def check_pronouns(uana, p_ana):
    if uana.person == '1per':
        if uana.number == 'sing':
            answer_word = random.choice(d['NPRO']['1per']['sing'])
            make_infl(answer_word, p_ana)
        else:
            answer_word = random.choice(d['NPRO']['1per']['plur'])
            make_infl(answer_word, p_ana)

    elif uana.person == '2per':
        if uana.number == 'sing':
            answer_word = random.choice(d['NPRO']['2per']['sing'])
            make_infl(answer_word, p_ana)
        else:
            answer_word = random.choice(d['NPRO']['2per']['plur'])
            make_infl(answer_word, p_ana)
    else:
        if uana.number == 'sing':
            answer_word = random.choice(d['NPRO']['3per']['sing'])
            make_infl(answer_word, p_ana)
        else:
            answer_word = random.choice(d['NPRO']['3per']['plur'])
            make_infl(answer_word, p_ana)

def check_adjshs(uana, p_ana):
    if uana.number == 'sing':
        if uana.gender == 'masc':
            answer_word = random.choice(d['ADJS']['sing']['masc'])
            make_infl(answer_word, p_ana)
        elif uana.tag.gender == 'femn':
            answer_word = random.choice(d['ADJS']['sing']['femn'])
            make_infl(answer_word, p_ana)
        else:
            answer_word = random.choice(d['ADJS']['sing']['neut'])
            make_infl(answer_word, p_ana)

    else:
        answer_word = random.choice(d['ADJS']['plur'])
        make_infl(answer_word, p_ana)

def make_infl(answer_word, p_ana):
    rand_ana = []
    cl_word = []
    answer_word_ana = morph.parse(answer_word)[0]
    # print(answer_word_ana)
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
    get_adjs = adjs(get_lemmas)
    get_others = others(get_lemmas)
    get_message = parse_umessage(umessage)
    check_all(get_message, d, get_lemmas)
  
if __name__ == '__main__':
    main()
