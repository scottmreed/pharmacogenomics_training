import json
import csv

def countX(lst, x, y, z):
    count_x = 0
    count_y = 0
    count_z = 0

    for ele in lst:
        if (ele == x):
            count_x += 1
        elif (ele == y):
            count_y += 1
        elif (ele == z):
            count_z += 1
        else:
            print(ele)
    return count_x, count_y, count_z

all_classes = []

with open("mutation_data_all_dict.json") as f:
    data = json.load(f)
    print(len(data))
    with open("./AlphaMissense_aa_substitutions.tsv", "r") as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')

        for item in rd:
            if item[0] in data.keys():
                if item[1] in data[item[0]]:
                    print(item)
                    c = item[3]
                    c_clean = c.replace("'", "")
                    all_classes.append(c_clean)
            # else:
            #     print('nope', item)

num_benign, num_pathogenic, num_ambiguous = countX(all_classes, "benign", "pathogenic", "ambiguous")

percent_benign = (num_benign / len(all_classes))*100
percent_pathogenic = (num_pathogenic / len(all_classes))*100
percent_ambiguous = (num_ambiguous / len(all_classes))*100

print(f"benign = {percent_benign}"
      f"pathogenic = {percent_pathogenic}"
      f"ambiguous = {percent_ambiguous}")

with open("AM_results_all.txt", 'w') as p:
    p.write(f"benign = {percent_benign}\n pathogenic = {percent_pathogenic}\n ambiguous={percent_ambiguous}"
            )