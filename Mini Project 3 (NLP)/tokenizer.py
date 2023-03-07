import spacy

lines = []

file1 = open('mostcommon.txt', 'r')
lines = file1.readlines()
file1.close()


nlp = spacy.load("en_core_web_sm")

d = dict()

for idx, line in enumerate(lines):  
    token = nlp(line.rstrip())[0]
    # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
    #         token.shape_, token.is_alpha, token.is_stop)
    
    d[line.rstrip()] = token.pos_

print(d)