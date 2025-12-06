import os
import pandas as pd
import unicodedata

from shapely import wkt
from pyproj import Transformer


class Transformation:

    def __init__(self, input_path: str, output_path):
        self.input_path = input_path
        self.output_path = output_path

        self.df = pd.read_csv(self.input_path, sep=",")
        self.accesibilidad_cols = [
            "accesibilidad_total",
            "e1_entrada_ppal",
            "e2_itinerarios_accesibles",
            "e3_zonas_atencion_publico",
            "e4_servicios_higienicos",
            "e5_elementos_accesibles"
        ]


    def __clean_text(self, text):
        if pd.isna(text):
            return text
        text = unicodedata.normalize("NFD", text)
        text = ''.join(c for c in text if unicodedata.category(c) != "Mn")
        text = text.replace("?", "")
        text = text.replace(",", "")
        return text.lower()
    
    def __clean_df(self):
        """
        Quita tildes y caracteres especiales de todas las columnas de tipo objeto (texto) del DataFrame.
        """
        for col in self.df.select_dtypes(include="object").columns:
            self.df[col] = self.df[col].apply(self.__clean_text)
    

    def __remove_duplicate_names(self):
        """
        Elimina filas cuya columna 'nombre' esté repetida.
        """
        if "nombre" not in self.df.columns:
            return
            
        before = len(self.df)

        self.df["nombre"] = self.df["nombre"].str.strip().str.lower()
        self.df = self.df.drop_duplicates(subset=["nombre"], keep="first").copy()

        after = len(self.df)
        print(f"Nombres duplicados eliminados: {before - after}")        


    def __add_lat_lon(self):
        """
        Añade las columnas 'lat' y 'lon' al DataFrame.
        """
        # Creamos transformer: de EPSG:25830 (UTM zona 30N) → EPSG:4326 (WGS84)
        transformer = Transformer.from_crs("EPSG:25830", "EPSG:4326", always_xy=True)
        coords = self.df["WKT"].apply(wkt.loads).apply(lambda p: transformer.transform(p.x, p.y))

        self.df["lat"] = coords.apply(lambda c: c[1])
        self.df["lon"] = coords.apply(lambda c: c[0])
       
        
        self.df.drop(columns=["WKT"], inplace=True)

    def __map_accessibilidad(self):
        """
        Convierte los valores de accesibilidad a números:
        """

        mapping = {
            "accesibilidad muy baja. barreras arquitectonicas": 1,
            "accesibilidad baja": 2,
            "accesibilidad media": 3,
            "accesibilidad alta": 4
        }
        

        for col in self.accesibilidad_cols:
            if col in self.df.columns:
                # Asignamos 0 por defecto a valores vacíos o nulos
                self.df[col] = (self.df[col].map(mapping).fillna(0).astype(int))


    def __remove_outliers(self):
        """
        Detecta y elimina filas con valores inusuales
        """

        # Outlier para latitud o longitud: fuera del rango esperado para Alicante
        lat_min, lat_max = 37.8, 38.9
        lon_min, lon_max = -0.9, 0.1

        lat_mask = self.df["lat"].between(lat_min, lat_max)
        lon_mask = self.df["lon"].between(lon_min, lon_max)
        before_rows = len(self.df)
        self.df = self.df[lat_mask & lon_mask].copy()
        
        # Outlier para accesibilidad:
        for col in self.accesibilidad_cols:
            if col in self.df.columns:
                # Solo conservamos filas con valores válidos entre 0 y 4
                self.df = self.df[self.df[col].between(0, 4)].copy()


        after_rows = len(self.df)
        print(f"Outliers eliminados: {before_rows - after_rows}")

    

    def __reverse_geocode(self):
        import requests

        """
        Enriquece los datos usando Nominatim (OpenStreetMap) a partir de lat/lon.
        """
        base_url = "https://nominatim.openstreetmap.org/reverse"

        # columnas nuevas
        self.df["direccion"] = ""
        self.df["barrio"] = ""
        self.df["ciudad"] = ""
        self.df["codigo_postal"] = ""
        self.df["tipo_lugar"] = ""

        default_value = "desconocido"
        for i, row in self.df.iterrows():
            print(f"__reverse_geocode(): iteration {i}")
            lat, lon = row["lat"], row["lon"]

            params = {"lat": lat, "lon": lon, "format": "jsonv2", "addressdetails": 1}

            try:
                r = requests.get(base_url, params=params, headers={"User-Agent": "AlicanteAccessibilityBot/1.0"})
                data = r.json()

                # Si no existe address, asignar defaults
                if "address" not in data:
                    raise ValueError("No address in response")

                addr = data["address"]

                self.df.at[i, "direccion"]      = self.__clean_text(addr.get("road", default_value))
                self.df.at[i, "barrio"]         = self.__clean_text(addr.get("neighbourhood", addr.get("suburb", default_value)))
                self.df.at[i, "ciudad"]         = self.__clean_text(addr.get("city", addr.get("town", default_value)))
                self.df.at[i, "codigo_postal"]  = self.__clean_text(addr.get("postcode", default_value))
                self.df.at[i, "tipo_lugar"]     = self.__clean_text(data.get("type", default_value))

            except Exception as e:
                print(f"Error en fila {i}: {e}")
                self.df.at[i, "direccion"] = default_value
                self.df.at[i, "barrio"] = default_value
                self.df.at[i, "ciudad"] = default_value
                self.df.at[i, "codigo_postal"] = default_value
                self.df.at[i, "tipo_lugar"] = default_value

            # Para no saturar el servicio
            # time.sleep(1)

    def transformate(self, add):
        if os.path.exists(self.output_path): 
            print(f"Existing output_path: {self.output_path}, skipping...\n")
            return
        self.__remove_duplicate_names() # Reducción de Redundancia
        self.__clean_df()               # + Limpieza
        if add: self.__add_lat_lon()    # Feature Engineering: Nuevas características
        self.__map_accessibilidad()     # Feature Engineering: Transformación a categorías
        self.__remove_outliers()        # Tratamiento de Outliers
        self.__reverse_geocode()        # Enriquecimiento de Datos
        self.df.to_csv(self.output_path, index= False)


if __name__ == "__main__":

    t1 = Transformation(
        input_path= "spoon/AccesibilidadEdificiosAlicante.csv",
        output_path="spoon/AccesibilidadEdificiosAlicante_transformation.csv"
    )
    t1.transformate(True)

    
    t2 = Transformation(
        input_path= "spoon/AccesibilidadEdificiosAlicante2.csv",
        output_path="spoon/AccesibilidadEdificiosAlicante2_transformation.csv"
    )
    t2.transformate(False)

