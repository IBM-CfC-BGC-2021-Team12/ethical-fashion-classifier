import csv
import json
import nltk
import re
import requests
from bs4 import BeautifulSoup

# From https://goodonyou.eco/most-ethical-and-sustainable-clothing-brands-from-us-and-canada/
ethical_brands = [
    "https://www.tentree.com/",
    "https://svala.co/",
    "https://www.337brand.com/",
    "https://www.harvestandmill.com/",
    "https://www.miakodanewyork.com/",
    "https://joinyesand.com/",
    "https://matethelabel.com/",
    "https://theclassictshirt.com/",
    "https://milonicki.com/",
    "https://knickey.com/",
    "https://hyergoods.com/",
    "https://nubeusa.com/",
    "https://shop-arielle.com/",
    "https://wearfranc.com/",
    "https://www.altarpdx.com/",
    "https://thercollective.com/",
    "https://malaikanewyork.com/",
    "https://www.happyearthapparel.com/",
    "https://unspun.io/",
    "https://www.fairindigo.com/",
    "https://www.threads4thought.com/",
    "https://www.outerknown.com/",
    "https://tonle.com/",
    "https://consciousstep.com/",
    "https://wamaunderwear.com/",
    "https://www.tamgadesigns.com/",
    "https://article22.com/",
    "https://whimsyandrow.com/",
    "https://aliceandwhittles.com/",
    "https://www.vitaminaswim.com/",
    "https://www.seekcollective.com/",
    "https://www.girlfriend.com/",
    "https://marahoffman.com/",
    "https://triarchy.com/",
    "https://eclipseglove.com/",
    "https://sotela.co/",
    "https://www.eileenfisher.com/",
    "https://www.boyish.com/",
    "https://grammarnyc.com/"
]
# From https://theprettyplaneteer.com/fast-fashion-brands-to-avoid/
unethical_brands = [
    "https://www.nike.com/",
    "https://www.victoriassecret.com/us/",
    "https://www.zara.com/us/",
    "https://www2.hm.com/en_us/index.html",
    "https://www.fashionnova.com/",
    "https://www.forever21.com/",
    "https://www.prettylittlething.us/",
    "https://shop.mango.com/us",
    "https://us.shein.com/",
    # "https://www.asos.com/us/", # Hangs.  May have scraping countermeasures
    "https://my.topshop.com/",
    "https://www.urbanoutfitters.com/",
    "https://www.bershka.com/us/women-c1010193132.html",
    "https://www.primark.com/",
    "https://www.stradivarius.com/",
    "https://www.pullandbear.com/us/",
    "https://us.boohoo.com/",
    "https://www.missguidedus.com/",
    "https://www.riachuelo.com.br/",
    "https://www.wish.com/",
    "https://www.aliexpress.com/",
    "https://www.zaful.com/",
    # "https://www.hollisterco.com/shop/us", # Hangs.  May have scraping countermeasures
    "https://www.nastygal.com/",
    # "https://www.abercrombie.com/shop/us", # Hangs.  May have scraping countermeasures
    "https://www.gymshark.com/",
    "https://www.anthropologie.com/",
    "https://us.brandymelville.com/",
    "https://www.ae.com/us/en",
    "https://www.freepeople.com/",
    "https://www.gap.com/",
    "https://www.na-kd.com/en",
    "https://www.newlook.com/uk",
    "https://www.walmart.com/",
    # "https://www.uniqlo.com/us/en/home/", # Hangs.  May have scraping countermeasures
    "https://www.riverisland.com/",
    "https://oldnavy.gap.com/",
    "https://www.target.com/",
    "https://www.oysho.com/gb/"
]

training_data_file = open("fashion-brands-train.csv", "wt")

index_ethical_80percent = int(len(ethical_brands) * .8)
index_unethical_80percent = int(len(unethical_brands) * .8)

print(f"Ethical data 80% train/test split index: {index_ethical_80percent}.")
print(f"Unethical data 80% train/test split index: {index_unethical_80percent}.")

for url in ethical_brands[:index_ethical_80percent]:
    print(f"Creating train feature text for {url}.")
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    text = soup.get_text().lower()
    list_of_words = nltk.tokenize.casual_tokenize(text)
    string_of_words = " ".join(list_of_words)
    alnum_only = re.sub(r'[^a-zA-Z ]', '', string_of_words)
    feature_text = alnum_only[:1024]
    training_data_file.write(feature_text + ",ETHICAL\n")

for url in unethical_brands[:index_unethical_80percent]:
    print(f"Creating train feature text for {url}.")
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    text = soup.get_text().lower()
    list_of_words = nltk.tokenize.casual_tokenize(text)
    string_of_words = " ".join(list_of_words)
    alnum_only = re.sub(r'[^a-zA-Z ]', '', string_of_words)
    feature_text = alnum_only[:1024]
    training_data_file.write(feature_text + ",UNETHICAL\n")

training_data_file.close()

test_data_file = open("fashion-brands-test.csv", "wt")

for url in ethical_brands[index_ethical_80percent:]:
    print(f"Creating test feature text for {url}.")
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    text = soup.get_text().lower()
    list_of_words = nltk.tokenize.casual_tokenize(text)
    string_of_words = " ".join(list_of_words)
    alnum_only = re.sub(r'[^a-zA-Z ]', '', string_of_words)
    feature_text = alnum_only[:1024]
    test_data_file.write(feature_text + ",ETHICAL\n")

for url in unethical_brands[index_unethical_80percent:]:
    print(f"Creating test feature text for {url}.")
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    text = soup.get_text().lower()
    list_of_words = nltk.tokenize.casual_tokenize(text)
    string_of_words = " ".join(list_of_words)
    alnum_only = re.sub(r'[^a-zA-Z ]', '', string_of_words)
    feature_text = alnum_only[:1024]
    test_data_file.write(feature_text + ",UNETHICAL\n")

test_data_file.close()

