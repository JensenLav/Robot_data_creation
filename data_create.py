#%%
import random
import json
#%%
colors = ["red block", "green block", "blue block", "yellow block"]
block_num = [1,2,3,4,5,6,7,8]
str_table = "table"
str_on = "on"
#%%
"""
these functions create a goal state and current state
"""
def rand_goal(block_array):
    seed = random.randint(1, 1000000)
    random.seed(seed)
    rand_final = []
    obj_num_goal = random.randint(2, len(block_array))
    randomized_colors = random.sample(block_array, obj_num_goal)
    for i in range(len(randomized_colors) - 1):
        rand_final.append((randomized_colors[i], str_on, randomized_colors[i + 1]))
    rand_final.append((randomized_colors[-1], str_on ,str_table))
    rand_final.reverse()
    return obj_num_goal, seed, rand_final, randomized_colors



def rand_state(block_array, obj_num_goal):
    rand_state_arr = []
    percent_on_blocks = random.randint(1, obj_num_goal)
    for i in range(len(block_array)):
        if i < percent_on_blocks:
            rand_state_arr.append((block_array[i], str_on, str_table))
        else:
            rand_state_arr.append((block_array[i], str_on, block_array[i-1]))
    return rand_state_arr
#%%
"""
This code block combines goal state and current state then writes it to data_collection file as a json
"""
def read_data(file_name):
    with open(file_name, "r") as f1:
        data = f1.read()
        entries = data.split('data_')
        count = len(entries[1:])
    return count

def collect_data(num):
     f2 = open("data_collection", "a")
     count = 0
     offset = read_data(f"data_collection")
     while count < num:
        rand_goal_list = rand_goal(colors)
        rand_state_list = rand_state(rand_goal_list[3], rand_goal_list[0])
        combined_json = {
            "Goal_State": rand_goal_list[2],
            "Current_State": rand_state_list,
            "Pick": None,
            "Place": None
        }

        final_json = json.dumps(combined_json, indent=3)
        f2.write(f"data_{count + 1 + offset}:\n")
        f2.write(final_json)
        f2.write("\n")
        count+=1
     f2.close()
collect_data(1)
#%%
"""
when called prompts a user to fill in pick and place
"""

def update_pick_and_place(file_name):
    with open(file_name, "r") as f:
        data = f.read()
        entries = data.split('data_')
    with open(file_name, "w") as f:
        for entry in entries[1:]:
            lines = entry.split('\n')
            if len(lines) > 1:
                json_data = json.loads('\n'.join(lines[1:]))
                if json_data["Pick"] is None or json_data["Place"] is None:
                    try:
                        pick = input(f"Enter 'Pick' value for data_{entries.index(entry)}\n goal state: \n {json_data['Goal_State']} \n current state:\n {json_data['Current_State']} ")
                        place = input(f"Enter 'Place' value for data_{entries.index(entry)}\n goal state: \n {json_data['Goal_State']} \n current state:\n {json_data['Current_State']} ")
                        json_data["Pick"] = pick
                        json_data["Place"] = place
                    except KeyboardInterrupt:
                        print(f"Keyboard Interrupt, No changes made to data_{entries.index(entry)}")
                        final_json = json.dumps(json_data, indent=3)
                        f.write(f"data_{entries.index(entry)}:\n")
                        f.write(final_json)
                        f.write("\n")
                        break

                    final_json = json.dumps(json_data, indent=3)
                    f.write(f"data_{entries.index(entry)}:\n")
                    f.write(final_json)
                    f.write("\n")
                else:
                    final_json = json.dumps(json_data, indent=3)
                    f.write(f"data_{entries.index(entry)}:\n")
                    f.write(final_json)
                    f.write("\n")

update_pick_and_place("data_collection")
#%%
"""
this function prompts a user for a number to lookup/ modify data
"""
def modify_entry(file_name, entry_num, new_pick, new_place):
    with open(file_name, "r") as f:
        data = f.read()
        entries = data.split('data_')
    with open(file_name, "w") as f:
        for idx, entry in enumerate(entries[1:], start=1):
            lines = entry.split('\n')
            if len(lines) > 1:
                json_data = json.loads('\n'.join(lines[1:]))
                if idx == entry_num:
                    json_data["Pick"] = new_pick
                    json_data["Place"] = new_place

                final_json = json.dumps(json_data, indent=3)
                f.write(f"data_{idx}:\n")
                f.write(final_json)
                f.write("\n")

# Example usage:
#modify_entry("data_collection", 3, "red block", "blue block")

def prompt_modify(file_name):
    with open(file_name, "r") as f:
        data = f.read()
        entries = data.split('data_')
        try:
            num = int(input(f"what entry do you want to look at? valid range(1-{len(entries) - 1}"))
            if num < 1 or num > len(entries) - 1:
                print("Invalid entry number")
            else:
                lines = entries[num].split('\n')
                if len(lines) > 1:
                    json_data = json.loads('\n'.join(lines[1:]))
                new_pick = input(f"Enter new pick value:  \n {json_data['Current_State']}\n {json_data['Goal_State']} \n {json_data['Pick']} \n {json_data['Place']}")
                new_place = input(f"Enter new place value:  \n {json_data['Current_State']}\n {json_data['Goal_State']} \n {json_data['Pick']} \n {json_data['Place']}")
                modify_entry(file_name, int(num), new_pick, new_place)
        except KeyboardInterrupt:
            print("Keyboard Interrupt, No changes made")
prompt_modify("data_collection")
#%%
"""
deletes everything in data_collection
"""
with open("data_collection", "w") as f:
    pass