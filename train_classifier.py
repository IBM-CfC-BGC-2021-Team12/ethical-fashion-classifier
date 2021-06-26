"""
Based on instructions and example code at https://cloud.ibm.com/docs/natural-language-classifier?topic=natural-language-classifier-natural-language-classifier#create-train
"""

import json
import sys
from ibm_watson import NaturalLanguageClassifierV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

if len(sys.argv) < 3:
    print("Usage:")
    print("python3 train_classifier.py <api key> <classifier url> <training data file>")
    sys.exit(0)

apikey = sys.argv[1]
url = sys.argv[2]
training_data_file = sys.argv[3]

authenticator = IAMAuthenticator(apikey)
natural_language_classifier = NaturalLanguageClassifierV1(
    authenticator=authenticator
)

natural_language_classifier.set_service_url(url)

with open(training_data_file, 'rb') as training_data, \
        open('classifier.json', 'wt') as classifier_file:
    classifier = natural_language_classifier.create_classifier(
        training_data=training_data,
        training_metadata='{"name": "TutorialClassifier","language": "en"}'
    ).get_result()
    json.dump(classifier, classifier_file)
print("Wrote classifier JSON data to classifier.json")
print(json.dumps(classifier, indent=2))

