/* (Accesibilidad general + Baños adaptados específicos) */
[out:csv(
    ::id, 
    ::type, 
    name, 
    "wheelchair", 
    "toilets:wheelchair", 
    ::lat, 
    ::lon
  ; true; ",")][timeout:25];

// Definimos el área: Alicante
{{geocodeArea:Alicante}}->.searchArea;

(
  // Buscamos cualquiera con la etiqueta 'wheelchair'
  node["wheelchair"](area.searchArea);
  way["wheelchair"](area.searchArea);
  relation["wheelchair"](area.searchArea);
  
  node["toilets:wheelchair"="yes"](area.searchArea);
);

// Usamos 'center' para obtener coordenadas únicas incluso en edificios
out center;
