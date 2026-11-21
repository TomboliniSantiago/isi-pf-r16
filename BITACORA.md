# Bitácora

Registro de lo hecho en cada sesión de trabajo y de lo pendiente al cerrarla (push a `main`).

---

## 2026-10-30

**16:27** — Repositorio creado (`66148d2`).

**18:06** — Base del proyecto (`f18ffc4`, en `main`).
- Backend FastAPI + SQLAlchemy sobre Azure SQL (`pfinalbasedd`).
- CUU-015: login con contraseña (bcrypt) y token JWT, bloqueo temporal tras 3 intentos fallidos, cambio obligatorio de la contraseña temporal, cierre de sesión.
- CUU-018: alta, modificación, consulta, baja lógica, reactivación y restablecimiento de contraseña de usuarios. Solo para Administrador.
- Auditoría de accesos y operaciones sobre usuarios en `AUDITORIA_LOG`.
- Migración 001 (columnas de bloqueo y contraseña temporal, índices únicos, `origen` en auditoría).
- Frontend: login, cambio de contraseña y gestión de usuarios.
- Comando `crear-admin` para el primer administrador.
- Se descartó por ahora la publicación en ECR/Docker.

## 2026-10-31

**14:17** — CRUD de usuarios sin inicio de sesión para desarrollo (`d957012`, rama `crud-usr`).
- Endpoints `/api/auth/dev/usuarios` y pantalla `/dev/usuarios`, auditados como `sin_sesion`.
- No se puede dar de baja ni cambiar el perfil del último administrador activo.
- Conexión con el usuario de aplicación `APPusr`.

**14:36** — Correcciones de conexión (`c0b8d61`).
- El timeout de login de ODBC no se aplicaba (`Connection Timeout` no es una clave válida); ahora se pasa a pyodbc.
- Base no disponible responde 503 con mensaje claro.

**14:43** — Selector de perfil bloqueado al crear usuarios sin sesión (`dff57b6`, rama `fix/crud`).

## 2026-11-03

**20:46** — Segundo factor por correo, recupero y cambio de contraseña (rama `feature/2fa-correo`, sin commit).
- Login en dos pasos: contraseña y luego código de 6 dígitos enviado por correo.
- Recupero de contraseña (CUU-015 camino 1.a) validando identidad con código.
- El cambio voluntario de contraseña pide código; el cambio obligatorio de la temporal no.
- Códigos de un solo uso: vencen a los 10 min, 5 intentos, reenvío cada 60 s, guardados como hash.
- Envío de correo en modo consola (desarrollo) o SMTP.
- Migración 002 (`CODIGO_VERIFICACION`), aplicada.
- Reintento automático de conexión mientras Azure SQL serverless se reanuda (error 40613).
- `iniciar.bat` para levantar backend y frontend juntos.
- README reducido a la puesta en marcha; se crea esta bitácora.

### Pendientes al cierre

- Commit de `feature/2fa-correo`, pull request y merge a `main` (lo del 31/10 tampoco está en `main`).
- Configurar un SMTP real (Gmail con contraseña de aplicación) y probar el envío.
- Compartir las migraciones 001 y 002 con el equipo: no están en el repositorio.
- El logout no invalida el token JWT: sigue vigente hasta que vence (60 min).
- Quitar el CRUD sin sesión (`/api/auth/dev/usuarios` y `/dev/usuarios`) antes de exponer la aplicación.
- Los errores no controlados (CUU-018 \*.a) se registran solo en consola, no en la base.
- Usuarios heredados con `activo='1'` y roles `ADMIN`/`VENTAS`/`AUDITOR` no pueden ingresar.
- Cambiar la contraseña de `APPusr` (es débil y se compartió en el chat) y verificar que `JWT_SECRET` tenga al menos 32 caracteres.
- Definición de terminado: faltan criterios de aceptación escritos, integración continua y revisión de código.
- Siguiente en el roadmap (fase 1, hito 06/11): CUU-005 Plan de Cuentas, CUU-007 Clientes y CUU-008 Proveedores.

**20:51** — Segundo factor por correo integrado a `main` (`ebc5eb8`, PR #4). Cuenta de Google creada para el envío.

## 2026-11-05

**20:30** — CUU-005 Gestionar Plan de Cuentas (rama `feature/cuu005-plan-cuentas`, sin commit).
- Alta, modificación, consulta y baja lógica de cuentas, con reactivación.
- Jerarquía: el código de una subcuenta empieza con el del padre, hereda su tipo, y solo los rubros (no imputables) pueden tener subcuentas.
- Tipos Activo, Pasivo, Patrimonio neto, Ingresos y Gastos; naturaleza deudora o acreedora, obligatoria en cuentas imputables.
- Códigos duplicados rechazados, incluidos los de cuentas dadas de baja.
- No se puede dar de baja una cuenta con movimientos, con subcuentas activas o configurada como predeterminada.
- Alta y modificación en dos pasos: el sistema valida y muestra los datos antes de confirmar (pasos 4-5).
- Consulta con ubicación en la jerarquía y movimientos de la cuenta (2.c).
- Cuentas predeterminadas para los asientos automáticos: ventas, deudores por ventas, IVA débito, compras, proveedores, IVA crédito y resultado del ejercicio.
- Modifican Contador y Administrador; los demás perfiles solo consultan. Todo queda auditado.
- Migración 003 (`naturaleza`, índice único de código, `CUENTA_PREDETERMINADA`), pendiente de aplicar.
- La IP bloqueada por el firewall de Azure (error 40615) ahora se informa con un mensaje claro.

**20:46** — Plan de Cuentas adaptado a los datos existentes (23 cuentas, 23 movimientos).
- Se usan las convenciones que ya tiene la base: `imputable`/`activo` = `'1'`/`'0'` y tipos `INGRESOS`/`GASTOS`. No se modifica ninguna fila.
- Las reglas de jerarquía se validan en las altas y cuando cambia el código, el padre o el tipo; las cuentas heredadas que no las cumplen pueden seguir editándose.
- Inconsistencias heredadas detectadas: 1.1.1 Caja y Bancos es imputable, tiene movimientos y subcuentas; 2.1.2.02 IVA Crédito Fiscal está bajo 1.1.2 con código del Pasivo (se puede corregir desde la pantalla).

**20:57** — Script de datos de prueba `db/datos_prueba.sql` (fuera del repositorio, como las migraciones).
- Vacía todas las tablas y carga datos consistentes: 6 usuarios (uno por perfil, uno con contraseña temporal y uno dado de baja), empresa emisora, 5 clientes, 4 proveedores, 6 productos, Plan de Cuentas de 70 cuentas, 7 cuentas predeterminadas, 3 ventas, 3 compras y 10 asientos.
- Totales de comprobantes y partida doble verificados por `db/generar_datos_prueba.py`, que regenera el script.

**21:10** — Coherencia de las cuentas predeterminadas (rama `feature/cuu005-plan-cuentas`, sin commit).
- Cada uso exige un tipo y una naturaleza: Ventas → Ingresos/acreedora; Deudores por ventas e IVA crédito → Activo/deudora; IVA débito y Proveedores → Pasivo/acreedora; Compras → Activo o Gastos/deudora; Resultado del ejercicio → Patrimonio neto.
- Una cuenta predeterminada no puede editarse para quedar incoherente ni dejar de ser imputable.
- La pantalla muestra el requisito de cada uso y ofrece solo las cuentas que lo cumplen. Verificado contra los datos de prueba: las 7 asignaciones son coherentes.

**21:12** — Commit `028afbe` de CUU-005 subido a `origin/feature/cuu005-plan-cuentas`; pull request contra `main` pendiente de revisión.

## 2026-11-06

**19:34** — CUU-007 Gestionar Clientes (rama `feature/cuu007-clientes`, sin commit). PR #5 (CUU-005) ya integrado a `main`.
- Alta por CUIT: se valida el dígito verificador, se consulta el padrón de ARCA (simulador desacoplado con respuestas fijas) y se detectan duplicados, incluidos clientes dados de baja.
- Código de cliente derivado del id (CLI-000001), sin columna nueva.
- Modificación con auditoría; el CUIT solo cambia si el cliente no tiene comprobantes.
- Consulta con historial de ventas e indicador de comprobantes pendientes.
- Baja bloqueada si hay ventas sin CAE o sin asiento asentado; reactivación.
- Modifican Contador y Administrativo (actores del caso de uso); el resto solo consulta. CUIT obligatorio para todos.
- Migración 004 (índice único de CUIT en `CLIENTE`), pendiente de aplicar.
- Bug detectado al verificar contra la base: SQL Server no admite `EXISTS` como columna; las pruebas con SQLite no lo detectaban.

**20:03** — CUU-008 Gestionar Proveedores (misma rama, sin commit).
- Mismo criterio que clientes: alta por CUIT con padrón simulado y control de duplicados, código PRV-000001, modificación auditada, consulta con historial de compras, baja lógica y reactivación. Modifican Contador y Administrativo.
- Pendiente de procesamiento = compra sin asiento asentado (COMPRA no tiene CAE).
- Formulario y tipos de datos compartidos entre clientes y proveedores.
- Migración 005 (índice único de CUIT en `PROVEEDOR`), pendiente de aplicar.
- Verificado contra la base: listado, búsqueda por CUIT, historial, reglas de baja y duplicado detectado por el padrón.

**20:18** — CUU-007 integrado a `main` (`1751c90`, PR #6). El trabajo de CUU-008 pasa a la rama `feature/cuu008-proveedores`, sin commit, e incluye el formulario compartido entre clientes y proveedores.
- Regla agregada a `CLAUDE.md`: las bajas son siempre lógicas, nunca se borran filas.

**20:31** — Commit `dba6c3a` de CUU-008 subido a `origin/feature/cuu008-proveedores`; pull request contra `main` pendiente de revisión.

## 2026-11-10

**12:16** — CUU-001 Registrar venta: se decide hacer antes el núcleo contable (CUU-003/004), respetando el roadmap. Quedan definidas para CUU-001: carga manual, solo importes de cabecera y cuenta del Debe según la condición de cobro (Caja, Deudores por ventas o Banco). CUU-008 ya integrado a `main` (PR #7).

**12:25** — CUU-003 Gestionar Libro Diario y CUU-004 Registrar asiento manual (rama `feature/cuu003-004-libro-diario`, sin commit).
- Motor de asientos compartido (lo usarán ventas y compras): partida doble, cuentas vigentes e imputables, importe en Debe o Haber por línea, numeración correlativa al contabilizar.
- Estados: pendiente (borrador, sin número ni efecto contable), vigente (asentado) y anulado.
- Sin edición destructiva: anular un asiento vigente genera un contra-asiento con Debe y Haber invertidos; modificarlo lo revierte y crea uno nuevo. Los borradores se descartan o reemplazan. Ninguna fila se borra.
- Los asientos de ventas y compras no se modifican ni anulan desde el Libro Diario.
- Libro Diario con filtros por período, cuenta, tipo y estado; detalle de cada asiento; carga manual con totales y diferencia en vivo y confirmación previa.
- Registran Contador y Administrativo; el resto solo consulta. Todo auditado.
- Migración 006 (`referencia`, `id_asiento_revertido`, índice único de número), pendiente de aplicar. **Aplicarla antes de integrar la rama**: sin ella también falla la consulta de movimientos del Plan de Cuentas.

**13:43** — Migración 006 aplicada y verificada (columnas, índice único y FK). Libro Diario verificado en solo lectura contra la base real: 10 asientos balanceados, filtros por cuenta, período, tipo y estado y movimientos del Plan de Cuentas funcionando. Los datos de prueba numeraban el borrador (N° 10); se corrige el generador para que los borradores queden sin número.

**13:44** — Commit `bdf06b6` y push de `feature/cuu003-004-libro-diario`; PR a `main` pendiente de aprobación. Siguiente: CUU-001 Registrar venta.

**14:05** — CUU-003/004 integrado a `main` (PR #8). CUU-001 Registrar venta (rama `feature/cuu001-registrar-venta`, sin commit).
- Carga manual del comprobante: cliente vigente (o alta de cliente nuevo desde la venta), Factura A/B/C, punto de venta, número, fecha de emisión, fecha contable, condición de cobro, neto, IVA, otros impuestos y total, en pesos.
- Asiento propuesto antes de confirmar: Debe según condición de cobro (Contado → Caja, Cuenta Corriente → Deudores por ventas, Transferencia → Banco); Haber Ventas, IVA débito fiscal y Otros impuestos de ventas. Nuevas claves predeterminadas CAJA, BANCO y OTROS_IMPUESTOS_VENTAS.
- Duplicados (mismo emisor, tipo, punto de venta y número, no anulada), cuenta no determinada (el usuario la elige o la configura), total que no coincide (solo se guarda pendiente).
- Estados de la venta: pendiente (sin asiento), contabilizada y anulada. Solo se modifica una pendiente; anular una contabilizada revierte su asiento; con CAE no se anula (nota de crédito).
- Validaciones fiscales mínimas: Factura C sin IVA; emisor RI emite A/B, Monotributo/Exento emite C.
- Navegación comprobante ↔ asiento (detalle de la venta y enlace desde el Libro Diario).
- Migración 007 (`fecha_contable`, `importe_otros_impuestos`, `estado` e índice del comprobante), **pendiente de aplicar**. Datos de prueba actualizados (requieren la 007).
- 32 pruebas nuevas; suite completa 217 OK; lint y build OK.

**14:32** — Migración 007 aplicada y verificada en solo lectura contra la base real: columnas e índice creados, las 3 ventas quedaron contabilizadas con su asiento, filtros y búsqueda por número y cliente funcionando, propuesta de asiento balanceada y duplicado detectado. Faltan asignar CAJA, BANCO y OTROS_IMPUESTOS_VENTAS (o volver a correr los datos de prueba).

**14:34** — Datos de prueba recargados: 10 cuentas predeterminadas (CAJA, BANCO y OTROS_IMPUESTOS_VENTAS asignadas), venta 3 por transferencia y borrador sin número. Verificado en solo lectura.

**14:35** — Commit `f76de8d` y push de `feature/cuu001-registrar-venta`; PR a `main` pendiente de aprobación. Siguiente sugerido: CUU-006 Libro Mayor (cierra la Fase 2), luego CUU-002.

**14:40** — CUU-001 integrado a `main` (PR #9). CUU-006 Consultar Libro Mayor (rama `feature/cuu006-libro-mayor`, sin commit).
- El Mayor se calcula desde los asientos contabilizados (con número), sin tabla propia: la tabla LIBRO_MAYOR del esquema base queda sin uso. No requiere migración.
- Cuenta imputable o rubro (reúne sus cuentas imputables; omite las que no tienen saldo ni movimientos). Período desde/hasta.
- Saldo inicial acumulado, Debe, Haber, saldo después de cada movimiento y saldo final (D/A). Incluye asientos anulados y sus contra-asientos; los borradores no impactan. 2.a: sin movimientos informa el saldo arrastrado.
- Enlace al comprobante de venta desde el movimiento y a la cuenta desde el Plan de Cuentas.
- Verificado en solo lectura contra la base real: Banco cierra en 9.479.700, la suma de saldos de todas las cuentas da 0.
- Datos de prueba: la venta 2 pasa a Cuenta Corriente (su asiento debita Deudores por ventas y no se cobró).
- 12 pruebas nuevas; suite completa 229 OK; lint y build OK.

**14:43** — Commit `34b18df` en `feature/cuu006-libro-mayor` (sin push: lo sube el usuario). Siguiente: CUU-002 Registrar compra.

**14:45** — CUU-006 integrado a `main` (PR #10). CI con GitHub Actions (rama `ci/pruebas-automaticas`, commit sin push): en cada PR a main y push a main corre lint, formato y pytest del backend y build del frontend. Simulado localmente sin `.env`: 229 OK. Pendiente: proteger `main` exigiendo que pase el CI.

**17:55** — CI integrado a `main` (PR #11). CUU-002 Registrar compra (rama `feature/cuu002-registrar-compra`, sin commit).
- Mismo diseño que CUU-001: carga manual, asiento propuesto, duplicados (por proveedor, tipo, punto de venta y número), cuentas elegibles si faltan, total que no coincide (solo pendiente), estados pendiente/contabilizada/anulada y reversión al anular.
- Asiento: Debe Compras (neto), IVA crédito fiscal y Otros impuestos de compras; Haber según condición de pago (Contado → Caja, Cuenta Corriente → Proveedores, Transferencia → Banco). Nueva clave OTROS_IMPUESTOS_COMPRAS (Activo).
- Fiscal mínimo: solo la Factura A discrimina IVA; proveedor RI emite A/B, Monotributo/Exento emite C.
- Alta de proveedor desde la compra; enlaces al comprobante desde Libro Diario y Libro Mayor; una compra anulada ya no bloquea la baja del proveedor.
- Refactor: módulo común de comprobantes (asiento propuesto, selección de cuentas, búsqueda por número) usado por ventas y compras.
- Migración 008 (`fecha_contable`, `importe_otros_impuestos`, `estado` e índice del comprobante en COMPRA), **pendiente de aplicar**. Datos de prueba actualizados (requieren la 008): compras con condición coherente con su asiento.
- 30 pruebas nuevas; suite completa 259 OK; lint y build OK.

**18:00** — Migración 008 y datos de prueba aplicados y verificados en solo lectura contra la base real: columnas e índice creados, las 3 compras contabilizadas con su asiento y condición coherente, búsqueda y duplicado funcionando, 11 cuentas predeterminadas asignadas, suma de saldos 0.

## 2026-11-13

**21:53** — Nuevo logo de EugenIA en la pantalla de login (`6bc002c`, rama `feature/logo-login`).

**22:30** — Correos de códigos de verificación en HTML (`a6d69b5` y `0af6e76`, rama `feature/mail-html`).
- Inicio de sesión, recupero y cambio de contraseña salen como multipart: texto plano de respaldo y versión HTML.
- Plantilla maquetada con tablas y estilos en línea (compatible con Gmail y Outlook): encabezado EugenIA, código en recuadro, vencimiento y pie automático. Todo lo interpolado se escapa.
- Pruebas unitarias de la plantilla.

## 2026-11-14

**15:50** — Logo y correo HTML integrados a `main` (PR #13 y #14).

**15:50** — CUU-016 Registrar comprobante con OCR/NLP (`74915e6`, rama `feature/cuu016-ocr-comprobantes`). Adelanta la Fase 4 (hito 27/11).
- Carga de PDF, PNG o JPG para compra o venta, con tamaño máximo configurable (`COMPROBANTE_MAX_MB`). El original se guarda en `backend/almacenamiento/` (fuera del repositorio) con su hash SHA-256; un archivo ya cargado y no descartado se rechaza como duplicado.
- Lectura: PDF digital con `pypdf`; imágenes y PDF escaneados con Tesseract (opcional, `TESSERACT_CMD`). Sin Tesseract, los campos se completan a mano.
- Intérprete por patrones: CUIT, razón social, tipo, punto de venta, número, fecha, neto, IVA y total, cada uno con su confianza (la del patrón por la del OCR). Validaciones de coherencia (dígito verificador del CUIT, neto + IVA = total, fecha).
- Revisión obligatoria de los campos con confianza menor a `OCR_UMBRAL_CONFIANZA` (0,8) o con validaciones en error; sugerencia de proveedor o cliente por CUIT.
- Se guardan el valor extraído, el definitivo y las marcas corregido y revisado de cada campo (`DOCUMENTO_CAMPO`).
- Al registrar se crea la compra o venta en la misma transacción que el documento, usando los servicios de CUU-001/002 (nuevo parámetro `confirmar_transaccion`). El OCR nunca contabiliza sin la confirmación del usuario.
- Estados del documento: pendiente de revisión, registrado y descartado (baja lógica). Todo auditado.
- Pantallas de carga, listado, revisión con vista del archivo y detalle; enlace al documento desde el detalle de la compra o la venta.
- Migración 009 (`DOCUMENTO` y `DOCUMENTO_CAMPO`). Dependencias nuevas: `python-multipart`, `pypdf`, `pytesseract` y `Pillow`.
- 28 pruebas nuevas (documentos e intérprete).

**16:31** — CUU-016 integrado a `main` (PR #15).

## 2026-11-19

**11:54** — El logout invalida el token JWT (rama `fix/logout-invalida-token`, sin commit). Resuelve el pendiente del 03/11.
- Cada token lleva un identificador único (`jti`). Al cerrar sesión se registra en `SESION_REVOCADA` y la autenticación lo rechaza aunque no haya vencido ("La sesión fue cerrada").
- Solo se cierra la sesión actual: las de otros dispositivos del mismo usuario siguen vigentes.
- Se guarda el `jti`, nunca el token. Los tokens emitidos antes del cambio (sin `jti`) dejan de aceptarse: hay que volver a iniciar sesión una vez.
- Las filas de `SESION_REVOCADA` no se borran. Si la tabla crece, se podrían depurar las que ya vencieron (`expira`), porque esos tokens se rechazan igual.
- Migración 010 (`db/010_sesiones_revocadas.sql`), **pendiente de aplicar antes de integrar la rama**: sin ella falla toda request autenticada. Si `APPusr` tiene permisos por tabla, otorgarle SELECT e INSERT.
- 5 pruebas nuevas; suite completa 301 OK; lint y formato OK.
- Bitácora completada con lo del 13 y 14/11.

### Pendientes al cierre

- Aplicar la migración 010, hacer commit y abrir el PR de `fix/logout-invalida-token`.
- Siguen abiertos del 03/11: quitar el CRUD sin sesión (`/api/auth/dev/usuarios`), cambiar la contraseña de `APPusr` y proteger `main` exigiendo que pase el CI.
- Siguiente en el roadmap (Fase 5, hito 04/12): CUU-017 Validar comprobante con ARCA, CUU-022 Consultar estado del comprobante y CUU-013 Consultar historial de auditoría.

**12:31** — Logout integrado a `main` (PR #16). CUU-016: lectura de facturas preimpresas (rama `fix/ocr-pdf-por-posicion`, sin commit).
- Prueba con una factura real (NURIA, PDF digital, guardada fuera del repositorio en `pf/`): los caracteres especiales (ñ, ú, º) se leían bien, pero el PDF ubica cada carácter en su propio bloque de texto y la extracción devolvía un carácter por renglón, así que no se reconocía ningún campo.
- Motor: si el texto sale fragmentado, se rearman los renglones según la posición de cada carácter (con pypdf, sin dependencias nuevas). Los PDF que ya se leían bien, como los de ARCA, siguen por el mismo camino.
- Intérprete: fecha con rótulo "Fecha:" y año de dos dígitos; se ignoran las fechas de inicio de actividades y de vencimiento; TOTAL sin tomar SUB-TOTAL; IVA con alícuota sin "%" toma el importe; sin "Neto Gravado" se usa el último SUB-TOTAL (confianza 0,7, queda para revisar).
- Resultado con la factura real: 9 de 10 campos correctos y la aritmética cierra. La razón social del emisor no está en el texto (es el logo): queda para completar a mano. Neto, total, punto de venta y número quedan con confianza menor a 0,8, así que la revisión es obligatoria.
- Pruebas con un PDF sintético que imita esa plantilla (datos ficticios). 12 pruebas nuevas; suite completa 313 OK; lint y formato OK.

**12:54** — CUU-016: análisis de cuatro facturas electrónicas reales (misma rama, sin commit). Las cuatro son Factura B a consumidor final, de cuatro generadores distintos (TCPDF, JasperReports, iText y Crystal Reports) y guardadas fuera del repositorio en `pf/`. Los caracteres se leían bien; los problemas eran de interpretación.
- Fecha: `Fecha Emisión:` sin "de" se reconoce como fecha de emisión.
- Se quitan las etiquetas HTML que algunos generadores dejan como texto (`<b>Razón social:</b>`).
- El IVA nunca toma una alícuota (`IVA 10.5%`): sin importe al lado, queda vacío.
- Punto de venta y número juntos detrás de `Comp. Nro`, `FACTURA:` o `Nº` (confianza 0,9).
- Facturas B y C, con las mismas reglas que CUU-001/002. Compra B o C y venta C: IVA 0 y neto igual al total. Venta B: el IVA es el "IVA Contenido" de la Ley 27.743 y el neto, el total menos ese IVA; sin ese dato, quedan vacíos para completar. El intérprete recibe la operación del documento. Las confianzas derivadas no superan la del tipo ni la del total.
- No se fuerza: razón social sin rótulo, tipo con letra y código separados, rótulos e importes en columnas distintas. Quedan para la revisión obligatoria.
- 17 pruebas nuevas con datos ficticios; suite completa 330 OK; lint y formato OK.

**14:19** — CUU-016: factura modelo de la empresa piloto (Agro Arroyo Insumos SRL, FAC 00003-00012698, guardada fuera del repositorio en `pf/`) y comprobantes en moneda extranjera (misma rama, sin commit).
- La factura la genera Microsoft Print to PDF, que separa rótulos e importes; además está **en dólares** (cotización 1.545,50). El sistema solo registraba en pesos: el OCR habría tomado los dólares como pesos.
- Motor: la lectura por posición pasa a ser la predeterminada para todos los PDF (la estándar queda como respaldo si no hay posiciones). Comparada en las seis facturas reales, iguala o mejora todos los campos.
- Intérprete: importes con prefijo `u$s`/`US$`/`USD`/`€`; el IVA genérico no salta de renglón (el encabezado "IVA" de la tabla tomaba el código de producto); se quita el código de cliente delante de la razón social (`00701 - ...`).
- Moneda (decisión: convertir a pesos). Nuevos campos del documento `moneda` (ARS, USD o EUR) y `cotizacion`, sin migración (son filas de `DOCUMENTO_CAMPO`). Sin indicación se asume pesos con cotización 1. En moneda extranjera sin cotización hay una validación de error.
- Registro: el documento conserva los importes en la moneda original (extraídos y finales); la compra o venta se crea en pesos (cada importe por la cotización, redondeado al centavo; si las partes suman el total, el total en pesos es la suma convertida) y guarda `moneda` y `cotizacion` en sus columnas existentes. El asiento queda en pesos. Auditado con moneda, cotización e importes en pesos. Verificado: 34.088,12 USD × 1.545,5 = 52.683.189,46, el total en pesos que declara la factura.
- Frontend: selector de moneda y cotización en la revisión, con la equivalencia en pesos; total del listado con su moneda; moneda y cotización en el detalle de compras y ventas.
- Resultado con la factura modelo: los 12 campos correctos, ninguno para revisar.
- 19 pruebas nuevas (factura sintética en dólares con datos ficticios, detección de moneda, conversión y redondeo); suite completa 349 OK; lint, formato y build del frontend OK.
- Pendiente: la carga manual de CUU-001/002 sigue solo en pesos (la moneda extranjera entra únicamente por OCR).

## 2026-11-20

**10:12** — CUU-016: rama `fix/ocr-pdf-por-posicion` con commit (`cffd58f`) y publicada. Tesseract 5.4 instalado localmente con idioma español (ruta en `TESSERACT_CMD` del `.env`).
- Primera prueba de OCR sobre imagen: foto JPEG de una factura de compra al exterior (vendedor en China, en inglés y en USD), guardada fuera del repositorio en `pf/`.
- Tesseract: confianza promedio 0,86; acentos y caracteres especiales correctos. Errores menores, propios de la foto (`!` por `I`, `+` por `#`, `0`/`O` e `I`/`1` en el SKU), en ningún campo relevante.
- Intérprete: reconoce solo la moneda (USD, para revisar). No reconoce total, fecha, número ni tipo, porque no es un comprobante argentino (rótulos "Order Date" y "TOTAL FOB", sin CUIT del emisor ni tipo A/B/C). Se completa a mano en la revisión. No se adapta el intérprete: una importación se registra distinto (despacho, IVA de importación) y está fuera del alcance.
- **Limitación conocida (CUIT del receptor):** el intérprete tomó como CUIT el CUIL del comprador ("Bill To") con confianza 0,81, por encima del umbral, así que no se marca para revisión obligatoria. Solo descarta el CUIT de la empresa: si la factura está a nombre de otra persona o el CUIT de la empresa no está configurado, el del receptor puede pasar como el del proveedor.
  - Impacto bajo: el CUIT y la razón social definitivos salen de la contraparte que elige el usuario (`id_contraparte`). El extraído solo sugiere el proveedor, así que no genera un asiento erróneo inadvertido (R-02).
  - Arreglo posible si hiciera falta: bajar la confianza por debajo del umbral cuando el número tiene el rótulo "CUIL" o está en el bloque del receptor ("Bill To", "Señor/es", "Cliente").
  - Decisión: no se corrige ahora; queda para el registro de limitaciones de la Fase 7.

**12:01** — CUU-016: PDF con las letras dibujadas como trazos y moneda mal detectada (rama `fix/ocr-moneda-y-pdf-vectorial`, sin commit).
- Prueba con una factura real de FIX SCR (FCE MiPyME A 00005-00002846, guardada fuera del repositorio en `pf/`). No está escaneada: se imprimió a PDF desde un escritorio remoto (Acrobat Distiller). El formulario preimpreso es una imagen de fondo de baja resolución y los datos están encima como trazos vectoriales, sin caracteres de texto. pypdf no encontraba texto y Tesseract solo recibía las imágenes de fondo (el formulario vacío): no se reconocía ningún campo.
- Motor: un PDF sin texto se renderiza página por página a 300 dpi en escala de grises y se reconoce con Tesseract, igual que una imagen. Antes se reconocían las imágenes incrustadas, que pierden lo dibujado encima. Nueva dependencia **pypdfium2 5.15.2** (licencia BSD-3/Apache-2.0, trae PDFium incluido, sin instalar nada en el servidor). PyMuPDF quedó descartado por su licencia AGPL.
- Intérprete: un `u$s`/`US$`/`USD` sin rótulo de moneda solo define USD si precede a un importe rotulado (total, neto o subtotal) en el mismo renglón. Antes, una mención en la descripción ("u$s 8.975,75 TC divisa 1.516") convertía en dólares una factura en pesos.
- Resultado con FIX SCR: punto de venta, número y fecha correctos; moneda en pesos. Todos con confianza entre 0,4 y 0,65, así que la revisión es obligatoria. No reconoce:
  - neto, IVA y total: los rótulos están en el fondo, lejos de los importes;
  - tipo: FCE MiPyME no está entre los admitidos y no se agrega, porque tiene su propio régimen;
  - CUIT del emisor: en el fondo a 72 dpi queda ilegible. Toma el del receptor (John Deere CF), es decir, la limitación anotada a las 10:12, ahora con una factura argentina real.
- Regresión: las otras seis facturas reales dan exactamente los mismos campos que en `main`.
- 4 pruebas nuevas (página renderizada con el trazo visible a 300 dpi y casos de moneda); suite completa 353 OK; lint y formato OK.
- Para instalar: `pip install -r requirements.txt` en cada entorno (incluido el CI, que ya lo hace).

**15:54** — Pendientes de seguridad del 03/11 resueltos por decisión:
- `/api/auth/dev/usuarios` (CRUD de usuarios sin sesión) se mantiene hasta el paso a producción; recién ahí se quita.
- La contraseña de `APPusr` queda como está.
- `main` está protegida en GitHub: no se puede hacer merge hasta que pasen los checks de frontend y backend.
- Siguiente: Fase 5, empezando por CUU-017 Validar comprobante con ARCA.

## 2026-11-21

**10:01** — CUU-017 Validar comprobante con ARCA (rama `feature/cuu017-validar-arca`, sin commit).
- Decisiones (20/11): se validan **compras y ventas**; la validación **no bloquea la contabilización**, solo avisa.
- **Migración 011** (`db/011_validacion_arca.sql`, **pendiente de aplicar antes de integrar**: sin ella fallan las consultas de compras y ventas). Agrega:
  - en COMPRA: `cae` y `cae_vencimiento`;
  - en VENTA: `cae_vencimiento`;
  - en ambas: `estado_fiscal` (por defecto PENDIENTE, también en las filas existentes);
  - la tabla `VALIDACION_ARCA` con el historial de intentos (datos enviados, respuesta, diferencias, usuario y fechas).
  - Si `APPusr` tiene permisos por tabla, otorgarle SELECT, INSERT y UPDATE sobre `VALIDACION_ARCA`.
- **Adaptador** `app/arca/comprobantes.py`, desacoplado de la lógica contable. Sigue el contrato del servicio de constatación de comprobantes de ARCA: CUIT del emisor, tipo (código ARCA), punto de venta, número, fecha, total y CAE.
  - Solo existe `ArcaSimulado`. Con cualquier CAE informa el comprobante tal como se envió, con el CAE vigente por 10 días.
  - CAE de prueba para los caminos alternativos:
    - `99999999999900`: ARCA no responde;
    - `...01`: el comprobante no existe;
    - `...02`: CAE vencido;
    - `...03`: total distinto;
    - `...04`: error del servicio.
- **Estados fiscales:**
  - Pendiente;
  - En validación;
  - Válido;
  - No válido (4.a);
  - Observado (5.a: el CAE vencía antes de la fecha de emisión);
  - Pendiente de auditoría (6.a: los datos difieren, con la lista de diferencias);
  - Error de integración (3.a: queda pendiente y se puede reintentar).
- **Reintento controlado:**
  - el intento se guarda EN_VALIDACION antes de consultar a ARCA, así queda en el historial aunque no haya respuesta;
  - no se lanza una segunda consulta mientras otra está en curso;
  - una consulta sin respuesta por más de 120 s (`ARCA_VALIDACION_VENCIDA_SEGUNDOS`) se da por interrumpida.
- **Auditoría:** acción `VALIDACION_ARCA` con el estado anterior y el nuevo.
- **Modificaciones:** al modificar una compra o venta, el estado fiscal vuelve a pendiente solo si cambian datos fiscales (contraparte, tipo, número, fecha, total, CAE o su vencimiento). Así, contabilizar desde la revisión del asiento no pierde la validación.
- **Endpoints:**
  - `POST /api/compras|ventas/{id}/validar-arca`: solo contador y administrativo.
  - `GET .../validaciones`: historial, para cualquier usuario con sesión. Es la base de CUU-022.
- **OCR:** nuevos campos `cae` y `cae_vencimiento`, que pasan a la compra o venta al registrar.
  - Con el rótulo al lado, la confianza es 0,95.
  - Con rótulo y número separados se toma el único número suelto de 14 dígitos, con confianza 0,6, así que queda para revisar.
  - Facturas reales: se obtiene el CAE en 6 de 6 (FAC no se probó porque se movió a `facturas aa/`) y el vencimiento en 5. En FIX SCR el OCR parte la palabra "VENCIMIENTO".
- **Frontend:**
  - CAE y vencimiento en los formularios de compra y venta y en la revisión del OCR;
  - sección "Validación con ARCA" en el detalle (estado, botón, resultado con diferencias e historial);
  - columna ARCA en los listados;
  - aviso al contabilizar un comprobante no validado.
- **Pruebas:** 31 nuevas (22 de validación y 9 de OCR del CAE). Suite completa: 384 OK; lint, formato y build del frontend OK.
