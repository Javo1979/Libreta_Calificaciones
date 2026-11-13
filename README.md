# Libreta de calificaciones · PCEI Tungurahua

Consulta individual por cédula, 13 asignaturas en lista colorida, sello institucional y libreta A4 imprimible o guardable como PDF en una sola página.

## Ejecutar localmente

```sh
python -m pip install -r requirements.txt
python app.py
```

Abrir `http://127.0.0.1:5000`. El registro privado debe existir en `datos/calificaciones.json`, generado localmente con `importar_notas.py` a partir de los Excel de la institución. Las fuentes y el registro no forman parte del repositorio.

## Alojamiento Python (Render)

- Conectar este repositorio y usar el servicio definido en `render.yaml`, o crear un Web Service de Python.
- Build: `pip install -r requirements.txt`.
- Start: `waitress-serve --listen=0.0.0.0:$PORT app:app`.
- Variable `CALIFICACIONES_PATH`: `/etc/secrets/calificaciones.json`.
- Variable `TRUST_PROXY`: `1` únicamente cuando el servicio está detrás del proxy de confianza de Render.
- En **Environment → Secret Files**, crear `calificaciones.json` con el contenido del registro local. No subirlo al repositorio ni a la carpeta `static/`.
- El plan gratuito puede suspenderse por inactividad y tardar en responder a la primera visita. Verificar las condiciones y disponibilidad actuales en Render antes de crear el servicio. No se requiere contratar un plan de pago para esta configuración.

GitHub Pages no ejecuta Python. El `index.html` de la raíz dirige al portal en **https://libreta-calificaciones-pcei.onrender.com/**, donde se ejecuta la aplicación. El enlace anterior **https://javo1979.github.io/Libreta_Calificaciones/** se conserva como acceso al nuevo portal.

## Privacidad

El código público no contiene el padrón ni las calificaciones. El servidor devuelve solo el reporte solicitado y oculta parcialmente la cédula. Hay un límite básico de consultas por IP y no se guarda el reporte en el almacenamiento del navegador.

**La cédula no es una contraseña.** Una persona que conozca la cédula de un estudiante podría consultar su reporte. Para controlar identidad se requiere una clave o verificación adicional. El límite de consultas es básico y en memoria, no una garantía contra extracción automatizada.

## Pruebas

```sh
python -m unittest discover -s tests -v
```

Los datos de las pruebas son ficticios. La impresión A4 se verificó con las 13 asignaturas, incluso sin notas y con nombres largos. Ver `LEEME.md` para los criterios de importación y las observaciones de las fuentes.
