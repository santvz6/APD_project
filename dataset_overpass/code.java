/* 
   Salida en CSV - Misma lógica que el Código 1
   (Accesibilidad general + Baños adaptados específicos)
*/
[out:csv(
    ::id, 
    ::type, 
    name, 
    "wheelchair", 
    "toilets:wheelchair", 
    ::lat, 
    ::lon
  ; true; ",")][timeout:25];

// 1. Definir el área: Alicante
{{geocodeArea:Alicante}}->.searchArea;

// 2. Buscar EXACTAMENTE lo mismo que en el primer código
(
  // Buscar cualquier cosa con la etiqueta 'wheelchair'
  node["wheelchair"](area.searchArea);
  way["wheelchair"](area.searchArea);
  relation["wheelchair"](area.searchArea);
  
  // La línea extra que incluí en el primer código para baños específicos
  node["toilets:wheelchair"="yes"](area.searchArea);
);

// 3. Salida usando 'center' para que te de coordenadas únicas incluso en edificios
out center;