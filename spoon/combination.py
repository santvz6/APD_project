import pandas as pd

class Combination:
    def __init__(self, df1_path: str, df2_path: str, key: str):
        self.df1 = pd.read_csv(df1_path).rename(columns=lambda x: x.strip())
        self.df2 = pd.read_csv(df2_path).rename(columns=lambda x: x.strip())
        self.key = key  # columna por la que se alinean las filas
        self.result = None

    def __call__(self, *args, **kwds):
        self.merge_rows()
        self.save(kwds["output_path"])

    def merge_rows(self):
        """
        Fusiona filas de df2 en df1 usando la columna clave.
        Si df2 tiene columnas que df1 no tiene, se añaden.
        Rellena con vacío las celdas faltantes.
        """
        merged = pd.merge(self.df1, self.df2,
            on=self.key,    # key = nombre
            how="outer",    # incluye todas las filas de df1 y df2
            suffixes=("", "_df2")
        )

        # Unimos las columnas duplicadas si existieran
        for col in merged.columns:
            if col.endswith("_df2"):
                base_col = col[:-4]
                merged[base_col] = merged[base_col].combine_first(merged[col])
                merged.drop(columns=[col], inplace=True)

        # Rellenamos los NaN de forma segura
        for col in merged.columns:
            if merged[col].dtype == "object":
                merged[col] = merged[col].fillna("")
            else:
                merged[col] = merged[col].fillna(0)

        # Añadimos un id incremental
        merged.insert(0, "id", range(1, len(merged) + 1))
        self.result = merged
        return merged

    def save(self, output_path: str):
        if self.result is None:
            raise ValueError("Primero debes ejecutar merge_rows().")
        self.result.to_csv(output_path, index=False)


if __name__ == "__main__":
    combination = Combination(
        df1_path="spoon/AccesibilidadEdificiosAlicante_transformation.csv",
        df2_path="spoon/AccesibilidadEdificiosAlicante2_transformation.csv",
        key="nombre"  # columna que identifica la fila
    )
    combination(output_path="spoon/AccesibilidadAlicante_combination.csv")
