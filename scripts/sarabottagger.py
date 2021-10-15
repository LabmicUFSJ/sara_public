"""SaraBotTagger

Script to classify users from Twitter as bot or human.

This script use SaraBotTagger model by SARA.

SaraBotTagger was built using Random Forest.
"""
import sys

from sara.core.sarabottagger import SaraBotTagger

try:
    name_file = sys.argv[0]
    collection = sys.argv[1]
    database = sys.argv[2]
    population = int(sys.argv[3])
except IndexError as exc:
    print(f"erro {exc}")
    print(f"Input: python {name_file} <collection> <database>"
          "<number_of_users>")
    print("number_of_users = 0 check all accounts in collection.")
    sys.exit(-1)

print(f"Database:{database} \nCollection: {collection}")
population = None if population == 0 else population
# Atention: You will need specify the SarabotTagger model.
sara = SaraBotTagger(database, collection, population,
                     model='modelo_9.joblib')
human_list, bot_list, _ = sara.run()
print(f"Bots {len(bot_list)} Humans {len(human_list)}")
sara.save_json()
print('Saving Class probability ..')
sara.save_csv()
print('All data has been saved')
