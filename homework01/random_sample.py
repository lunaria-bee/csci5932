#!/usr/bin/env python3


import random, sys


def main (argc, argv):

    if argc != 4:
        print(f"Error: Invalid number of arguments ({argc-1}).", file=sys.stderr)
        exit(-1)

    path = argv[1]
    stratum_count = int(argv[2])
    samples_per_stratum = int(argv[3])

    # Collect data
    with open(argv[1]) as f:

        dict_keys = []
        word_data = []
        for line_number, line in enumerate(f.readlines()):

            # Collect field names from line 8
            if line_number == 8:
                dict_keys = line.split('\t')

            # Construct dictionary of word data
            elif line_number > 8:
                word_data.append(dict(zip(dict_keys, line.split('\t'))))

    # Choose samples
    sample = []
    stratum_size = len(word_data) // stratum_count
    stratum_lower_bound, stratum_upper_bound = 0, stratum_size
    for i in range(stratum_count):

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

    for word, result in results:
        print(f"{word}\t{result}")
    print(f"{score}/{stratum_count*samples_per_stratum} ({score/(stratum_count*samples_per_stratum):.4f})")


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
