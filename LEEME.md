# Portal de calificaciones · PCEI Tungurahua

Diseño tipo libreta: una asignatura por fila, con color propio, emoji, promedio final a la derecha y una felicitación o recomendación corta. La lista se mantiene en una sola columna tanto en celulares como en computadoras.

## Imprimir o descargar en PDF

Después de consultar una cédula, pulsar **Imprimir / Guardar PDF**. Se abre la impresión del navegador: elegir una impresora o **Guardar como PDF** (en algunos celulares aparece como «Guardar en PDF» o «Compartir»). La libreta tiene una versión compacta A4 vertical, preparada para las 13 materias en una sola hoja, con nombre, período, sello y mensajes. No incluye el formulario ni los elementos decorativos. Si se cambió la configuración del navegador, usar papel A4, escala 100 % y desactivar encabezados y pies del navegador. La descarga depende del diálogo de impresión del dispositivo; no envía las notas a un servicio externo.

## Abrir la página

1. Instalar Python 3.10 o superior.
2. En esta carpeta ejecutar `python -m pip install -r requirements.txt`.
3. Ejecutar `python importar_notas.py` si todavía no existe el registro o para actualizarlo.
4. Hacer doble clic en **iniciar.bat**.
5. Abrir **http://127.0.0.1:5000**. Mantener la ventana del servidor abierta.

El servidor es necesario: no abrir `templates/index.html` con doble clic. No requiere Node, servicios externos ni conexión a internet para mostrar la interfaz.

## Datos y criterios

- Curso: primero de Bachillerato, paralelo I. Primer período, agosto 2026–enero 2027, según las hojas por asignatura.
- Se muestran las 13 asignaturas y exclusivamente la columna **O: Promedio Final** de los archivos `.xls` adjuntos. No se recalculan las notas ni se toman los promedios parciales. Se mantienen dos decimales.
- Celda final vacía, error o texto: **Sin nota**. Un cero numérico sí es una calificación y se conserva como cero.
- `Registro_Calificaciones_Paralelo_I.xlsx`, hoja `1ro I Matemática`: únicamente se utiliza como padrón para asociar nombres y cédulas. Sus promedios NO reemplazan los `.xls`; hay diferencias de redondeo entre las fuentes.
- Los nombres se vinculan normalizando acentos, mayúsculas y espacios; una inconsistencia impide la importación, para no adjudicar notas a otra persona.
- `datos/informe_importacion.json` contiene el resumen de carga por materia sin cédulas ni nombres.
- Los mensajes son orientativos: 9–10 excelente, 7–8,99 buen avance, menos de 7 refuerzo. No representan una resolución oficial de promoción.

### Observaciones que deben confirmarse antes de publicar

1. **Educación Física:** el archivo `1.I - Educ. Fisica.xls` tiene como encabezado interno «Emprendimiento y Gestión». Se importan sus propios datos y se etiqueta por el nombre de archivo. Confirmar con el docente que esas notas pertenecen a Educación Física.
2. **Sello:** `static/sello.png` contiene el sello circular original proporcionado en `sello-nuevo.png`. Se utiliza en la página, el icono de la pestaña y la libreta impresa/PDF, conservando sus proporciones y transparencia.
3. El padrón XLSX menciona 2025–2026, mientras las hojas de asignaturas señalan agosto 2026–enero 2027. La página usa el período de las hojas de asignaturas.

## Actualizar las notas

Reemplazar los archivos de materias en la carpeta superior y el padrón XLSX dos niveles arriba, conservando sus nombres. Ejecutar `python importar_notas.py`. El servidor leerá los cambios en la siguiente consulta. Los Excel originales no se modifican.

## Privacidad y publicación

Las calificaciones completas permanecen en el servidor, en `datos/`, no dentro del JavaScript ni de archivos públicos. Cada consulta POST devuelve un solo reporte; la cédula se muestra parcialmente oculta y no se escribe en la URL. No hay analítica, cookies, fuentes remotas ni guardado en localStorage. Incluye límite básico de consultas por IP y cabeceras de seguridad.

**Conocer una cédula no demuestra identidad.** Esta versión queda disponible únicamente en el equipo local. Antes de publicarla en internet, implementar autenticación adicional (clave individual o código de verificación), HTTPS y protección persistente contra consultas automatizadas. El límite en memoria es básico, se reinicia con el proceso y no sustituye esas medidas. Configurar correctamente un proxy si se utiliza; no confiar sin validación en `X-Forwarded-For`. Nunca publicar la carpeta `datos/` ni servir toda esta carpeta mediante un servidor estático. No subir las cédulas o los Excel a repositorios públicos.

## Comprobar funcionamiento

Ejecutar `python -m unittest discover -s tests -v`. Las pruebas usan datos ficticios, no divulgan datos del alumnado.
