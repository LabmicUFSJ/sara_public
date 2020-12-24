"""Init"""

from pathlib import Path
import pandas as pd
import sys
from sara.core.sara_data import SaraData


try:
    data_dir_path = sys.argv[1]
    collection_name = sys.argv[2]
except IndexError as error:
    print('Error %s', error)
    print(f'Digite python {sys.argv[0]} <data_path> <collection_name>')
    sys.exit(-1)

collection_name = collection_name



database = SaraData(collection_name)

def load_users(path_to_file):
    """Return a list with users, read from file."""
    users = []
    with open(path_to_file,'r') as arq:
        for i in arq:
            screen_name = i.strip()
            users.append(screen_name)
    return users

def write_to_file(path_to_file, users):
    """Write users to file."""
    with open(path_to_file,'a') as arq:
        for usr_id in users:
            arq.write(str(usr_id))
            arq.write('\n')

data = SaraData(collection_name, storage_type='mongodb')
projection = {'_id':0, 'user.id_str':1}

p = Path(data_dir_path)

for data_path in p.iterdir():
    print(data_path)
    final_path = data_path.name.replace('.txt', '_id.txt')
    final_faltantes = data_path.name.replace('.txt', '_faltantes.txt')
    new_path = data_path.parent.joinpath('id', final_path)
    new_path_faltantes = data_path.parent.joinpath('faltantes', final_faltantes)
    new_path.parent.mkdir(parents=True, exist_ok=True)
    new_path_faltantes.parent.mkdir(parents=True, exist_ok=True)
    print(new_path)

    users = load_users(data_path)
    ids = []
    missing_data = []
    for s_name in users:

        # return first user
        tweets = data.get_filtered_tweet({'user.screen_name':s_name},
                                        projection, 1)
        id_str = None
        for i in tweets:
            try:
                # print(i.get('user')['id_str'])
                # print(s_name, i['user']['id_str'])
                id_str = i.get('user')['id_str']
                ids.append(id_str)
            except (IndexError, ValueError) as error:
                print(f'Error ao obter id do usuário {s_name}')
                sys.exit(-1)
        if not id_str:
            project_2 = {'_id':0, 'retweeted_status.user.id_str':1}
            t = data.get_filtered_tweet({'retweeted_status.user.screen_name':s_name}, project_2, 1)
            for k in t:
                n_id_str = None
                n_id_str = k['retweeted_status']['user']['id_str']
                if n_id_str:
                    missing_data.append(n_id_str)


    # save users ids
    write_to_file(new_path, ids)

    print(f'Usuários Faltantes {len(missing_data)}')
    if missing_data:
        write_to_file(new_path_faltantes, missing_data)

    # table = pd.DataFrame(csv_data)
    # print(f'Tamanho tabela {len(csv_data)}')

    # table.to_csv(new_path_csv, index=False)
    # # teste leitura
    # table2 = pd.read_csv(new_path_csv)

    print(f'Ids dos usuários salvos em: {new_path} .. OK')