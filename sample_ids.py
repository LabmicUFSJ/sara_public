"""
Generate a sample list from a list the ids.
- Recovery data from database
Input : list the ids
Output : list ids.txt and data from database in csv
"""
import sys
import os
import pandas as pd
from random import sample
from sara.core.metados import get_user_metadata
from sara.core.database import return_users

try:
    path_tree = sys.argv[1]
    sample_size = int(sys.argv[2])
    database = sys.argv[3]
    collection = sys.argv[4]
    save_folder = sys.argv[5]
    if not path_tree.endswith(".txt"):
        raise TypeError("Fomato inválido.. valido somente .txt")
    print(path_tree, sample_size, database, collection)
except (IndexError, TypeError) as error:
    print(f"Digite {sys.argv[0]}.py <path_file> <sample_size> "
          "<db_name> <collection_name> <save_folder>")
    print(f"Error: {error}")
    sys.exit()

# paths
path = f"samples_result/{collection}/{save_folder}/"
path_sample = f"{path}samples_{collection}_{save_folder}.txt"
path_csv = f"{path}/sample_{collection}_{save_folder}.csv"
path_metadata = f"{path}/sample_{collection}_{save_folder}_metadata.csv"

# crete path tree
if not os.path.exists(path):
    os.makedirs(path)

# load users ids
stream = [arq.strip() for arq in open(path_tree)]

# make a sample from data
samples = sample(stream, sample_size)

print(len(samples))
users = return_users(database, collection, samples)
print(f"Users returned {len(users)}")
users_metadata = [get_user_metadata(meta) for meta in users]

# save txt
with open(path_sample, 'w') as arq:
    for usr_id in samples:
        arq.write(str(usr_id)+"\n")

# save csv
table = pd.DataFrame(users)
table.to_csv(path_csv, index=False)
# save metadata
table = pd.DataFrame(users_metadata)
table.to_csv(path_metadata, index=False)
