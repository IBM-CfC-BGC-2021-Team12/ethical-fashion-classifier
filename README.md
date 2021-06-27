# Ethical Fashion Classifier

This repository contains Python scripts that

-  create ethical fashion train/test data sets,
-  train an [IBM Cloud Natural Language Classifier](https://cloud.ibm.com/catalog/services/natural-language-classifier), and
-  test the classifier.

Note that these scripts are written to be as understandable as possible for a beginner programmer.  They do not factor repeated code into reusable functions, they use several intermediate variables to make processes clearer, they do not guard against execution on module import (`if __name__=='__main__'`), or use any unnecessary Python features.  Modifying these scripts to make them more [Pythonic](https://docs.python-guide.org/writing/style/) could be a fun project for an intermediate Pythonista. :)

## Text Classification

Text classification is a supervised learning problem where the input is a text document (e.g., a web page), and the output is some category to which the text document belongs.

For our application, the text documents will be the web pages of fashion brands and the outputs will be `{ETHICAL, UNETHICAL}`.

For additional background written at an introductory level, see [Machine Learning](machine-learning.md)

## Requirements

To use these scripts you need:

- Python 3, which you can install from https://python.org
- the Python requests library
- the NLTK library
- the Beautiful Soup library
- IBM Watson Python SDK

And, of course, you need the API key and service URL for an [IBM Cloud Natural Language Classifier](https://cloud.ibm.com/catalog/services/natural-language-classifier) instance.

### How to install

Install Python 3 using the instructions at https://python.org.  Then open a command-line terminal and execute the following commands:

```
pip3 install requests
pip3 install nltk
pip3 install beautifulsoup4
pip3 install --upgrade "ibm-watson>=5.1.0"
```

## Creating Data Sets

Data sets are built from the web sites of human-classified ethical and unethical fashion brands, as listed on https://goodonyou.eco/most-ethical-and-sustainable-clothing-brands-from-us-and-canada/ and https://theprettyplaneteer.com/fast-fashion-brands-to-avoid/.

The `create_datasets.py` script:

- fetches each web page,
- extracts the text,
- converts letters to lower case,
- removes extra whitespace by tokenizing and then joining the list of tokens with " ",
- removes non-alphanumeric characters using a regular expression substitution, and
- writes the first 1024 characters and the appropriate `ETHICAL` or `UNETHICAL` label to the CSV data set file.

The 1024 character limit is a constraint of IBM Cloud Natural Language Classifier.

> This repository includes data sets generated by `create_datasets.py`.  You normally wouldn't include generated code in a repository, but we include it here in case some students have trouble running the script, and to provide an example of what the data sets look like.

The `create_datasets.py` script takes a few minutes to run, since it's fetching the text of the web pages for every URL in its list of ethical an unethical fashion brands (as of this writing, 74 web pages).  The output will look something like:

```
Training set size: 59, 31 ETHICAL (0.53), 28 UNETHICAL (0.47)
Test set size: 15, 8 ETHICAL (0.53), 7 UNETHICAL (0.47)
Creating train feature text for https://www.tentree.com/.
...
Creating test feature text for https://www.oysho.com/gb/.
```

## Training the Classifier

Once you have a training data set you can use it to train your classifier with:

> Substitute your own API key and classifier service URL for <apikey> and <service-url>.

```
python3 train_classifier.py <apikey> <classifer-url> fashion-brands-train.csv
```

You should get an output something like:

```
Wrote classifer JSON data to classifier.json
{
  "classifier_id": "f1985cx420-nlc-42",
  "name": "TutorialClassifier",
  "language": "en",
  "created": "2021-06-26T19:28:20.390Z",
  "url": "https://api.us-east.natural-language-classifier.watson.cloud.ibm.com/instances/5d3ee9bb-3a90-440f-8196-e0f26cf636a1/v1/classifiers/f1985cx420-nlc-42",
  "status_description": "The classifier instance is in its training phase, not yet ready to accept classify requests",
  "status": "Training"
}
```

Training will take a few minutes (typically < 10).  You can query the status of the classifier (and update the `classifier.json` file produced when training was started) with:

```
python3 update_status.py <apikey>
```

Once you get an output like this, you're ready to query the classifier: (Notice the status changed from 'Training' to 'Available')

```
Previous classifier status:
{'classifier_id': 'f1985cx420-nlc-42',
 'created': '2021-06-26T19:28:20.390Z',
 'language': 'en',
 'name': 'TutorialClassifier',
 'status': 'Training',
 'status_description': 'The classifier instance is in its training phase, not '
                       'yet ready to accept classify requests',
 'url': 'https://api.us-east.natural-language-classifier.watson.cloud.ibm.com/instances/5d3ee9bb-3a90-440f-8196-e0f26cf636a1/v1/classifiers/f1985cx420-nlc-42'}
apikey='tXOiM7j6bFi94FrZkOB4MUZ9OiBsRaidRpbTQ5CeLc0P'
classifier_url='https://api.us-east.natural-language-classifier.watson.cloud.ibm.com/instances/5d3ee9bb-3a90-440f-8196-e0f26cf636a1'
classifier_id='f1985cx420-nlc-42'

Updated classifer status:
{
  "classifier_id": "f1985cx420-nlc-42",
  "name": "TutorialClassifier",
  "language": "en",
  "created": "2021-06-26T19:28:20.390Z",
  "url": "https://api.us-east.natural-language-classifier.watson.cloud.ibm.com/instances/5d3ee9bb-3a90-440f-8196-e0f26cf636a1/v1/classifiers/f1985cx420-nlc-42",
  "status_description": "The classifier instance is now available and is ready to take classifier requests.",
  "status": "Available"
}
```

## Testing the Classifier

Once you've trained the classifier and it's available, you can test its performance using the test set created by above by running `test_classifier.py`:

```
python3 test_classifier.py <apikey> fashion-brands-test.csv
```

Once it finishes querying the classifier for each case in your test set, it should print a report like:

```
Error rate on fashion-brands-test.csv: 0.2 (3/15).
```

The error rate shown above is the test error on `fashion-brands-test.csv` for a classifier trained with `fashion-brands-train.csv`.  Yes, with minimal preprocessing the classifier achieves an 80% accuracy rate!

## Querying the Classifier With an Unseen Fashion Brand

The whole point of this training and testing is to create a system that allows a fashion shopper to get an assessment of the ethical status of an arbitrary fashion brand.  The training phase produces the predictive model, the testing phase gives us some confidence in the model, the next step is to *use* the model.

**This is your task!**  By reading the IBM Cloud Natural Language Classifier documentation at https://cloud.ibm.com/docs/natural-language-classifier?topic=natural-language-classifier-natural-language-classifier#getting-started-classify and studying the code in the scripts in this repository (especially `test_classifier.py`) you should be able to write a script that queries the classifier for a prediction of the ethical status of a fashion brand that it was neither trained nor tested on.

## Word Clouds

Just for fun, we also created a script, `extract_words.py`, which extracted words appearing on web sites of ethical and unethical brands, saved in `ethical-words.txt` and `unethical-words.txt`.  To get a feel for the most frequently occurring words in each category, create [word clouds](https://en.wikipedia.org/wiki/Tag_cloud) for each of these word lists.  There are online word cloud generators, but it's fairly simple to create one with Python code using a library such as this one: https://github.com/amueller/word_cloud.  Note that if you use that particular library, you'll need the following dependencies:

```
pip3 install numpy
pip3 install pillow
pip3 install matplotlib
```
#Description of the fashionably late
  
  Fast fashion is a phenomenon that has taken consumerism by storm these past few years and its effects on the Earth have been catastrophic. Even though some consumers may be aware of the effects of their cheap consumerism, they do not have the resources to make better decisions that will benefit them. Our intended users are consumers that are young, targeted by fast fashion, care about the environment, and can’t afford good quality clothes for their price range.
  
  Our solution was to develop an app that provides information about fast fashion, what consumers can do to stop contributing to it, and alternatives to fast fashion. Our main feature is a scanner that utilizes an IBM Natural Language Classifier to allow consumers to know if the brands they are buying from are ethical or unethical.
  
  We decided to go with the IBM Natural Language Classifier because we wanted a feature where consumers would be able to scan the tag of clothes and be able to easily access the needed information. Once the scanner recognizes the brand name, the app will find the brand's web site, extract text from the brand's home page, and send that text to the IBM Cloud Natural Language classifier, which returns a prediction of the ethical status of the brand based on the text.
