import argparse
import csv
import itertools
import sys


# Parse arguments

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--numeric",
                    action="store_true", default=False)  # args.numeric -n for numeric , optional
parser.add_argument("-p", "--percentage", action="store_true", default=False)  # args.percentage , optional
parser.add_argument("-o", "--output", type=str)  # args.output, optional

parser.add_argument("support", type=int)   # args.support , mandatory
parser.add_argument("filename")  # args.filename , mandatory

args = parser.parse_args()


# Read from csv

all_baskets = []
input_file = open(args.filename, 'r')
csv_reader = csv.reader(input_file, delimiter=',')

for row in csv_reader:
    stripped_items = [field.strip().lower() for field in row]
    all_baskets.append(stripped_items)
input_file.close()


# Returns unique basket items

def get_unique_items(basket):
    unique_basket = set(basket)

    return list(unique_basket)

# Checks if args.support should be a percentage

if args.percentage:
    temp = args.support
    count = 0
    for basket in all_baskets:
        for item in basket:
            count += 1

    args.support = int(temp*count/100)

# First pass

def first_pass(F, S):
    counts = {}
    freqk = {}

    for basket in F:
        items = get_unique_items(basket)
        for item in items:
            try:
                counts[item] += 1
            except:  # if the key isn't found counts[key] is initialised to 1
                if item not in counts.keys():
                    counts[item] = 1

    for item in counts:
        if counts[item] >= S:
            freqk[item] = counts[item]

    return freqk


# Next passes

def next_passes(F, freqk, k, S ):

    counts = {}
    freq = {}

    pairs = list(itertools.combinations(freqk.keys(), 2))  # unique pairs

    for basket in F:
        items = get_unique_items(basket)  # unique items of each basket
        candidates = []
        for pair in pairs:

            if args.numeric:
                candidate = tuple(set(pair[0]) | set(pair[1]) - set(pair[0]) & set(pair[1]))
            else:
                if isinstance(pair[0], tuple):
                    candidate = tuple(set(pair[0]) | set(pair[1]) - set(pair[0]) & set(pair[1]))
                else:
                    candidate = tuple(pair)

            if candidate not in candidates:
                candidates.append(candidate)

                if len(candidate) == k + 1 and set(candidate).issubset(set(items)):
                    try:
                        counts[candidate] += 1
                    except:     # if the key isn't found counts[key] is initialised to 1
                        if candidate not in counts.keys():
                            counts[candidate] = 1


    for itemset in counts:
        if counts[itemset] >= S:
            freq[itemset] = counts[itemset]
    return freq

# Main algorithm


def a_priori(F, S):
    all_freq = {}
    k = 1
    freqk = first_pass(F, S)

    while freqk:

        all_freq.update(freqk)
        freq = next_passes(F, freqk, k, S)
        freqk = freq
        k += 1


    return all_freq



results = a_priori(all_baskets, args.support) # invoke main

# Creating optional output form

for key in results:
     if not isinstance(key, tuple):
         results[(key,)] = results.pop(key)


key_lengths = []
for key in results:
    key_lengths.append(len(key))


new_rez = []
for length in list(set(key_lengths)):
    lil_dict = {}
    for key in results:
        if len(key) == length:
            lil_dict[key] = results[key]
    new_rez.append(lil_dict)

# Either prints or writes the output in a csv file

if args.output is not None:
    output_file = open(args.output, 'w')
    csv_writer = csv.writer(output_file, delimiter=';')

    for freqs in new_rez:
        row = []
        for key in sorted(freqs.keys()):
            row.append("{0}:{1}".format(key, freqs[key]))
        csv_writer.writerow(row)

    output_file.close()


if args.output is None:

    csv_writer = csv.writer(sys.stdout, delimiter=';')

    for freqs in new_rez:
        row = []
        for key in sorted(freqs.keys()):
            row.append("{0}:{1}".format(key, freqs[key]))
        csv_writer.writerow(row)


