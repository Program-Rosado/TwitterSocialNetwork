import json
import time
import networkx as nx
import numpy as np
from collections import defaultdict
from scipy.sparse import csr_matrix

counter = 0 
influence_scores = defaultdict(int)

start_time = time.time()
################################################################################################
##############################  Store User and Language Data     ###############################
################################################################################################

language_data_file = '/home/lambda3/socialNetwork/tweeter_language_data.json'

language_list = {} 
with open(language_data_file, 'r') as json_file:
    for line in json_file:
        if line.strip():
            try:
                data = json.loads(line)
                user = data.get('original_user')
                language = data.get('language')
                language_list[user] = language
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
end_time = time.time()
total_time = end_time - start_time
len(language_list)
print("Time Taken for Language Data: " + str(total_time) + " seconds")
################################################################################################
############  Get Top 20 Influential Users (based on tweets and retweets)     ##################
################################################################################################
start_time = time.time()

with open('/home/lambda3/socialNetwork/tweet_retweet_data.json', 'r') as json_file:
    for line in json_file:
        if line.strip():
            try:
                row = json.loads(line)
                original_user = row['original_user']
                retweeters = row['retweeters']
                
                # Increase influence score for the original user
                influence_scores[original_user] += 1
                
                # Increase influence scores for retweeters
                for retweeter in retweeters:
                    influence_scores[retweeter] += 1
                counter += 1
                print(counter)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

# Sort the dictionary by influence scores and get the top 20 influential users
top_influential_users = sorted(influence_scores.items(), key=lambda x: x[1], reverse=True)[:100]

# Print the top 20 influential users
for user, score in top_influential_users:
    print(f"User: {user}, Influence Score: {score}")

end_time = time.time()
total_time = end_time - start_time

print("Time Taken: " + str(total_time) + " seconds")

# TOP 20 INFLUENTIAL USERS
# User: zaynmalik, Influence Score: 36742
# User: Ksa_Ad_All, Influence Score: 30110
# User: twitteer2m, Influence Score: 29962
# User: TheMattEspinosa, Influence Score: 28368
# User: Z_o_d_i_a_c_o, Influence Score: 27959
# User: NiallOfficial, Influence Score: 25751
# User: COMOMOLA5, Influence Score: 21376
# User: a_9_z, Influence Score: 20723
# User: Harry_Styles, Influence Score: 20435
# User: PrncesSyahrinii, Influence Score: 20184
# User: carterreynolds, Influence Score: 19672
# User: BieberAnnual, Influence Score: 18515
# User: LeyAdolescente, Influence Score: 18431
# User: Calum5SOS, Influence Score: 18244
# User: bi366, Influence Score: 17830
# User: NotersBijaks, Influence Score: 17396
# User: medyassfenomenn, Influence Score: 17219
# User: justinbieber, Influence Score: 17163
# User: tuitanic, Influence Score: 17163
# User: girlposts, Influence Score: 17042
# Time Taken: 49.92408037185669 seconds

start_time = time.time()
top_influential_names = set(user for user, _ in top_influential_users)

output_file_path = '/home/lambda3/socialNetwork/top_100_tweeters_retweeters.json'

with open('/home/lambda3/socialNetwork/tweet_retweet_data.json', 'r') as json_file, \
     open(output_file_path, 'w') as output_file:
    for line in json_file:
        if line.strip():
            try:
                row = json.loads(line)
                original_user = row.get('original_user')
                retweeters = row.get('retweeters', [])
                
                # Check if the original user or retweeters are top influencers
                if original_user in top_influential_names:
                    output_file.write(line)
                else:
                    for retweeter in retweeters:
                        if retweeter in top_influential_names:
                            output_file.write(line)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
end_time = time.time()
total_time = end_time - start_time
print("Time Taken: " + str(total_time) + " seconds")

################################################################################################
####################################  Adajency Matrix     ######################################
################################################################################################

def load_user_ids(file_path):
    user_to_id = {}
    with open(file_path, 'r') as file:
        for line in file:
            user, user_id = line.strip().split(',')
            user_to_id[user] = int(user_id)
    return user_to_id

def save_user_ids(user_to_id, file_path):
    with open(file_path, 'w') as file:
        # Write user IDs in chunks to reduce I/O overhead
        chunk_size = 1000  # Adjust this value based on performance testing
        users = list(user_to_id.items())
        for i in range(0, len(users), chunk_size):
            chunk = users[i:i + chunk_size]
            for user, user_id in chunk:
                file.write(f"{user},{user_id}\n")

def load_data(file_path, max_rows=None):
    with open(file_path, 'r') as json_file:
        row_counter = 0
        for line in json_file:
            if line.strip():
                try:
                    row = json.loads(line)
                    yield row  # Yield each row one at a time
                    row_counter += 1
                    if max_rows is not None and row_counter >= max_rows:
                        break  # Stop the generator if max_rows is reached
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")

# Create a generator for loading data
data_generator = load_data('/home/lambda3/socialNetwork/top_100_tweeters_retweeters.json')

# # Runtimes (changing max_rows)
# # 10            Time Taken: 0.0003001689910888672 seconds
# # 100           Time Taken: 0.014852762222290039 seconds
# # 1,000         Time Taken: 0.010419607162475586 seconds
# # 10,000        Time Taken: 0.5511295795440674 seconds
# # 100,000       Time Taken: 36.43090605735779 seconds
# # 1,000,000     Killed (w/ just data generator)

user_ids_file = '/home/lambda3/socialNetwork/user_id.txt'
user_to_id = load_user_ids(user_ids_file)

filtered_language_list = {username: language for username, language in language_list.items() if username in user_to_id}

data_list = list(data_generator)
all_users = set()

# Gets all unique users
for data in data_list:
    all_users.add(data['original_user'])
    for retweeter in data['retweeters']:
        all_users.add(retweeter)


# Create a mapping of user to ID
user_to_id = {user: i for i, user in enumerate(all_users)}
# print(user_to_id)

# Initialize the adjacency matrix
num_users = len(all_users)
adjacency_matrix = [[0] * num_users for _ in range(num_users)]

# Populate the adjacency matrix based on retweet relationships
for data in data_list:
    original_user = data['original_user']
    retweeters = data['retweeters']
    
    original_user_id = user_to_id[original_user]
    for retweeter in retweeters:
        retweeter_id = user_to_id[retweeter]
        adjacency_matrix[original_user_id][retweeter_id] = 1

# Print the adjacency matrix
# for row in adjacency_matrix:
#     print(row)

save_user_ids(user_to_id, user_ids_file)
end_time = time.time()
total_time = end_time - start_time

print("Time Taken for adj. matrix: " + str(total_time) + " seconds")
print("Shape of adjacency matrix:", (len(adjacency_matrix), len(adjacency_matrix[0])))
###############################################################################################

start_time = time.time()
G = nx.DiGraph()

for user in user_to_id:
    if user in filtered_language_list and filtered_language_list[user] is not None:
        language = filtered_language_list[user]
        G.add_node(user, language=language)
    else:
        G.add_node(user)

# # Print the nodes (for debugging purposes)
# print("Nodes:")
# print(G.nodes())

# Add edges based on adjacency matrix
for i in range(num_users):
    for j in range(num_users):
        if adjacency_matrix[i][j] == 1:
            source_user = list(user_to_id.keys())[i]
            target_user = list(user_to_id.keys())[j]
            # print(f"Adding edge: {source_user} -> {target_user}")
            G.add_edge(source_user, target_user)

# Check if the adjacency matrix contains a 1
contains_one = any(1 in row for row in adjacency_matrix)

if contains_one:
    print("Adjacency matrix contains at least one edge (contains a 1).")
else:
    print("Adjacency matrix does not contain any edges (does not contain a 1).")

# Save the graph as a GraphML file
nx.write_graphml(G, 'social_network.graphml')

save_user_ids(user_to_id, user_ids_file)
end_time = time.time()
total_time = end_time - start_time
print(total_time)


###############################################################################################