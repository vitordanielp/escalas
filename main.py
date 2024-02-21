import pandas as pd


################### ESCALAS ###################

def execEscalas():
    columns = ["data", "sala", "medico", "unidade"]
    df = pd.read_csv("escala.csv", sep=";", header=None, names=columns)
    df["periodo"] = ""
    df["hora"] = ""

    def extraiHora(data):
        return data[11:16].replace(":", ".")

    def limpaData(data):
        # Data no formato "dd/mm/yyyy"
        return f"{data[0:2]}/{data[3:5]}/{data[6:10]}"

    def extraiPeriodo(hora):
        if hora < 13.25:
            return "MANHA"
        else:
            return "TARDE"

    df["hora"] = df["data"].apply(extraiHora).astype(float)
    df["periodo"] = df["hora"].apply(extraiPeriodo)
    df["data"] = df["data"].apply(limpaData)
    del df["hora"]
    df = df.drop_duplicates()
    df = df.sort_values(["data", "sala"])

    df_lago_sul = df.loc[df["unidade"] == "LAGO SUL"]
    df_asa_sul = df.loc[df["unidade"] == "ASA SUL"]
    df_lago_sul = df_lago_sul.reset_index(drop=True)
    df_asa_sul = df_asa_sul.reset_index(drop=True)

    def separar_salas(dataFrame):
        salas_unidade = dataFrame["sala"].unique()
        unidade = dataFrame.unidade[0].lower().replace(" ", "-")
        with open(f"dados/{unidade}/salas.txt", "w") as file:
            for sala in sorted(salas_unidade):
                file.writelines(sala + ";")
        for sala in salas_unidade:
            new_df = dataFrame.loc[dataFrame["sala"] == sala]
            new_df.to_json(f"dados/{unidade}/{sala}.json",
                           index=False, orient="records")

    separar_salas(df_lago_sul)
    separar_salas(df_asa_sul)
    del df, df_asa_sul, df_lago_sul, columns
# Fim do script para escalas


################### PACOTES DE EXAMES ###################

def execPacotes():
    columns = ["nome", "mamografia", "ampliacao", "densi", "us mamas"]
    df = pd.read_csv("pacotes.csv", sep=";", names=columns)
    df = df.fillna(value="-")
    
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x.lower())
        
    def corrigeEscrita(str):
        return str.replace("saude", "saúde").replace("policia", "polícia").replace("camara", "câmara")
    
    df.nome = df.nome.apply(corrigeEscrita)
    df.ampliacao = df.ampliacao.apply(lambda x: x.lower().replace("ampliacao", "ampliação"))

    df.to_json("dados/pacotes/pacotes.json", index=False, orient="records")


if __name__ == "__main__":
    execEscalas()
    execPacotes()
