from os import path
from PIL import Image
import numpy as np
import matplotlib
matplotlib.use('SVG') #set the backend to SVG
import matplotlib.pyplot as plt
import os
import re
from wordcloud import WordCloud
import random
import sys
# Read the whole text.

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(20,20)

def red_color(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 100%,50%)"

def black_color(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 100%,1%)"

def generate_treemap(texto_limpo):
    import collections
    # print(collections.Counter(texto_limpo))
    resultado=collections.Counter(texto_limpo)
    size=[]
    grupo=[]
    treemap=[]
    for i in resultado:
        element={}
        if(resultado[i]>0):
            size.append(resultado[i])
            grupo.append(i)
            element["name"]=i
            element["children"]=[{"name":i,"value":resultado[i]}]
            treemap.append(element)
    print(treemap)

try:
    NAME_FILE=sys.argv[1]
    #levanta uma excessão generiuca
    if(".tpmodel" not in NAME_FILE):
        raise Exception
        #print("formato Invalid")
except Exception as e :
    print("Erro\nDigite o nome do arquivo com as modelagens de topico\nExtensao .tpmodel")
    exit()

text = open(NAME_FILE,"r").read()
text=text.strip()
text=text.replace("Topic:","").replace("Words:"," ")
text=text.replace("+","")
text=re.sub(r"\d.","",text)
text=re.sub(r"\s{2}","_",text)
text=text.split("_")
texto_limpo=[]
for i in text:
    if(len(i)>1):
        texto_limpo.append(i.strip().replace("\""," ").strip().replace(" ","_"))
text=" ".join(texto_limpo)


# {
#    name: 'Alcohol/Fremented',
 #   children: [{
#      name: 'Winey', value: 1
#    },
#
#

wordcloud = WordCloud().generate(text)


# lower max_font_size
wordcloud = WordCloud(max_words=300,height=300,width=800,max_font_size=40,margin=1,min_font_size=4,background_color="white").generate(text)
figure = plt.figure()
plt.imshow(wordcloud.recolor(color_func=black_color, random_state=0), interpolation="bilinear")
plt.axis("off")
fig = plt.gcf() #get current figure
fig.set_size_inches(10,10)  
plt.savefig(NAME_FILE+"_black.pdf", dpi=1200)
#plt.show()
# figure.savefig(NAME_FILE+"_cloud22.svg")
