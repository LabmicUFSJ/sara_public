import base
import tf_idf_modelagem_bigrama

noticias = base.carrega_colecao_completo(
    "brumadinhoinflux", "colecao_processada"
)

path = "resultados/"


def to_int_str(data):
    return str(int(data))


def get_key(i):
    data = i['data'].split("/")
    new_data = (
        to_int_str(data[1])
        + "/"
        + to_int_str(data[0])
        + "/"
        + to_int_str(data[2])
    )
    return new_data


def by_date(date):
    return date['data']


lista = sorted(noticias, key=by_date)
datas = set()
for i in lista:
    # print(i['data'])
    datas.add(i['data'])
print(len(datas))
arquivo = open(path + "sumario_datas", "w")
dicio_data = {}
for d in datas:
    conjunto_dias = []
    for i in lista:
        if d == i['data']:
            # agrupa os dados de acordo com  a data
            conjunto_dias.append(i)
    dicio_data[d] = conjunto_dias

for i in dicio_data:
    arquivo.write(
        "dia:" + str(i) + ",N_noticias:" + str(len(dicio_data[i])) + "\n"
    )
print("Sumario gerado, iniciando analises dos dados")
tf_idf_modelagem_bigrama.analise_periodo(dicio_data, 2)
print("Processamento Completo")
