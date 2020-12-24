"""
Sara pre_processing.
"""

from os import name
import sys

import pandas as pd
from sara.core.pre_processing import PreProcessing


try:
    name = sys.argv[1]
except (IndexError, KeyError) as error:
    print(f'Erro {error}, digite python {sys.argv[0]} <file.csv>')
    sys.exit(-1)

# load csv
table_csv = pd.read_csv(name)

clean = PreProcessing()



text = clean.clean_texts(table_csv.full_text)


table_csv['full_text'] = text

name_clean = name.split('.csv')[0] +"_clean.csv"

# salva o csv
table_csv.to_csv(name_clean, index=False)

# load csv
pd.read_csv(name_clean)
