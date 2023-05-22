from inspect import unwrap
from bs4 import BeautifulSoup
from googletrans import Translator
# from google_trans_new import google_translator  
import re
t = Translator()

def spanRemover(soup):      # Remove previous spans
    spans = soup.find_all('span')
    for i in spans:
        sp = soup.span.unwrap()

def spanInsert(tag):
    # if not tag.string:
    #     return str(tag)
    # norwegian = '''\n <span class="multilang" lang="no">''' + translateTagCont(tag) + '</span'
    list_string = str(tag).split('>')
    list_string.insert(1, '''<span class="multilang" lang="en"''')
    half = '>'.join(list_string)
    
    half_string_list = half.split("<")
    half_string_list.insert(-1, '''/span> \n <span class="multilang" lang="no">''' + translateTagCont(tag) + '</span>')
    return '<'.join(half_string_list)

def translateTagCont(tag):
    finalString = ""
    for c in tag.contents:
        if str(c)[0] == "\\" or not str(c).strip():
            finalString = finalString + str(c) + " "
        else:
            finalString = finalString + t.translate(str(c), src="en", dest="no").text + " "

    return finalString

def translateHTMLCode(filename):

    with open(filename) as fp:
        soup = BeautifulSoup(fp, "html.parser")

    spanRemover(soup)

    tagsTBT = ["h3", "h4", "p"]#, "li"]
    for tag in tagsTBT:
        paras = soup.find_all(tag)
        for par in paras:
            pars = spanInsert(par)
            par.replace_with(BeautifulSoup(pars, "html.parser"))

    o = open("output.html", "w", encoding='utf-8')
    o.write(str(soup))
    o.close()

# new_span    = soup.new_tag("span", **{'class':'multilang'}, lang="en")
# new_span_no = soup.new_tag("span", **{'class':'multilang'}, lang="no")
translateHTMLCode("input.html")

# string = '''To find the vector \(\overrightarrow{AB}\) we simply subtract the position vector or \(A\) from the position vector of \(B\):'''
# test = re.split(r"\(", string)
# print(test)