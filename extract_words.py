import csv

inputs = ["fashion-brands-train.csv", "fashion-brands-test.csv"]

ethical_words = []
unethical_words = []
for input in inputs:
    with open(input) as fin:
        reader = csv.reader(fin)
        for row in reader:
            if row[1] == "ETHICAL":
                ethical_words += row[0].split()
            else:
                unethical_words += row[0].split()

with open("ethical-words.txt", "wt") as ethical_out, \
     open("unethical-words.txt", "wt") as unethical_out:
    ethical_out.write(" ".join(ethical_words))
    unethical_out.write(" ".join(unethical_words))

