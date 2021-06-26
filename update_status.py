import json, sys
from ibm_watson import NaturalLanguageClassifierV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pprint import pprint

if len(sys.argv) < 2:
    print("Usage:")
    print("python3 update_status.py <api key>")
    sys.exit(0)

apikey = sys.argv[1]

with open("classifier.json", "rt") as classifier_file:
    classifier = json.load(classifier_file)

print("Previous classifier status:")
pprint(classifier)

# The classifier_url is NOT the full classifier_url listed in the classifier
# JSON description.  It is only the part before "/v1/...".  Learning experience:
# bad API design!
classifier_url = classifier['url'].split("/v1/")[0]
classifier_id = classifier['classifier_id']

print(f"{apikey=}")
print(f"{classifier_url=}")
print(f"{classifier_id=}")

authenticator = IAMAuthenticator(apikey)
natural_language_classifier = NaturalLanguageClassifierV1(
    authenticator=authenticator
)

natural_language_classifier.set_service_url(classifier_url)

status = natural_language_classifier.get_classifier(classifier_id).get_result()
print("\nUpdated classifer status:")
print(json.dumps(status, indent=2))
with open("classifier.json", "wt") as classifier_file:
    json.dump(status, classifier_file)
