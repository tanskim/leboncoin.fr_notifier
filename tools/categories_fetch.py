import urllib.request
from lxml import etree
import pprint


def strip_all(text):
    text = text.lower()
    text = text.replace(' & ', '_')
    text = text.replace(' - ', '_')
    text = text.replace('-', '_')
    text = text.replace(' / ', '_')
    text = text.replace(' ', '_')
    text = text.replace('é', 'e')
    text = text.replace('ê', 'e')
    text = text.replace('ô', 'o')
    text = text.replace('î', 'i')
    text = text.replace('\'', ' ')
    return text


def get_leboncoin_categories(url='https://www.leboncoin.fr/annonces/offres/ile_de_france/'):
    req = urllib.request.urlopen(
        'https://www.leboncoin.fr/annonces/offres/ile_de_france/')
    tree = etree.fromstring(req.read(), parser=etree.HTMLParser())
    root = tree.xpath('//*[@id="search_category"]')
    options = root[1]

    cat = {}

    for o in options[1:]:
        stext = o.text.strip()
        if stext.startswith('--'):
            title_cat = stext[3:-3]
            cat[title_cat] = []
            continue
        cat[title_cat] += [strip_all(stext)]
    return cat


pprint.pprint(get_leboncoin_categories())
