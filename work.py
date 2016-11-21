import os
import re
import json
from flask import Flask
from flask import url_for, render_template, request, redirect

def open_files():
    thai_dictionary = {}

    for i in range(187, 207):
        for y in range (1, 75):
            try:
                file = open('thai_pages' + os.sep + str(i) + '.' + str(y)+ '.html', 'r')
                lines = file.read()
                regPostThai = re.compile('<td class=th><a href=.*?>(.*?)</a></td>', flags=re.U | re.DOTALL)
                thai_words = regPostThai.findall(lines)
                regPostTransl = re.compile('<td class=pos>.*?</td><td>(.*?)</td>', flags=re.U | re.DOTALL)
                transl = regPost.findall(lines)
        
                new_thai = []
                regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
                regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
                for t in thai_words:
                    clean_t = regSpace.sub("", t)
                    clean_t = regTag.sub("", clean_t)
                new_thai.append(clean_t)

                new_transl = []
                regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
                regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
                regNum = re.compile('&#[0-10][0-10];', flags=re.U | re.DOTALL )
                for t in transl:
                    clean_t = regSpace.sub("", t)
                    clean_t = regTag.sub("", clean_t)
                    clean_t = regNum.sub("", clean_t)
                new_transl.append(clean_t) 

                thai_dictionary = dict(zip(thai_words, transl)) # map two lists into a dictionary

                file.close()

            except:
                print('No such file ' + str(i) + '.' + str(y))

    return thai_dictionary

def make_json(thai_dictionary):
    with open('thai.json', 'w') as jsonfile:
        json.dump(thai_dictionary, jsonfile)

    pass

def make_json_invert(thai_dictionary):   
    thai_dictionary_r = {thai_dictionary[thai_words]: thai_words
        for thai_words in thai_dictionary}
    with open('eng.json', 'w') as jsonfile:
        json.dump(thai_dictionary_r, jsonfile)

    pass

@app.route('/')
def index():
    if request.args:
        return redirect(url_for('results', text=request.args['text']))

    return render_template('index.html')

@app.route('/results')
def results():
    result = {}
    text = request.args['text'].lower()

    for json_data in make_json_invert():
        question_data = json_data['transl']
        answer_data = json_data['thai_words']

    return render_template('results.html', result=result, text=text)

#def get_english:
#    with open('eng.json') as jsonfile:
#        json_data = json.load(jsonfile)

#    return json_data
#def main():
#    thai = open_files()
#    thai_english = make_json(thai)
#    enlish_thai = make_json_invert(thai)


if __name__ == '__main__':
   app.run(debug=True)



            
