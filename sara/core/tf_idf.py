"""Generate TF-IDF"""
import uuid

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from sara.core.config import tf_idf_path
from sara.core.utils import create_path

create_path(tf_idf_path)


def get_tf_idf(corpus):
    """Return a dataframe table with TF-IDF scores and save csv."""
    print('Running TF-IDF :)')
    vectorizer = TfidfVectorizer()
    vector = vectorizer.fit_transform(corpus)
    table = pd.DataFrame(vector[0].T.todense(),
                         index=vectorizer.get_feature_names(),
                         columns=["TF-IDF"])
    table = table.sort_values('TF-IDF', ascending=False)
    print(table.head(25))
    name = uuid.uuid4().hex
    table.to_csv(f'{tf_idf_path}/{name}.csv')
    print(f'file saved with name {name}.csv in {tf_idf_path}')
    return table
