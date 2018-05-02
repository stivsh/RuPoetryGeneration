import os
import pickle
import string
from collections import Counter
#clean and prepare textes

def prepare_texts(textes):

    #remove some laters
    replasements = [('\t',''),
                   ('»','"'),
                   ('«','"'),
                   ('—','-'),
                   (';',','),
                   (':',','),
                   ('\n',' '),
                   ('#',' ')]

    def perform_repls(text):
        for r in replasements:
            text = text.replace(r[0],r[1])
        return text
    
    def remove_multiple_punctuation(text):
        carters_of_new_text = []
        last_added = '.'
        for c in text:
            if not(last_added in  string.punctuation and c in  string.punctuation):
                last_added = c
                carters_of_new_text.append(c)
        return "".join(carters_of_new_text)

    textes = [ perform_repls(t) for t in textes ]
    textes = [ remove_multiple_punctuation(t) for t in textes ]
    #remove reare laters
    later_counter = Counter()
    for t in textes:
        later_counter.update(t)
    total_count = sum(later_counter.values())
    later_prob = { later:count/total_count for later,count in later_counter.most_common() }
    z_prob = later_prob['ё']
    alphabit = set([ l for l,prob in later_prob.items() if prob >= z_prob ])

    def remove_reare(text):
        return ''.join([ l if l in alphabit else ' ' for l in text  ])

    textes = [ remove_reare(t) for t in textes ]

    #remove multiple spaces
    textes = [ " ".join(t.split()) for t in textes ]

    #add end of poem symbol
    textes = [ t+' # ' for t in textes if len(t) > 150 and len(t) < 2000 ]

    return textes

def get_textes():
    textes = None
    if not os.path.isfile('data/textes.pkl'):
        print('prepare textes')
        with open('data/poems.pkl','rb') as f:
            poems = pickle.load(f)
        textes = [ poem['text'].lower() for poem in poems ]
        textes = prepare_texts(textes)
        with open('data/textes.pkl', 'wb') as f:
            pickle.dump(textes, f)
    else:
        with open('data/textes.pkl','rb') as f:
            textes = pickle.load(f)
    return textes
