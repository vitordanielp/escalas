import pandas as pd

columns = ["data", "sala", "medico", "unidade"]
df = pd.read_csv("escala.csv", sep=";", header=None, names=columns)
df["periodo"] = ""
df["hora"] = ""


def extraiHora(data):
    return data[11:13]


def limpaData(data):
    # Data no formato "yyyy/mm/dd"
    return f"{data[6:10]}/{data[3:5]}/{data[0:2]}"


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

salas_ignoradas = ["DENS ASA SUL", "DENS LAGO SUL",
                   "CONSULTORIO NUTRICAO", "RESSONANCIA MAGNETIC"]

df = df.loc[~df["sala"].isin(salas_ignoradas)]
df = df.sort_values(["data", "sala"])

# df_asa_sul = df.loc[df["unidade"] == "ASA SUL"]
# del df_asa_sul["unidade"]

# df_lago_sul = df.loc[df["unidade"] == "LAGO SUL"]
# del df_lago_sul["unidade"]

# df.to_csv("escala.csv", sep=";", index=False)
# df_lago_sul.to_csv("escala_lago.csv", sep=";", index=False)
# df_asa_sul.to_csv("escala_asa.csv", sep=";", index=False)
df.to_json("escala.json", orient="records")
# df_lago_sul.to_json("escala_lago.json", orient="records")
# df_asa_sul.to_json("escala_asa.json", orient="records")
