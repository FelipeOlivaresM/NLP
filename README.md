# Proyect final NLP

Para la realización de este proyecto se realizo la captura de 1.681.002 Tweets relacionados con la pandemia del covid-19, esto con el fin de analizarlos y poder entrenar un modelo de ML que fuera capaz de discriminar si el texto del Tweet esta asociado a un sentimiento positivo o negativo, además de identificar un sentimiento mas especifico como el luto, los diferentes programas usados para la captura, procesamiento y limpieza de los datos junto con el entrenamiento del modelo y sus resultados se presentan a continuación y están presentes en este repositorio, es importante destacar también que se descartaron los Retweets y para el entrenamiento del modelo se usaron solo datos en idiomas ingles y español, los cuales al momento de su captura fueron normalizados y se capturaron de diferentes países de todo el mundo.

### Captura y preprocesamiento de datos:

A continuación se muestran de forma gráfica las fechas en las que se capturaron los datos junto con la cantidad de Tweet que se capturaron en cada fecha.

![Fechas de captura](captura_de_datos/graficas_datos/arregaldos/0_analisis_fechas.png)

La captura de los Tweets no se restringió a ciertas zonas especificas, sin embargo, debido a las políticas de Twitter los usuarios si así lo desean pueden proteger su ubicación o compartirla, por defecto Twitter protege la ubicación de sus usuarios, en consecuencia la mayoría de las ubicaciones en las que se originan los Tweets son desconocidas, en la siguiente gráfica se muestra con mas detalle la cantidad de Tweets de los que se conoce su origen en contraste con los Tweets cuyo origen geográfico es desconocido.

![Paises desconocidos vs conocidos](captura_de_datos/graficas_datos/arregaldos/0_analisis_paises.png)

Los idiomas como ya fue mencionado se restringieron a ingles o español, sin embargo, algunos datos pudieron sufrir daños o en algunos casos por razones desconocidas el idioma no fue registrado, las proporciones de los idiomas de la totalidad de los Tweets capturados se muestra a continuación.

![Proporcion de idiomas](captura_de_datos/graficas_datos/arregaldos/0_analisis_idiomas.png)

Como se menciono al principio uno de los objetivos del proyecto es discriminar los textos que tienen el sentimiento de luto asociados y los que no, para esto en primera instancia se realizo un prefiltrado de datos usando palabras o mensajes relacionados con luto, como “rip” o “descansa en la gloria de dios” que se buscaron en el texto del Tweet, estos fueron etiquetados manualmente para ser usados posteriormente en el entrenamiento de un modelo de ML el cual fue entrenado para realizar esta tarea, los resultados del prefiltrado con etiquetas se muestra a continuacion.

![Datos prefiltrado luto](captura_de_datos/graficas_datos/arregaldos/0_analisis_preconteo_mourning.png)

De los datos que tuvieron coincidencias y fueron clasificados como asociados al luto la proporción de idiomas es la siguiente.

![Proporcion de idiomas datos prefiltrado luto](captura_de_datos/graficas_datos/arregaldos/0_analisis_idiomas_preconteo_mourning.png)
