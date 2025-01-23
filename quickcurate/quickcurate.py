import matplotlib.pyplot as plt
import json

from IPython.display import clear_output

from spikeinterface.widgets import UnitSummaryWidget
from spikeinterface import load_sorting_analyzer

def print_logo():
    print("\t  _   _  ")
    print("\t (q)_(p) ")
    print("\t \ . . /    Quick")
    print("\t =\ t /=      Curate")
    print("\t   \_/\n")

def make_label_dict(label_list):
    label_dict = {}
    for label in label_list:
        label_dict[ label[0] ] = label[1:]
    return label_dict

def question_text(label_dict):
    txt = "(Exit)? (U)ndo previous label? Or is this unit: "
   
    first = True
    for first_letter, rest_of_label in label_dict.items():
        if first is True:
            txt += f"({first_letter}){rest_of_label}"
            first = False
        else:
            txt += f", ({first_letter}){rest_of_label}"
    txt += "? "
    return txt

def are_label_rules_broken(labels):

    user_label_letter_list = [ label[0] for label in labels ]

    if len(set(user_label_letter_list)) != len(user_label_letter_list):
        rules_broken = True
        print("\nYou've broken RULE #1: each label must start with a different letter!!!!!!!!")
    elif 'u' in  user_label_letter_list:
        rules_broken = True
        print("\nYou've broken RULE #2: no label may start with u (this is resered for undoing)!!!!!!!!")
    else:
        rules_broken = False

    return rules_broken

def curate(
        labels=None, 
        sorting_analyzer=None, 
        output_file=None, 
        figsize=None
    ):
    """
    Launch a diaglog allowing the user to curate units based a `spikeinterface` 
    Sorting Analyzer.

    Parameters
    ----------
    labels : list of str, default: None
        List of labels used for curation.
    sorting_analyzer : SortingAnalyzer, default: None
        A `spikeinterface` SortingAnalyzer, to curate.
    output_file : str, default: None
        File to output the results in. If None, no file is saved.
    figsize : tuple, default: None
        Size of figure, e.g., (10,5) passed to matplotlib.
    
    Returns
    -------
    curation_dict: dict
        Dictionary of labels for each unit curated.
    """

    assert labels is not None, "Please supply `labels` e.g. curate(labels = ['good', 'bad'])"
    assert are_label_rules_broken(labels) is False, "Your labels have broken the rules.\n\nRULES:\n\t1. Each word must start with a different letter.\n\t2. None of these letters can be u."

    assert sorting_analyzer is not None, "Please supply a `sorting_analyzer` e.g. curate(sorting_analyzer = my_sa)"

    print_logo()
    label_dict = make_label_dict(labels)

    curation_dict = {}
    a=0

    print("Making first plot (takes extra time as caching is taking place...)")
    while a < len(sorting_analyzer.unit_ids):
        
        unit_id = sorting_analyzer.unit_ids[a]

        exit_time = False
        undo_time = False

        fig = plt.figure(figsize=figsize)
        UnitSummaryWidget(
            sorting_analyzer, 
            unit_id=unit_id, 
            figure=fig,
            subwidget_kwargs = {
                'unit_locations': {'plot_all_units': False},
                }
        )
        clear_output(wait=True)
        plt.show()

        unit_label = False
        while unit_label not in label_dict:
            if unit_label is not False:
                if unit_label.lower() == 'u':
                    undo_time = True
                    print("Going back one unit...")
                    a = max(a-1,0)
                    break
                elif unit_label == "exit":
                    exit_time = True
                    break
                elif unit_label not in label_dict:
                    print(f"{unit_label} is not an accepted label name.")

            unit_label = input(question_text(label_dict))

        if exit_time is True:
            break
        if undo_time is True:
            continue
        
        curation_dict[unit_id] = unit_label + label_dict[unit_label]
        print(f"You lablled unit {unit_id} as {unit_label + label_dict[unit_label]}.")
        a += 1

        if output_file is not None:
            with open(output_file, 'w') as json_file:
                json.dump(curation_dict, json_file)

    clear_output(wait=True)
    print(f"\nPhew - tiring work! You labelled {a} units.")
    if output_file is not None:
        print(f"The curated unit dict can be found at {output_file}.")

    return curation_dict