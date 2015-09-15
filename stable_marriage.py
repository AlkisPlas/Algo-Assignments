import sys
import json
from collections import OrderedDict

command1 = sys.argv[1]
input_filename = sys.argv[2]

# Loading preferences from input file
new_file = open(input_filename, "r")
preferences = json.load(new_file)
men_pref = preferences["men_rankings"]
women_pref = preferences["women_rankings"]
new_file.close()

# Setting up preferences for choosers and receivers
if command1 == "-m":
    chooser_pref = men_pref
    receiver_pref = women_pref
elif command1 == "-w":
    chooser_pref = women_pref
    receiver_pref = men_pref

# Initialising choosers to free
free_choosers = []
for chooser in chooser_pref:
    free_choosers.append(chooser)

# Dictionary to hold the couples
engaged = {}
for chooser in chooser_pref:
    engaged[chooser] = None

# Checks if the receiver prefers another chooser
def break_up(current_chooser, current_receiver):
    for old_chooser in engaged:
        if engaged[old_chooser] == current_receiver: # if another pair of (old_chooser, current_receiver) exists
            if receiver_pref[current_receiver].index(current_chooser) < receiver_pref[current_receiver].index(old_chooser):
                engaged[old_chooser] = None  # chooser key breaks up with receiver
                engaged[current_chooser] = current_receiver
                free_choosers.append(old_chooser)  # old_chooser is free again
            else:
                free_choosers.append(current_chooser)
            break


# Main algorithm Execution
while free_choosers:
    chooser = free_choosers.pop()
    if len(chooser_pref[chooser]) != 0:
        receiver = chooser_pref[chooser].pop(0)  # receiver is now the highest preference who hasn't been proposed to
        if receiver not in engaged.values():
            engaged[chooser] = receiver  # chooser and receiver are now engaged
        else:
            break_up(chooser, receiver)

engaged = dict([(str(k), str(v)) for k, v in engaged.items()])  # gets rid of unicode encoding
sorted_engaged = OrderedDict(sorted(engaged.items(), key=lambda t: t[0]))  # sorts the engaged dict by key

if len(sys.argv) == 3:
    print(json.dumps(sorted_engaged, indent=3))
else:
    command2 = sys.argv[3]
    output_filename = sys.argv[4]
    a_file = open(output_filename+".json", "w+")
    json.dump(sorted_engaged, a_file)
    a_file.close()
