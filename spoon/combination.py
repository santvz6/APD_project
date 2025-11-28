import pandas as pd

class Combination:
    def __init__(self, df1_path: str, df2_path: str):
        self.df1 = pd.read_csv(df1_path)
        self.df2 = pd.read_csv(df2_path)
        self.result = None

    def __call__(self, *args, **kwds):
        self.concatenate()
        self.save()

    def concatenate(self):
        # Concatenación vertical
        merged = pd.concat([self.df1, self.df2], ignore_index=True)
        merged.insert(0, "id", range(1, len(merged) + 1))
        self.result = merged
        return merged

    def save(self, output_path: str):
        if self.result is None:
            raise ValueError("Primero debes ejecutar concatenate().")
        self.result.to_csv(output_path, index=False)


if __name__ == "__main__":
    combination = Combination(
        df1_path= "spoon/AccesibilidadEdificiosAlicante_transformation.csv",
        df2_path= "spoon/AccesibilidadGeneralAlicante_transformation.csv"
    )
    combination()