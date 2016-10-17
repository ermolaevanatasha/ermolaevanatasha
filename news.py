import urllib.request
import time
import re

def find_clean_text(f, html):
    regPostText = re.compile('<div class="article-content">(.*?)</div>', flags=re.U | re.DOTALL)
    text = regPostText.findall(html)
    new_text = []
    regTag = re.compile('<.*?>')
    regSpace = re.compile('\s{2,}')
    for tx in text:
        clean_tx = regSpace.sub("", tx)
        clean_tx = regTag.sub("", clean_tx)
        new_text.append(clean_tx)
    for tx in new_text:
        f.write(tx)
        
def find_author(html):
    regPostAuthor = re.compile('<span class="createby">\n.*?</span>', flags=re.U | re.DOTALL) 
    author = regPostAuthor.findall(html)
    if author == []:
        f.write('@au Noname' + '\n')
    else:       
        new_author = []
        regTag = re.compile('<.*?>')
        regSpace = re.compile('\s{2,}')
        for a in author:
            clean_a = regSpace.sub("", a)
            clean_a = regTag.sub("", clean_a)
            new_author.append(clean_a)
        
    return new_author

def find_title(html):
    regPostTitles = re.compile('<title>.*?</title>', flags=re.U | re.DOTALL) 
    titles = regPostTitles.findall(html)
    new_titles = []
    regTag = re.compile('<.*?>')
    regSpace = re.compile('\s{2,}')
    for t in titles:
        clean_t = regSpace.sub("", t)
        clean_t = regTag.sub("", clean_t)
        new_titles.append(clean_t)

    return new_titles
        
def find_date(html):
    regPostDate = re.compile('<span class="createdate">\n.*?</span>', flags=re.U | re.DOTALL) 
    dates = regPostDate.findall(html)
    new_dates = []
    regTag = re.compile('<.*?>')
    regSpace = re.compile('\s{1,}')
    regNum = re.compile('\d{2}:\d{2}')
    for d in dates:
        clean_d = regSpace.sub("", d)
        clean_d = regTag.sub("", clean_d)
        clean_d = regNum.sub("", clean_d)
        new_dates.append(clean_d)
        
    return new_dates
            
def find_url(f, pageUrl):
    page_url = '@url' + ' ' + pageUrl  + '\n'
    f.write(page_url)
    
import os

def make_record(name, new_dates):
    for dat in new_dates:
        dat = dat.split('.')
    filename = os.path.join('News', name, dat[2], dat[1])
    if not os.path.exists(filename):
        os.makedirs(filename)
    return filename
    
def make_metadata(path, new_author, new_titles, new_dates, pageUrl):
    row = '%s\t%s\t\t\t%s\t%s\tпублицистика\t\tnotopic\t\t\tнейтральный\tн-возраст\tн-уровень\tрайонная\t%s\tКрасное знамя\t\t%s\tгазета\tРоссия\tУдмурсткая республика\tru'
    metadata = open("/Users/nata/Desktop/News/metadata.csv", 'a', encoding = 'utf-8')
    metadata.write(row %(''.join(path), ''.join(new_author), ''.join(new_titles), ''.join(new_dates), ''.join(pageUrl), ''.join(new_dates)) + '\n')
    metadata.close()
           
arr = []
commonUrl = 'http://kr-znamya.ru/index.php?option=com_content&view=article&id='
name = 'plain_text'
name_mystem_xml = 'mystem_xml'
name_mystem_plain = 'mystem_plain_text'
dirs = '/Users/nata/Desktop'

for i in range(12737, 13008): 
    pageUrl = commonUrl + str(i)
    with urllib.request.urlopen(pageUrl) as response:
        time.sleep(2)
        html = response.read().decode('utf-8')
        new_author = find_author(html)
        new_titles = find_title(html)
        new_dates = find_date(html)
        create_folder = make_record(name, new_dates)
        create_folder_mystem = make_record(name_mystem_xml, new_dates)
        create_folder_mystem_plain = make_record(name_mystem_plain, new_dates)
    f = open(create_folder + os.sep + 'Article' + str(i) + ".txt", "w", encoding = 'utf-8')
    arr.append(pageUrl)

    for a in new_author:
        f.write('@au' + ' ' + a + '\n')
    for t in new_titles:
        f.write('@ti' + ' ' + t + '\n')
    for d in new_dates:
        f.write('@da' + ' ' + d + '\n')
    find_url(f, pageUrl)
    find_clean_text(f, html)
    path = []
    make_path = make_record(name, new_dates)
    path.append(make_path)
    make_metadata(path, new_author, new_titles, new_dates, pageUrl)
    f.close()
    inp = dirs + '/' + create_folder
    lst = os.listdir(inp)
    for fl in lst:
        os.system(r'/Users/nata/Desktop/mystem ' + inp + os.sep + fl + ' ' + dirs + '/' + create_folder_mystem + os.sep + fl + ' -cnid --format xml --eng-gr')
        os.system(r'/Users/nata/Desktop/mystem ' + inp + os.sep + fl + ' ' + dirs + '/' + create_folder_mystem_plain + os.sep + fl + ' -cnid --format text --eng-gr')
