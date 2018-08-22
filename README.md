# localidades_AR
Script para generar localidades de Argentina a partir de la base de Correo Argentino

Los archivos incluyen el script principal que genera el csv con las localidades, un archvio de dependencia(tabla_ciudad_bsas.csv) que contiene los codigos postales de Capital Federal que se agregan a los datos que se traen del servidor de Correo Argentino y el csv final que produce el script. Si con el tiempo se hacen cambios la base o se agregan localidades se podra correr el script para generar un csv nuevo mientras que no cambie la forma en que opera el formulario de Consulta de CPA.

Este script aprovecha que la pagina trae todas las localidades con los respectivos codigos postales cuando se le consulta a la base con un POST que contiene headers y body con parametros correspondientes a la provincia en question. Este proceso se repite por cada provincia.
