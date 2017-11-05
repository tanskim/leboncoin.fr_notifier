#!/usr/bin/env python3

import urllib.request
import http.client
from lxml import etree
from pprint import pprint


def strip_all(text):
    text = text.lower()
    text = text.replace(' & ', '_')
    text = text.replace(' - ', '_')
    text = text.replace('-', '_')
    text = text.replace(' / ', '_')
    text = text.replace(' ', '_')
    text = text.replace('é', 'e')
    text = text.replace('è', 'e')
    text = text.replace('ê', 'e')
    text = text.replace('ô', 'o')
    text = text.replace('î', 'i')
    text = text.replace('ù', 'u')
    text = text.replace('ë', 'e')
    text = text.replace('ç', 'c')
    text = text.replace('â', 'a')
    text = text.replace('à', 'a')
    text = text.replace('\'', '_')
    return text


def leboncoin_get_regions():
    regions_reslt = []
    req = urllib.request.urlopen(
        'https://www.leboncoin.fr/')
    tree = etree.fromstring(req.read(), parser=etree.HTMLParser())
    root = tree.xpath('//*[@id="home"]/section[2]/ul/li')

    if root == []:
        return regions_reslt

    for li in root:
        regions_reslt += [li.getchildren(
        )[0].attrib['href'].strip().split('/')[-2]]
    return regions_reslt


def leboncoin_check_categories_link(dict_categories=None):

    if dict_categories == None:
        dict_categories = leboncoin_get_categories()

    dict_reslt = {}
    url = "/{}/offres/?th=1"
    con = http.client.HTTPSConnection("www.leboncoin.fr", 443)

    for k in dict_categories.keys():
        for cat_name in dict_categories[k]:
            con.request('GET', url.format(cat_name))
            response = con.getresponse()
            if response.getcode() == 200:
                dict_reslt[cat_name] = "OK"
            else:
                dict_reslt[cat_name] = "FAIL : " + str(response.getcode())
            response.read()
    con.close()
    return dict_reslt


def leboncoin_get_categories(url='https://www.leboncoin.fr/annonces/offres/ile_de_france/'):
    categories_rslt = {}
    req = urllib.request.urlopen(
        'https://www.leboncoin.fr/annonces/offres/ile_de_france/')
    tree = etree.fromstring(req.read(), parser=etree.HTMLParser())
    root = tree.xpath('//*[@id="search_category"]')

    if root == []:
        return categories_rslt

    options = root[1]
    for o in options[1:]:
        stext = o.text.strip()
        if stext.startswith('--'):
            title_cat = stext[3:-3]
            categories_rslt[title_cat] = []
            continue
        categories_rslt[title_cat] += [strip_all(stext)]
    return categories_rslt


#lbcdict = leboncoin_get_categories()
# pprint(lbcdict)
# print("Get categories fail" if lbcdict == {} else "Get categoires OK")
pprint(leboncoin_check_categories_link())
# pprint(leboncoin_get_regions())
