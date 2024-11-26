#%%
import random
import json

#%%
colors = ["red block", "green block", "blue block", "yellow block"]
block_num = [1,2,3,4,5,6,7,8]
str_table = "table"
str_on = "on"
#%%
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
 def collect_data(num):
     f = open("data_collection", "w")
     count = 0
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
        f.write(f"data_{count + 1}:\n")
        f.write(final_json)
        f.write("\n")
        count+=1
     f.close()
collect_data(1)