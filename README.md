# Morella v2

Este repositorio corresponde a la versión 2 de Morella, un sistema de gestión en desarrollo para una empresa de Rosario (Argentina), la cual se dedica a la administración de panteones sociales. 

Los cambios mas importantes respecto de la versión 1 son: La implementación de una GUI creada mediante la utilización de la librería PySide6 y el uso de código reutilizable mediante la programación orientada a objetos.

Al momento esta versión se encuentra en desarrollo, sin haberse lanzado todavía la version Alpha.

## Base de datos
La base de datos se encuentra en un servidor de PostgreSQL alojado en Ubuntu.
Mediante la utilización de bash y cronejobs se realiza automáticamente un respaldo diario de la base de datos, éstos se guardan en una carpeta sincronizada a la nube mediante el servicio de Dropbox. 

Para ahorrar espacio sólo se almacenan 15 respaldos, luego, cada vez que se crea uno nuevo, se elimina el más antiguo. 

También es posible realizar un respaldo de forma manual a través de un ícono en el menú de aplicaciones de Ubuntu, al cual puede accederse a través de RDP.
