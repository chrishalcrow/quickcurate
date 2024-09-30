import matplotlib
import matplotlib.pyplot as plt

from PIL import Image
import os
import matplotlib.pyplot as plt
import numpy as np
import json
from pathlib import Path

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

def crop_img(img):

    crop_left = 0
    while np.all(img[:,crop_left] == [255,255,255,255]) == True:
        crop_left += 1

    crop_top = 0
    while np.all(img[crop_top,:] == [255,255,255,255]) == True:
        crop_top += 1

    crop_right = np.shape(img)[1] - 1
    while np.all(img[:,crop_right] == [255,255,255,255]) == True:
        crop_right -= 1

    crop_bottom = np.shape(img)[0] - 1
    while np.all(img[crop_bottom,:] == [255,255,255,255]) == True:
        crop_bottom -= 1

    return img[crop_top:crop_bottom,crop_left:crop_right,:]

def curate(labels=None, report_folder=None, output_file=None):
    """
    Launch a diaglog allowing the user to curate units based on the images
    in a `spikeinterface` report folder.

    Parameters
    ----------
    labels : list of str, default: None
        List of labels used for curation.
    report_folder : str or Path, default: None
        Path to a `spikeinterface` report folder.
    output_file, str or Path, default: None
        File to output the results in. If None, no file is saved.
    
    Returns
    -------
    curation_dict: dict
        Dictionary of labels for each unit curated.
    """

    assert labels is not None, "Please supply `labels` e.g. curate(labels = ['good', 'bad'])"

    label_dict = make_label_dict(labels)

    using_jupyter = False
    if matplotlib.get_backend() == "macosx":
        matplotlib.use('module://matplotlib-backend-kitty')
    elif matplotlib.get_backend() == "module://matplotlib_inline.backend_inline":
        using_jupyter = True
        from IPython.display import clear_output

    if output_file is not None:
        keep_file = "n"
        while os.path.isfile(output_file) and keep_file != "y":
            keep_file = input(f"The file '{output_file}' already exists. Doing this curation will OVERWRITE the file.\nDo you want to conintue (y/n)? ")
            if keep_file == "n":
                print("\nYou can specify the output_file path when you run quickcurate as follows:\n\tquickcurate 'report_folder' --output_file 'my_output_file.json'\n")
                return
            print("")

    units_folder = Path(report_folder) / Path('units')

    file_names = os.listdir(units_folder)
    unit_list = [ int(file_name.split('.')[0]) for file_name in file_names ]
    unit_list = sorted(unit_list)
    sorted_file_names = [ str(unit) + '.png' for unit in unit_list ]

    curation_dict = {}
    a = 0
    while a < len(sorted_file_names):
        
        file_name = sorted_file_names[a] 
        unit_id = file_name.split('.')[0]

        exit_time = False
        undo_time = False

        print()
        
        img = crop_img(np.asarray(Image.open(units_folder / file_name)))
        imgplot = plt.imshow(img)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

        unit_label = False
        while unit_label not in label_dict:
            if unit_label is False:
                True
            elif unit_label.lower() == 'u':
                undo_time = True
                print("Going back one unit...")
                a = max(a-1,0)
                if using_jupyter:
                    clear_output(wait=True)
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
        
        if using_jupyter:
            clear_output(wait=True)

        print(f"You lablled unit {unit_id} as {unit_label + label_dict[unit_label]}.")
        
        curation_dict[unit_id] = unit_label + label_dict[unit_label]

        if output_file is not None:
            with open(output_file, 'w') as json_file:
                json.dump(curation_dict, json_file)

        a += 1

    print(f"\nPhew - tiring work! You labelled {a} units.")
    if output_file is not None:
        print(f"The curated unit dict can be found at {output_file}.")

    return curation_dict