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

    ignore_list = (
        'of', 'the', 'in', 'queen', 'king', 'sir',
        'I', 
        # "II", "III", "IV", "V", "VI","VII", "VIII",
    )

    options1 = []
    options2 = []
    for option in name1.split(' '):
        if option not in ignore_list:
            options1.append(option)
            if len(options1) > 4:
                break

    for option in name2.split(' '):
        if option not in ignore_list:
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
assert liberal_compare('queen elizabeth', 'elizabeth I')
assert not liberal_compare('elizabeth', 'peter the great')
assert not liberal_compare('queen elizabeth', 'queen')

# convert 100 to "2nd century"
# convert -100 to "2nd century BC"
def year2century(year):
    is_bc = year < 0
    number = abs((abs(year)- (1 * is_bc))//100) + 1

    if number == 1:
        sth = 'st'
    elif number == 2:
        sth = 'nd'
    elif number == 3:
        sth = 'rd'
    else:
        sth = 'th'

    century = f'{number}{sth} century'
    if is_bc:
        century = century + ' BC'
    # print(century)
    return century

assert year2century(-200) == '2nd century BC'
assert year2century(-100) == '1st century BC'
assert year2century(0) == '1st century'
assert year2century(100) == '2nd century'
assert year2century(200) == '3rd century'
assert year2century(300) == '4th century'
