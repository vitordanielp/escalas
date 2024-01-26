import pandas as pd

columns = ["unidade", "sala", "medico", "data"]
df = pd.read_csv("novo.csv", sep=";", header=None, names=columns)
df["periodo"] = ""
df["hora"] = ""


def extraiHora(data):
    return data[11:13]

def limpaData(data):
    return data[:10]

def extraiPeriodo(hora):
    if hora < 13:
        return "Manhã"
    else:
        return "Tarde"


df["hora"] = df["data"].apply(extraiHora).astype(int)
df["periodo"] = df["hora"].apply(extraiPeriodo)
df["data"] = df["data"].apply(limpaData)
del df["hora"]
df = df.drop_duplicates()

salas_ignoradas = ["MAMO ASA SUL", "MAMO LAGO SUL", "DENS ASA SUL",
                   "DENS LAGO SUL", "CONSULTORIO NUTRICAO", "RESSONANCIA MAGNETIC"]

df = df.loc[~df["sala"].isin(salas_ignoradas)]
df = df.sort_values(["data", "sala"])

df_asa_sul = df.loc[df["unidade"] == "ASA SUL"]
del df_asa_sul["unidade"]

df_lago_sul = df.loc[df["unidade"] == "LAGO SUL"]
del df_lago_sul["unidade"]

df.to_csv("escala.csv", sep=";", index=False)
df_lago_sul.to_csv("escala_lago.csv", sep=";", index=False)
df_asa_sul.to_csv("escala_asa.csv", sep=";", index=False)
df.to_json("escala.json", orient="records")
df_lago_sul.to_json("escala_lago.json", orient="records")
df_asa_sul.to_json("escala_asa.json", orient="records")
