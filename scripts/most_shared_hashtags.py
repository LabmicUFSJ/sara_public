"""
Script with example

SARA

Get a dataframe with the most common hashtags.

Example
hashtah, count
a, 10
b, 5
"""
import sys

import pandas as pd

from sara.core.sara_data import SaraData
from sara.core.utils import get_hashtags

try:
    collection = sys.argv[1]
    database = sys.argv[2]

except IndexError as error:
    print(f"Error {error}")
    print(f"Please input python {sys.argv[0]} <collection> <database>")
    sys.exit(-1)

# Create database instance
data = SaraData(collection, database)
project = {"entities.hashtags": 1}
# retrieve Tweets from database
tweets = data.get_projected_data(project, 0)

# A list of tuples
# Return a top 10 the most shared Hashtags
common_hashtags = get_hashtags(tweets, 10)

# Create DataFrame
table = pd.DataFrame(common_hashtags, columns=['hashtag', 'count'])

# Most Common hashtags as DataFrame
print(table.head())
