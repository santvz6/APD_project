import pandas as pd
import unicodedata

from shapely import wkt
from pyproj import Transformer


class Transformation:

    def __init__(self, input_path: str, output_path):
        self.input_path = input_path
        self.output_path = output_path

        self.df = pd.read_csv(self.input_path)

        
    def __add_lon_lat(self):
        """
        Añade las columnas 'lat' y 'lon' al DataFrame.
        """
        # Creamos transformer: de EPSG:25830 (UTM zona 30N) → EPSG:4326 (WGS84)
        transformer = Transformer.from_crs("EPSG:25830", "EPSG:4326", always_xy=True)
        self.df["lon"], self.df["lat"] = zip(*self.df["WKT"].apply(wkt.loads).apply(lambda point: transformer.transform(point.x, point.y)))
        self.df.drop(columns=["WKT"], inplace=True)


    def __remove_special_char(self):
        """
        Quita tildes y caracteres especiales de todas las columnas de tipo objeto (texto) del DataFrame.
        """
        def clean_text(text):
            if pd.isna(text):
                return text
            text = unicodedata.normalize("NFD", text)
            text = ''.join(c for c in text if unicodedata.category(c) != "Mn")
            text = text.replace("?", "")
            return text
        
        for col in self.df.select_dtypes(include="object").columns:
            self.df[col] = self.df[col].apply(clean_text)
    

    def transformate(self):
        self.__add_lon_lat()
        self.__remove_special_char()
        self.df.to_csv(self.output_path, index= False)


if __name__ == "__main__":

    t = Transformation(
        input_path= "spoon/AccesiblidadEdificiosAlicante.csv",
        output_path="spoon/AccesiblidadEdificiosAlicante_transformation.csv"
    )
    t.transformate()