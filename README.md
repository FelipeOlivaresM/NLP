# Proyect final NLP

Instalar requerimientos con: pip install -r requirements.txt

Para la realización de este proyecto se realizo la captura de 1.748.265 Tweets relacionados con la pandemia del covid-19, esto con el fin de analizarlos y poder entrenar un modelo de ML que fuera capaz de discriminar si el texto del Tweet esta asociado a un sentimiento positivo o negativo, además de identificar un sentimiento mas especifico como el luto, los diferentes programas usados para la captura, procesamiento y limpieza de los datos junto con el entrenamiento del modelo y sus resultados se presentan a continuación y están presentes en este repositorio, es importante destacar también que se descartaron los Retweets y para el entrenamiento del modelo se usaron solo datos en idiomas ingles y español, los cuales al momento de su captura fueron normalizados y se capturaron de diferentes países de todo el mundo.

### Captura y preprocesamiento de datos:

A continuación se muestran de forma gráfica las fechas en las que se capturaron los datos junto con la cantidad de Tweet que se capturaron en cada fecha día a día y de forma acumulativa.

<table width="100%" style="border-collapse: collapse; border: none;" cellspacing="0" cellpadding="0">
<tr style="padding: 0px; margin: 0px; border: none;">
<td style="padding: 0px; margin: 0px; border: none; line-height:0;">
<img src="captura de datos/graficas datos/0_analisis_fechas_dia_a_dia.png" width="100%" height="auto" style="padding: 0px; margin: 0px; border: none; line-height:0;"/>
</td>
<td style="padding: 0px; margin: 0px; border: none; line-height:0;">
<img src="captura de datos/graficas datos/0_analisis_fechas_acomulativo.png" width="100%" height="auto" style="padding: 0px; margin: 0px; border: none; line-height:0;"/>
</td>
</tr>
</table>

La captura de los Tweets no se restringió a ciertas zonas especificas, sin embargo, debido a las políticas de Twitter los usuarios si así lo desean pueden proteger su ubicación o compartirla, por defecto Twitter protege la ubicación de sus usuarios, en consecuencia la mayoría de las ubicaciones en las que se originan los Tweets son desconocidas, en la siguiente gráfica se muestra con mas detalle la cantidad de Tweets de los que se conoce su origen en contraste con los Tweets cuyo origen geográfico es desconocido, ademas se muestra la grafica de proporciones de idiomas, los idiomas como ya fue mencionado se restringieron a ingles o español, sin embargo, algunos datos pudieron sufrir daños o en algunos casos por razones desconocidas el idioma no fue registrado, las proporciones de los idiomas de la totalidad de los Tweets capturados se muestra junto a la grafica de ubicaciones.

<table width="100%" style="border-collapse: collapse; border: none;" cellspacing="0" cellpadding="0">
<tr style="padding: 0px; margin: 0px; border: none;">
<td style="padding: 0px; margin: 0px; border: none; line-height:0;">
<img src="captura de datos/graficas datos/0_analisis_paises.png" width="100%" height="auto" style="padding: 0px; margin: 0px; border: none; line-height:0;"/>
</td>
<td style="padding: 0px; margin: 0px; border: none; line-height:0;">
<img src="captura de datos/graficas datos/0_analisis_idiomas.png" width="100%" height="auto" style="padding: 0px; margin: 0px; border: none; line-height:0;"/>
</td>
</tr>
</table>

Como se menciono al principio uno de los objetivos del proyecto es discriminar los textos que tienen el sentimiento de luto asociados y los que no, para esto en primera instancia se realizo un prefiltrado de datos usando palabras o mensajes relacionados con luto, como “rip” o “descansa en la gloria de dios” que se buscaron en el texto del Tweet, estos fueron etiquetados manualmente para ser usados posteriormente en el entrenamiento de un modelo de ML el cual fue entrenado para realizar esta tarea, de los datos que tuvieron coincidencias y fueron clasificados como asociados al luto ademas se identifico la proporcion de los idiomas en los que estaban escritos, los resultados del prefiltrado con etiquetas se muestra a continuación junto con los resultados de la proporcion de idiomas obtenida en este prefiltrado.

<table width="100%" style="border-collapse: collapse; border: none;" cellspacing="0" cellpadding="0">
<tr style="padding: 0px; margin: 0px; border: none;">
<td style="padding: 0px; margin: 0px; border: none; line-height:0;">
<img src="captura de datos/graficas datos/0_analisis_preconteo_mourning.png" width="100%" height="auto" style="padding: 0px; margin: 0px; border: none; line-height:0;"/>
</td>
<td style="padding: 0px; margin: 0px; border: none; line-height:0;">
<img src="captura de datos/graficas datos/0_analisis_idiomas_preconteo_mourning.png" width="100%" height="auto" style="padding: 0px; margin: 0px; border: none; line-height:0;"/>
</td>
</tr>
</table>

Uniendo los datos de varios grupos trabajando en el mismo proyecto se logro obtener la siguiente proporción de datos certificados sin repetir, donde es y en son los idiomas y 1 y 0 indican si el sentimiento de luto se encuentra presento o no respectivamente en el texto, tambien se trabajo en identificar las emociones presentes en un texto, para lograr esto se recolectaron datos en ingles y en español y se etiquetaron como 0 para sentimientos positivos, 1 para negativos y 2 para neutrales, en un principio se conto con la siguiente distribucion de datos.

<table width="100%" style="border-collapse: collapse; border: none;" cellspacing="0" cellpadding="0">
<tr style="padding: 0px; margin: 0px; border: none;">
<td style="padding: 0px; margin: 0px; border: none; line-height:0;">
<img src="entrenamiento de modelos/graficas datos/distribucion_datos_mourning_c0.png" width="100%" height="auto" style="padding: 0px; margin: 0px; border: none; line-height:0;"/>
</td>
<td style="padding: 0px; margin: 0px; border: none; line-height:0;">
<img src="entrenamiento de modelos/graficas datos/distribucion_datos_sentiments_c0.png" width="100%" height="auto" style="padding: 0px; margin: 0px; border: none; line-height:0;"/>
</td>
</tr>
</table>

Sin embargo los datos estaban des balanceados, por lo que se procedió a balancear los datos, la proporción de los datos ya balanceados y preparados para usarse en el entrenamiento de modelos de machine learning es la siguiente.

<table width="100%" style="border-collapse: collapse; border: none;" cellspacing="0" cellpadding="0">
<tr style="padding: 0px; margin: 0px; border: none;">
<td style="padding: 0px; margin: 0px; border: none; line-height:0;">
<img src="entrenamiento de modelos/graficas datos/distribucion_datos_mourning_c1.png" width="100%" height="auto" style="padding: 0px; margin: 0px; border: none; line-height:0;"/>
</td>
<td style="padding: 0px; margin: 0px; border: none; line-height:0;">
<img src="entrenamiento de modelos/graficas datos/distribucion_datos_sentiments_c1.png" width="100%" height="auto" style="padding: 0px; margin: 0px; border: none; line-height:0;"/>
</td>
</tr>
</table>

A pesar de ser proporciones de datos bastante significativas no son suficientes para entrenar modelos del todo sólidos usando solamente los vectores de texto como features, además, al limitar los datos al balancear el dataset de entrenamiento el vocabulario de estos modelos a veces se queda corto respecto al vocabulario de la totalidad de los datos, lo que afecta el desempeño de los modelos cuando encuentran nuevos valores.
