import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

archivo_entrada = os.path.join(DATA_DIR, "Biblioteca.csv")

df = pd.read_csv(archivo_entrada)

df.columns = df.columns.str.strip()

for col in ['Genero', 'Autor', 'Editorial', 'Estado']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()


def generar_resumen(df, columna, nombre_salida):
    if columna not in df.columns:
        print(f"⚠️ La columna '{columna}' no existe en el archivo")
        return

    total = len(df)

    resumen = df[columna].value_counts(dropna=False).reset_index()
    resumen.columns = [columna, 'conteo']

    resumen['porcentaje'] = (resumen['conteo'] / total).map(lambda x: f"{x:.4f}")

    ruta_salida = os.path.join(DATA_DIR, nombre_salida)
    resumen.to_csv(ruta_salida, index=False)

    print(f"✅ Generado: {ruta_salida}")

def generar_resumen_genero_subgenero(df, nombre_salida):
    columnas = ['Genero', 'Subgenero']

    for col in columnas:
        if col not in df.columns:
            print(f"⚠️ La columna '{col}' no existe en el archivo")
            return

    total = len(df)

    resumen = (
        df.groupby(['Genero', 'Subgenero'], dropna=False)
        .size()
        .reset_index(name='conteo')
    )

    resumen['porcentaje'] = (resumen['conteo'] / total * 100).map(lambda x: f"{x:.2f}")

    # Orden opcional (muy recomendable)
    resumen = resumen.sort_values(by='conteo', ascending=False)

    ruta_salida = os.path.join(DATA_DIR, nombre_salida)
    resumen.to_csv(ruta_salida, index=False)

    print(f"✅ Generado: {ruta_salida}")

def generar_resumen_fecha_genero(df, nombre_salida):
    columnas = ['FechaPrimeraPublicacion', 'Genero']

    for col in columnas:
        if col not in df.columns:
            print(f"⚠️ La columna '{col}' no existe en el archivo")
            return

    total = len(df)

    resumen = (
        df.groupby(['FechaPrimeraPublicacion', 'Genero'], dropna=False)
        .size()
        .reset_index(name='conteo')
    )

    resumen['porcentaje'] = (resumen['conteo'] / total * 100).map(lambda x: f"{x:.2f}")

    # Orden recomendado
    resumen = resumen.sort_values(
        by=['FechaPrimeraPublicacion', 'conteo'],
        ascending=[True, False]
    )

    ruta_salida = os.path.join(DATA_DIR, nombre_salida)
    resumen.to_csv(ruta_salida, index=False)

    print(f"✅ Generado: {ruta_salida}")


generar_resumen(df, 'Genero', 'resumen_genero.csv')
generar_resumen(df, 'Autor', 'resumen_autor.csv')
generar_resumen(df, 'Editorial', 'resumen_editorial.csv')
generar_resumen(df, 'Estado', 'resumen_estado.csv')
generar_resumen(df, 'FechaPrimeraPublicacion', 'resumen_fecha.csv')
generar_resumen(df, 'Tipo', 'resumen_tipo.csv')
generar_resumen_genero_subgenero(df, 'resumen_genero_subgenero.csv')

generar_resumen_fecha_genero(df, 'resumen_fecha_genero.csv')

print("\n🎉 Proceso terminado")