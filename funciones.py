import pandas as pd 

def datos(archivo):

    extension = archivo.split('.')[-1].lower()

    if extension == 'csv':
        df = pd.read_csv(archivo)
    elif extension == 'xlsx':
        df = pd.read_excel(archivo)
    else:
        raise ValueError(f"Este formato no está soportado para esta función: .{extension}")

    return df

def nulos(df):

    columnas_numericas = df.select_dtypes(include=['float64', 'int64']).columns

    columnas_pares = columnas_numericas[::2]
    columnas_impares = columnas_numericas[1::2]

    df[columnas_pares] = df[columnas_pares].fillna(df[columnas_pares].mean())
    df[columnas_impares] = df[columnas_impares].fillna(99)

    columnas_no_numericas = df.select_dtypes(exclude=['float64', 'int64']).columns
    df[columnas_no_numericas] = df[columnas_no_numericas].fillna("Este_es_un_valor_nulo")

    return df

def find_nulos(df):
    
    nulos_por_columna = df.isnull().sum()
    nulos_totales = df.isnull().sum().sum()

    return {
        "nulos_por_columna": nulos_por_columna,
        "nulos_totales": nulos_totales
    }

def atipicos(data):

    cuantitativas = data.select_dtypes(include=["float64", "int64"])

    y = cuantitativas
    percentile25 = y.quantile(0.25)  # Q1
    percentile75 = y.quantile(0.75)  # Q3
    iqr = percentile75 - percentile25

    Limite_Superior_iqr = percentile75 + 1.5 * iqr
    Limite_Inferior_iqr = percentile25 - 1.5 * iqr
    print("Límite superior permitido:", Limite_Superior_iqr)
    print("Límite inferior permitido:", Limite_Inferior_iqr)

    data_filtrada = cuantitativas[(y <= Limite_Superior_iqr) & (y >= Limite_Inferior_iqr)]
    data_filtrada = data_filtrada.fillna(round(data_filtrada.mean(), 1))
    Datos_limpios = pd.concat([data.select_dtypes(include=["object"]), data_filtrada], axis=1)

    Datos_limpios.to_csv("London.csv", index=False)

    return Datos_limpios