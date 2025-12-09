"""
Nota:
Decidir el mapeo CSV → RDF (conceptualmente)

Aunque no veamos todas las columnas, por lo que se ve en el fichero, tendrás algo parecido a:

id, nombre,métricas de accesibilidad (e1_entrada_ppal, e2_itinerarios_accesibles, …),lat,lon,
direccion,barrio,ciudad,codigo_postal,tipo_lugar

Vamos a mapear así:

cada fila → self.SCHEMA:Place
nombre → self.SCHEMA:name
direccion → self.SCHEMA:address


barrio → self.SCHEMA.addressLocality o self.SCHEMA:addressRegion (podemos dejarlo en self.SCHEMA:address)
ciudad → self.SCHEMA:addressLocality
codigo_postal → self.SCHEMA:postalCode
lat → self.SCHEMA:latitude
lon → self.SCHEMA:longitude
tipo_lugar → self.SCHEMA:category
campos de accesibilidad → también self.SCHEMA:category o self.SCHEMA:accessibilitySummary (si queremos algo más textual)

No hace falta complicarse: con 5-7 propiedades ya está muy bien para la práctica.

"""

import pandas as pd
import os

from rdflib import Graph, Namespace, Literal, RDF
from rdflib.namespace import XSD

class RDFTransformation:
    
    city_to_qid = {
        "alacant / alicante": "Q11959",      
        "altea": "Q82028",                    
        "aspe": "Q57814",                     
        "la vila joiosa / villajoyosa": "Q163104", 
        "novelda": "Q163124",         
        "calp": "Q81696",                    
        "almoradi": "Q163145",             
        "la vall de laguar": "Q103583",    
        "onil": "Q163176",                   
        "castalla": "Q163157",               
        "sant joan d'alacant": "Q163133",
        "desconocido": None                
    }

        
    osm_to_qid = {
        "restaurant": "Q11707",
        "cafe": "Q177634",
        "bar": "Q17628",
        "fast_food": "Q177634",
        "pub": "Q227275",
        "school": "Q3918",
        "university": "Q3918",
        "kindergarten": "Q165956",
        "library": "Q7075",
        "hospital": "Q16917",
        "clinic": "Q174728",
        "pharmacy": "Q12140",
        "supermarket": "Q10943",
        "park": "Q22698",
        "playground": "Q163948",
        "bank": "Q41176",
        "cinema": "Q177220",
        "theatre": "Q16647",
        "police": "Q85218",
        "bus_station": "Q55488",
        "train_station": "Q55488",
        "parking": "Q264676",
        "desconocido": None
    }

    def __init__(self, csv_path="spoon/AccesibilidadAlicante_combination.csv"):
        self.df = pd.read_csv(csv_path, encoding="utf-8", sep=",")
        print(self.df.head())

        # Vocabulario schema.org
        self.SCHEMA = Namespace("https://schema.org/")
        # Espacio de nombres para nuestros recursos
        self.EX = Namespace("http://example.org/accesibilidad/")
        # Espacio de nombres de WikiData
        self.WD = Namespace("http://www.wikidata.org/entity/")

        self.g = Graph()        
        self.g.bind("schema", self.SCHEMA)
        self.g.bind("ex", self.EX)
        self.g.bind("wd", self.WD)  # <lugar_i> schema:name wd:Q11975 .

        # <lugar_XX> schema:containedInPlace wd:Q11975 .

    def __call__(self, *args, **kwds):
        self.__generate_uri()
        self.__save_rdf()


    def __generate_uri(self):
        """ 
        | Columna CSV   | Propiedad RDF           |
        | ------------- | ------------------------|
        | nombre        | schema:name             |
        | direccion     | schema:address          |
        | barrio        | schema:addressRegion    |
        | ciudad        | schema:addressLocality  |
        | codigo_postal | schema:postalCode       |
        | lat           | schema:latitude         |
        | lon           | schema:longitude        |
        | tipo_lugar    | schema:category         |
       """
        
        for idx, row in self.df.iterrows():

            # URI única para cada lugar
            recurso = self.EX[f"lugar_{row['id']}"]

            # Tipo principal del recurso 
            self.g.add((recurso, RDF.type, self.SCHEMA.Place)) # <http://example.org/accesibilidad/lugar_i> schema:name "string_name" 

            # Nombre del lugar
            if pd.notna(row["nombre"]):
                self.g.add((recurso, self.SCHEMA.name, Literal(row["nombre"])))

            # Dirección
            if pd.notna(row["direccion"]):
                self.g.add((recurso, self.SCHEMA.address, Literal(row["direccion"])))

            # Ciudad
            if pd.notna(row["ciudad"]):
                ciudad_norm = row["ciudad"].lower().strip()
                self.g.add((recurso, self.SCHEMA.addressLocality, Literal(row["ciudad"])))

                # ENRIQUECIMIENTO: asignamos el QID correcto según la ciudad
                if ciudad_norm in self.city_to_qid:
                    qid = self.city_to_qid[ciudad_norm]
                    if qid is not None:  
                        self.g.add((recurso, self.SCHEMA.containedInPlace, self.WD[qid]))



            # Barrio (lo añadimos dentro de address)
            if pd.notna(row["barrio"]):
                self.g.add((recurso, self.SCHEMA.addressRegion, Literal(row["barrio"])))

            # Código postal
            if pd.notna(row["codigo_postal"]):
                postal = str(row["codigo_postal"]).replace(".0", "0")
                self.g.add((recurso, self.SCHEMA.postalCode, Literal(postal)))

            # Coordenadas
            if pd.notna(row["lat"]):
                self.g.add((recurso, self.SCHEMA.latitude, Literal(float(row["lat"]), datatype=XSD.float)))

            if pd.notna(row["lon"]):
                self.g.add((recurso, self.SCHEMA.longitude, Literal(float(row["lon"]), datatype=XSD.float)))

            # Tipo de lugar (por ejemplo: colegio, cafetería, parada, etc.)
            if pd.notna(row["tipo_lugar"]):
                self.g.add((recurso, self.SCHEMA.category, Literal(row["tipo_lugar"])))
                
                # Enriquecimiento: tipo de lugar → QID de Wikidata
                tipo_norm = str(row["tipo_lugar"]).lower().strip()
                if tipo_norm in self.osm_to_qid:
                    qid_tipo = self.osm_to_qid[tipo_norm]
                    if qid_tipo is not None:
                        self.g.add((recurso, self.SCHEMA.additionalType, self.WD[qid_tipo]))


            # Accesibilidad global
            if pd.notna(row["accesibilidad_total"]):
                self.g.add((recurso, self.SCHEMA.accessibilitySummary, Literal(int(row["accesibilidad_total"]), datatype=XSD.int)))

            # Campos de accesibilidad específicos (los unificamos en un texto)
            detalles_accesibilidad = []

            for campo in [
                "e1_entrada_ppal",
                "e2_itinerarios_accesibles",
                "e3_zonas_atencion_publico",
                "e4_servicios_higienicos",
                "e5_elementos_accesibles"
            ]:
                if pd.notna(row[campo]):
                    detalles_accesibilidad.append(f"{campo}:{row[campo]}")

            # Guardamos los detalles de accesibilidad agrupados
            if detalles_accesibilidad:
                self.g.add((recurso, self.SCHEMA.accessibilityFeature, Literal(", ".join(detalles_accesibilidad))))


    def __save_rdf(self, output_path=os.path.join("rdf", "accesibilidad.ttl")):         
        self.g.serialize(output_path, format="turtle")
        print("Fichero RDF generado:", output_path)
        print("Número de tripletas generadas:", len(self.g))


    
        

if __name__ == "__main__":
    rdf = RDFTransformation()
    rdf()
