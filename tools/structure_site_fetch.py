#!/usr/bin/env python3

import urllib.request
import http.client
from lxml import etree
import pprint
from time import sleep


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


def get_form_struct_by_category(category_name='all'):
    from_struct_reslt = {}

    category_name = 'voitures'
    category_name = get_categories() if category_name == 'all' else category_name


def get_car_brands_list():
    brands_reslt = []
    req = urllib.request.urlopen('https://www.leboncoin.fr/voitures/offres/')
    tree = etree.fromstring(req.read(), parser=etree.HTMLParser())
    root = tree.xpath('//*[@id="brand_select"]/optgroup')

    if root == [] or len(root) != 2:
        return brands_reslt

    root_common_brands = root[0].getchildren()
    root_other_brands = root[1].getchildren()

    for elem in root_common_brands:
        brands_reslt += [elem.attrib['value'].replace(' ', '_')]
    for elem in root_other_brands:
        brands_reslt += [elem.attrib['value'].replace(' ', '_')]

    return brands_reslt


def get_car_models_list(lst_brands='all'):
    models_reslt = {}
    url = 'https://www.leboncoin.fr/beta/ajax/brand_model_list.html?brand={}'

    lst_brands = get_car_brands_list() if lst_brands == 'all' else lst_brands

    n, t = 1, len(lst_brands)
    for brand in lst_brands:
        print("fetching model of '{}' #{}/{}".format(brand, n, t))
        req = urllib.request.urlopen(url.format(brand))
        tree = etree.fromstring(req.read(), parser=etree.HTMLParser())
        root = tree.xpath('/html/body/option')

        for elem in root:
            if brand in models_reslt:
                models_reslt[brand] += [elem.text]
            else:
                models_reslt[brand] = [elem.text]
        n += 1
    return models_reslt


def get_regions():
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


def check_categories_link(dict_categories=None):

    if dict_categories == None:
        dict_categories = get_categories()

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


def get_categories(url='https://www.leboncoin.fr/annonces/offres/ile_de_france/'):
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


#f = open('car_models_list_pp.tmp', 'w')
#pp = pprint.PrettyPrinter(stream=f)
# pp.pprint(get_car_models_list())
# f.close()

# lbcdict = get_categories()
# pprint(lbcdict)
# print("Get categories fail" if lbcdict == {} else "Get categoires OK")

pprint.pprint(get_categories())
