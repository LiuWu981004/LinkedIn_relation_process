def inverse(input_string, annotated):
    {'ner': [{'start': 1, 'end': 2, 'type': 'PER'}]}
    

def g(, start, end):
    """
    
    :param start: 混合文本的索引 
    :param end: 
    :return: 
    """
    mask=[...]
    

def process_document(en_text):
    sentence_texts=split_sentences(en_text)
    ind=[]         
    encn_text=[]
    for sent in sentence_texts:
        enind, cnind, cn_sent=process_sentence(sent)
        ind.extend(enind)
        ind.extend(cnind)
        encn_text.extend(sent)
        encn_text.extend(cn_sent)
        
    return ind, ''.join(encn_text)
    
    

    

def process_sentence(en_sentence):
    """
    :param en_sentence: 
    :return:  mask: 1 for chinese, 0 for english 
    """
    cn_sentence=translate(en_sentence)
    cnind=[1]*len(cn_sentence)
    enind=[0]*len(en_sentence)
    return enind, cnind, cn_sentence
    