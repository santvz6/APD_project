import pandas as pd
from shapely import wkt
from pyproj import Transformer


df = pd.read_csv("dataset/AccesiblidadEdificiosAlicante.csv")

# Crear transformer: de EPSG:25830 (UTM zona 30N) → EPSG:4326 (WGS84)
transformer = Transformer.from_crs("EPSG:25830", "EPSG:4326", always_xy=True)

df["lon"], df["lat"] = zip(*df["WKT"].apply(wkt.loads).apply(lambda point: transformer.transform(point.x, point.y)))

df.to_csv("dataset/AccesiblidadEdificiosAlicante_WKT.csv", index= False)
print(df[["WKT", "lat", "lon"]].head())
