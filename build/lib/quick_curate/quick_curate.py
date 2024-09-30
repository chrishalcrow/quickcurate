import matplotlib
matplotlib.use('module://matplotlib-backend-kitty')
import matplotlib.pyplot as plt

from PIL import Image
import os
import matplotlib.pyplot as plt
import numpy as np
import json
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

def make_label_dict(label_list):
    label_dict = {}
    for label in label_list:
        label_dict[ label[0] ] = label[1:]
    return label_dict

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

def run_curation(label_list, report_path, output_file):

    print("\n")
    print("    ()-().----. Quick     .")
    print(""" jsg \\"/` ___  ;_________.'""")
    print("      ` ^^   ^^    Curator ")
    print("\n")

    keep_file = "n"
    while os.path.isfile(output_file) and keep_file != "y":
        keep_file = input(f"The file '{output_file}' already exists. Doing this curation will OVERWRITE the file.\nDo you want to conintue (y/n)? ")
        if keep_file == "n":
            output_file = input("Please input your new output filename, which should end in '.json'. This is a json file containing the curated labels: ")
    print("")

    label_dict = make_label_dict(label_list)

    print("The current labels are ", end='')
    for first_letter, rest_of_label in label_dict.items():
        print(f"({first_letter}){rest_of_label}, ", end='')
    accept_default_labels = input("\nDo you accept these (y/n)? ")

    rules_broken = False
    while rules_broken or (accept_default_labels == "n"):
        accept_default_labels = "y"
        print("\nPlease enter your custom labels.")
        print("\nRULES:\n\t1. Each label must be a single word.\n\t2. Each word must start with a different letter.\n\t3. None of these letters can be u.\n\t4. Please enter them with a single space between each. E.g. 'good bad noise'")
        user_label_input = input("\nWhat are your labels? ")
        user_label_list = user_label_input.split(' ')

        user_label_letter_list = [ label[0] for label in user_label_list ]
        if len(set(user_label_letter_list)) != len(user_label_letter_list):
            rules_broken = True
            print("\nYou've broken RULE #2: each label must start with a different letter!!!!!!!!")
        elif 'u' in  user_label_letter_list:
            rules_broken = True
            print("\nYou've broken RULE #3: no label may start with u (this is resered for undoing)!!!!!!!!")
        else:
            rules_broken = False

        label_dict = make_label_dict(user_label_list)

    file_names = os.listdir(report_path)
    unit_list = [ int(file_name.split('.')[0]) for file_name in file_names ]
    unit_list = sorted(unit_list)
    sorted_file_names = [ str(unit) + '.png' for unit in unit_list ]

    curation_dict = {}
    a = 0
    while a < len(sorted_file_names):
        print()
        file_name = sorted_file_names[a] 
        img = crop_img(np.asarray(Image.open(report_path + file_name)))
        imgplot = plt.imshow(img)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

        unit_id = file_name.split('.')[0]
        unit_label = input(question_text(label_dict))

        if unit_label.lower() == 'u':
            print("Going back one unit...")
            a = max(a-1,0)
        elif unit_label == "exit":
            break
        else:
            while unit_label not in label_dict: 
                print(f"{unit_label} is not an accepted label name.")
                unit_label = input(question_text(label_dict))

            print(f"You've lablled unit {unit_id} as {unit_label + label_dict[unit_label]}.")

            curation_dict[unit_id] = unit_label + label_dict[unit_label]

            with open(output_file, 'w') as json_file:
                json.dump(curation_dict, json_file)

            a += 1

    print(f"Phew - tiring work! You labelled {a} units.")
