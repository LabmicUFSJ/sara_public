"""
Choose random user as Bot or Human
"""
import sys
import random


from sara.core.database import load_users
from sara.core.utils import create_path


def user_input():
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
    return database, collection, population


class RandomBot:
    def __init__(self, database, collection, size_population):
        self.database = database
        self.collection = collection
        self.sample_size = size_population
        self.path_sample = f'classification_random/{collection}'
        self.path_human = f'{self.path_sample}/humans.txt'
        self.path_bot = f'{self.path_sample}/bots.txt'

        create_path(self.path_sample)

    def coin(self):
        return random.randint(0, 1)

    @classmethod
    def write_result(cls, path_sample, samples):
        with open(path_sample, 'w') as arq:
            for usr_id in samples:
                arq.write(str(usr_id)+"\n")

    def main(self):
        """Main method."""
        print("Gerando um conjunto aleatorio de classificação de usuários.")
        users = load_users(self.database, self.collection, None)
        random.shuffle(users)
        humans = []
        bots = []
        flag_bots = 0
        flag_humans = 0
        for user in users:
            if self.coin():
                if len(humans) < self.sample_size:
                    humans.append(user['id'])
                else:
                    flag_humans = 1
            else:
                if len(bots) < self.sample_size:
                    bots.append(user['id'])
                else:
                    flag_bots = 1
            if flag_bots and flag_humans:
                break
        print(len(humans), len(bots))
        self.write_result(self.path_human, humans)
        self.write_result(self.path_bot, bots)


if __name__ == "__main__":
    database, collection, population = user_input()
    randombot = RandomBot(database, collection, population)
    randombot.main()
