import csv
import json
import sys
import nltk
import re
import requests
from bs4 import BeautifulSoup
from ibm_watson import NaturalLanguageClassifierV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from pprint import pprint

if len(sys.argv) < 2:
    print("Usage:")
    print("python3 update_status.py <api key>")
    sys.exit(0)

apikey = sys.argv[1]
test_data_file = sys.argv[2]

with open("classifier.json", "rt") as classifier_file:
    classifier = json.load(classifier_file)

# The classifier_url is NOT the full classifier_url listed in the classifier
# JSON description.  It is only the part before "/v1/...".  Learning experience:
# bad API design!
classifier_url = classifier['url'].split("/v1/")[0]
classifier_id = classifier['classifier_id']

authenticator = IAMAuthenticator(apikey)
natural_language_classifier = NaturalLanguageClassifierV1(
    authenticator=authenticator
)

num_test_cases = 0
num_errors = 0
with open(test_data_file) as test_data:
    test_data_reader = csv.reader(test_data)
    for row in test_data_reader:
        num_test_cases += 1
        feature_text = row[0]
        correct_class = row[1]
        natural_language_classifier.set_service_url(classifier_url)
        classes = natural_language_classifier.classify(
            classifier_id,
            feature_text).get_result()
        predicted_class = classes['top_class']
        if predicted_class != correct_class:
            num_errors += 1

error_rate = num_errors / num_test_cases
print(f"Error rate on {test_data_file}: {error_rate:.2} ({num_errors}/{num_test_cases}).")

