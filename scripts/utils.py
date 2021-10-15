"""common code related to scripts."""
import sys


def handler_input():
    """Handler user input."""
    try:
        network_name = sys.argv[1]
        collection = sys.argv[2]
        database = sys.argv[3]
        directed = sys.argv[4]
        limit = int(sys.argv[5])
        source = sys.argv[6]
        # limite de tweets a serem utilizados
    except IndexError as exc:
        print(f"erro {exc}")
        print(f"ERRO!!\nDigite:\n>python3 {sys.argv[0]} <nome_rede>"
              " <nome_colecao> <database> <True||False> <limite> <r|m>")
        print("Info True: Rede direcionada, False: Rede não direcionada"
              "\nInfo limite:0 para utilizar a base completa")
        print("Info r: para gerar uma rede utilizando retweets, "
              "m: gera a rede utilizando menções(@)")
        sys.exit(-1)

    print("---Inputed Data---\n")
    print(f"Network name: {network_name} \n"
          f"Collection: {collection} \n"
          f"Database: {database} \n"
          f"Directed: {directed} \n"
          f"Type: {source}")
    print("-----------------")
    return network_name, collection, database, directed, limit, source


def is_directed(directed):
    """check if network is directed."""
    if directed.lower() == 'true':
        return True
    if directed.lower() == 'false':
        return False

    raise TypeError("Error, Valid type is True or False."
                    f"You passed the type: {type(directed)}")
