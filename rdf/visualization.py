import os
import folium
import pandas as pd


class RDFVisualization:
    
    colors = ["blue", "red", "orange", "yellow", "green"]

    def __init__(self, csv_path= os.path.join("spoon", "AccesibilidadAlicante_combination.csv")):
        self.df = pd.read_csv(csv_path)
    
        

    def __call__(self, *args, **kwds):
        self.levelmap_accesibilidad()
        self.heatmap_accesibilidad()
        self.visualization_cluster()


    def levelmap_accesibilidad(self):
        # Centro aproximado en Alicante
        m = folium.Map(location=[38.3452, -0.4810], zoom_start=13)
    
        for level in sorted(self.df['accesibilidad_total'].unique()):
            fg = folium.FeatureGroup(name=f"Nivel {int(level)}")
            for _, row in self.df[self.df['accesibilidad_total'] == level].iterrows():
                lat, lon = row["lat"], row["lon"]
                if pd.notna(lat) and pd.notna(lon):
                    folium.CircleMarker(
                        location=[lat, lon],
                        radius=5,
                        popup=f"{row['nombre']} (Accesibilidad: {row['accesibilidad_total']})",
                        color=RDFVisualization.colors[int(level)],
                        fill=True,
                        fill_opacity=0.8,
                    ).add_to(fg)
            fg.add_to(m)
        
        folium.LayerControl().add_to(m)
        m.save(os.path.join("rdf", "mapa_accesibilidad_niveles.html"))
        

    def heatmap_accesibilidad(self):
        from folium.plugins import HeatMap

        m = folium.Map(location=[38.3452, -0.4810], zoom_start=13)
        heat_data = [[row['lat'], row['lon'], row['accesibilidad_total']] 
                    for _, row in self.df.iterrows() if pd.notna(row['lat']) and pd.notna(row['lon'])]
        HeatMap(heat_data, radius=25).add_to(m)
        m.save(os.path.join("rdf", "heatmap_accesibilidad.html"))


    def visualization_cluster(self):
        from folium.plugins import MarkerCluster

        m = folium.Map(location=[38.3452, -0.4810], zoom_start=13)
        cluster = MarkerCluster().add_to(m)
        
        for _, row in self.df.iterrows():
            lat, lon = row["lat"], row["lon"]
            if pd.notna(lat) and pd.notna(lon):
                folium.Marker(
                    location=[lat, lon],
                    popup=f"{row['nombre']} - Accesibilidad: {row['accesibilidad_total']}"
                ).add_to(cluster)
        
        m.save(os.path.join("rdf", "cluster_accesibilidad.html"))


if __name__ == "__main__":
    visualization = RDFVisualization()
    visualization()
    










