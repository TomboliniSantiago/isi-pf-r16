# EugenIA: alcance funcional del 70% y roadmap de implementación

## 1. Objetivo

El objetivo es alcanzar al **18 de diciembre de 2026** una versión integrada y demostrable de EugenIA que cubra aproximadamente el **70% del alcance funcional previsto**.

El porcentaje no se medirá únicamente por cantidad de pantallas o casos de uso. La prioridad será completar un **circuito contable vertical de punta a punta**, incluyendo una primera implementación funcional de OCR, validación con ARCA, auditoría y visualización financiera.

El documento funcional del proyecto define **23 casos de uso**. Al completar 16 casos se alcanza aproximadamente un **69.6% por cantidad**, pero el criterio principal será que esos casos formen un sistema coherente, persistente, verificable y demostrable.

---

# 2. Alcance recomendado para el 70%

## 2.1 Seguridad y administración básica

### Casos de uso incluidos

- **CUU-015: Iniciar sesión**
- **CUU-018: ABM de usuarios**

### Funcionalidad mínima

- Inicio y cierre de sesión.
- Alta, modificación, consulta y baja lógica de usuarios.
- Roles mínimos:
  - Administrador.
  - Contador.
  - Administrativo.
  - Consulta.
- Protección de rutas y endpoints.
- Contraseñas almacenadas con hash seguro.
- Auditoría de accesos y operaciones críticas.

### Fuera de esta etapa

- Inicio de sesión con proveedores externos.
- Segundo factor de autenticación.
- Recuperación avanzada de cuenta.
- Permisos configurables con granularidad extrema.

---

## 2.2 Parametrización contable

### Caso de uso incluido

- **CUU-005: Gestionar Plan de Cuentas**

### Funcionalidad mínima

- Alta, modificación, consulta y baja lógica de cuentas.
- Jerarquía del plan de cuentas.
- Clasificación en Activo, Pasivo, Patrimonio Neto, Ingresos y Gastos.
- Validación de códigos duplicados.
- Restricción para impedir la eliminación de cuentas con movimientos.
- Definición de cuentas predeterminadas para ventas, compras, IVA y resultados.

Esta funcionalidad es estructural: sin un plan de cuentas válido no existe un sistema contable integrado.

---

## 2.3 Entidades comerciales

### Casos de uso incluidos

- **CUU-007: Gestionar Clientes**
- **CUU-008: Gestionar Proveedores**

### Funcionalidad mínima

- Alta, modificación, consulta y baja lógica.
- CUIT.
- Razón social.
- Condición frente al IVA.
- Domicilio.
- Estado activo o inactivo.
- Búsqueda y filtros.
- Asociación con comprobantes.

### Fuera de esta etapa

- Importación masiva avanzada.
- Scoring de clientes o proveedores.
- Cuentas corrientes completas.
- Conciliación automática.

---

## 2.4 Circuito de ventas y compras

### Casos de uso incluidos

- **CUU-001: Registrar venta**
- **CUU-002: Registrar compra**

### Funcionalidad mínima

- Asociación con cliente o proveedor.
- Tipo y número de comprobante.
- Punto de venta.
- Fecha de emisión.
- Fecha contable.
- Neto gravado.
- IVA.
- Otros impuestos.
- Total.
- Moneda.
- Estado del comprobante.
- Generación del asiento contable correspondiente.
- Validación de partida doble.

### Flujo integral esperado

1. El usuario selecciona o crea el cliente o proveedor.
2. Registra el comprobante.
3. El sistema valida datos e importes.
4. Se genera el asiento contable.
5. El asiento aparece en el Libro Diario.
6. Los movimientos actualizan el Libro Mayor.
7. Los datos impactan en el Balance General y el Estado de Resultados.
8. El usuario puede consultar el estado y la trazabilidad del comprobante.

---

## 2.5 Núcleo contable

### Casos de uso incluidos

- **CUU-003: Gestionar Libro Diario**
- **CUU-004: Registrar asiento manual**
- **CUU-006: Consultar Libro Mayor**

### Funcionalidad mínima

- Validación de que el total del Debe sea igual al total del Haber.
- Numeración de asientos.
- Fecha contable.
- Concepto, origen y referencia.
- Asientos automáticos originados por compras y ventas.
- Asientos manuales.
- Consulta por cuenta, fecha, tipo y origen.
- Cálculo de saldo inicial, Debe, Haber y saldo final.
- Anulación o reversión controlada.
- Prohibición de eliminar libremente asientos contabilizados.

Para esta etapa se recomienda implementar reversión contable en lugar de edición destructiva de asientos confirmados.

---

## 2.6 Estados contables principales

### Casos de uso incluidos

- **CUU-009: Generar Balance General**
- **CUU-010: Generar Estado de Resultados**

### Funcionalidad mínima

- Selección de período.
- Subtotales por rubro.
- Total de Activo, Pasivo y Patrimonio Neto.
- Validación de la ecuación patrimonial.
- Ingresos, costos y gastos.
- Resultado del ejercicio.
- Navegación desde un total hacia las cuentas que lo componen.
- Comparación básica con otro período, si hay datos suficientes.

---

## 2.7 Registro de comprobantes mediante OCR/NLP

### Caso de uso incluido

- **CUU-016: Registrar comprobante con OCR/NLP**

### Funcionalidad mínima

- Carga de archivos PDF, PNG o JPG.
- Almacenamiento del archivo original.
- Extracción de:
  - CUIT.
  - Razón social.
  - Tipo de comprobante.
  - Punto de venta.
  - Número.
  - Fecha.
  - Neto.
  - IVA.
  - Total.
- Presentación de los datos extraídos para revisión.
- Indicador de confianza o advertencia en campos dudosos.
- Corrección manual antes de confirmar.
- Conservación del valor extraído y del valor corregido.
- Creación de un borrador de compra o venta.

### Flujo esperado

> Cargar comprobante → extraer datos → revisar → corregir → registrar → generar asiento.

El OCR no contabilizará directamente sin confirmación humana.

---

## 2.8 Integración mínima con ARCA

### Casos de uso incluidos

- **CUU-017: Validar comprobante con ARCA**
- **CUU-022: Consultar estado de comprobante**

### Funcionalidad mínima

- Adaptador de ARCA separado de la lógica contable.
- Envío o consulta de los datos requeridos para validación.
- Estados mínimos:
  - Pendiente.
  - En validación.
  - Válido.
  - Inválido.
  - Error de integración.
- Registro de fecha, resultado y detalle de cada intento.
- Reintento controlado.
- Historial de validaciones.
- Simulador del servicio externo para desarrollo y demostraciones.

Si no se dispone de credenciales o un ambiente de prueba oficial, deberá quedar implementado el contrato del adaptador y un servicio simulado con respuestas repetibles.

---

## 2.9 Auditoría funcional

### Caso de uso incluido

- **CUU-013: Consultar Historial de Auditoría**

### Funcionalidad mínima

- Registro de:
  - Usuario.
  - Fecha y hora.
  - Acción.
  - Entidad afectada.
  - Identificador.
  - Valores principales anteriores y posteriores.
  - Origen de la operación.
- Filtros por fecha, usuario, entidad y acción.
- Auditoría de cambios sobre comprobantes, asientos, usuarios y plan de cuentas.

La auditoría deberá demostrar la trazabilidad entre extracción OCR, corrección humana, validación externa y contabilización.

---

## 2.10 Dashboard financiero mínimo viable

### Caso de uso incluido parcialmente

- **CUU-021: Consultar Dashboard Financiero**

### Funcionalidad mínima

- Ventas del período.
- Compras del período.
- Resultado estimado.
- IVA débito e IVA crédito.
- Comprobantes pendientes de validación.
- Comprobantes observados.
- Evolución mensual básica.
- Filtro por período.
- Acceso desde los indicadores hacia el detalle.

### Fuera de esta etapa

- Predicciones.
- Personalización de widgets.
- Indicadores configurables.
- Tableros múltiples por usuario.

---

# 3. Casos de uso incluidos, parciales y posteriores

## 3.1 Casos completos

1. **CUU-001:** Registrar venta.
2. **CUU-002:** Registrar compra.
3. **CUU-003:** Gestionar Libro Diario.
4. **CUU-004:** Registrar asiento manual.
5. **CUU-005:** Gestionar Plan de Cuentas.
6. **CUU-006:** Consultar Libro Mayor.
7. **CUU-007:** Gestionar Clientes.
8. **CUU-008:** Gestionar Proveedores.
9. **CUU-009:** Generar Balance General.
10. **CUU-010:** Generar Estado de Resultados.
11. **CUU-013:** Consultar Historial de Auditoría.
12. **CUU-015:** Iniciar sesión.
13. **CUU-016:** Registrar comprobante con OCR/NLP.
14. **CUU-017:** Validar comprobante con ARCA.
15. **CUU-018:** ABM de usuarios.
16. **CUU-022:** Consultar estado del comprobante.

Esto representa **16 de 23 casos de uso**, aproximadamente **69.6% por cantidad**.

## 3.2 Casos parciales

- **CUU-011:** Exportar Libro Diario.
  - Como máximo, exportación sencilla a CSV o Excel.
- **CUU-021:** Consultar Dashboard Financiero.
  - Indicadores y gráficos mínimos, sin personalización ni predicción.

## 3.3 Casos posteriores

- **CUU-012:** Exportar Libro Mayor.
- **CUU-014:** Exportar Libro IVA a ARCA.
- **CUU-019:** Gestionar Alertas de Auditoría.
- **CUU-020:** Generar Reportes Automáticos.
- **CUU-023:** Obtener Recomendaciones Financieras Inteligentes.

También se postergan:

- Conciliación automática.
- Predicciones financieras.
- Recomendaciones generativas productivas.
- Búsqueda contable conversacional.
- Clasificación automática sin confirmación.
- Procesamiento masivo.
- Multimoneda completa.
- Multiempresa.
- Cierres y reaperturas contables avanzadas.

---

# 4. Roadmap hasta el 18 de diciembre de 2026

## Supuestos de planificación

- Inicio del roadmap: **28 de octubre de 2026**.
- Fecha objetivo: **18 de diciembre de 2026**.
- Duración calendario: **52 días**.
- Modalidad: fases cortas con integración continua.
- Cada fase debe terminar con funcionalidades ejecutables, pruebas y una demostración interna.
- Las ramas de trabajo deben integrarse con frecuencia para evitar una integración masiva al final.

---

## Fase 0: Base técnica y definición de contratos

**Fechas:** 28 al 30 de octubre de 2026  
**Hito:** arquitectura ejecutable y equipo trabajando sobre una base común.

### Objetivos

- Consolidar alcance y criterios de aceptación.
- Definir arquitectura del frontend, backend y base de datos.
- Preparar repositorio, ramas, integración continua y ambientes.
- Definir convenciones de código y estrategia de pruebas.
- Definir contratos iniciales de OCR y ARCA.

### Entregables

- Estructura base del repositorio.
- Aplicación levantando localmente.
- Configuración segura de variables de entorno.
- Esquema inicial de base de datos.
- Pipeline de compilación, lint y pruebas.
- Datos semilla mínimos.
- Backlog priorizado por caso de uso.
- Documento de decisiones técnicas.

### Criterio de salida

Un desarrollador debe poder clonar el repositorio, configurar el entorno y ejecutar frontend, backend, base de datos y pruebas siguiendo instrucciones documentadas.

---

## Fase 1: Seguridad, usuarios y maestros

**Fechas:** 31 de octubre al 6 de noviembre de 2026  
**Casos de uso:** CUU-015, CUU-018, CUU-005, CUU-007 y CUU-008.  
**Hito:** sistema administrable con usuarios y datos maestros persistentes.

### Objetivos

- Implementar autenticación y autorización por roles.
- Implementar ABM de usuarios.
- Implementar Plan de Cuentas.
- Implementar clientes y proveedores.
- Establecer auditoría base para las entidades implementadas.

### Entregables

- Inicio y cierre de sesión.
- Protección de rutas y endpoints.
- Gestión de usuarios y roles.
- CRUD de cuentas contables con jerarquía y validaciones.
- CRUD de clientes y proveedores.
- Migraciones y datos semilla.
- Pruebas de autenticación, permisos y reglas de negocio.

### Criterio de salida

Un administrador puede crear usuarios; un contador puede iniciar sesión, configurar el plan de cuentas y administrar clientes y proveedores; un usuario sin permisos no puede ejecutar operaciones restringidas.

---

## Fase 2: Núcleo contable

**Fechas:** 7 al 13 de noviembre de 2026  
**Casos de uso:** CUU-003, CUU-004 y CUU-006.  
**Hito:** motor contable operativo y consistente.

### Objetivos

- Diseñar e implementar asientos y movimientos.
- Validar partida doble.
- Implementar Libro Diario.
- Implementar asientos manuales.
- Implementar Libro Mayor y cálculo de saldos.
- Incorporar reversión controlada.

### Entregables

- Modelo de asiento y detalle contable.
- Numeración y estados de asiento.
- Registro de asiento manual.
- Consulta del Libro Diario con filtros.
- Consulta del Libro Mayor.
- Cálculo de saldo inicial, Debe, Haber y saldo final.
- Reversión de asientos confirmados.
- Pruebas unitarias del motor contable.

### Criterio de salida

El sistema rechaza asientos desbalanceados y refleja correctamente los movimientos confirmados en el Libro Diario y el Libro Mayor.

---

## Fase 3: Ventas, compras e impacto contable

**Fechas:** 14 al 20 de noviembre de 2026  
**Casos de uso:** CUU-001 y CUU-002.  
**Hito:** circuito transaccional conectado con el núcleo contable.

### Objetivos

- Implementar registro de ventas.
- Implementar registro de compras.
- Calcular neto, IVA, otros impuestos y total.
- Generar asientos automáticos.
- Vincular comprobantes con clientes, proveedores y asientos.

### Entregables

- Formularios y endpoints de ventas y compras.
- Validaciones fiscales y aritméticas mínimas.
- Generación automática de asientos.
- Consulta del asiento desde el comprobante.
- Consulta del comprobante desde el asiento.
- Pruebas de integración del circuito completo.

### Criterio de salida

Una compra o venta confirmada genera un asiento balanceado, aparece en el Libro Diario y actualiza los saldos del Libro Mayor.

---

## Fase 4: OCR/NLP y gestión del comprobante digital

**Fechas:** 21 al 27 de noviembre de 2026  
**Caso de uso:** CUU-016.  
**Hito:** carga asistida de comprobantes funcionando de punta a punta.

### Objetivos

- Permitir la carga de PDF, PNG y JPG.
- Almacenar el archivo original de forma segura.
- Extraer campos relevantes.
- Permitir revisión y corrección humana.
- Crear borradores de compras o ventas.

### Entregables

- Servicio de carga de archivos.
- Adaptador de OCR/NLP.
- Pantalla de revisión de campos extraídos.
- Manejo de campos dudosos.
- Persistencia del valor extraído y del corregido.
- Conversión del resultado en borrador de comprobante.
- Conjunto de comprobantes de prueba controlados.
- Pruebas de archivos inválidos, campos faltantes y duplicados.

### Criterio de salida

El usuario carga un comprobante, revisa la extracción, corrige los datos necesarios y genera un borrador listo para registrar y contabilizar.

---

## Fase 5: Validación con ARCA, estados y auditoría

**Fechas:** 28 de noviembre al 4 de diciembre de 2026  
**Casos de uso:** CUU-017, CUU-022 y CUU-013.  
**Hito:** comprobantes trazables con validación fiscal desacoplada.

### Objetivos

- Implementar el contrato del adaptador de ARCA.
- Implementar integración real si existe ambiente habilitado o simulador si no existe.
- Gestionar estados del comprobante.
- Registrar intentos, errores y respuestas.
- Completar historial de auditoría.

### Entregables

- Adaptador de ARCA desacoplado.
- Servicio simulado configurable para desarrollo.
- Estados Pendiente, En validación, Válido, Inválido y Error de integración.
- Reintentos controlados.
- Historial de validaciones.
- Consulta de estado del comprobante.
- Consulta de auditoría con filtros.
- Pruebas de respuesta válida, inválida, timeout y error externo.

### Criterio de salida

Cada comprobante permite conocer su estado actual, el historial de validaciones y las acciones realizadas por los usuarios, incluso cuando el servicio externo falla.

---

## Fase 6: Estados contables y dashboard

**Fechas:** 5 al 11 de diciembre de 2026  
**Casos de uso:** CUU-009, CUU-010 y versión parcial de CUU-021.  
**Hito:** información contable visible y verificable.

### Objetivos

- Generar Balance General.
- Generar Estado de Resultados.
- Implementar dashboard financiero mínimo.
- Habilitar filtros por período.
- Permitir navegación hacia el detalle.

### Entregables

- Balance General por período.
- Validación de la ecuación patrimonial.
- Estado de Resultados por período.
- Indicadores de ventas, compras, resultado, IVA y comprobantes.
- Gráfico de evolución mensual.
- Enlaces a los movimientos que originan los totales.
- Exportación básica del Libro Diario si la capacidad del equipo lo permite.
- Pruebas de totales y consistencia entre informes.

### Criterio de salida

Los datos registrados en ventas, compras y asientos se reflejan de forma consistente en los libros, estados contables y dashboard.

---

## Fase 7: Integración, estabilización y entrega

**Fechas:** 12 al 18 de diciembre de 2026  
**Hito final:** versión candidata demostrable del 70% funcional.

### Objetivos

- Corregir defectos críticos.
- Completar pruebas end-to-end.
- Revisar seguridad y permisos.
- Mejorar experiencia de usuario en los circuitos principales.
- Preparar datos y guion de demostración.
- Congelar el alcance y producir la versión candidata.

### Entregables

- Suite de pruebas unitarias, integración y end-to-end prioritaria.
- Revisión de permisos por rol.
- Manejo uniforme de errores.
- Datos de demostración repetibles.
- Documentación de instalación y ejecución.
- Manual breve de usuario.
- Registro de limitaciones conocidas.
- Release candidata etiquetada.
- Demostración integral.

### Criterio de salida al 18 de diciembre

La versión debe ejecutar sin interrupciones el recorrido integral definido en la sección siguiente, conservar los datos, producir asientos balanceados, soportar fallos controlados y permitir rastrear las operaciones realizadas.

---

# 5. Demostración integral esperada

La presentación final deberá poder ejecutar este recorrido:

1. Un administrador crea un usuario contador.
2. El contador inicia sesión.
3. Configura el plan de cuentas.
4. Registra un proveedor.
5. Carga una factura de compra en PDF.
6. El OCR extrae sus datos.
7. El contador corrige un campo y confirma.
8. El sistema valida el comprobante mediante el adaptador de ARCA.
9. Se genera automáticamente el asiento.
10. El asiento aparece en el Libro Diario.
11. Los movimientos aparecen en el Libro Mayor.
12. Se registra una venta.
13. Se actualizan el Balance General y el Estado de Resultados.
14. El dashboard muestra los indicadores principales.
15. La auditoría permite ver quién cargó, corrigió, validó y confirmó el comprobante.

Si este recorrido funciona con datos persistentes, validaciones, manejo de errores, seguridad, pruebas y trazabilidad, el sistema puede considerarse un **70% funcional íntegro y defendible**.

---

# 6. Prioridades de ejecución

## Prioridad 1: obligatoria

- Seguridad y usuarios.
- Plan de Cuentas.
- Clientes y proveedores.
- Motor de asientos.
- Libro Diario y Libro Mayor.
- Compras y ventas.
- Generación automática de asientos.
- Balance General y Estado de Resultados.

## Prioridad 2: diferenciadora del proyecto

- OCR/NLP con revisión humana.
- Adaptador de ARCA real o simulado.
- Estados del comprobante.
- Auditoría de punta a punta.

## Prioridad 3: visible, pero recortable

- Dashboard.
- Exportación básica.
- Comparación entre períodos.
- Mejoras visuales no esenciales.

Si existe un desvío, se debe recortar primero la Prioridad 3. No conviene recortar pruebas del motor contable, seguridad, persistencia ni trazabilidad.

---

# 7. Definición de terminado

Un caso de uso solo se considerará terminado cuando cumpla con lo siguiente:

- Criterios de aceptación documentados.
- Interfaz o endpoint funcional.
- Persistencia real.
- Validaciones de negocio.
- Control de permisos.
- Manejo de errores.
- Auditoría cuando corresponda.
- Pruebas unitarias de reglas críticas.
- Prueba de integración cuando participe más de un componente.
- Compilación, lint y pruebas exitosas.
- Revisión del código.
- Documentación mínima actualizada.
- Sin secretos ni credenciales dentro del repositorio.

---

# 8. Riesgos y mitigaciones

## Integración tardía

**Riesgo:** que frontend, backend, OCR y contabilidad funcionen por separado pero no juntos.  
**Mitigación:** realizar una integración demostrable al final de cada fase y mantener un flujo end-to-end activo desde la Fase 3.

## OCR poco preciso

**Riesgo:** que distintos formatos de facturas produzcan resultados inconsistentes.  
**Mitigación:** revisión humana obligatoria, indicador de campos dudosos y conjunto controlado de comprobantes de prueba.

## Falta de acceso a ARCA

**Riesgo:** no disponer de credenciales o ambiente externo habilitado.  
**Mitigación:** contrato de integración desacoplado, adaptador simulado y registro completo de solicitudes y respuestas.

## Inconsistencia contable

**Riesgo:** asientos desbalanceados o informes que no coinciden con los libros.  
**Mitigación:** invariantes de partida doble, transacciones de base de datos, pruebas unitarias y pruebas cruzadas entre Libro Diario, Libro Mayor y estados contables.

## Exceso de alcance

**Riesgo:** intentar completar recomendaciones inteligentes, reportes automáticos y exportaciones avanzadas antes del núcleo.  
**Mitigación:** congelar los 16 casos completos, tratar el dashboard como parcial y postergar explícitamente el resto.

## Código generado por IA sin control

**Riesgo:** introducir errores, dependencias innecesarias o reglas de negocio inventadas.  
**Mitigación:** cambios pequeños, revisión de diffs, pruebas obligatorias, instrucciones de repositorio y prohibición de incorporar código que no pueda ser explicado por el equipo.

---

# 9. Hitos de control

- **30 de octubre:** base técnica ejecutable.
- **6 de noviembre:** seguridad y maestros terminados.
- **13 de noviembre:** núcleo contable operativo.
- **20 de noviembre:** compras y ventas integradas con contabilidad.
- **27 de noviembre:** OCR/NLP conectado al circuito de comprobantes.
- **4 de diciembre:** ARCA, estados y auditoría operativos.
- **11 de diciembre:** estados contables y dashboard listos.
- **18 de diciembre:** versión candidata, documentación y demostración integral.

---

# 10. Resumen ejecutivo

El alcance recomendado para el 18 de diciembre de 2026 es completar 16 de los 23 casos de uso y entregar parcialmente el Dashboard Financiero y la exportación del Libro Diario.

El resultado no será solamente una colección de CRUD. Será un sistema capaz de:

- Administrar usuarios y roles.
- Mantener el plan de cuentas.
- Administrar clientes y proveedores.
- Registrar compras y ventas.
- Crear asientos automáticos y manuales.
- Consultar Libro Diario y Libro Mayor.
- Generar Balance General y Estado de Resultados.
- Cargar comprobantes mediante OCR/NLP.
- Revisar y corregir la extracción.
- Validar comprobantes mediante un adaptador de ARCA.
- Consultar estados e historial.
- Auditar las acciones realizadas.
- Mostrar indicadores financieros básicos.

Este recorte concentra el esfuerzo en el flujo principal y conserva las características que diferencian a EugenIA: automatización documental, integración fiscal, trazabilidad y apoyo a la gestión contable.
