# ADP_project

## Apartado 1: Definición del proyecto centrado en los datos (10%)

**Descripción**

Selecciona una temática: patrimonio cultural, turismo, movilidad, medio ambiente, etc. Identifica algunas preguntas que puedas realizar para solventar un problema en concreto. Por ejemplo, ¿en qué medida ha mejorado Alicante en materia de movilidad en los últimos años? ¿Qué atracciones turísticas se encuentran disponibles en Alicante y cómo podemos visualizarlas de forma atractiva? 

Este apartado está compuesto por las siguientes tareas que deben ser debidamente cumplimentadas y justificadas en el documento final de la entrega. Durante las prácticas se consensuará con el profesorado de la asignatura.

 

### Tareas

- Selección de la temática o dominio en el que se desarrollará el proyecto
- Identificar el problema a resolver 
- Lienzo del problema (4W)
    * Who, quiénes son las partes interesadas
    * What, cuál es el problema o necesidad y cuál es su naturaleza
    * Where, la situación, momento y contexto dónde se produce
    * Why, cuál es el beneficio y su impacto, tanto en las partes interesadas como en la sociedad
- Marcar objetivos del proyecto
- Casos de uso
- Definir métricas clave y evaluar en función de los objetivos y casos de uso

---

**Temática**: Movilidad y Discapacidad 

**Problema a Resolver**: ¿Cómo crear una almacen de datos que ayude a las personas de movilidad reducida a encontrar lugares accesibles en la ciudad? 

**Lienzo del problema**
* **Who:** personas de movilidad reducida ("no se tiene en cuenta a gente en muletas")
* **What:** Moverse por la ciudad
* **Where:** Lugares públicos de la ciudad en el día a día 
* **Why:** Ayudar a las personas de movilidad reducida a ser más independiente y planificar sus rutas 
<br>

**Objetivos del proyecto:**
- O1: Identificar los lugares accesibles
- O2: Clasificar las zonas de la ciudad 
- Ubicar los lugares accesibles (en caso de que haya)
- (opt.) Identificar los transportes accesibles <br><br>


**Casos de uso:**

_"funcionalidad a alto nivel"_
- Visitas a lugares públicos
- Día a Día
- Momentos en los que no disponen de ayuda
- Organizarse en el tiempo <br><br>

**Métricas clave y evaluar en función de los objetivos y casos de uso:** <br><br>
    _"cómo medimos que dicho objetivo se haya completado"_ <br>

- **O1: Identificar los lugares accesibles:**
    * Completa: Cualquier persona de movilidad reducida puede acceder
    * Parcial: Cualquier persona de movilidad reducida con ayuda externa o mecánica puede acceder
    * Nula: Ninguna persona de movilidad reducida puede acceder 

- **O2: Clasificar las zonas de la ciudad:**
    * Zona temporalmente no accesible: Ninguna persona de movilidad reducia puede acceder por causas temporales
    * Zona totalmente accesible: Cualquier persona de movilidad reducida puede acceder
    * Zona parcialmente accesible: Cualquier persona de movilidad reducida con ayuda externa o mecánica puede acceder
    * Zona innacesible: Ninguna persona de movilidad reducida puede acceder 
