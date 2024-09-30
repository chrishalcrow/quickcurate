from .quickcurate import curate
import argparse
from pathlib import Path

def print_logo():
    print("\t  _   _  ")
    print("\t (q)_(p) ")
    print("\t \ . . /    Quick")
    print("\t =\ t /=      Curate")
    print("\t   \_/\n")

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "report_folder", 
        type=str, 
        help="The path to your spikeinterface generated report"
    )

    parser.add_argument(
        "--output_file",
        type=str,
        help="Where to save the curated labels. By default, these are saved in the report folder as 'curated_labels.json'"
    )

    parser.add_argument(
        "--labels",
        type=str,
        help="List of labels used for curation. Should be in the form e.g. '[sua, mua, noise]'"
    )

    print_logo()

    args = parser.parse_args()

    if args.output_file is None:
        args.output_file = Path(args.report_folder) / Path("curated_labels.json")

    assert (Path(args.report_folder) / Path('units')).is_dir(), f"Cannot find 'units' folder in {args.report_folder}"
    
    if args.labels is None:
        labels = ["sua", "mua", "bad"]

        print("The current labels are ", end='')
        for label in labels:
            print(f"{label}, ", end='')
        accept_default_labels = input("\nDo you accept these (y/n)? ")

        rules_broken = False
        while rules_broken or (accept_default_labels == "n"):
            accept_default_labels = "y"
            print("\nPlease enter your custom labels.")
            print("\nRULES:\n\t1. Each label must be a single word.\n\t2. Each word must start with a different letter.\n\t3. None of these letters can be u.\n\t4. Please enter them with a single space between each. E.g. 'good bad noise'")
            user_label_input = input("\nWhat are your labels? ")
            labels = user_label_input.split(' ')

            user_label_letter_list = [ label[0] for label in labels ]
            if len(set(user_label_letter_list)) != len(user_label_letter_list):
                rules_broken = True
                print("\nYou've broken RULE #2: each label must start with a different letter!!!!!!!!")
            elif 'u' in  user_label_letter_list:
                rules_broken = True
                print("\nYou've broken RULE #3: no label may start with u (this is resered for undoing)!!!!!!!!")
            else:
                rules_broken = False
    else:
        labels = args.labels

    print()
    curate(labels, args.report_folder, args.output_file)
