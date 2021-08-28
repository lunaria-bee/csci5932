#!/usr/bin/env python3

'''Determine familiarity with a random sample of words

Usage: random_sample.py WORDLIST NUMBER_OF_STRATA SAMPLES_PER_STRATA

WORDLIST: Path to file containing the words to test. First line of the file should be a
list of tab-separated column names, with each subsequent line being an entry in the word
list with tab-separated columns. One column must be named "lemma," and should contain the
word to test.

NUMBER_OF_STRATA: How many strata to divide the word list into when selecting the sample.

SAMPLES_PER_STRATA: How many words from each stratum to select for the sample.

'''


import random, sys


def main (argc, argv):

    if argc != 4:
        print(f"Error: Invalid number of arguments ({argc-1}).", file=sys.stderr)
        exit(-1)

    path = argv[1]
    number_of_strata = int(argv[2])
    samples_per_stratum = int(argv[3])

    # Read word list + metadata
    with open(argv[1]) as f:

        dict_keys = []
        word_data = []
        for line_number, line in enumerate(f.readlines()):

            # Collect field names
            if line_number == 0:
                dict_keys = line.split('\t')

            # Construct dictionary of word data
            elif line_number > 0:
                word_data.append(dict(zip(dict_keys, line.split('\t'))))

    # Select stratified sample
    sample = []
    stratum_size = len(word_data) // number_of_strata
    stratum_lower_bound, stratum_upper_bound = 0, stratum_size
    for i in range(number_of_strata):

        # Choose random word from current stratum
        sample.extend(
            random.sample(
                word_data[stratum_lower_bound:stratum_upper_bound],
                samples_per_stratum))

        # Reassign bounds
        stratum_lower_bound = stratum_upper_bound
        if i == 98:
            # Before the last iteration, expand the stratum to fill the entire remaining
            # word list, to correct for truncating stratum_size.
            stratum_upper_bound = len(word_data)
        else:
            stratum_upper_bound += stratum_size


    # Determine familiarity
    score = 0
    results = []
    for word in sample:

        valid_input = False
        while not valid_input:

            print(f"Do you know the word '{word['lemma']}'?")
            choice = input("(1: yes, 0: no)> ")

            valid_input = True
            if choice == '0':
                results.append((word['lemma'], 0))
            elif choice == '1':
                score += 1
                results.append((word['lemma'], 1))
            else:
                print("Error: Invalid input. Must be '1', '2', or '3'.")
                valid_input = False

        print()

    # Print results
    for word, result in results:
        print(f"{word}\t{result}")
    print(f"{score}/{number_of_strata*samples_per_stratum}",
          f"({score/(number_of_strata*samples_per_stratum):.4f})")


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
