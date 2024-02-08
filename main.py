import pandas as pd

columns = ["data", "sala", "medico", "unidade"]
df = pd.read_csv("escala.csv", sep=";", header=None, names=columns)
df["periodo"] = ""
df["hora"] = ""


def extraiHora(data):
    return data[11:13]


def limpaData(data):
    # Data no formato "dd/mm/yyyy"
    return f"{data[0:2]}/{data[3:5]}/{data[6:10]}"


def extraiPeriodo(hora):
    if hora < 13:
        return "MANHA"
    else:
        return "TARDE"


df["hora"] = df["data"].apply(extraiHora).astype(int)
df["periodo"] = df["hora"].apply(extraiPeriodo)
df["data"] = df["data"].apply(limpaData)
del df["hora"]
df = df.drop_duplicates()
df = df.sort_values(["data", "sala"])

df_asa_sul = df.loc[df["unidade"] == "ASA SUL"]
del df_asa_sul["unidade"]

df_lago_sul = df.loc[df["unidade"] == "LAGO SUL"]
del df_lago_sul["unidade"]


def separar_salas(dataFrame):
    salas_unidade = dataFrame["sala"].unique()
    for sala in salas_unidade:
        dataFrame.loc[df["sala"] == sala].to_json(
            f"dados/{sala}.json", orient="records")


separar_salas(df_lago_sul)
separar_salas(df_asa_sul)
