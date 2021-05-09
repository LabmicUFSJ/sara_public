import sys
from sara.core.sara_bot import SaraBot


try:
    name_file = sys.argv[0]
    database = sys.argv[1]
    collection = sys.argv[2]
    population = int(sys.argv[3])
except IndexError as exc:
    print(f"erro {exc}")
    print(f"Digite {name_file} <banco> <colecao> <tamanho_populacao>")
    print("tamanho_populacao = 0 checa todos os usuários da coleção.")
    sys.exit()

print(f"Banco a ser utilizado:{database} \nColecao: {collection}")
population = None if population == 0 else population
sara = SaraBot(database, collection, population)
human_list, bot_list = sara.run()
print(f"Bots {len(bot_list)} Humanos {len(human_list)}")
sara.save_json()
