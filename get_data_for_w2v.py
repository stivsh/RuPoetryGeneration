from clear_texts import *
import pickle
import numpy as np

def tokenize(text, reverce = False):
    tokens = (('-', ' <dash> '),
        (',', ' <comma> '),
        ('.', ' <period> '),
        ('?', ' <question> '),
        ('"', ' <double_quote> '),
        ('!', ' <exclamation> '))
    for t in tokens:
        if not reverce:
            text = text.replace(t[0], t[1])
        else:
            text = text.replace(t[1], t[0])
        
    return " ".join(text.split())



def remove_reare_words(tokend_text):
    words = tokend_text.split()
    w_counter = Counter(words)
    
    words_with_in_border = []
    
    for word, count_in_text in w_counter.items():
        if count_in_text > 3:
            words_with_in_border.append(word)
    
    new_words = [ w if w in words_with_in_border else "<rear_w>" for w in words ]
    return " ".join(new_words)
    


def get_vocab_dicts(prepared_text):
    word_to_inx = { key:inx for inx,key in enumerate(set(prepared_text.split())) }
    inx_to_word = list(set(prepared_text.split()))
    return word_to_inx, inx_to_word
    
def get_emb_data():
    if not os.path.isfile('data/emb_data.pkl'):
        prepared_text = get_prepared_text()
        dicts = get_dicts(prepared_text = prepared_text)
        data = get_data()
        with open('data/emb_data.pkl', 'wb') as f:
            pickle.dump({'prepared_text':prepared_text,
                         'dicts':dicts,
                         'data':data}, f)
            
    with open('data/emb_data.pkl','rb') as f:
        emb_data = pickle.load(f)
    return emb_data

def get_prepared_text():
    if not os.path.isfile('data/emb_data.pkl'):
        text = ''.join(get_textes())
        tokend_text = tokenize(text)
        prepared_text = remove_reare_words(tokend_text)
    else:
        prepared_text = get_emb_data()['prepared_text']
    return prepared_text

def get_dicts(prepared_text = None):
    if not os.path.isfile('data/emb_data.pkl'):
        word_to_inx, inx_to_word = get_vocab_dicts(prepared_text if prepared_text else get_prepared_text())
    else:
        word_to_inx, inx_to_word = get_emb_data()['dicts']
    
    return word_to_inx, inx_to_word
    
def get_data():
    if not os.path.isfile('data/emb_data.pkl'):
        word_to_inx, inx_to_word = get_dicts()
        def encode(prepared_text):
            return np.array([word_to_inx[w] for w in prepared_text.split() ])
            
        poems = get_prepared_text().split('#')
        poems = [ encode(" ".join(p.split())+' #') for p in poems ]
        data = poems
    else:
        data = get_emb_data()['data']
    return data

