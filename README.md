La base de datos astra almacena datos en dos tablas. 
La primera __Muestra__, que contiene columnas de datos de proporción de porosidad, temperatura, espesor y relajamiento. 
La segunda __Madera__ , que contiene columnas de datos de identificación, nombre del tipo de madera y rhoc (capacidad térmica).
El objetivo de estos datos y la utilidad esperada del programa es encontrar la capacidad térmica de cada una de las maderas
y relacionar las tablas en base a la porosidad de las maderas, pues una misma porosidad puede estar relacionada a dos maderas diferentes.

Se usó SQLModel implementando los métodos de CRUD, creando nuevas filas en las tablas, leyendo datos de las tablas,
actualizando datos, eliminando datos ya ingresados y su respectiva confirmación. Se pudo plantear las bases para usar
Relationship Attributes entre tablas.
Sin embargo, no fue posible solucionar el problema *'Muestra' object has no attribute 'maderas'*.
Cabe destacar que a la hora de implementar la relación many to many de acuerdo al tutorial, ocurría exactamente el mismo error,
en ese caso siendo *'Hero' object has no attribute 'teams'*.En consecuencia fue imposible implementar un sistema de 
ingreso de datos que se pudieran relacionar mediante un *link_model* para hacer los cálculos de la capacidad térmica de las maderas.
