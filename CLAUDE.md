# Contexto del proyecto EugenIA (ISI-PF-R16)

Alcance y roadmap vigentes (cargados siempre):
@docs/alcance_70_y_roadmap_eugenia.md

Documento completo del proyecto (Etapas 1-3, análisis, factibilidad y los 23 casos de uso): `docs/PF-Etapa3_Unido_completo.md`. Es extenso; leé la sección que necesites cuando haga falta (por ejemplo, la especificación de un CUU).

Stack propuesto: backend Python (FastAPI), OCR Tesseract + Google Vision, NLP spaCy, base relacional SQL (MS SQL / MySQL), Docker, APIs ARCA y BCRA.

Reglas:
- Respetar partida doble: ningún asiento se confirma si Debe ≠ Haber; usar reversión en lugar de edición destructiva.
- El OCR nunca contabiliza sin confirmación humana; guardar valor extraído y valor corregido.
- El adaptador de ARCA va desacoplado de la lógica contable, con simulador para desarrollo.
- Auditar operaciones críticas (usuario, fecha, acción, entidad, valores antes/después).
- No inventar reglas de negocio ni agregar dependencias innecesarias; cambios pequeños y con pruebas.
- Sin secretos ni credenciales en el repositorio.
- Responder en español.
