# Ethical Fashion Classifier

This repository contains Python scripts that

-  create ethical fashion train/test data sets,
-  train an IBM Cloud Natural Language Classifier, and
-  test the classifier.

## Requirements

To use these scripts you need

- Python 3, which you can install from python.org,
- the Python requests library,
- the NLTK library, and
- the Beautiful Soup library.

### How to install

Install Python 3 using the instructions at python.org.  Then open a command-line terminal and execute the following commands:

```
pip3 install requests
pip3 install nltk
pip3 install beautifulsoup4
```

## Creating Data Sets

The `create_datasets.py` script fetches the web sites of human-classified ethical and unethical fashion brands, as listed on https://goodonyou.eco/most-ethical-and-sustainable-clothing-brands-from-us-and-canada/ and https://theprettyplaneteer.com/fast-fashion-brands-to-avoid/.

The `create_datasets.py` script:

- fetches each web page,
- extracts the text,
- converts letters to lower case,
- removes extra whitespace by tokenizing and then joining the list of tokes with " ",
- removes non-alphanumeric characters using a regular expression substitution, and
- writes the first 1024 characters and the appropriate `ETHICAL` or `UNETHICAL` label to the CSV data set file.

The 1024 character limit is a requirement of IBM Cloud Natural Language Classifier.
