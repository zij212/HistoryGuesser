from Levenshtein import distance 
import unidecode

def remove_punctuation(name):
    name = name.replace('.','')
    name = name.replace(',','')
    name = name.replace("'",'')
    name = name.replace('"','')
    name = name.replace(';','')
    name = name.replace(':','')
    name = name.replace('/','')
    return name

# Makes a generous comparison between a submitted answer and a proper answer
# genghis == Gengis
# genghis == Genghiss
# Atatürk == ataturk
# Peter the Great == Peter == Great != the
def liberal_compare(name1, name2):
    # ignore care
    name1 = name1.lower()
    name2 = name2.lower()
    # ignore punctuation
    name1 = remove_punctuation(name1)
    name2 = remove_punctuation(name2)

    # convert accents to ascii letters
    name1 = unidecode.unidecode(name1)
    name2 = unidecode.unidecode(name2)

    options1 = []
    options2 = []
    for option in name1.split(' '):
        if option not in ('of', 'the', 'in',):
            options1.append(option)
            if len(options1) > 4:
                break

    for option in name2.split(' '):
        if option not in ('of', 'the', 'in',):
            options2.append(option)
            if len(options2) > 4:
                break

    for option1 in options1:
        for option2 in options2:
            if distance(option1, option2) < 2:
                return True
    

assert liberal_compare('ghengis', 'GHENGiS')
assert liberal_compare('ghengis', 'GENGiS')
assert liberal_compare('Atatürk', 'ataturk')
assert liberal_compare('Atatürk', 'atatark')
assert liberal_compare('Peter the great', 'peter')
assert liberal_compare('Peter great', 'peter the great')
assert not liberal_compare('the', 'peter the great')
assert liberal_compare('the greatt', 'peter the great')
