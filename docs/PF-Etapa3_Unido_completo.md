**Universidad Tecnológica**

**Nacional**

***Proyecto Final***

***“Sistema inteligente de apoyo y gestión contable, con integraciones a ARCA, OCR y NLP”***

**Autores:**

| **Legajo** | **Nombre y Apellido**       | **E-mail**                   |
|------------|-----------------------------|------------------------------|
| 44840      | Cortéz, Agustín             | cortez.agustinsist@gmail.com |
| 47431      | Tombolini, Santiago Alfredo | santitombo@gmail.com         |
| 46904      | Tulian, Maria Laura         | marialauratulian1@gmail.com  |

**Docente:** Marcelo Roca

**Comisión:** 503 - **Año:** 2026

# Índice

[**Índice 1**](#índice)

[**Abstract 6**](#abstract)

[**ETAPA 1 8**](#etapa-1)

[**1. Análisis de la organización 8**](#análisis-de-la-organización)

> [1.1. Descripción de L.A.S Tech 8](#descripción-de-l.a.s-tech)
>
> [1.2. Objetivos Principales 8](#objetivos-principales)
>
> [1.3. Objetivos Secundarios 9](#objetivos-secundarios)
>
> [1.4. Organigrama 10](#organigrama)
>
> [1.5. Matriz FODA 11](#matriz-foda)
>
> [1.6. Análisis de los principales procesos 11](#análisis-de-los-principales-procesos)
>
> [1.6.1. Procesos de ingeniería y producto 11](#procesos-de-ingeniería-y-producto)
>
> [1.6.2. Procesos de integración y adaptabilidad 12](#procesos-de-integración-y-adaptabilidad)
>
> [1.6.3. Procesos de Crecimiento y Relación con el Cliente 13](#procesos-de-crecimiento-y-relación-con-el-cliente)

[**2. Análisis de problemas 14**](#análisis-de-problemas)

> [2.1. Carga manual excesiva de datos 14](#carga-manual-excesiva-de-datos)
>
> [2.2. Reducción de errores mediante automatización 14](#reducción-de-errores-mediante-automatización)
>
> [2.3. Duplicación de pagos y registros 14](#duplicación-de-pagos-y-registros)
>
> [2.4. Procesos lentos de validación documental 14](#procesos-lentos-de-validación-documental)

[**3. Análisis de objetivos 15**](#análisis-de-objetivos)

> [3.1. Automatización del ciclo de ingesta de datos 15](#automatización-del-ciclo-de-ingesta-de-datos)
>
> [3.2. Erradicación de inconsistencias y errores de carga 15](#erradicación-de-inconsistencias-y-errores-de-carga)
>
> [3.3. Implementación de un sistema de auditoría preventiva 15](#implementación-de-un-sistema-de-auditoría-preventiva)
>
> [3.4. Agilización de la validación y cumplimiento 15](#agilización-de-la-validación-y-cumplimiento)

[**4. Propuesta de alternativas de solución 16**](#propuesta-de-alternativas-de-solución)

> [4.1. Megacontable 16](#megacontable)
>
> [4.2. Nexito 17](#nexito)
>
> [4.3. Evolutiva IA 18](#evolutiva-ia)
>
> [4.4. Dijit.app 19](#dijit.app)
>
> [4.5. Tango 20](#tango)

[**ETAPA 2 22**](#etapa-2)

[**5. Análisis de factibilidad 22**](#análisis-de-factibilidad)

> [5.1. Factibilidad técnica 22](#factibilidad-técnica)
>
> [5.1.1. Stack tecnológico propuesto 22](#stack-tecnológico-propuesto)
>
> [5.1.2. Habilidades del equipo vs. requerimientos del proyecto 22](#habilidades-del-equipo-vs.-requerimientos-del-proyecto)
>
> [5.1.3. Disponibilidad de herramientas 23](#disponibilidad-de-herramientas)
>
> [5.1.4. Riesgos técnicos identificados 23](#riesgos-técnicos-identificados)
>
> [5.2. Factibilidad Operativa 24](#factibilidad-operativa)
>
> [5.2.1. Capacidad de los usuarios finales para adoptar el sistema 24](#capacidad-de-los-usuarios-finales-para-adoptar-el-sistema)
>
> [5.2.2. Impacto en los procesos actuales de los clientes 25](#impacto-en-los-procesos-actuales-de-los-clientes)
>
> [5.2.3. Capacidad de la organización para operar el sistema internamente 26](#capacidad-de-la-organización-para-operar-el-sistema-internamente)
>
> [5.2.4. Capacitación y soporte 26](#capacitación-y-soporte)
>
> [5.3. Factibilidad Legal 27](#factibilidad-legal)
>
> [5.3.1. Protección de datos personales 27](#protección-de-datos-personales)
>
> [5.3.2. Normativa fiscal y cumplimiento con ARCA 27](#normativa-fiscal-y-cumplimiento-con-arca)
>
> [5.3.3. Propiedad intelectual 28](#propiedad-intelectual)
>
> [5.3.4. Contratos con clientes 28](#contratos-con-clientes)
>
> [5.4. Factibilidad económica-financiera 29](#factibilidad-económica-financiera)
>
> [5.4.1. Proyección de costos 29](#proyección-de-costos)
>
> [5.4.2. Inversión inicial 31](#inversión-inicial)
>
> [5.4.3. Modelo de ingresos 31](#modelo-de-ingresos)
>
> [5.4.4. Punto de equilibrio 31](#punto-de-equilibrio)
>
> [5.4.5. Egresos anuales 32](#egresos-anuales)
>
> [5.4.6. Tabla de flujo de caja 33](#tabla-de-flujo-de-caja)
>
> [5.4.7. Cálculo de VAN y TIR 33](#cálculo-de-van-y-tir)
>
> [5.4.8. Análisis de sensibilidad 34](#análisis-de-sensibilidad)
>
> [5.4.9. Estrategias de financiamiento 34](#estrategias-de-financiamiento)
>
> [5.4.10. Escalabilidad y rentabilidad a largo plazo 35](#escalabilidad-y-rentabilidad-a-largo-plazo)
>
> [5.5. Conclusión de factibilidad 35](#conclusión-de-factibilidad)

[**6. Precio y forma de pago 37**](#precio-y-forma-de-pago)

> [6.1. Criterios de fijación de precios 37](#criterios-de-fijación-de-precios)
>
> [6.2. Planes disponibles 37](#planes-disponibles)
>
> [6.3. Forma de pago 38](#forma-de-pago)

[**7. Análisis de Factibilidad (Tango) 38**](#análisis-de-factibilidad-tango)

[**8. Diagrama de Gantt 41**](#diagrama-de-gantt)

[**ETAPA 3 43**](#etapa-3)

[**9. Análisis de datos 43**](#análisis-de-datos)

[10. Definición de metodología 45](#definición-de-metodología)

[**11. Cálculo de tamaño de sistema 46**](#cálculo-de-tamaño-de-sistema)

> [11.1. Tabla de puntos de función 53](#tabla-de-puntos-de-función)
>
> [11.2. Puntos de función no ajustados (PFNA) 53](#puntos-de-función-no-ajustados-pfna)
>
> [11.3. Cálculo del Valor de Ajuste 58](#cálculo-del-valor-de-ajuste)
>
> [11.4. Rango de Variación del VAF 60](#rango-de-variación-del-vaf)
>
> [11.5. Cálculo de Puntos de Función Ajustados (PFA) 61](#cálculo-de-puntos-de-función-ajustados-pfa)
>
> [11.6. Conclusión cálculo del tamaño 61](#conclusión-cálculo-del-tamaño)

[**12. Diseño 62**](#diseño)

> [**12.1. Registrar venta 65**](#registrar-venta)
>
> [12.1.1. Caso de uso 65](#caso-de-uso)
>
> [12.1.2. Diagramas de actividad y estado 69](#diagramas-de-actividad-y-estado)
>
> [**12.2. Registrar compra 70**](#registrar-compra)
>
> [12.2.1. Caso de uso 70](#caso-de-uso-1)
>
> [12.2.2. Diagramas de actividad y estado 75](#diagramas-de-actividad-y-estado-1)
>
> [**12.3. Gestionar Libro Diario 76**](#gestionar-libro-diario)
>
> [12.3.1. Caso de uso 76](#caso-de-uso-2)
>
> [12.3.2. Diagramas de actividad y estado 79](#diagramas-de-actividad-y-estado-2)
>
> [**12.4. Registrar asiento manual 80**](#registrar-asiento-manual)
>
> [12.4.1. Caso de uso 80](#caso-de-uso-3)
>
> [12.4.2. Diagramas de actividad y estado 82](#diagramas-de-actividad-y-estado-3)
>
> [12.4.3. Ejemplos de asientos contables a contemplar 82](#ejemplos-de-asientos-contables-a-contemplar)
>
> [**12.5. Gestionar Plan de Cuentas 88**](#gestionar-plan-de-cuentas)
>
> [12.5.1. Caso de uso 88](#caso-de-uso-4)
>
> [12.5.2. Diagramas de actividad y estado 91](#diagramas-de-actividad-y-estado-4)
>
> [12.5.3. Ejemplo de Plan de Cuentas 91](#ejemplo-de-plan-de-cuentas)
>
> [**12.6. Consultar Libro Mayor 95**](#consultar-libro-mayor)
>
> [12.6.1. Caso de uso 95](#caso-de-uso-5)
>
> [12.6.2. Diagramas de actividad y estado 96](#diagramas-de-actividad-y-estado-5)
>
> [12.6.3. Ejemplo de Libro Mayor 96](#ejemplo-de-libro-mayor)
>
> [**12.7. Gestionar Clientes 98**](#gestionar-clientes)
>
> [12.7.1. Caso de uso 98](#caso-de-uso-6)
>
> [12.7.2. Diagramas de actividad y estado 100](#diagramas-de-actividad-y-estado-6)
>
> [**12.8. Gestionar Proveedores 101**](#gestionar-proveedores)
>
> [12.8.1. Caso de uso 101](#caso-de-uso-7)
>
> [12.8.2. Diagramas de actividad y estado 103](#diagramas-de-actividad-y-estado-7)
>
> [**12.9. Generar Balance General 104**](#generar-balance-general)
>
> [12.9.1. Caso de uso 104](#caso-de-uso-8)
>
> [12.9.2. Diagramas de actividad y estado 106](#diagramas-de-actividad-y-estado-8)
>
> [**12.10. Generar Estado de Resultados 107**](#generar-estado-de-resultados)
>
> [12.10.1. Caso de uso 107](#caso-de-uso-9)
>
> [12.10.2. Diagramas de actividad y estado 108](#diagramas-de-actividad-y-estado-9)
>
> [**12.11. Exportar Libro Diario 109**](#exportar-libro-diario)
>
> [12.11.1. Caso de uso 109](#caso-de-uso-10)
>
> [12.11.2. Diagramas de actividad y estado 110](#diagramas-de-actividad-y-estado-10)
>
> [**12.12. Exportar Libro Mayor 111**](#exportar-libro-mayor)
>
> [12.12.1. Caso de uso 111](#caso-de-uso-11)
>
> [12.12.2. Diagramas de actividad y estado 112](#diagramas-de-actividad-y-estado-11)
>
> [**12.13. Consultar historial de auditoría 113**](#consultar-historial-de-auditoría)
>
> [12.13.1. Caso de uso 113](#caso-de-uso-12)
>
> [12.13.2. Diagramas de actividad y estado 114](#diagramas-de-actividad-y-estado-12)
>
> [**12.14. Exportar Libro IVA a ARCA 115**](#exportar-libro-iva-a-arca)
>
> [12.14.1. Caso de uso 115](#caso-de-uso-13)
>
> [12.14.2. Diagramas de actividad y estado 117](#diagramas-de-actividad-y-estado-13)
>
> [12.14.3. Ejemplo de Exportación del Libro IVA a ARCA 118](#ejemplo-de-exportación-del-libro-iva-a-arca)
>
> [**12.15. Iniciar Sesión 120**](#iniciar-sesión)
>
> [12.15.1. Caso de uso 120](#caso-de-uso-14)
>
> [12.15.2. Diagramas de actividad y estado 123](#diagramas-de-actividad-y-estado-14)
>
> [**12.16. Registrar comprobante con OCR 124**](#registrar-comprobante-con-ocr)
>
> [12.16.1. Caso de uso 124](#caso-de-uso-15)
>
> [12.16.2. Diagramas de actividad y estado 127](#diagramas-de-actividad-y-estado-15)
>
> [**12.17. Validar comprobante con ARCA 128**](#validar-comprobante-con-arca)
>
> [12.17.1. Caso de uso 128](#caso-de-uso-16)
>
> [12.17.2. Diagramas de actividad y estado 130](#diagramas-de-actividad-y-estado-16)
>
> [**12.18. Gestionar Usuarios 131**](#gestionar-usuarios)
>
> [12.18.1. Caso de uso 131](#caso-de-uso-17)
>
> [12.18.2. Diagramas de actividad y estado 133](#diagramas-de-actividad-y-estado-17)
>
> [**12.19. Gestionar Alertas de Auditoría 134**](#gestionar-alertas-de-auditoría)
>
> [12.19.1. Caso de uso 134](#caso-de-uso-18)
>
> [12.19.2. Diagramas de actividad y estado 136](#diagramas-de-actividad-y-estado-18)
>
> [**12.20. Generar Reportes Automáticos 137**](#generar-reportes-automáticos)
>
> [12.20.1. Caso de uso 137](#caso-de-uso-19)
>
> [12.20.2. Diagramas de actividad y estado 139](#diagramas-de-actividad-y-estado-19)
>
> [**12.21. Consultar Dashboard Financiero 140**](#consultar-dashboard-financiero)
>
> [12.21.1. Caso de uso 140](#caso-de-uso-20)
>
> [12.21.2. Diagramas de actividad y estado 142](#diagramas-de-actividad-y-estado-20)
>
> [**12.22. Consultar estado de comprobante 143**](#consultar-estado-de-comprobante)
>
> [12.22.1. Caso de uso 143](#caso-de-uso-21)
>
> [12.22.2. Diagramas de actividad y estado 145](#diagramas-de-actividad-y-estado-21)
>
> [12.23. Obtener recomendaciones financieras inteligentes 146](#obtener-recomendaciones-financieras-inteligentes)
>
> [12.23.1. Caso de uso 146](#caso-de-uso-22)
>
> [12.23.2. Diagramas de actividad y estado 149](#diagramas-de-actividad-y-estado-22)

[**13. Análisis de riesgos 150**](#análisis-de-riesgos)

> [**13.1. Identificación de riesgos 152**](#identificación-de-riesgos)
>
> [**13.2. Inventario activos 154**](#inventario-activos)
>
> [**13.3. Riesgo 1: Phishing y acceso no autorizado 160**](#riesgo-1-phishing-y-acceso-no-autorizado)
>
> [13.3.1. Identificación de riesgo 160](#identificación-de-riesgo)
>
> [13.3.2. Tratamiento de riesgos 164](#tratamiento-de-riesgos)
>
> [13.3.3. Planes de Contingencia, Recuperación y Continuidad de Negocio 167](#planes-de-contingencia-recuperación-y-continuidad-de-negocio)
>
> [**13.4. Riesgo 2: Error de interpretación OCR/IA 172**](#riesgo-2-error-de-interpretación-ocria)
>
> [13.4.1. Identificación de riesgo 172](#identificación-de-riesgo-1)
>
> [13.4.2. Tratamiento de riesgos 177](#tratamiento-de-riesgos-1)
>
> [13.4.3. Planes de Contingencia, Recuperación y Continuidad de Negocio 181](#planes-de-contingencia-recuperación-y-continuidad-de-negocio-1)
>
> [**13.5. Riesgo 3: Vulnerabilidad de seguridad en la aplicación y exposición de información sensible 185**](#riesgo-3-vulnerabilidad-de-seguridad-en-la-aplicación-y-exposición-de-información-sensible)
>
> [13.5.1. Identificación de riesgo 185](#identificación-de-riesgo-2)
>
> [13.5.2. Tratamiento de riesgos 188](#tratamiento-de-riesgos-2)
>
> [13.5.3. Planes de Contingencia, Recuperación y Continuidad de Negocio 191](#planes-de-contingencia-recuperación-y-continuidad-de-negocio-2)

[**Anexo I - Gantt actualizado 195**](#anexo-i---gantt-actualizado)

[**Anexo II - Tabla comparativa de las alternativas 196**](#anexo-ii---tabla-comparativa-de-las-alternativas)

[**Anexo III - Apartado Legal 198**](#anexo-iii---apartado-legal)

[**Anexo IV - Bibliografía 199**](#anexo-iv---bibliografía)

# **Abstract**

En la actualidad, la contabilidad empresarial enfrenta un desafío crítico: la creciente cantidad de datos financieros supera la capacidad de análisis manual y de los sistemas tradicionales. Muchas organizaciones continúan utilizando herramientas aisladas y procesos manuales que dificultan la integración de información y retrasan la detección de errores o inconsistencias. Como resultado, las empresas operan con visibilidad limitada sobre su situación financiera real, aumentando el riesgo de pérdidas económicas y/o decisiones incorrectas

En respuesta a esta problemática, el presente proyecto propone el desarrollo de EugenIA, un sistema inteligente de nueva generación orientado al apoyo contable, administrativo y comercial de empresas mediante el uso de técnicas de Inteligencia Artificial y análisis predictivo de datos.

A día de hoy, se insume demasiado tiempo en la carga manual de datos revisando facturas o comprobantes de pago, lo que infiere en puntos de dolor en los procesos críticos de las empresas contables. Para solucionar esto, el sistema incorpora un módulo específico para la digitalización y análisis de comprobantes de pago y facturas, con base en tecnologías OCR (Optical Character Recognition) y modelos NLP (Natural Language Processing).  
A través del OCR, los documentos físicos son convertidos en texto estructurado permitiendo extraer automáticamente datos clave. Posteriormente, los modelos de NLP validan la coherencia de los registros y, al mismo tiempo, interpretan el contexto de cada comprobante. De esta manera, la combinación de OCR y NLP permite transformar documentos en información estructurada y automatizar la carga de datos al sistema contable, logrando un proceso más ágil, preciso y confiable

Además, el sistema contable implementa integraciones mediante APIs con organismos fiscales y reguladores, permitiendo la interoperabilidad automática para la presentación de información tributaria, emisión de comprobantes electrónicos y cumplimiento normativo. Asimismo, aborda el problema de los cambios constantes en normativas fiscales mediante un módulo inteligente que monitorea las APIs conectadas y notifica automáticamente actualizaciones normativas, reduciendo el riesgo de errores y asegurando la adaptación oportuna a nuevos requerimientos legales.

Otro de los pilares fundamentales de EugenIA, es su motor inteligente de análisis financiero, capaz de detectar errores contables en tiempo real, identificar pagos duplicados, reconocer registros inconsistentes y alertar sobre valores fuera de rango. Esta funcionalidad reduce significativamente los riesgos operativos y mejora la confiabilidad de la información financiera.

La plataforma también incorpora modelos predictivos avanzados, capaces de anticipar compras y ventas futuras, proyectar ingresos y egresos, detectar tendencias económicas y prever posibles déficits financieros antes de que se conviertan en problemas críticos. Esto permite a las empresas pasar de una gestión reactiva a una gestión predictiva basada en datos, optimizando la planificación y reduciendo la incertidumbre financiera.

Asimismo, integrará un módulo inteligente de recomendaciones financieras que analiza el comportamiento económico de la empresa y, a partir de datos como conciliaciones bancarias, predicciones de flujo de caja y vencimientos, a la par que propondrá acciones concretas para optimizar recursos, reducir gastos innecesarios y mejorar la toma de decisiones con respaldo analítico.

También contará con dashboards inteligentes y reportes automatizados, diseñados para transformar información compleja en visualizaciones claras y accionables. Estos paneles permiten monitorear indicadores clave en tiempo real, detectar variaciones significativas y generar alertas tempranas que facilitan la toma de decisiones informadas.

#  

# ETAPA 1

# Análisis de la organización

## **Descripción de L.A.S Tech**

L.A.S Tech es una startup tecnológica fundada por tres estudiantes de la carrera de Ingeniería en Sistemas de Información de la UTN, que surge a partir de la identificación directa de problemáticas reales en la gestión contable. Con una antigüedad de dos años, la empresa nace del vínculo cercano con el sector: por un lado, la experiencia de una contadora en el ámbito profesional y, por otro, la operación de una empresa de acopio de granos. Este origen le permitió a la organización comprender en profundidad las dificultades operativas, la rigidez de los sistemas existentes y la necesidad de soluciones más adaptables.

A partir de este conocimiento, L.A.S Tech se especializa en el desarrollo de sistemas de apoyo a la gestión contable, diseñados para ajustarse a los requerimientos específicos de distintos tipos de empresas. Su propuesta de valor se centra en la flexibilidad, la escalabilidad y la orientación a la resolución de problemas concretos, permitiendo a las organizaciones mejorar su eficiencia operativa y optimizar la toma de decisiones. La arquitectura de sus soluciones busca integrarse de manera fluida con los procesos existentes, reduciendo fricciones y tiempos de adopción.

En sus dos años de trayectoria, la empresa ha consolidado un enfoque ágil de desarrollo y una estructura organizacional compacta, lo que le permite iterar rápidamente sobre sus productos y adaptarse a las necesidades cambiantes del mercado. Este modelo le otorga una ventaja competitiva en entornos dinámicos, posicionándose como una alternativa tecnológica cercana, especializada y alineada con las realidades del sector contable y empresarial.

## **Objetivos Principales**

El objetivo principal de L.A.S Tech es desarrollar y consolidar una solución tecnológica integral que optimice la gestión contable de las organizaciones, permitiendo automatizar procesos, reducir errores operativos y mejorar la calidad de la información para la toma de decisiones. A través de un sistema flexible y adaptable, la empresa busca responder a las necesidades específicas de distintos sectores, garantizando escalabilidad y facilidad de integración con los procesos existentes, con el fin de convertirse en una herramienta clave para la eficiencia y competitividad empresarial.

## Objetivos Secundarios 

1.  **Automatización de captura y procesamiento de comprobantes**

Desarrollar un módulo basado en tecnologías de OCR y modelos de NLP que permita digitalizar, interpretar y estructurar automáticamente la información contenida en facturas y comprobantes de pago. Este objetivo busca reducir la carga manual de datos, mejorar la precisión en los registros contables y acelerar los procesos administrativos críticos.

2.  **Integración e interoperabilidad mediante APIs**

Implementar una arquitectura de integración que permita la conexión fluida con organismos fiscales, sistemas externos y plataformas de terceros. Esto incluye la automatización de la presentación de información tributaria, la emisión de comprobantes electrónicos y la adaptación dinámica a cambios normativos mediante monitoreo continuo.

3.  **Validación inteligente y detección de anomalías**

Construir un motor de análisis en tiempo real capaz de identificar errores contables, registros inconsistentes, pagos duplicados y valores fuera de rango. Este objetivo apunta a mejorar la calidad y confiabilidad de la información financiera, reduciendo riesgos operativos.

4.  **Modelos predictivos y analítica avanzada**

Desarrollar e integrar modelos de análisis predictivo que permitan anticipar ingresos, egresos, tendencias económicas y posibles déficits financieros. Se busca transformar la gestión empresarial de un enfoque reactivo a uno predictivo, basado en datos.

5.  **Sistema de recomendaciones financieras inteligentes**

Implementar un módulo que, a partir del análisis del comportamiento económico de la empresa, genere propuestas de acción orientados a optimizar recursos, reducir costos y mejorar la toma de decisiones estratégicas.

6.  **Visualización de datos y reportes automatizados**

Diseñar dashboards interactivos y reportes automatizados que presenten información financiera de manera clara y en tiempo real. Este objetivo incluye la generación de alertas tempranas y la visualización de indicadores clave para facilitar la toma de decisiones informada

## Organigrama



##  Matriz FODA

#### 

## Análisis de los principales procesos

### Procesos de ingeniería y producto

Estos procesos aseguran que la startup mantenga su ventaja competitiva, la agilidad y la cercanía con el problema.

#### Diagnóstico y Relevamiento "In-Situ" (Discovery)

Uno de los procesos más importantes dentro de L.A.S. Tech es el diagnóstico y relevamiento inicial de las necesidades del cliente. Este proceso representa un activo estratégico para la empresa, ya que su origen estuvo vinculado a la observación directa de problemáticas reales dentro del sector contable y agroindustrial. Antes de comenzar cualquier desarrollo, la empresa realiza entrevistas técnicas, reuniones de análisis y observación del flujo de trabajo cotidiano de los usuarios finales. Esto permite identificar fricciones, tareas repetitivas y necesidades que muchas veces no son contempladas por los sistemas estándar del mercado. A partir de esta información, se construye un backlog de producto priorizado en función de problemas concretos del negocio, permitiendo que el desarrollo esté orientado a generar soluciones con valor real para el cliente.

#### Ciclo de desarrollo ágil e iterativo (Scrum/Kanban)

Una vez detectadas las necesidades, L.A.S. Tech trabaja bajo metodologías ágiles de desarrollo, principalmente utilizando enfoques como Scrum o Kanban. El trabajo se organiza en ciclos cortos o sprints, donde se desarrollan funcionalidades específicas que pueden ser evaluadas, probadas y ajustadas de manera continua. Este modelo permite obtener retroalimentación temprana y realizar modificaciones en tiempos reducidos, adaptándose rápidamente a cambios en los requerimientos del cliente. Desde una perspectiva estratégica, esta capacidad de iteración constante representa una ventaja competitiva importante frente a empresas de software más tradicionales, cuyos procesos suelen ser más rígidos y menos flexibles.

### Procesos de integración y adaptabilidad

#### Control de calidad y QA especializado

En una solución orientada a procesos contables y administrativos, verificar únicamente que el sistema funcione correctamente desde lo técnico no resulta suficiente. También es fundamental asegurar que la información procesada sea precisa y confiable, especialmente cuando se trabaja con datos que impactan directamente en la gestión financiera o impositiva de un cliente. Por este motivo, L.A.S. Tech incorpora un proceso de control de calidad enfocado no solo en el rendimiento del software, sino también en la exactitud de los resultados obtenidos.

Dentro de este proceso se realizan pruebas funcionales y pruebas de estrés para comprobar cómo responde el sistema ante distintos volúmenes de información o múltiples operaciones simultáneas. A su vez, se validan datos contables, fiscales y administrativos mediante casos reales o simulados, verificando que los cálculos generados por el software sean correctos y estén alineados con la normativa vigente. De esta manera, no solo se comprueba que la aplicación “corra” correctamente, sino también que la información que entrega sea confiable para la toma de decisiones del cliente.

###  Procesos de Crecimiento y Relación con el Cliente

L.A.S. Tech no solo entrega código, entrega una nueva forma de trabajar.

#### Consultoría de transformación digital

La implementación de una nueva solución tecnológica no finaliza cuando el software está desarrollado, sino cuando los usuarios logran incorporarlo de manera efectiva a su trabajo diario. Entendiendo esta realidad, L.A.S. Tech complementa su propuesta tecnológica con un fuerte enfoque consultivo, acompañando a sus clientes durante todo el proceso de adopción digital.

Para ello, la empresa brinda capacitaciones, asistencia técnica y acompañamiento durante la implementación de cada solución. El objetivo es facilitar la transición hacia nuevas formas de trabajo, reducir tiempos de adaptación y asegurar que la tecnología genere impacto real dentro de la operación del cliente. Este enfoque permite construir relaciones de largo plazo y posiciona a la empresa no solo como proveedor de software, sino también como socio estratégico en procesos de transformación digital.

#### Gestión de feedback y mejora continua

En un entorno tecnológico altamente dinámico, mantener la competitividad requiere evolucionar de manera constante junto con las necesidades del mercado y de los usuarios. Por esta razón, L.A.S. Tech incorpora un proceso continuo de recolección y análisis de feedback como parte central de su modelo de mejora.

A través de reuniones periódicas, seguimiento post implementación y contacto directo con usuarios finales, principalmente contadores, administrativos y responsables operativos, la empresa identifica oportunidades de mejora, nuevas funcionalidades y posibles ajustes en la experiencia de uso. Esta información se reincorpora al ciclo de desarrollo, permitiendo una evolución constante del producto y asegurando que las soluciones continúen generando valor en contextos reales de aplicación.

# Análisis de problemas

## Carga manual excesiva de datos 

Muchas empresas aún realizan la carga de información contable de manera manual, ingresando datos provenientes de facturas y comprobantes uno por uno. Este proceso incrementa la carga operativa, limita la productividad y dificulta la gestión eficiente de grandes volúmenes de información.

## Reducción de errores mediante automatización 

La disminución de la carga manual de datos, a través de tecnologías de digitalización y automatización, permite minimizar errores de registro, evitar omisiones y asegurar la coherencia entre comprobantes. Con ello se fortalece la confiabilidad de la información financiera, se agilizan los procesos y se reduce el riesgo de decisiones empresariales incorrectas o incumplimientos fiscales.

## **Duplicación de pagos y registros**

La ausencia de mecanismos eficientes de control y validación puede provocar que una misma operación sea registrada más de una vez o que determinados pagos se procesen de forma duplicada. Este tipo de errores genera pérdidas económicas, inconsistencias contables y dificultades para realizar auditorías o conciliaciones financieras. En entornos donde existen múltiples fuentes de información y procesos manuales, detectar estas duplicaciones suele convertirse en una tarea compleja y tardía.

## **Procesos lentos de validación documental**

La revisión y validación manual de facturas, comprobantes y documentos administrativos representa una tarea lenta y altamente demandante, especialmente en empresas que manejan grandes volúmenes de operaciones diarias. Los equipos administrativos deben invertir tiempo considerable en verificar datos, controlar coherencia entre registros y validar documentación, lo que retrasa otros procesos internos y disminuye la productividad.

# Análisis de objetivos

## **Automatización del** c**iclo de** i**ngesta de** d**atos**

**Objetivo:** Reducir en un 70-80% el tiempo dedicado a la carga manual de comprobantes y facturas mediante el uso de tecnologías de extracción automática.

Este objetivo ataca directamente el problema 2.1. Al automatizar la entrada de datos, la startup transforma el rol del administrativo: de ser un "digitador" de datos a un "validador" de información. Esto libera ancho de banda para tareas de mayor valor estratégico.

## **Erradicación de** i**nconsistencias y** e**rrores de** c**arga**

**Objetivo:** Lograr una tasa de precisión superior al **99%** en el procesamiento de documentos financieros, minimizando la intervención humana en la transcripción.

Resuelve el problema **2.2**. La precisión es el activo más valioso en contabilidad. Al estandarizar cómo se lee y se registra cada dato, se elimina la subjetividad o el cansancio humano, garantizando que los balances finales sean un reflejo fiel de la realidad.

## **Implementación de un** s**istema de** a**uditoría** p**reventiva**

**Objetivo:** Detectar y alertar el **100%** de los pagos o registros duplicados de forma instantánea antes de que impacten en el flujo de caja o libros contables.

Se enfoca en el problema **2.3**. No se trata solo de registrar, sino de controlar. Este objetivo convierte al sistema en un "guardián" financiero que protege el patrimonio de la empresa, evitando pérdidas económicas directas a causa de pagos dobles que suelen ser difíciles de recuperar.

## **Agilización de la** v**alidación y** c**umplimiento**

**Objetivo:** Optimizar los tiempos de validación documental y fiscal, logrando que el control de coherencia entre registros se realice en tiempo real (segundos) en lugar de días.

**Análisis:** Ataca el problema **2.4**. En un entorno fiscal dinámico, la velocidad de validación es clave para evitar multas. Al integrar la validación con organismos externos, L.A.S. Tech permite que la empresa esté "al día" permanentemente, eliminando los cuellos de botella de fin de mes.

# Propuesta de alternativas de solución

## **Megacontable**

*Link a pagina web:* [**<u>https://megacontable.com.ar/</u>**](https://megacontable.com.ar/)

**Megacontable** es un estudio contable argentino que combina la contabilidad tradicional con tecnología de inteligencia artificial. Su propuesta central es modernizar y automatizar la gestión contable y administrativa de empresas de todos los tamaños, prometiendo una reducción de hasta el 75% en tiempo dedicado a tareas rutinarias y una disminución del 90% en errores de registro.

- **Contabilidad Automatizada** Ofrecen soluciones contables impulsadas por IA para automatizar registros, conciliaciones y análisis financieros con precisión y rapidez. El sitio menciona que esto permite generar informes financieros automatizados con análisis predictivo, mantener el cumplimiento fiscal y normativo actualizado de forma automática, y reducir errores de registro y conciliación en un 90%.

- **Back Office Contable** permite delegar la contabilidad y administración financiera a su equipo de profesionales, quienes trabajan respaldados por sus herramientas tecnológicas propias. La idea es que la empresa cliente no tenga que ocuparse internamente de estas tareas, liberando tiempo para enfocarse en su negocio principal.

- **Recursos Humanos** Incluye gestión integral de nóminas, legajos digitales y procesos de RRHH, optimizados con herramientas de última generación. No se detalla más en el sitio qué procesos específicos de RRHH abarca más allá de estos tres puntos.

- **Asesoría Contable Inteligente** Se trata de consultoría estratégica que utiliza análisis predictivo basado en IA para ayudar a tomar decisiones financieras. Está orientada a negocios que necesitan no solo llevar sus números, sino interpretarlos para tomar mejores decisiones.

Desarrollan herramientas propias basadas en Inteligencia Artificial, Machine Learning, automatización mediante RPA (robots de proceso) y Blockchain para la seguridad de las transacciones.

En resumen, es un estudio contable que apunta a empresas que quieren externalizar o modernizar su área contable y de RRHH, aprovechando la tecnología para ganar eficiencia y reducir errores.

## **Nexito**

*Link a pagina web:* [<u>https://nexito.tech/productos/ocr-empresarial/argentina</u>](https://nexito.tech/productos/ocr-empresarial/argentina)

**Nexito Technology** es una empresa de tecnología con presencia en New York, España y Latinoamérica que ofrece soluciones de automatización inteligente e inteligencia artificial para empresas. En su página para Argentina presentan su producto **Nexito Financial Suite**, enfocado en la automatización del procesamiento de documentos fiscales y contables mediante tecnología OCR (reconocimiento óptico de caracteres) potenciada con IA.

Su propuesta apunta a resolver uno de los desafíos más complejos del ecosistema fiscal argentino: la gestión de comprobantes electrónicos bajo las normativas de ARCA, con sus múltiples tipos de documentos y regímenes de retención que varían por jurisdicción provincial.

El sistema recibe facturas electrónicas, remitos y comprobantes desde distintos canales como email, WhatsApp o plataforma web, y extrae automáticamente los datos clave de cada documento: CUIT, razón social, CAE, conceptos, subtotales, IVA y totales. Además verifica la validez del CAE contra el servicio web de ARCA, detectando comprobantes apócrifos o con fecha vencida. Es compatible con todos los tipos de comprobantes ARCA: facturas tipo A, B, C, M y E, remitos, órdenes de compra, recibos de pago y certificados de retención de Ingresos Brutos, incluyendo también facturas de exportación con campos de aduana, incoterm y datos del despachante.

Uno de los puntos destacados es la gestión de retenciones multijurisdiccionales: el sistema clasifica automáticamente las retenciones de IIBB por jurisdicción provincial, identificando si corresponden a AGIP (CABA), ARBA (Buenos Aires), API (Santa Fe), ATER (Entre Ríos), entre otras, y aplica los porcentajes según el padrón vigente de cada organismo. A partir de los comprobantes procesados, también genera los datos necesarios para el régimen de información CITI Compras y CITI Ventas de ARCA (RG 3685), en formato compatible con el aplicativo.

En cuanto a integraciones, se conecta con los principales ERPs y software contable utilizados en Argentina: SAP S/4HANA, SAP Business One, Tango Gestión, Bejerman, ContaWin, Microsoft Dynamics y sistemas a medida.

## **Evolutiva IA**

*Link a pagina web:* [<u>https://evolutivaia.com</u>](https://evolutivaia.com)

Evolutiva IA es una empresa costarricense, con sede en San Joaquín de Flores, Heredia, que ofrece soluciones de inteligencia artificial diseñadas especialmente para PYMES y profesionales independientes en Costa Rica y el resto de Latinoamérica.

Su propuesta central es democratizar el acceso a la IA, partiendo de la idea de que esta tecnología no debería ser exclusiva de las grandes corporaciones. Cuentan con más de 45 implementaciones completadas y han trabajado en sectores como retail, finanzas y salud.

Su oferta se organiza en cinco grandes áreas.

1.  **Automatización inteligente**, que abarca desde la automatización de comunicaciones mediante asistentes virtuales, chatbots y mensajería automatizada, hasta la automatización de procesos de negocio como contabilidad, nómina, costeo de producto y gestión de pedidos e inventarios.

2.  **Inteligencia de negocio**, donde ofrecen herramientas de analítica prescriptiva, sistemas de recomendación, pronóstico de ventas, generación de informes y planes de negocio con IA.

3.  **Marketing con IA,** que incluye generación de contenido, landing pages, automatización de campañas, análisis de audiencia y sentimiento, segmentación de mercado y optimización SEO y SEM.

4.  **Asistentes sectoriales**, es decir, soluciones específicas para áreas como finanzas y contabilidad, recursos humanos y el sector salud, donde ofrecen herramientas de predicción de riesgo clínico, dictado médico, soporte a la decisión clínica y gestión de interconsultas.

5.  **Capacitación y consultoría**, que va desde diagnósticos de madurez digital y consultoría estratégica hasta talleres y conferencias sobre IA, incluyendo formación específica para el personal de salud.

Un punto destacado de su enfoque es que no trabajan con soluciones genéricas, sino que desarrollan herramientas personalizadas según las necesidades y el presupuesto de cada cliente, acompañando el proceso desde la evaluación inicial hasta la implementación y el soporte posterior.

Entre sus casos de éxito mencionan un cliente cuyo departamento comercial, usando GPTs personalizados, logró en cuatro meses ahorrar 160 horas mensuales e incrementar su productividad un 48,9%.

## **Dijit.app**

*Link a pagina web***:** [<u>https://www.dijit.app/gestion-de-facturas-con-ia-y-ocr-para-asesorias</u>](https://www.dijit.app/gestion-de-facturas-con-ia-y-ocr-para-asesorias)

Dijit.app es una plataforma SaaS española de gestión documental con inteligencia artificial y tecnología OCR, orientada especialmente a asesorías y gestorías contables, aunque también opera en sectores como hostelería, logística, retail, construcción, turismo y sanidad. Tiene delegaciones en Madrid y Málaga, además de una sede tecnológica en Tallin, Estonia.

Su propuesta central es eliminar la entrada manual de datos de facturas, reduciendo hasta un 98% el tiempo dedicado a esa tarea, con una precisión del 99% en la extracción de información.

El proceso es simple: el usuario arrastra o carga los documentos en formato PDF o imagen, el OCR escanea el texto, la IA clasifica e interpreta los datos, y el resultado se integra automáticamente con el sistema contable del cliente. Todo el procesamiento toma aproximadamente 3 segundos por página.

En cuanto a las funcionalidades que ofrece, el sistema realiza la captura y extracción automática de datos como proveedor, NIF/CIF, número de factura, base imponible, IVA y total. También hace la asignación automática de cuentas contables mediante machine learning, lo que significa que el sistema aprende y se adapta al plan de cuentas de cada cliente con el uso. Además incluye control de precios en albaranes, con detección de variaciones y alertas automáticas, gestión y archivo organizado de documentos con filtros inteligentes, y un portal multiusuario que permite a los propios clientes de la asesoría cargar su documentación y descargar sus datos en Excel directamente.

En materia de integraciones, Dijit.app se conecta con sistemas contables y ERPs mediante API REST, API SOAP, conexión SQL directa o exportación en formatos Excel, XML, CSV y JSON. También cuenta con conectores nativos para Microsoft Dynamics Business Central, Sage, A3 ERP, A3 ECO, Cegid Diez, Ágora POS, ICG Manager y Alba IBS, entre otros.

La tecnología detrás del producto combina modelos de IA generativa de OpenAI (GPT), Anthropic (Claude) y Meta (Llama), sobre infraestructura cloud de Microsoft Azure con servidores ubicados en Europa, cumpliendo con el Reglamento General de Protección de Datos (RGPD).

## **Tango**

***Link a pagina web*:** [<u>https://www.axoft.com/tango/software-de-gestion/</u>](https://www.axoft.com/tango/software-de-gestion/)

Tango Gestión es un software de gestión empresarial (ERP) desarrollado por Axoft Argentina S.A., líder del mercado argentino con más de 30 años de trayectoria. Es utilizado por PyMEs, grandes empresas, estudios contables, distribuidoras, comercios e industrias de todo el país. Su propuesta central es integrar en una sola plataforma todos los procesos administrativos, contables y operativos de una empresa, manteniéndose permanentemente actualizado con la normativa fiscal argentina.

En cuanto a las funcionalidades que ofrece, encontramos:

1.  **Contabilidad y finanzas:** Cubre todos los requerimientos de registración contable: asientos automáticos, libros diarios y mayor, balances, cierre de ejercicio, conversión de moneda y ajuste por inflación. Incluye tesorería con administración de caja, bancos, cheques y tarjetas, y conciliación bancaria automática.

2.  **Facturación e impuestos:** Permite emitir facturas electrónicas compatibles con ARCA, generar automáticamente los libros IVA Compras y Ventas, y liquidar Ingresos Brutos con convenio multilateral.

3.  **Compras, ventas y stock:** Administra el circuito completo de ventas y pedidos, órdenes de compra con autorizaciones, recepción de mercadería y cuentas corrientes de clientes y proveedores. El módulo de stock permite manejar múltiples depósitos, controlar saldos, valorizar inventario y configurar alertas de faltante.

4.  **Recursos Humanos:** Incluye liquidación de sueldos para todos los convenios de trabajo, recibos, cálculo de Ganancias, control de personal y exportación de información a organismos oficiales. Se complementa con el módulo de bienes de uso para gestionar altas, amortizaciones, revalúos y bajas con sus asientos contables correspondientes.

5.  **Integraciones y APIs:** Gracias a su API REST propia (Tango Tiendas, documentada públicamente), permite conectarse con plataformas externas, desarrollos a medida, aplicaciones móviles y servicios de terceros.

En el Anexo II se incorpora una tabla comparativa de todas las alternativas.

# ETAPA 2

# 5. Análisis de factibilidad

## Factibilidad técnica 

La factibilidad técnica analiza si el equipo cuenta con los conocimientos, herramientas y recursos tecnológicos necesarios para llevar adelante el desarrollo del sistema.

### Stack tecnológico propuesto

| **Capa** | **Tecnología** | **Justificación** |
|----|----|----|
| **Frontend** | Django/flask/tkinter | Ecosistema maduro, soporte de dashboards interactivos |
| **Backend** | Python (FastAPI) | Alto rendimiento, ecosistema IA/ML muy desarrollado |
| **OCR** | Tesseract + Google Vision API | Combinación de solución open-source y API comercial de alta precisión |
| **NLP** | spaCy + OpenAI API | Procesamiento local + capacidad semántica avanzada |
| **Base de datos** | SQL DB Type (MS SQL- MySQL, Aurora) | Relacional para datos contables, cache para procesos en tiempo real |
| **Infraestructura** | Cloud + Dockerización | Escalabilidad, despliegue automatizado y control de versiones |
| **APIs externas** | ARCA, BCRA | Integración fiscal y bancaria para el mercado argentina |

### **Habilidades del equipo vs. requerimientos del proyecto**

El equipo está conformado por tres integrantes con formación en Ingeniería en Sistemas de Información, con conocimientos en desarrollo de software, bases de datos, arquitectura de sistemas y gestión de proyectos. Adicionalmente, el equipo tiene experiencia directa con el sector contable, lo cual facilita la comprensión del dominio del problema.

| **Requerimiento técnico** | **Nivel del equipo** | **Observación** |
|----|----|----|
| Desarrollo backend (Python / Node.js) | **Alto** | Experiencia consolidada en la carrera |
| Bases de datos relacionales | **Alto** | PostgreSQL cubierto en materias de la carrera |
| Desarrollo frontend (React.js) | **Medio** | Conocimiento básico, se profundizará durante el desarrollo |
| Integración con APIs de ARCA | **Medio** | Requiere estudio de documentación técnica de ARCA |
| OCR (Tesseract / Google Vision) | **Básico** | Conocimiento teórico; implementación práctica a desarrollar |
| NLP (spaCy / OpenAI API) | **Básico** | Se utilizarán librerías y APIs existentes para reducir la brecha |
| DevOps / CI-CD / Cloud | **Básico** | Se prevén cursos específicos y uso de servicios administrados |
| Modelos predictivos / ML | **Básico** | Se integrarán mediante librerías (scikit-learn, statsmodels) |

*Estrategia para cerrar las brechas identificadas*: se realizarán cursos específicos en las áreas de menor experiencia, y se priorizará el uso de frameworks, librerías y servicios administrados por sobre el desarrollo desde cero. Esto reduce significativamente el riesgo técnico.

### **Disponibilidad de herramientas**

La mayoría de las tecnologías seleccionadas son de código abierto o cuentan con planes gratuitos o educativos. Las APIs comerciales (Google Vision, OpenAI) disponen de créditos de prueba suficientes para la etapa de desarrollo y piloto. La infraestructura cloud de AWS puede ser utilizada en su capa gratuita durante las primeras fases del proyecto.

### **Riesgos técnicos identificados** 

1.  Precisión del OCR en documentos de baja calidad o formatos no estandarizados.

2.  Variabilidad en la estructura de los comprobantes emitidos por distintos sistemas contables del mercado argentino.

3.  Cambios frecuentes en las APIs de organismos fiscales (ARCA) que pueden requerir actualizaciones periódicas.

4.  Curva de aprendizaje en la calibración de modelos NLP para terminología contable específica.

En todos estos casos se plantea una estrategia de mitigación basada en pruebas iterativas, mantenimiento continuo y el uso de proveedores con SLA definidos para las APIs críticas.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><p>Conclusión técnica:</p>
<p>El equipo cuenta con una base técnica sólida en backend, bases de datos y arquitectura de sistemas, lo que reduce el riesgo de las áreas centrales del proyecto. Las brechas detectadas (OCR, NLP, DevOps/Cloud y modelos predictivos) son abordables mediante capacitación puntual y el uso de librerías y servicios ya maduros, sin necesidad de desarrollo desde cero. Por lo tanto, la factibilidad técnica se considera VIABLE, condicionada a un plan de capacitación en las áreas de menor experiencia y a pruebas iterativas frente a la variabilidad de los comprobantes y las APIs de ARCA.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## Factibilidad Operativa

La factibilidad operativa evalúa si el sistema, una vez desarrollado, podrá ser utilizado de manera efectiva por los usuarios finales y si la organización que lo adopte estará en condiciones de sostener su operación.

### **Capacidad de los usuarios finales para adoptar el sistema** 

Los usuarios principales del sistema son contadores, administrativos y responsables financieros. En general, este perfil tiene experiencia en el uso de herramientas de gestión como Tango, ARCA web y planillas de cálculo. Se espera que la curva de adopción sea moderada, ya que el sistema busca reemplazar tareas manuales repetitivas y no requiere conocimientos técnicos avanzados.

Planificamos desarrollar una interfaz intuitiva, con guías de uso integradas y un manual de capacitación para facilitar la adopción. Además, el equipo acompañará presencialmente la etapa de capacitación para asegurar una apropiación efectiva del sistema.

*Riesgo operativo identificado:*

Algunos usuarios, especialmente los de mayor antigüedad en sus roles, pueden mostrar resistencia a abandonar procesos manuales que conocen bien. La principal preocupación no es la complejidad técnica del sistema, sino el cambio de hábitos.

*Mitigación propuesta:*

- Acompañamiento presencial del equipo de L.A.S Tech durante la etapa de piloto.

- Implementación gradual: en una primera fase el sistema convive con los procesos actuales, sin reemplazarlos abruptamente.

- Canal de soporte directo disponible durante los primeros tres meses de uso.

### **Impacto en los procesos actuales de los clientes**

Para la implementación de EugenIA se optó por no realizar una migración completa, sino por establecer un período de coexistencia entre ambos sistemas. Bajo este esquema, todo lo nuevo correspondiente al corriente año fiscal se gestionará a través de EugenIA, mientras que lo ya tratado o en curso al momento de la implementación continuará gestionándose en el sistema actual del cliente hasta su cierre. Este enfoque reduce la resistencia al cambio y facilita una transición gradual, evitando interrupciones sobre procesos contables ya iniciados.

- Carga manual de facturas y comprobantes → reemplazado por digitalización automática con OCR.

- Validación de documentos → automatizado mediante reglas de negocio y detección de anomalías.

- Generación de reportes → automatizado con dashboards en tiempo real.

- Presentación de información a organismos fiscales → integrado con APIs de ARCA.

### **Capacidad de la organización para operar el sistema internamente**

El equipo de L.A.S Tech está conformado por tres integrantes con perfiles complementarios, lo que favorece un desarrollo ágil y una adecuada distribución de responsabilidades. Sin embargo, durante el primer año de operación el equipo debe asumir simultáneamente las actividades de desarrollo, mantenimiento, soporte a usuarios, gestión de clientes y tareas administrativas, lo que representa una carga operativa considerable.

La carga operativa mensual estimada para este período se encuentra entre 190 y 240 horas, contemplando tanto las actividades técnicas como las de gestión y el apoyo de un asesor externo para los aspectos legales y normativos.

Considerando que cada integrante dedica aproximadamente 25 horas semanales al proyecto (100 horas mensuales), el equipo dispone de una capacidad total de 300 horas por mes. Esto permite cubrir la carga de trabajo prevista con un margen suficiente para afrontar imprevistos o incrementos puntuales en la demanda. No obstante, el principal riesgo identificado es la falta de redundancia dentro del equipo, ya que la ausencia temporal de alguno de sus integrantes podría afectar significativamente la continuidad de las operaciones.

La planificación de las actividades, responsables y plazos correspondientes al primer año de operación se presenta en el diagrama de Gantt incluido al final de esta entrega.

### **Capacitación y soporte** 

El plan de capacitación prevé reuniones con cada cliente durante la fase piloto, complementadas con manuales de uso y vídeos instructivos. El soporte post-implementación estará a cargo del equipo de L.A.S Tech durante los primeros 3 meses, con disponibilidad horaria extendida.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;"><p><em>Conclusión operativa:</em></p>
<p>El perfil de los usuarios finales (contadores, administrativos) y su familiaridad previa con herramientas de gestión favorecen una adopción moderada del sistema. El principal riesgo no es técnico sino cultural, resistencia al cambio de hábitos, mitigado mediante implementación gradual, acompañamiento presencial y soporte dedicado durante los primeros meses. La carga operativa estimada (190–240 hs/mes) es cubierta por la disponibilidad del equipo (300 hs/mes), aunque sin margen de redundancia ante ausencias. En consecuencia, <strong>la factibilidad operativa se considera VIABLE</strong>, sujeta a sostener la dedicación horaria comprometida por los tres integrantes.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## Factibilidad Legal

Este apartado revisa los aspectos normativos y legales que impactan sobre el desarrollo y operación del sistema.

### **Protección de datos personales**

El sistema procesará datos financieros sensibles de empresas y personas físicas. En Argentina, la protección de datos personales está regulada por la Ley 25.326 de Protección de Datos Personales y su decreto reglamentario. EugenIA deberá:

- Registrar la base de datos ante la Agencia de Acceso a la Información Pública (AAIP).

- Implementar medidas de seguridad adecuadas para proteger la confidencialidad e integridad de los datos.

- Establecer políticas de acceso diferenciado según roles de usuario.

- Definir períodos de retención de información y mecanismos de eliminación segura.

### **Normativa fiscal y cumplimiento con ARCA**

El sistema interactúa con los servicios web de ARCA (ex-AFIP), lo que requiere cumplir con sus especificaciones técnicas para la emisión de comprobantes electrónicos, consulta de CAE y presentación de información fiscal. El equipo deberá obtener los certificados digitales correspondientes y mantenerse actualizado ante cambios normativos.

### **Propiedad intelectual** 

El software desarrollado en el marco de este proyecto será propiedad de L.A.S Tech, quien conservará los derechos sobre su diseño, desarrollo e implementación. Para su construcción se prevé el uso de bibliotecas, frameworks y herramientas de terceros de código abierto, seleccionadas en función de que sus licencias sean compatibles con fines comerciales, como MIT o Apache 2.0.

Asimismo, en caso de integrar servicios o APIs externas, como las ofrecidas por Google o OpenAI, su utilización se realizará respetando los términos y condiciones establecidos por cada proveedor, sin efectuar modificaciones, redistribución ni uso indebido de los modelos o servicios proporcionados.

### **Contratos con clientes**

Como parte de la factibilidad legal del proyecto, previo a la comercialización del servicio se contempla la elaboración de contratos de prestación de servicios con cada cliente. Estos acuerdos tendrán como finalidad formalizar la relación comercial y establecer de manera clara los derechos y obligaciones de ambas partes.

Dentro de dichos contratos se incluirán aspectos vinculados al alcance del servicio ofrecido, los niveles de servicio comprometidos, la confidencialidad y protección de la información procesada, así como también los mecanismos previstos para la resolución de posibles conflictos. De esta manera, se busca contar con un marco legal adecuado que brinde seguridad y respaldo desde las primeras etapas de implementación comercial del proyecto.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;"><p><em>Conclusión legal:</em></p>
<p><em>No se identifican impedimentos normativos que bloqueen el desarrollo o la comercialización del sistema. Las obligaciones aplicables, registro de la base de datos ante la AAIP, cumplimiento de la Ley 25.326, certificación digital ante ARCA y uso de licencias de terceros compatibles con fines comerciales, son conocidas, gestionables y compatibles con el cronograma del proyecto. Por lo tanto, <strong>la factibilidad legal se considera VIABLE</strong>, debiendo incorporarse su cumplimiento desde las primeras etapas de implementación, antes de la comercialización con el primer cliente.</em></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## Factibilidad económica-financiera

El análisis económico evalúa los costos de desarrollo e implementación del sistema, los ingresos proyectados, el punto de equilibrio y la rentabilidad del proyecto mediante los indicadores VAN y TIR.

Supuestos a tener en cuenta en esta etapa:

- Se trabaja con valores en pesos argentinos, dado que el mercado objetivo son PyMEs locales.

- El período de análisis es de 5 años.

- La tasa de descuento utilizada para el cálculo del VAN es del 40% anual, considerando el contexto inflacionario del país,

> Según el índice publicado por la Federación Argentina de Consejos Profesionales de Ciencias Económicas (FACPCE), la inflación interanual se ubicó en torno al 33,2% hacia mayo de 2026, pero adoptamos una tasa de descuento del 40% anual como criterio conservador para el cálculo del VAN.

- Se proyecta la incorporación de 3 clientes en el primer año, con crecimiento progresivo.

- Los integrantes del equipo trabajan sin salario de mercado pleno durante la fase inicial, dado el carácter de startup en etapa temprana.

### **Proyección de costos**

Los costos del proyecto se dividen en costos de desarrollo (únicos) y costos operativos recurrentes.

**Costos de desarrollo (año 1):**

| **Concepto** | **Detalle** | **Valor estimado (ARS)** |
|----|----|----|
| Horas de desarrollo (3 personas x 12 meses) | ~4.320 hs totales | \$ 52.420.113,25 |
| Licencias APIs externas (año 1) | Google Vision + OpenAI | \$ 1.200.000 |
| Infraestructura cloud (AWS, año 1) | Servidores + almacenamiento | \$ 759.960 |
| Hardware de trabajo del equipo | Equipamiento | \$ 2.501.400 |
| **TOTAL COSTO DE DESARROLLO** |  | **\$ 56.881.473,25** |

***Nota sobre tarifa horaria para desarrollo utilizada***: \$12.134,29 por hora. Esta tarifa representa aproximadamente el 60% del salario promedio por hora proyectado para febrero de 2026 por el Consejo Profesional de Ciencias Informáticas de la provincia de Córdoba(CPCIPC) la cual indica un sueldo mensual de \$3.235.809,46 para el rol de Desarrollador de aplicaciones/ Desarrollador Back-end equivalente a unos \$20.223,81 al mes. Como se dijo anteriormente, se utiliza solo un 60% ya que durante la fase inicial se trabaja sin salario pleno.

**Costos operativos mensuales (a partir del año 2):**

| **Concepto** | **Costo mensual (ARS)** | **Notas** |
|----|----|----|
| Infraestructura cloud (AWS) | \$ 63.330 | Variable según uso |
| APIs de IA (OpenAI + fallback) | \$ 95.000 | Varía con volumen de documentos |
| Mantenimiento del sistema | \$ 125.000 | Soporte, actualizaciones |
| Herramientas de productividad | \$ 30.000 | GitHub, Jira, etc. |
| **TOTAL MENSUAL BASE** | **\$ 313.330** |  |
| **Con contingencia (20%)** | **\$ 376.000** |  |

### **Inversión inicial**

Se define la inversión inicial como el 30% del costo de desarrollo más la infraestructura y hardware:

***inversión inicial = 30% valor del desarrollo + infraestructura cloud + hardware***

***inversión inicial = \$ 17.064.441,98 + \$ 759.960 + \$ 2.501.400***

***inversión inicial = \$ 20.325.801,98***

### **Modelo de ingresos**

El modelo de ingresos es SaaS (Software as a Service) con suscripción mensual. Se plantean dos planes:

- **Plan PyME**: \$ 500.000/mes por empresa (hasta 500 comprobantes mensuales).

- **Plan Empresa**: \$ 1.250.000/mes por empresa (uso ilimitado + soporte prioritario).

Para el análisis de flujo de caja se utiliza un promedio de \$ 800.000/mes por cliente(asumiendo una cartera compuesta en un 60% por clientes Plan PyME y un 40% por clientes Plan Empresa), con la siguiente proyección de incorporación:

| **Año** | **Clientes activos** | **Ingreso anual (ARS)** | **Ingreso mensual promedio** |
|----|----|----|----|
| 1 | 3 | \$ 28.800.000 | \$ 2.400.000 |
| 2 | 7 | \$ 67.200.000 | \$ 5.600.000 |
| 3 | 12 | \$ 115.200.000 | \$ 9.600.000 |
| 4 | 18 | \$ 172.800.000 | \$ 14.400.000 |
| 5 | 25 | \$ 240.000.000 | \$ 20.000.000 |

### **Punto de equilibrio**

El punto de equilibrio es el momento en que los ingresos cubren exactamente los egresos operativos, sin considerar la recuperación de la inversión inicial.

Con costos operativos mensuales de aproximadamente \$376.000 (con contingencia) y un ingreso promedio de \$800.000 por cliente, se necesitan al menos 1 cliente activo para cubrir los gastos corrientes. En la práctica, el punto de equilibrio operativo se alcanza desde el inicio de las operaciones con el primer cliente incorporado.

Es importante diferenciar este punto de equilibrio operativo de la recuperación de la inversión inicial (payback), que son dos indicadores diferentes. Si bien el negocio es operativamente rentable desde el primer cliente, el flujo de caja total del Año 1 resulta negativo (-\$4.798.145,73) una vez que se descuenta la inversión inicial de \$20.325.801,98. Esto se debe a que dicha inversión se concentra en los primeros meses del proyecto, mientras que los ingresos recién comienzan a escalar con la incorporación progresiva de clientes. La inversión se recupera íntegramente durante el Año 2, cuyo flujo de caja (\$39.895.352,48) cubre tanto el déficit remanente del Año 1 como el resto del capital invertido.

### **Egresos anuales**

El saldo restante del costo de desarrollo es de \$ 39.817.031,28 que representa el 70% faltante. Este se amortiza en 18 cuotas mensuales de \$2.212.057,29, distribuidas en los primeros dos años: 6 cuotas en el año 1 y las 12 restantes en el año 2.

**Año 1:**

***Egreso anual 1 = Inversión inicial + 6x cuota de desarrollo***

***Egreso anual 1 = \$ 20.325.801,98 + 6 x \$2.212.057,29***

***Egreso anual 1 = \$33.598.145,73***

**Año 2:**

***Egreso anual 2 = infraestructura anual + 12x cuota de desarrollo***

***Egreso anual 2 = \$ 759.960 + 12 x \$2.212.057,29***

***Egreso anual 2 = \$ 27.304.647,52***

**Año 3, 4 y 5:**

A partir del año 3 el desarrollo ya está saldado. Los egresos corresponden únicamente a infraestructura cloud, licencias de APIs y mantenimiento.

***Egreso anual 3/4/5 = infraestructura + mantenimiento del sistema***

***Egreso anual 3/4/5 = \$ 759.960 + \$ 1.500.000 = \$ 2.259.960***

### **Tabla de flujo de caja**

| **Año** | **Ingresos anuales** | **Egresos anuales** | **Flujo de caja** |
|---------|----------------------|---------------------|-------------------|
| 1       | \$ 28.800.000,00     | \$33.598.145,73     | \$ -4.798.145,73  |
| 2       | \$ 67.200.000,00     | \$ 27.304.647,52    | \$ 39.895.352,48  |
| 3       | \$ 115.200.000,00    | \$ 2.259.960,00     | \$ 112.940.040,00 |
| 4       | \$ 172.800.000,00    | \$ 2.259.960,00     | \$ 170.540.040,00 |
| 5       | \$ 240.000.000,00    | \$ 2.259.960,00     | \$ 237.740.040,00 |

### **Cálculo de VAN y TIR**

El VAN (Valor Actual Neto) se calcula como la suma del valor presente de los flujos de caja futuros menos la inversión inicial, aplicando una tasa de descuento del 40% anual. La TIR (Tasa Interna de Retorno) es la tasa que hace que el VAN sea igual a cero. Ambos indicadores fueron calculados con Excel.

| **Indicador**         | **Valor**        |
|-----------------------|------------------|
| **Inversión inicial** | \$ 20.325.801,98 |
| **VAN**               | **\$94.264.798** |
| **TIR**               | **137,1%**       |

A los fines de la evaluación económica del proyecto, se adopta el escenario moderado (75% de los clientes proyectados) como referencia para los indicadores VAN y TIR, en lugar del escenario optimista. Esta decisión responde a un criterio de prudencia financiera, dado el contexto de alta inflación e incertidumbre macroeconómica de Argentina, así como el carácter de startup en etapa temprana del proyecto, resulta más conservador planificar sobre una proyección de incorporación de clientes algo menor a la base, en lugar de asumir el cumplimiento pleno de la proyección optimista.

### **Análisis de sensibilidad**

Dado que los proyectos en contextos de alta inflación presentan mayor incertidumbre, se analizaron tres escenarios según la cantidad de clientes incorporados:

| **Escenario**                   | **VAN**       | **TIR** |
|---------------------------------|---------------|---------|
| Optimista (proyección base)     | \$140.876.090 | 177,8%  |
| Moderado (75% de los clientes)  | \$94.264.798  | 137,1%  |
| Pesimista (50% de los clientes) | \$47.860.831  | 93,3%   |

En todos los escenarios, el VAN resulta ampliamente positivo y la TIR supera en gran medida la tasa de descuento del 40%, lo que confirma la viabilidad económica del proyecto incluso en contextos adversos.

### **Estrategias de financiamiento**

Si bien con los nuevos precios el flujo de caja del año 1 es positivo y cubre la inversión inicial, el proyecto puede igualmente requerir capital de trabajo durante los primeros meses de operación, previos a la consolidación de la cartera de clientes. Las estrategias que se consideran viables son:

- Fondos de fomento a la innovación: programas como el FONTAR del MINCyT, que otorgan financiamiento no reembolsable a proyectos tecnológicos.

- Concursos de emprendedorismo: convocatorias de la UTN, el BID Laboral o el programa Nación Emprendedora.

- Capital semilla de inversores ángel: a cambio de un porcentaje minoritario de la empresa en su etapa temprana.

- Reducción de costos iniciales: uso de créditos gratuitos de OpenAI y AWS para nuevos desarrolladores, y adopción de modelos open-source (Llama) para reducir dependencia de APIs pagas.

### **Escalabilidad y rentabilidad a largo plazo**

Si EugenIA logra consolidar 25 clientes activos al cabo de 5 años (escenario optimista), los ingresos anuales superan los \$240.000.000 con costos operativos de apenas \$2.259.960, lo que representa un margen bruto superior al 99%. Incluso bajo el escenario moderado adoptado como referencia (75% de la proyección, equivalente a unos 18-19 clientes activos al quinto año), el margen bruto se mantiene en niveles similares, dado que los costos operativos de mantenimiento no escalan proporcionalmente con la cantidad de clientes.

A mayor escala, el modelo permite incorporar nuevos módulos (gestión de nómina, integración con BCRA, reportes de auditoría externa) que amplían el ticket promedio por cliente sin aumentar proporcionalmente los costos. Esto posiciona a EugenIA como un sistema escalable con alta rentabilidad a largo plazo.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;"><p><em>Conclusión económica:</em></p>
<p>El proyecto presenta flujo de caja positivo desde el primer año de operación, recupera la inversión inicial en el corto plazo y exhibe un VAN positivo y una TIR que supera ampliamente la tasa de descuento (40%) en los tres escenarios analizados (optimista, moderado y pesimista). El principal punto de atención es la necesidad de capital de trabajo durante los primeros meses, para lo cual se identificaron alternativas concretas de financiamiento (FONTAR, concursos de emprendedorismo, capital semilla). En consecuencia, <strong>la factibilidad económica se considera VIABLE</strong>, incluso bajo supuestos conservadores de incorporación de clientes.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## Conclusión de factibilidad 

A partir del análisis realizado en las distintas dimensiones de factibilidad, se concluye que el proyecto EugenIA es viable y se recomienda avanzar con su desarrollo. A continuación se resumen los puntos clave de cada dimensión analizada:

| **Dimensión** | **Resultado** | **Observación principal** |
|----|----|----|
| Factibilidad Operativa | **VIABLE** | Equipo con capacidad suficiente. Requiere MVP acotado y plan de capacitación. |
| Factibilidad Técnica | **VIABLE** | Stack maduro y documentado. Brechas de conocimiento abordables con capacitación. |
| Factibilidad Legal | **VIABLE** | Sin impedimentos legales. Requiere cumplimiento de Ley 25.326 y certificados ARCA. |
| Factibilidad Económica | **VIABLE** | VAN positivo en todos los escenarios. Requiere financiamiento para cubrir el déficit del año 1. |

Desde el punto de vista técnico, el equipo cuenta con la formación necesaria y el stack tecnológico elegido es adecuado y con amplio soporte. Las brechas identificadas son manejables con capacitación específica y el uso estratégico de librerías y APIs existentes.

En cuanto a la factibilidad operativa, el sistema está diseñado para integrarse gradualmente con los procesos existentes de los clientes, minimizando la fricción durante la adopción. La carga operativa del equipo en el primer año es manejable, siempre que se mantenga una buena organización interna y se automaticen las tareas repetitivas.

Respecto a la dimensión legal, no se identificaron obstáculos normativos que impidan el desarrollo, y las acciones necesarias para el cumplimiento son parte del plan de implementación desde el inicio.

Finalmente, el análisis económico demuestra que el proyecto es rentable incluso bajo supuestos conservadores. Con una inversión inicial de \$20.325.801,98 se proyecta un VAN de \$94.264.798 y una TIR del 137,1% en el escenario moderado. El único punto de atención es el financiamiento del déficit del primer año, para el cual se identificaron estrategias concretas y accesibles.

En síntesis, EugenIA presenta condiciones favorables en todos los ejes analizados, lo que justifica su desarrollo como Proyecto Final y su posterior lanzamiento al mercado como solución tecnológica para el sector contable argentino.

# Precio y forma de pago

## Criterios de fijación de precios

La definición de los precios de EugenIA responde a un análisis combinado de tres factores: el costo real del servicio (infraestructura, APIs de IA y mantenimiento), el valor que el sistema genera para cada segmento de cliente, y la necesidad de recuperar la inversión inicial en un plazo máximo de dos años.

En el mercado local de soluciones SaaS para administración contable y documental, los precios de referencia para herramientas de automatización de comprobantes oscilan entre \$ 200.000 y \$ 900.000 mensuales según funcionalidad y volumen. EugenIA se posiciona en ese rango con una propuesta de valor diferencial: procesamiento inteligente basado en IA, integración con ARCA y generación automática de reportes, a un costo operativo propio de apenas \$ 376.000 mensuales.

El precio del Plan PyME se estableció en \$ 500.000/mes como punto de entrada accesible para empresas de menor escala, cubriendo ampliamente los costos operativos desde el primer cliente y generando margen desde el inicio. El Plan Empresa, a \$ 1.250.000/mes, refleja el mayor volumen de procesamiento, el soporte prioritario y el valor estratégico que representa para organizaciones con operaciones más complejas.

## Planes disponibles

| **PLAN PyME — \$ 500.000 / mes** |
|----|
| hasta 500 comprobantes mensuales |
| Procesamiento de facturas, remitos y recibos \| Integración con ARCA \| Panel de control y reportes básicos \| Soporte estándar (48 hs habiles) \| Actualizaciones incluidas |

| **PLAN EMPRESA — \$ 1.250.000 / mes** |
|----|
| volumen ilimitado de comprobantes |
| Todo lo incluido en Plan PyME \| Procesamiento ilimitado de documentos \| Módulos avanzados de auditoría y nómina \| Integración con sistemas contables externos \| Soporte prioritario (4 hs hábiles) |

## Forma de pago

La suscripción se abona de forma mensual, con las siguientes condiciones:

| **Condición** | **Detalle** |
|----|----|
| Periodicidad | Mensual, por adelantado (primeros 4 días hábiles de cada mes) |
| Medio de pago | Transferencia bancaria CBU / CVU |
| Vencimiento | 5 días hábiles desde la emisión de la factura |
| Facturación | Factura A o B según condición impositiva del cliente |
| Ajuste de precio | Revisión semestral según variación del IPC (INDEC) |
| Penalidad por mora | Interés del 3% mensual sobre el saldo vencido |

***Nota sobre actualización de precios:** Dado el contexto macroeconómico argentino, los precios se expresan en pesos y se ajustan semestralmente por IPC. Esta política garantiza la sostenibilidad del servicio y protege el margen operativo del proyecto frente a variaciones inflacionarias, asegurando la continuidad y calidad del sistema para todos los clientes activos*

# Análisis de Factibilidad (Tango) 

**Desde el punto de vista técnico**, Tango es un ERP robusto y ampliamente probado en Argentina, con más de 30 años de evolución. Cuenta con una arquitectura modular (Contabilidad, Ventas, Compras, Stock, Sueldos, etc.), total integración entre módulos y fuerte compatibilidad con facturación electrónica, controladores fiscales y normativas locales. El stack es estable, aunque tradicional (no nativo cloud en todas sus versiones, aunque ofrece Tango Nube). Las brechas técnicas suelen resolverse con partners certificados.

**En cuanto a la factibilidad operativa**, el sistema es intuitivo para usuarios con experiencia contable, pero requiere un proceso de implementación y capacitación significativo (especialmente en PyMEs). Su gran ventaja es la alta compatibilidad con los flujos de trabajo existentes en estudios contables y empresas argentinas, lo que reduce la curva de adopción una vez implementado. La carga operativa posterior es baja gracias a la automatización de procesos repetitivos.

**Respecto a la dimensión legal**, Tango destaca por su excelente cumplimiento normativo. Está permanentemente actualizado con las exigencias de ARCA, ARBA, y demás organismos. No presenta obstáculos legales relevantes y facilita el cumplimiento de la Ley de Protección de Datos Personales (25.326).

**Finalmente, el análisis económico** muestra que, si bien la inversión inicial y los costos recurrentes son significativos (licencias mensuales desde ~\$600.000 + IVA en la nube, más implementación y módulos adicionales), representa una opción de bajo riesgo por su trayectoria y ecosistema de soporte. El retorno se obtiene principalmente por la reducción de errores, ahorro de tiempo y mejor control administrativo, aunque el payback es más largo que soluciones más modernas y livianas.

**En síntesis**, Tango Gestión es una solución altamente viable y de bajo riesgo técnico y legal, ampliamente aceptada en el mercado argentino. Su principal desafío radica en los costos y la rigidez relativa frente a soluciones más ágiles y basadas en IA. Resulta especialmente recomendable para empresas que priorizan estabilidad, cumplimiento normativo y ecosistema local consolidado.

A partir del análisis realizado en las distintas dimensiones de factibilidad, se concluye que **la implementación del sistema Tango Gestión es viable** y representa una solución madura y confiable para la gestión contable y administrativa en el mercado argentino. A continuación, se resumen los puntos clave de cada dimensión:

| **Dimensión** | **Resultado** | **Observación principal** |
|----|----|----|
| **Factibilidad Operativa** | **VIABLE** | Alta adopción en el mercado. Requiere capacitación inicial y posible reingeniería de procesos. |
| **Factibilidad Técnica** | **VIABLE** | Plataforma madura con excelente soporte local. Integración probada con ARCA y otros sistemas. |
| **Factibilidad Legal** | **VIABLE** | Totalmente adaptado a la normativa argentina. Cumple con Ley 25.326 y actualizaciones constantes de ARCA/ARBA. |
| **Factibilidad Económica** | **VIABLE** | Inversión conocida y predecible. Buen retorno a mediano plazo, aunque con costos elevados de licenciamiento y mantenimiento. |

# Diagrama de Gantt

El proyecto fue estructurado en siete etapas principales, incorporando tanto la selección del proyecto como la elaboración del abstract dentro de la planificación inicial. Las etapas definidas son: Abstract, Análisis, Diseño, Codificación, Ajuste, Piloto y Puesta en marcha final.

Cada una de estas etapas se encuentra desagregada mediante una Estructura de Desglose del Trabajo (EDT) de carácter complejo, lo que permite identificar, organizar y gestionar de manera detallada las tareas específicas involucradas en el desarrollo del proyecto.

Si bien el diagrama presenta las etapas de manera organizada, esto no implica que el desarrollo se realice siguiendo una secuencia estrictamente lineal. En concordancia con la metodología Scrum adoptada, el trabajo se ejecutará iterativamente mediante *sprints*, durante los cuales se desarrollarán, validarán y ajustarán incrementos funcionales del sistema.

El diagrama de Gantt correspondiente se presenta en el Anexo I. En el mismo el porcentaje de completitud de una tarea se denota en la linea negra que la atraviesa al medio (o la ausencia de la misma)

Los roles del proyecto son:

- Team Leader (Tulián, Maria Laura)

- Product Owner / QA / DBA (Cortéz, Agustín)

- Scrum Master / Desarrollo / Arquitectura / DevOps (Tombolini, Santiago A.)

Las etapas del proyecto y sus responsables son las siguientes

**Abstract**

- Team Leader / Product Owner

**Análisis**

- Team Leader / Product Owner

- QA / DBA

**Diseño**

- Desarrollo / Arquitectura / DevOps

- QA / DBA

**Codificación**

- Desarrollo / Arquitectura / DevOps

**Ajuste**

- QA / DBA

- Desarrollo / Arquitectura / DevOps

**Piloto**

- Team Leader / Product Owner

- QA / DBA

- Desarrollo / Arquitectura / DevOps

**Puesta en marcha final**

- Team Leader / Product Owner

- QA / DBA

- Desarrollo / Arquitectura / DevOps

# ETAPA 3

# Análisis de datos

El modelo de datos de EugenIA define la estructura de la base de datos y las relaciones entre las entidades que intervienen en el sistema. Su diseño busca mantener la integridad y consistencia de la información, facilitando la gestión de los procesos comerciales, contables y documentales.

A continuación, se presenta el Diagrama Entidad-Relación (DER), que representa las entidades, sus atributos, las claves primarias y foráneas y las relaciones establecidas entre ellas.



# Definición de metodología 

Como metodología para el desarrollo elegimos Scrum, esta elección responde principalmente a las características particulares del proyecto EugenIA y al contexto en el que será desarrollado. A diferencia de los sistemas tradicionales, cuyos requerimientos suelen estar claramente definidos desde el inicio, EugenIA incorpora componentes innovadores basados en Inteligencia Artificial, Reconocimiento Óptico de Caracteres (OCR), Procesamiento de Lenguaje Natural (NLP) e integración con organismos externos como ARCA y potencialmente BCRA. Estas tecnologías presentan un alto grado de incertidumbre técnica, ya que gran parte de su comportamiento y efectividad solo puede validarse mediante pruebas reales e iteraciones sucesivas.

En este contexto, un enfoque tradicional como Waterfall implicaría definir exhaustivamente todos los requisitos al comienzo del proyecto y postergar la validación de los resultados hasta etapas avanzadas del desarrollo. Esto representaría un riesgo considerable, debido a que funcionalidades críticas como la detección de errores contables, el procesamiento automático de comprobantes o la generación de recomendaciones financieras inteligentes podrían requerir ajustes continuos a medida que se obtengan datos reales y retroalimentación de los usuarios. Scrum permite abordar esta problemática mediante ciclos cortos de desarrollo denominados sprints, en los que se construyen incrementos funcionales del producto, se validan tempranamente y se incorporan mejoras de manera continua.

Otro factor determinante es la necesidad de mantener una interacción permanente con los futuros usuarios del sistema. EugenIA está orientado a contadores, administrativos y responsables financieros, quienes poseen amplio conocimiento del negocio pero pueden descubrir nuevas necesidades o identificar oportunidades de mejora una vez que interactúan con prototipos funcionales. La filosofía de Scrum favorece precisamente esta dinámica, permitiendo mostrar avances periódicos, recopilar observaciones y adaptar el Product Backlog en función de las necesidades reales detectadas durante el proyecto. De esta forma, el sistema evoluciona junto con el conocimiento adquirido y se minimiza el riesgo de desarrollar funcionalidades que no aporten suficiente valor al cliente.

En base a esta metodología, se define lo siguiente:

El proyecto se desarrollará en sprints de 2 a 4 semanas y se espera tener el primer prototipo completo en no menos de 4 meses.

- El Rol de TL será llevado a cabo por Laura Tulian.

- El Rol de Product Owner será llevado a cabo por Agustín Cortéz.

- Y el Scrum Master estará compuesto por Tombolini Santiago.

El proyecto utilizará un repositorio git para el manejo de versiones.

# Cálculo de tamaño de sistema

Para estimar el tamaño funcional de EugenIA, se utiliza el método de Puntos de Función (PF), que permite cuantificar las funcionalidades que ofrece el sistema desde la perspectiva del usuario. Para ello, se identifican y clasifican las funciones de transacción, entradas externas (EE), salidas externas (SE) y consultas externas (CE)— y las funciones de datos, archivos lógicos internos (ALI) y archivos de interfaz externa (AIE)—, asignándoles un puntaje según su complejidad.

A partir de esta clasificación, se calculan los Puntos de Función No Ajustados (PFNA) y, posteriormente, se determina el Valor del Factor de Ajuste (VAF), con el objetivo de obtener una estimación del tamaño funcional total del sistema.

**Caso de uso 1: Registrar venta. PF 20**

1.  EE: Registrar venta/comprobante. Compleja = **6 PF**

2.  EE: Dar de alta cliente. Baja = **3 PF**

3.  EE: Dar de alta cuenta contable. Baja = **3 PF**

4.  SE: Generar y mostrar asiento contable. Media = **5 PF**

5.  CE: Buscar/seleccionar cliente. Baja = **3 PF**

**Total: 20 PF**

**Caso de uso 2: Registrar compra. PF 20**

1.  EE: Registrar compra/comprobante. Compleja = **6 PF**

2.  EE: Dar de alta proveedor. Baja = **3 PF**

3.  EE: Dar de alta cuenta contable. Baja = **3 PF**

4.  SE: Generar y mostrar asiento contable. Media = **5 PF**

5.  CE: Buscar/seleccionar proveedor. Baja = **3 PF**

**Total: 20 PF**

**Caso de uso 3: Gestionar Libro Diario. PF 14**

1.  CE: Consultar Libro Diario utilizando filtros. Media = **4 PF**

2.  CE: Consultar detalle de asiento. Baja = **3 PF**

3.  EE: Modificar asiento contable. Media = **4 PF**

4.  EE: Anular asiento contable. Baja = **3 PF**

**Total: 14 PF**

**Caso de uso 4: Registrar asiento manual. PF 14**

1.  EE: Registrar asiento contable manual. Compleja = **6 PF**

2.  SE: Calcular, validar y mostrar el asiento con totales de Debe y Haber. Media = **5 PF**

3.  CE: Seleccionar/consultar cuentas contables para imputación. Baja = **3 PF**

**Total: 14 PF**

**Caso de uso 5: Gestionar Plan de Cuentas. PF 18**

1.  EE: Alta de cuenta contable. Media = **4 PF**

2.  EE: Modificación de cuenta contable. Media = **4 PF**

3.  EE: Baja lógica de cuenta contable. Baja = **3 PF**

4.  CE: Consultar listado de cuentas vigentes. Baja = **3 PF**

5.  CE: Consultar detalle de una cuenta e historial de movimientos. Media = **4 PF**

**Total: 18 PF**

**Caso de uso 6: Consultar Libro Mayor. PF 7**

1.  SE: Consultar movimientos y calcular saldo inicial, Debe, Haber y saldo final. Compleja = **7 PF**

**Total: 7 PF**

**Caso de uso 7: Gestionar Clientes. PF 15**

1.  EE: Alta de cliente. Media = **4 PF**

2.  EE: Modificación de cliente. Media = **4 PF**

3.  EE: Baja lógica/desactivación de cliente. Baja = **3 PF**

4.  CE: Consultar cliente e historial de comprobantes asociados. Media = **4 PF**

**Total: 15 PF**

**Caso de uso 8: Gestionar Proveedores. PF 15**

1.  EE: Alta de proveedor. Media = **4 PF**

2.  EE: Modificación de proveedor. Media = **4 PF**

3.  EE: Baja lógica/desactivación de proveedor. Baja = **3 PF**

4.  CE: Consultar proveedor e historial de comprobantes asociados. Media = **4 PF**

**Total: 15 PF**

**Caso de uso 9: Generar Balance General. PF 12**

1.  SE: Generar Balance General, calcular subtotales y totales y validar igualdad patrimonial. Compleja = **7 PF**

2.  SE: Informar diferencia patrimonial detectada. Media = **5 PF**

**Total: 12 PF**

**Caso de uso 10: Generar Estado de Resultados. PF 7**

1.  SE: Generar Estado de Resultados, calcular subtotales y Resultado del Ejercicio. Compleja = **7 PF**

**Total: 7 PF**

**Caso de uso 11: Exportar Libro Diario. PF 7**

1.  SE: Generar y exportar Libro Diario en PDF o Excel. Compleja = **7 PF**

**Total: 7 PF**

**Caso de uso 12: Exportar Libro Mayor. PF 7**

1.  SE: Generar y exportar movimientos y saldos del Libro Mayor en PDF o Excel. Compleja = **7 PF**

**Total: 7 PF**

**Caso de uso 13: Consultar Historial de Auditoria. PF 4**

1.  CE: Consultar historial de auditoría mediante filtros. Media = **4 PF**

**Total: 4 PF**

**Caso de uso 14: Exportar Libro IVA a ARCA. PF 19**

1.  SE: Generar archivo de comprobantes. Compleja = **7 PF**

2.  SE: Generar archivo de alícuotas de IVA. Compleja = **7 PF**

3.  SE: Validar estructura y datos de exportación. Media = **5 PF**

**Total: 19 PF**

**Caso de uso 15: Iniciar sesión. PF 12**

1.  EE: Autenticar usuario mediante correo, contraseña y token 2FA. Media = **4 PF**

2.  EE: Restablecer/cambiar contraseña. Media = **4 PF**

3.  SE: Generar y enviar token de autenticación 2FA. Baja = **4 PF**

**Total: 12 PF**

**Caso de uso 16: Registrar comprobante con OCR/NLP. PF 17**

1.  EE: Cargar y registrar comprobante digital. Compleja = **6 PF**

2.  EE: Corregir/completar datos extraídos mediante OCR/NLP. Media = **4 PF**

3.  SE: Procesar OCR/NLP y presentar información estructurada obtenida. Compleja = **7 PF**

**Total: 17 PF**

**Caso de uso 17: Validar comprobante con ARCA. PF 11**

1.  EE: Actualizar estado fiscal del comprobante según la validación. Media = **4 PF**

2.  SE: Validar vigencia del CAE, comparar información e informar el resultado. Compleja = **7 PF**

**Total: 11 PF**

**Caso de uso 19: Gestionar Alertas de Auditoría. PF 8**

1.  CE: Consultar listado de alertas pendientes y detalle de inconsistencias. Media = **4 PF**

2.  EE: Registrar acción/observación sobre una alerta y actualizar su estado. Media = **4 PF**

**Total: 8 PF**

**Caso de uso 20: Consultar Dashboard Financiero. PF 12**

1.  SE: Calcular y visualizar indicadores, métricas y gráficos financieros. Compleja = **7 PF**

2.  SE: Actualizar indicadores y visualizaciones según filtros o período. Media = **5 PF**

**Total: 12 PF**

**Caso de uso 21: Generar Reportes Automáticos. PF 15**

1.  CE: Consultar tipos de reportes disponibles. Baja = **3 PF**

2.  SE: Procesar información y generar reporte. Compleja = **7 PF**

3.  SE: Emitir/exportar reporte en el formato seleccionado. Media = **5 PF**

**Total: 15 PF**

**Caso de uso 22: ABM Usuario. PF 11**

1.  EE: Alta de usuario. Media = **4 PF**

2.  EE: Modificación de usuario y permisos. Media = **4 PF**

3.  EE: Baja/desactivación de usuario. Baja = **3 PF**

**Total: 11 PF**

**Caso de uso 24: Consultar Estado de Comprobante. PF 7**

1.  CE: Consultar estado actual del comprobante. Baja = **3 PF**

2.  CE: Consultar historial de validaciones e inconsistencias del comprobante. Media = **4 PF**

**Total: 7 PF**

**Caso de uso 25: Obtener Recomendaciones Financieras Inteligentes. PF 18**

1.  SE: Analizar información histórica, calcular indicadores e identificar tendencias y patrones. Compleja = **7 PF**

2.  SE: Generar y clasificar recomendaciones financieras con justificación. Compleja = **7 PF**

3.  CE: Consultar detalle, indicadores y tendencias asociados a una recomendación. Media = **4 PF**

**Total: 18 PF**

**Funciones de Datos**

ALI

- Ventas / Comprobantes = **7 PF**

- Compras / Comprobantes = **7 PF**

- Clientes = **7 PF**

- Proveedores = **7 PF**

- Plan de Cuentas = **7 PF**

- Asientos / Libro Diario = **7 PF**

- Libro Mayor / Saldos Contables = **7 PF**

- Movimientos Contables = **7 PF**

- Historial de Auditoría = **7 PF**

- Alertas de Auditoría = **7 PF**

- Usuarios = **7 PF**

- Comprobantes y Estado Fiscal = **7 PF**

- Comprobantes Digitalizados y Datos Estructurados = **7 PF**

- Información Contable Auditada = **7 PF**

- Información Contable / Financiera = **7 PF**

- Comprobantes y Estado de Procesamiento = **7 PF**

- Recomendaciones Financieras = **7 PF**

**Subtotal ALI = 119 PF**

AIE

- Padrón de ARCA = **5 PF**

- Información Fiscal de Comprobantes obtenida desde ARCA = **5 PF**

**Subtotal AIE = 10 PF**

## Tabla de puntos de función



## Puntos de función no ajustados (PFNA)

| **CUU** | **Var** | **Descripción** | **Complejidad** | **Valuación (PF)** |
|----|----|----|----|----|
| **CUU-001 Registrar venta** | EE | Registrar venta/comprobante | Complejo | 6 |
|  | EE | Dar de alta cliente | Bajo | 3 |
|  | EE | Dar de alta cuenta contable | Bajo | 3 |
|  | SE | Generar y mostrar asiento contable | Medio | 5 |
|  | CE | Buscar/seleccionar cliente | Bajo | 3 |
| **CUU-002 Registrar compra** | EE | Registrar compra/comprobante | Complejo | 6 |
|  | EE | Dar de alta proveedor | Bajo | 3 |
|  | EE | Dar de alta cuenta contable | Bajo | 3 |
|  | SE | Generar y mostrar asiento contable | Medio | 5 |
|  | CE | Buscar/seleccionar proveedor | Bajo | 3 |
| **CUU-003 Gestionar Libro Diario** | CE | Consultar Libro Diario utilizando filtros | Medio | 4 |
|  | CE | Consultar detalle de asiento | Bajo | 3 |
|  | EE | Modificar asiento contable | Medio | 4 |
|  | EE | Anular asiento contable | Bajo | 3 |
| **CUU-004 Registrar asiento manual** | EE | Registrar asiento contable manual | Complejo | 6 |
|  | SE | Calcular, validar y mostrar el asiento con totales de Debe y Haber | Medio | 5 |
|  | CE | Seleccionar/consultar cuentas contables para imputación | Bajo | 3 |
| **CUU-005 Gestionar Plan de Cuentas** | EE | Alta de cuenta contable | Medio | 4 |
|  | EE | Modificación de cuenta contable | Medio | 4 |
|  | EE | Baja lógica de cuenta contable | Bajo | 3 |
|  | CE | Consultar listado de cuentas vigentes | Bajo | 3 |
|  | CE | Consultar detalle de una cuenta e historial de movimientos | Medio | 4 |
| **CUU-006 Consultar Libro Mayor** | SE | Consultar movimientos y calcular saldo inicial, Debe, Haber y saldo final | Complejo | 7 |
| **CUU-007 Gestionar Clientes** | EE | Alta de cliente | Medio | 4 |
|  | EE | Modificación de cliente | Medio | 4 |
|  | EE | Baja lógica/desactivación de cliente | Bajo | 3 |
|  | CE | Consultar cliente e historial de comprobantes asociados | Medio | 4 |
| **CUU-008 Gestionar Proveedores** | EE | Alta de proveedor | Medio | 4 |
|  | EE | Modificación de proveedor | Medio | 4 |
|  | EE | Baja lógica/desactivación de proveedor | Bajo | 3 |
|  | CE | Consultar proveedor e historial de comprobantes asociados | Medio | 4 |
| **CUU-009 Generar Balance General** | SE | Generar Balance General, calcular subtotales y totales y validar igualdad patrimonial | Complejo | 7 |
|  | SE | Informar diferencia patrimonial detectada | Medio | 5 |
| **CUU-010 Generar Estado de Resultados** | SE | Generar Estado de Resultados, calcular subtotales y Resultado del Ejercicio | Complejo | 7 |
| **CUU-011 Exportar Libro Diario** | SE | Generar y exportar Libro Diario en PDF o Excel | Complejo | 7 |
| **CUU-012 Exportar Libro Mayor** | SE | Generar y exportar movimientos y saldos del Libro Mayor en PDF o Excel | Complejo | 7 |
| **CUU-013 Consultar Historial de Auditoria** | CE | Consultar historial de auditoría mediante filtros | Medio | 4 |
| **CUU-014 Exportar Libro IVA a ARCA** | SE | Generar archivo de comprobantes | Complejo | 7 |
|  | SE | Generar archivo de alícuotas de IVA | Complejo | 7 |
|  | SE | Validar estructura y datos de exportación | Medio | 5 |
| **CUU-15 Iniciar sesión** | EE | Autenticar usuario mediante correo, contraseña y token 2FA | Medio | 4 |
|  | EE | Restablecer/cambiar contraseña | Medio | 4 |
|  | SE | Generar y enviar token de autenticación 2FA | Bajo | 4 |
| **CUU-016 Registrar comprobante con OCR/NLP** | EE | Cargar y registrar comprobante digital | Complejo | 6 |
|  | EE | Corregir/completar datos extraídos mediante OCR/NLP | Medio | 4 |
|  | SE | Procesar OCR/NLP y presentar información estructurada obtenida | Complejo | 7 |
| **CUU-017 Validar comprobante con ARCA** | EE | Actualizar estado fiscal del comprobante según la validación | Medio | 4 |
|  | SE | Validar vigencia del CAE, comparar información e informar el resultado | Complejo | 7 |
| **CUU-18 Gestionar Usuarios** | EE | Alta de usuario | Medio | 4 |
|  | EE | Modificación de usuario y permisos | Medio | 4 |
|  | EE | Baja/desactivación de usuario | Bajo | 3 |
| **CUU-019 Gestionar Alertas de Auditoría** | CE | Consultar listado de alertas pendientes y detalle de inconsistencias | Medio | 4 |
|  | EE | Registrar acción/observación sobre una alerta y actualizar su estado | Medio | 4 |
| **CUU-020 Generar Reportes Automáticos** | CE | Consultar tipos de reportes disponibles | Bajo | 3 |
|  | SE | Procesar información y generar reporte | Complejo | 7 |
|  | SE | Emitir/exportar reporte en el formato seleccionado | Medio | 5 |
| **CUU-021 Consultar Dashboard Financiero** | SE | Calcular y visualizar indicadores, métricas y gráficos financieros | Complejo | 7 |
|  | SE | Actualizar indicadores y visualizaciones según filtros o período | Medio | 5 |
| **CUU-022 Consultar Estado de Comprobante** | CE | Consultar estado actual del comprobante | Bajo | 3 |
|  | CE | Consultar historial de validaciones e inconsistencias del comprobante | Medio | 4 |
| **CUU-023 Obtener Recomendaciones Financieras Inteligentes** | SE | Analizar información histórica, calcular indicadores e identificar tendencias y patrones | Complejo | 7 |
|  | SE | Generar y clasificar recomendaciones financieras con justificación | Complejo | 7 |
|  | CE | Consultar detalle, indicadores y tendencias asociados a una recomendación | Medio | 4 |
| **Total PFNA** |  | 119 - ALI | 10 - AIE | 419 |

## Cálculo del Valor de Ajuste

El Factor de Ajuste de Valor (conocido como VAF por sus siglas en inglés, Value Adjustment Factor, o FA) es un componente clave en la metodología de Puntos de Función (IFPUG) que permite contemplar la complejidad técnica, operativa y del entorno donde se ejecutará un sistema de software.

Mientras que los Puntos de Función No Ajustados (PFNA) miden exclusivamente la funcionalidad que requiere el usuario (entradas, salidas, consultas y archivos de datos), el VAF pondera las características técnicas y ambientales del proyecto (como el rendimiento, la seguridad, el procesamiento distribuido o la facilidad de uso) para ajustar el tamaño final del software.

Este valor se calcula mediante la evaluación de las 14 GSC (General System Characteristics), como “comunicación de datos”, “procesamiento complejo”, “reusabilidad” entre otros. A cada una de estas se le asigna una puntuación de 0 a 5 según su grado de influencia:

> **0:** Sin influencia
>
> **1:** Incidental
>
> **2:** Moderada
>
> **3:** Media
>
> **4:** Significativa
>
> **5:** Esencial

Luego, se suman los puntajes de las 14 características para obtener el **TDI** (*Total Degree of Influence*), cuyo valor va desde **0** (mínima complejidad) hasta **70** (máxima complejidad):

| **Característica General del Sistema (GSC)** | **Puntaje** | **Justificación según el Sistema** |
|----|----|----|
| **Comunicación de Datos** | 4 | El sistema realiza transferencias continuas de datos e integración vía APIs externas con organismos fiscales (ARCA), BCRA y servicios de procesamiento OCR/NLP |
| **Procesamiento Distribuido** | 3 | La lógica de negocio y procesamiento se distribuye entre el cliente (web/dashboard), el servidor backend y APIs externas SaaS. |
| **Rendimiento** | 3 | Requiere alta respuesta en la validación fiscal, extracción de comprobantes en tiempo real y alertas preventivas sin cuellos de botella. |
| **Configuración Fuertemente Utilizada** | 3 | El entorno de ejecución debe gestionar la concurrencia en horas pico de procesamiento contable y cierre de ejercicio fiscal. |
| **Tasa de Transacciones** | 3 | Maneja volumen elevado de registros de comprobantes y consultas concurrentes, con procesamiento frecuente pero no crítico de tipo milisegundo bancario. |
| **Entrada de Datos en Línea** | 4 | La interacción, carga interactiva de parámetros, consultas de comprobantes e historiales se ejecutan mediante interfaces web en línea. |
| **Eficiencia del Usuario Final** | 5 | La razón de ser del sistema es automatizar tareas manuales mediante OCR/NLP, minimizando errores y aumentando al máximo la eficiencia del usuario contable. |
| **Actualización en Línea** | 4 | Transacciones como el alta de movimientos contables y actualización de estado fiscal de comprobantes se impactan de forma inmediata en las bases de datos. |
| **Procesamiento Complejo** | 5 | Alto nivel de complejidad lógica: modelos de NLP, reconocimiento OCR, reglas de auditoría de duplicidad, validaciones normativas y algoritmos predictivos. |
| **Reusabilidad** | 2 | Módulos transversales (autenticación, gestión de clientes, motores de validación) diseñados para ser reutilizados en un esquema multi-empresa o multi-cliente |
| **Facilidad de Instalación** | 1 | Despliegue en la nube mediante tecnología de contenedores (Docker) que facilita la puesta en marcha sin complejidades excesivas para el usuario final. |
| **Facilidad de Operación** | 3 | Automatización de respaldos, monitoreo autónomo de APIs fiscales y notificaciones de cambios normativos sin requerir intervención manual constante. |
| **Localizaciones Múltiples** | 1 | Diseñado para ser accedido por múltiples empresas y usuarios en distintas ubicaciones geográficas. |
| **Facilidad de Cambio / Flexibilidad** | 2 | Alta flexibilidad parametrizable para ajustar reglas de duplicidad, parámetros predictivos y adaptarse a cambios normativos de ARCA. |

Desde la planilla podemos ver que el TDI da un valor de **43 puntos**

## Rango de Variación del VAF

El VAF siempre se encuentra en un rango entre 0.65 y 1.35, lo que significa que la complejidad técnica puede modificar el tamaño funcional del sistema en hasta un ±35:

- **VAF = 0.65 (TDI = 0)**: El entorno técnico es extremadamente simple y reduce los puntos de función no ajustados en un 35%.

- **VAF = 1.00 (TDI = 35)**: Complejidad técnica promedio; el tamaño del sistema no sufre modificaciones.

- **VAF = 1.35 (TDI = 70)**: Alta complejidad técnica e integración; incrementa el tamaño del sistema en un 35%.

## Cálculo de Puntos de Función Ajustados (PFA)

$`VFA = 0,65\  + (0.01\ *\ TDI)\  = \ 0.65\  + \ (0.01\ *\ 43)\  = \ 1.08`$

$`PFA\  = \ PFNA\ *\ VFA\  = 419*\ 1.08\  = \ 452,52`$

## Conclusión cálculo del tamaño 

El tamaño funcional de **EugenIA** se determinó mediante el método de Puntos de Función, obteniendo un total de **419 Puntos de Función No Ajustados (PFNA)** a partir de las funcionalidades identificadas en los casos de uso. Aplicando un **Factor de Ajuste de Valor (VAF) de 1,08**, correspondiente a un **Grado Total de Influencia (TDI) de 43**, el tamaño final del sistema resulta de **452.52 PFA**

Por lo tanto, **EugenIA presenta un tamaño funcional estimado de 452.52 Puntos de Función Ajustados**. El incremento del **8 %** respecto del tamaño funcional base refleja la influencia de las características generales del sistema sobre su implementación.

En términos de complejidad técnica e integración, este ajuste permite caracterizar al proyecto como un sistema con un nivel de complejidad moderadamente alto. Esta valoración es coherente con las funcionalidades relevadas, que combinan procesamiento automatizado de información, OCR/NLP, integración con servicios externos como ARCA, generación de información contable y financiera, controles de auditoría y funcionalidades de análisis inteligente.

En conclusión, los 452.52 PFA no solo representan la magnitud funcional de eugenIA, sino también un sistema cuya implementación requiere resolver múltiples mecanismos de procesamiento, integración y control. Por ello, el tamaño obtenido resulta consistente con una solución de complejidad técnica e integración moderadamente alta, superior a la que correspondería a una aplicación puramente.

<table>
<colgroup>
<col style="width: 57%" />
<col style="width: 42%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Concepto</strong></th>
<th style="text-align: center;"><strong>Valor</strong></th>
</tr>
<tr>
<th><p><strong>Puntos de Función No Ajustados</strong></p>
<p><strong>(PFNA)</strong></p></th>
<th style="text-align: center;">419</th>
</tr>
<tr>
<th><em>Total Degree of Influence</em></th>
<th style="text-align: center;">43</th>
</tr>
<tr>
<th><strong>Fórmula de Ajuste</strong></th>
<th style="text-align: center;">(0.65 + 0.01 * FA)</th>
</tr>
<tr>
<th><strong>Puntos de Función Ajustados (PFA)</strong></th>
<th style="text-align: center;"><strong>452.52</strong></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# Diseño

A continuación, se enumeran los casos de uso identificados para el sistema, acompañados de una breve descripción de la funcionalidad que representa cada uno. Posteriormente, se desarrolla cada caso de uso en detalle en la sección de Análisis.

| **Código** | **Caso de uso** | **Descripción** |
|----|----|----|
| **CUU-001** | Registrar venta | Registrar una venta y generar automáticamente el asiento contable correspondiente. |
| **CUU-002** | Registrar compra | Registrar una compra y generar automáticamente el asiento contable correspondiente. |
| **CUU-003** | Gestionar Libro Diario | Consultar los asientos registrados y gestionar su modificación o anulación. |
| **CUU-004** | Registrar asiento manual | Registrar manualmente un asiento contable que no proviene de una compra o venta. |
| **CUU-005** | Gestionar Plan de Cuentas | Gestionar el alta, modificación, baja lógica y consulta de cuentas contables. |
| **CUU-006** | Consultar Libro Mayor | Consultar los movimientos y saldos históricos y actuales de las cuentas contables. |
| **CUU-007** | Gestionar Clientes | Dar de alta, modificar, desactivar y consultar clientes. |
| **CUU-008** | Gestionar Proveedores | Dar de alta, modificar, desactivar y consultar proveedores. |
| **CUU-009** | Generar Balance General | Generar automáticamente el Balance General o Estado Patrimonial a partir de la información contable. |
| **CUU-010** | Generar Estado de Resultados | Generar automáticamente el Estado de Resultados del período a partir de la información contable. |
| **CUU-011** | Exportar Libro Diario | Exportar los asientos registrados en el Libro Diario en formatos descargables. |
| **CUU-012** | Exportar Libro Mayor | Exportar los movimientos y saldos del Libro Mayor en formatos descargables. |
| **CUU-013** | Consultar historial de auditoria | Consultar el historial de altas, modificaciones y anulaciones para fines de auditoría y trazabilidad. |
| **CUU-014** | Exportar Libro IVA a ARCA | Generar los archivos correspondientes al Libro IVA para su presentación ante ARCA. |
| **CUU-015** | Iniciar sesión | Autenticar al usuario y habilitar el acceso al sistema mediante sus credenciales y mecanismos de autenticación. |
| **CUU-016** | Gestionar usuarios | Gestionar el alta, modificación y baja de usuarios del sistema. |
| **CUU-017** | Registrar comprobante con OCR/NLP | Procesar un comprobante digital mediante OCR/NLP, extraer sus datos relevantes y registrarlo en el sistema. |
| **CUU-018** | Validar comprobante con ARCA | Validar la autenticidad y vigencia de un comprobante fiscal mediante la integración con ARCA. |
| **CUU-019** | Gestionar alertas de auditoría | Consultar y gestionar alertas generadas ante posibles inconsistencias contables o fiscales. |
| **CUU-020** | Consultar dashboard financiero | Visualizar indicadores, métricas y gráficos financieros consolidados para apoyar la toma de decisiones. |
| **CUU-021** | Generar reportes automáticos | Generar automáticamente reportes contables, financieros y fiscales a partir de la información registrada. |
| **CUU-022** | Consultar estado de comprobante | Consultar el estado de procesamiento, validación y contabilización de un comprobante registrado. |
| **CUU-023** | Obtener recomendaciones financieras inteligentes | Obtener recomendaciones financieras generadas mediante análisis de datos e inteligencia artificial para apoyar la toma de decisiones. |

## Registrar venta

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Registrar venta**

**Nombre:** *CUU-001 - \<Registrar venta\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Registrar una venta a partir de un comprobante, generando automáticamente el asiento contable correspondiente y actualizando la información contable.

**Actor Primario (dueño de la meta):** Contador / Administrativo contable

**Actor Iniciador:** Contador / Administrativo contable

**Disparador:** El usuario carga un comprobante de venta en el sistema

**Precondiciones:**

- El usuario se encuentra autenticado y posee permisos para registrar ventas.

- El Plan de Cuentas se encuentra configurado.

- El comprobante de venta se encuentra disponible.

- El sistema se encuentra disponible para procesar el comprobante.

> **CAMINO BÁSICO**

1.  El usuario carga el comprobante de venta. El sistema procesa automáticamente el comprobante mediante OCR/NLP (CUU 16 - \<*Registrar comprobantes con OCR*\>) y obtiene los datos relevantes, como cliente, ítems, importes y condición de cobro.

2.  El sistema verifica si el comprobante ya se encuentra registrado.

3.  El sistema identifica automáticamente al cliente mediante su CUIT o razón social contra la base de los clientes identificados.

4.  El sistema determina automáticamente las cuentas intervinientes (Ventas, IVA débito Fiscal, Clientes o Caja según la condición de cobro) aplicando las reglas del Plan de Cuentas.

5.  El sistema genera automáticamente el asiento contable, calcula los importes de Debe y Haber y valida que se encuentre balanceado.

6.  El sistema muestra al usuario la información del asiento contable, incluyendo el cliente, las cuentas involucradas y los importes correspondientes de Debe y Haber. El usuario revisa los datos obtenidos y confirma su contabilización

7.  El sistema registra el asiento en el Libro Diario y actualiza los saldos de las cuentas correspondientes en el Libro Mayor.

8.  El sistema notifica al usuario que la venta fue contabilizada y deja el comprobante y el asiento contable disponibles para su consulta.

> **CAMINO ALTERNATIVO**

***1.a.* \<*Durante*\> *El usuario decide realizar la carga manual del comprobante:***

> ***1.a.1.*** El usuario ingresa manualmente los datos del comprobante de venta. El sistema registra la información proporcionada.
>
> **1.a.2.** Continúa en el Paso 2.

**2.a. \<Posterior\> El sistema detecta que el comprobante ya se encuentra registrado:**

> **2.a.1.** El sistema verifica que el comprobante corresponde a una venta ya registrada y detecta que se encuentra duplicado.
>
> **2.a.2.** El sistema informa al usuario que el comprobante ya fue registrado y muestra los datos de la venta existente.
>
> **2.a.3.** El sistema no continúa con la generación del asiento contable ni actualiza el Libro Diario o el Libro Mayor.
>
> **2.a.4.** FCU.

***3.a.* \<*Posterior*\> *El cliente no puede identificarse automáticamente y se encuentra registrado en el sistema:***

> ***3.a.1.*** El sistema informa que no pudo identificar al cliente y marca el comprobante como pendiente.
>
> **3.a.2.** El usuario busca y selecciona el cliente correspondiente entre los clientes registrados. El sistema asocia el cliente seleccionado al comprobante de venta.
>
> **3.a.3.** Continúa en el Paso 4.

***3.b.* \<*Posterior*\> *El cliente no puede identificarse automáticamente y no se encuentra registrado en el sistema: ***

> ***3.b.1.*** El sistema informa que no pudo identificar al cliente y marca el comprobante como pendiente.
>
> **3.b.2.** Continua en *CUU-007 - \<Gestionar Clientes\>* para registrar al nuevo cliente.
>
> **3.b.3.** El sistema asocia el nuevo cliente al comprobante de venta.
>
> **3.b.4.** Continúa en el Paso 4.

***4.a.* \<*Posterior*\> *El sistema no puede determinar automáticamente alguna de las cuentas contables necesarias y la cuenta correspondiente ya se encuentra configurada: ***

> ***4.a.1.*** El sistema informa la cuenta que no pudo determinar y marca el comprobante como pendiente.
>
> ***4.a.2.*** El usuario selecciona la cuenta correspondiente.
>
> **4.a.3.** Continua en el paso 5.

***4.b.* \<*Posterior*\> *El sistema no puede determinar automáticamente alguna de las cuentas contables necesarias y la cuenta correspondiente no se encuentra configurada: ***

> ***4.b.1.*** El sistema informa la cuenta que no pudo determinar y marca el comprobante como pendiente.
>
> **4.b.2.** Continua en *CUU-005 - \<Gestionar Plan de Cuentas\>, para configurar la cuenta en el plan de cuenta.*
>
> **4.b.3.** El sistema asocia la nueva cuenta al comprobante de venta.
>
> **4.b.4** Continúa en el Paso 5.

***5.a.* \<*Posterior*\> *El asiento generado no se encuentra balanceado:***

> ***5.a.1.** E*l sistema marca la venta como pendiente de revisión e informa la diferencia entre el Debe y el Haber.
>
> **5.a.2.** El usuario corrige la información correspondiente.
>
> **5.a.3.** Continúa en el Paso 6.

***6.a.* \<*Posterior*\> *El usuario no confirma la contabilización:***

> ***6.a.1.*** El usuario cancela o pospone la contabilización. El sistema conserva la venta en estado pendiente y no actualiza el Libro Diario ni el Libro Mayor.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** Venta registrada exitosamente.

**Éxito alternativo:** \<Omitido\>

**Fracaso:** Venta no registrada.

**Poscondición de sistema**

**Éxito:** Venta registrada en el sistema, asiento contable generado y registrado en el Libro Diario y cuentas correspondientes actualizadas en el Libro Mayor.

**Éxito alternativo:** Venta pendiente de confirmación o corrección.

**Fracaso:** Venta no contabilizada.

### Diagramas de actividad y estado



## Registrar compra

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Registrar compra**

**Nombre:** *CUU-002 - \<Registrar compra\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Registrar una compra a partir de un comprobante, generando automáticamente el asiento contable correspondiente y actualizando la información contable.

**Actor Primario (dueño de la meta):** Contador / Administrativo contable

**Actor Iniciador:** Contador / Administrativo contable

**Disparador:** El usuario carga un comprobante de compra en el sistema

**Precondiciones:**

- El usuario se encuentra autenticado y posee permisos para registrar compras.

- El Plan de Cuentas se encuentra configurado.

- El comprobante de compra se encuentra disponible.

- El sistema se encuentra disponible para procesar el comprobante.

> **CAMINO BÁSICO**

1.  El usuario carga el comprobante de compra. El sistema procesa automáticamente el comprobante mediante OCR/NLP (CUU 16 - \<*Registrar comprobantes con OCR*\>) y obtiene los datos relevantes, como proveedor, ítems, importes y condición de pago

2.  El sistema verifica si el comprobante ya se encuentra registrado.

3.  El sistema identifica automáticamente al proveedor mediante su CUIT o razón social contra la base de los proveedores identificados.

4.  El sistema determina automáticamente las cuentas intervinientes (Compras, IVA Crédito Fiscal, Proveedores o Caja según la condición de cobro) aplicando las reglas del Plan de Cuentas.

5.  El sistema genera automáticamente el asiento contable, calcula los importes de Debe y Haber y valida que se encuentre balanceado.

6.  El sistema muestra al usuario la información del asiento contable, incluyendo el proveedor, las cuentas involucradas y los importes correspondientes de Debe y Haber. El usuario revisa los datos obtenidos y confirma su contabilización

7.  El sistema registra el asiento en el Libro Diario y actualiza los saldos de las cuentas correspondientes en el Libro Mayor.

8.  El sistema notifica al usuario la compra contabilizada y deja el comprobante y el asiento disponibles para su consulta.

> **CAMINO ALTERNATIVO**

***1.a.* \<*Durante*\> *El usuario decide realizar la carga manual del comprobante:***

> ***1.a.1.*** El usuario ingresa manualmente los datos del comprobante de compra. El sistema registra la información proporcionada.
>
> **1.a.2.** Continúa en el Paso 2.

***2.a.* \<*Posterior*\> *El sistema detecta que el comprobante de compra ya se encuentra registrado.***

> ***2.a.1.*** El sistema informa al usuario que el comprobante ya fue registrado y muestra los datos del registro existente.
>
> ***2.a.2.*** El usuario verifica la información y el sistema no registra nuevamente el comprobante.
>
> ***2.a.3.*** FCU.

***3.a.* \<*Posterior*\> *El proveedor no puede identificarse automáticamente y se encuentra registrado en el sistema:***

> ***3.a.1.*** El sistema informa que no pudo identificar al proveedor y marca el comprobante como pendiente.
>
> **3.a.2.** El usuario busca y selecciona el proveedor correspondiente entre los proveedores registrados.
>
> **3.a.3.** El sistema asocia el proveedor seleccionado al comprobante de compra.
>
> **3.a.4.** Continúa en el Paso 4.

***3.b.* \<*Posterior*\> *El proveedor no puede identificarse automáticamente y no se encuentra registrado en el sistema: ***

> ***3.b.1.*** El sistema informa que no pudo identificar al proveedor y marca el comprobante como pendiente.
>
> **3.b.2.** Continua en *CUU-008 - \<Gestionar Proveedores\>, para registrar el proveedor*
>
> **3.b.3.** El sistema asocia el nuevo proveedor al comprobante de compra.
>
> **3.b.4.** Continúa en el Paso 4.

***4.a.* \<*Posterior*\> *El sistema no puede determinar automáticamente alguna de las cuentas contables necesarias y la cuenta correspondiente ya se encuentra configurada: ***

> ***4.a.1.*** El sistema informa la cuenta que no pudo determinar y marca el comprobante como pendiente.
>
> ***4.a.2.*** El usuario selecciona la cuenta correspondiente.
>
> **4.a.3.** Continúa en el Paso 5.

***4.b.* \<*Posterior*\> *El sistema no puede determinar automáticamente alguna de las cuentas contables necesarias y la cuenta correspondiente no se encuentra configurada: ***

> ***4.b.1.*** El sistema informa la cuenta que no pudo determinar y marca el comprobante como pendiente.
>
> **4.b.2.** Continua en *CUU-005 - \<Gestionar Plan de Cuentas\>, para configurar la cuenta en el plan de cuenta.*
>
> **4.b.3.** El sistema asocia la nueva cuenta al comprobante de compra.
>
> **4.b.4** Continúa en el Paso 5.

***5.a.* \<*Posterior*\> *El asiento generado no se encuentra balanceado:***

> ***5.a.1.** E*l sistema marca la compra como pendiente de revisión e informa la diferencia entre el Debe y el Haber.
>
> **5.a.2.** El usuario corrige la información correspondiente.
>
> **5.a.3.** Continúa en el paso 5.

***6.a.* \<*Posterior*\> *El usuario no confirma la contabilización:***

> ***6.a.1.*** El usuario cancela o pospone la contabilización. El sistema conserva la compra en estado pendiente y no actualiza el Libro Diario ni el Libro Mayor.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** Compra registrada exitosamente.

**Éxito alternativo:** \<Omitido\>

**Fracaso:** Compra no registrada.

**Poscondición de sistema**

**Éxito:** Compra registrada en el sistema, asiento contable generado y registrado en el Libro Diario, y cuentas correspondientes actualizadas en el Libro Mayor.

**Éxito alternativo:** Compra pendiente de confirmación o corrección.

**Fracaso:** Compra no contabilizada.

### Diagramas de actividad y estado



## Gestionar Libro Diario

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Gestionar Libro Diario**

**Nombre:** *CUU-003 - \<Gestionar Libro Diario\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Consultar los asientos contables registrados en el Libro Diario y acceder a las operaciones de modificación o anulación de los mismos.

**Actor Primario (dueño de la meta):** Contador / Administrativo contable

**Actor Iniciador:** Contador / Administrativo contable

**Disparador:** El usuario accede al Libro Diario.

**Precondiciones:**

- El usuario se encuentra autenticado y posee permisos para acceder al Libro Diario.

> **CAMINO BÁSICO**

1.  El usuario accede al Libro Diario y aplica filtros de búsqueda(periodo, cuenta, tipo asiento, estado).

2.  El sistema recupera y muestra los asientos que cumplen los criterios, con su detalle de cuentas, importe y estado(vigente/ anulado/pendiente)

3.  El usuario selecciona un asiento para consultar su detalle. El sistema muestra el asiento completo

> **CAMINO ALTERNATIVO**

***2.a.* \<*Durante*\>*El período seleccionado no contiene asientos:***

> ***1.a.1.*** El sistema informa que no existen movimientos registrados para dicho período.
>
> **1.a.2.** FCU

***2.b.* \<*Durante*\> *La cuenta seleccionada no contiene asientos:***

> ***1.b.1.*** El sistema informa que no existen movimientos registrados para dicha cuenta
>
> **1.b.2.** FCU

***3.a.* \<*Durante*\> *El usuario selecciona modificar el asiento:***

> ***3.a.1.*** .El usuario modifica los datos correspondientes. El sistema registra los cambios realizados.
>
> **3.a.2.** El sistema valida que el asiento mantenga la igualdad entre Debe y Haber.
>
> **3.a.3** El sistema presenta los cambios para su revisión y solicita la confirmación del usuario.
>
> **3.a.4.** El usuario confirma la modificación.
>
> **3.a.5.** El sistema actualiza el asiento en el Libro Diario y refleja los cambios correspondientes en el Libro Mayor.
>
> **3.a.6.** El sistema registra la operación en el historial de auditoría, incluyendo el asiento afectado, los cambios realizados, el usuario responsable y la fecha y hora de la operación.
>
> **3.a.7** FCU.

**3.a.2. \<*Durante*\> El asiento modificado no se encuentra balanceado:**

> **3.a.2.1.** El sistema informa la diferencia entre el Debe y el Haber.
>
> **3.a.2.2.** El usuario corrige los datos del asiento.
>
> **3.a.2.3.** El sistema vuelve a validar el asiento.
>
> *3.a.2.4.* Continua en el Paso 2.a.3

***3.b.* \<*Durante*\> *El usuario selecciona anular el asiento:***

> ***3.b.1.*** El usuario confirma la anulación. El sistema anula el asiento y actualiza el estado correspondiente.
>
> **3.b.2** El sistema muestra el asiento como anulado y actualiza las cuentas correspondientes del Libro Mayor.
>
> **3.b.4** El sistema registra la operación en el historial de auditoría, incluyendo el asiento afectado, los cambios realizados, el usuario responsable y la fecha y hora de la operación.
>
> **3.b.5** FCU.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** Consulta del Libro Diario realizada exitosamente.

**Éxito alternativo:** No existen asientos contables registrados para el período seleccionado.

**Fracaso:** No fue posible consultar el Libro Diario.

**Poscondición de sistema**

**Éxito:** El sistema muestra los asientos contables registrados en el Libro Diario y permite acceder a las operaciones de modificación o anulación según los permisos del usuario.

**Éxito alternativo:** El sistema informa que no existen asientos registrados para el período seleccionado.

**Fracaso:** El sistema no muestra la información del Libro Diario debido a falta de permisos o a un error de acceso a los datos.

### Diagramas de actividad y estado



## Registrar asiento manual

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Registrar asiento manual**

**Nombre:** *CUU-004 - \<Registrar asiento manual\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Registrar manualmente un asiento contable que no proviene de una compra o venta, actualizando el Libro Diario y los saldos de las cuentas correspondientes en el Libro Mayor.

**Actor Primario (dueño de la meta):** Contador / Administrativo contable

**Actor Iniciador:** Contador / Administrativo contable

**Disparador:** El usuario selecciona registrar asiento manual.

**Precondiciones:**

- El usuario se encuentra autenticado y posee permisos para registrar asientos manuales.

- El Plan de Cuentas se encuentra configurado.

- Existen cuentas contables disponibles para imputar el asiento.

> **CAMINO BÁSICO**

1.  El usuario selecciona la opción registrar asiento manual. El sistema solicita los datos del asiento, como fecha, concepto y cuentas contables involucradas.

2.  El usuario ingresa la fecha y el concepto del asiento y selecciona las cuentas correspondientes, indicando para cada una el importe a imputar al Debe o al Haber. El sistema valida automáticamente que las cuentas seleccionadas se encuentren vigentes y que los importes ingresados sean válidos.

3.  El sistema calcula los totales del Debe y del Haber y verifica que el asiento se encuentre balanceado.

4.  El sistema muestra al usuario el asiento completo, incluyendo fecha, concepto, cuentas e importes del Debe y Haber. El usuario revisa la información y confirma la contabilización.

5.  El sistema registra el asiento en el Libro Diario y actualiza los saldos de las cuentas correspondientes en el Libro Mayor.

6.  El sistema informa al usuario que el asiento fue registrado correctamente y lo deja disponible para su consulta.

> **CAMINO ALTERNATIVO**

**2.a. \<Durante\> El usuario ingresa un importe inválido: :**

> **2.a.1. El sistema informa el error e indica el importe que debe corregirse.**
>
> **2.a.2**. El usuario corrige el importe ingresado.
>
> **2.a.3.** El sistema vuelve a validar los datos y el caso de uso continúa en el paso 3.

**3.a. \<Durante\> El asiento no se encuentra balanceado:**

> **3.a.1.** El sistema informa la diferencia entre los totales del Debe y del Haber.
>
> **3.a.2.** El usuario modifica los importes o las cuentas correspondientes.
>
> **3.a.3**. El sistema vuelve a calcular los totales y validar el asiento.
>
> **3.a.4.** Si el asiento se encuentra balanceado, el caso de uso continúa en el paso 4.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** Asiento contable manual registrado correctamente.

**Éxito alternativo:** \<Omitido\>

**Fracaso:** Asiento no registrado debido a datos inválidos o falta de balance entre Debe y Haber.

**Poscondición de sistema**

**Éxito:** El asiento queda registrado en el Libro Diario y los saldos de las cuentas correspondientes se actualizan en el Libro Mayor.

**Éxito alternativo:** \<Omitido\>

**Fracaso:** El asiento no es contabilizado y no se modifican los saldos contables.

### Diagramas de actividad y estado



### Ejemplos de asientos contables a contemplar

Se relevaron y documentaron los principales tipos de asientos contables a contemplar por el sistema, agrupados según la naturaleza de las operaciones. Para cada tipo se definió un ejemplo concreto de imputación al Debe y al Haber, que sirve como referencia para el diseño de la generación de asientos.

Los tipos identificados se organizan en las siguientes categorías: asientos comerciales, de tesorería, de sueldos y cargas sociales, impositivos, de cierre y ajuste, y específicos del negocio.

**A. Asientos comerciales**

**1. Asiento de venta**

*Se emite una factura de venta a un cliente, a cobrar en cuenta corriente.*

| **Cuenta**                   | **Debe**   | **Haber**  |
|------------------------------|------------|------------|
| 1.1.2.01 Deudores por Ventas | 121.000,00 |            |
| 4.1 Ventas                   |            | 100.000,00 |
| 2.1.3.01 IVA Débito Fiscal   |            | 21.000,00  |

**2. Asiento de compra**

*Se recibe una factura de compra de mercadería, a pagar a proveedor.*

| **Cuenta**                                         | **Debe**  | **Haber** |
|----------------------------------------------------|-----------|-----------|
| 1.1.4.01 Mercadería de Reventa                     | 80.000,00 |           |
| 1.1.3.02 Saldo a Favor de IVA (IVA Crédito Fiscal) | 16.800,00 |           |
| 2.1.1.01 Proveedores Nacionales                    |           | 96.800,00 |

**3. Nota de crédito de venta**

*Se anula parcialmente una venta ya facturada (ej. devolución de mercadería).*

| **Cuenta**                   | **Debe**  | **Haber** |
|------------------------------|-----------|-----------|
| 4.1 Ventas                   | 50.000,00 |           |
| 2.1.3.01 IVA Débito Fiscal   | 10.500,00 |           |
| 1.1.2.01 Deudores por Ventas |           | 60.500,00 |

**4. Nota de crédito de compra**

*Un proveedor anula parcialmente una compra ya recibida.*

| **Cuenta**                      | **Debe**  | **Haber** |
|---------------------------------|-----------|-----------|
| 2.1.1.01 Proveedores Nacionales | 30.250,00 |           |
| 1.1.4.01 Mercadería de Reventa  |           | 25.000,00 |
| 1.1.3.02 IVA Credito Fiscal     |           | 5.250,00  |

**5. Nota de débito**

*Se le cargan intereses por mora a un cliente.*

| **Cuenta**                   | **Debe**  | **Haber** |
|------------------------------|-----------|-----------|
| 1.1.2.01 Deudores por Ventas | 12.100,00 |           |
| 4.2 Intereses Ganados        |           | 10.000,00 |
| 2.1.3.01 IVA Débito Fiscal   |           | 2.100,00  |

**B. Asientos de tesorería**

**6. Cobro a cliente (efectivo)**

*El cliente cancela la factura del ejemplo 1, en efectivo.*

| **Cuenta**                   | **Debe**   | **Haber**  |
|------------------------------|------------|------------|
| 1.1.1.01 Caja                | 121.000,00 |            |
| 1.1.2.01 Deudores por Ventas |            | 121.000,00 |

**7. Pago a proveedor (transferencia)**

*Se cancela la factura del ejemplo 2 con transferencia.*

| **Cuenta**                        | **Debe**  | **Haber** |
|-----------------------------------|-----------|-----------|
| 2.1.1.01 Proveedores Nacionales   | 96.800,00 |           |
| 1.1.1.03 Banco Cuenta Corriente A |           | 96.800,00 |

**8. Anticipo recibido de cliente**

*Un cliente adelanta un pago antes de que se le facture la mercadería.*

| **Cuenta**                        | **Debe**  | **Haber** |
|-----------------------------------|-----------|-----------|
| 1.1.1.03 Banco Cuenta Corriente A | 50.000,00 |           |
| 2.1.4.01 Anticipo de Clientes     |           | 50.000,00 |

**9. Anticipo entregado a proveedor**

*Se adelanta un pago a un proveedor antes de recibir la factura.*

| **Cuenta**                        | **Debe**  | **Haber** |
|-----------------------------------|-----------|-----------|
| 1.1.3.01 Anticipo a Proveedores   | 40.000,00 |           |
| 1.1.1.03 Banco Cuenta Corriente A |           | 40.000,00 |

**C. Asientos de sueldos y cargas sociales**

**10. Liquidación de sueldos (devengamiento)**

*Se registra el gasto de sueldos del mes, aún no pagado.*

| **Cuenta**                          | **Debe**   | **Haber**  |
|-------------------------------------|------------|------------|
| 5.2 Sueldos y Cargas Sociales       | 185.400,00 |            |
| 2.1.2.01 Sueldos y Jornales a Pagar |            | 150.000,00 |
| 2.1.2.02 Cargas Sociales a Pagar    |            | 35.400,00  |

**11. Pago de sueldos**

*Se transfiere el sueldo devengado en el ejemplo 11.*

| **Cuenta**                          | **Debe**   | **Haber**  |
|-------------------------------------|------------|------------|
| 2.1.2.01 Sueldos y Jornales a Pagar | 150.000,00 |            |
| 1.1.1.03 Banco Cuenta Corriente A   |            | 150.000,00 |

**12. Pago de cargas sociales / ART / cuota sindical**

*Se depositan las cargas sociales devengadas en el ejemplo 11, junto con ART y cuota sindical del período.*

| **Cuenta**                        | **Debe**  | **Haber** |
|-----------------------------------|-----------|-----------|
| 2.1.2.02 Cargas Sociales a Pagar  | 25.000,00 |           |
| 2.1.2.03 ART a Pagar              | 6.400,00  |           |
| 2.1.2.04 Cuota Sindical a Pagar   | 4.000,00  |           |
| 1.1.1.03 Banco Cuenta Corriente A |           | 35.400,00 |

**D. Asientos impositivos**

**13. Retención sufrida (IVA)**

*Un cliente cancela una factura de 121.000,00 pero retiene 14.520,00 de IVA al pagar.*

| **Cuenta**                           | **Debe**   | **Haber**  |
|--------------------------------------|------------|------------|
| 1.1.1.03 Banco Cuenta Corriente A    | 106.480,00 |            |
| 1.1.3.04 Retenciones de IVA Sufridas | 14.520,00  |            |
| 1.1.2.01 Deudores por Ventas         |            | 121.000,00 |

**14. Percepción sufrida (Ingresos Brutos)**

*Se recibe una factura de compra en la que el proveedor percibe Ingresos Brutos.*

| **Cuenta**                                       | **Debe**  | **Haber** |
|--------------------------------------------------|-----------|-----------|
| 1.1.4.01 Mercadería de Reventa                   | 80.000,00 |           |
| 1.1.3.02 IVA Credito                             | 16.800,00 |           |
| 1.1.3.05 Retenciones de Ingresos Brutos Sufridas | 1.200,00  |           |
| 2.1.1.01 Proveedores Nacionales                  |           | 98.000,00 |

**15. Retención practicada a un proveedor (empresa como agente de retención)**

*Al pagar la factura del ejemplo 2, la empresa retiene una parte y debe depositarla luego a ARCA (dos asientos).*

**15a. Pago con retención practicada**

| **Cuenta**                                  | **Debe**  | **Haber** |
|---------------------------------------------|-----------|-----------|
| 2.1.1.01 Proveedores Nacionales             | 96.800,00 |           |
| 1.1.1.03 Banco Cuenta Corriente A           |           | 90.000,00 |
| 2.1.3.02 Retenciones a Depositar (terceros) |           | 6.800,00  |

**15b. Depósito de la retención en ARCA**

| **Cuenta**                                  | **Debe** | **Haber** |
|---------------------------------------------|----------|-----------|
| 2.1.3.02 Retenciones a Depositar (terceros) | 6.800,00 |           |
| 1.1.1.03 Banco Cuenta Corriente A           |          | 6.800,00  |

**16. Determinación y pago del saldo técnico de IVA**

*Cierre mensual: se cancela el IVA Débito Fiscal contra el Crédito Fiscal acumulado y se paga la diferencia.*

| **Cuenta**                        | **Debe**   | **Haber** |
|-----------------------------------|------------|-----------|
| 2.1.3.01 IVA Débito Fiscal        | 126.000,00 |           |
| 1.1.3.02 IVA Credito              |            | 71.400,00 |
| 1.1.1.03 Banco Cuenta Corriente A |            | 54.600,00 |

**E. Asientos de cierre y ajuste**

**17. Apertura de ejercicio**

*Reapertura simplificada de los saldos patrimoniales al inicio de un nuevo ejercicio.*

| **Cuenta**                        | **Debe**   | **Haber**  |
|-----------------------------------|------------|------------|
| 1.1.1.01 Caja                     | 50.000,00  |            |
| 1.1.1.03 Banco Cuenta Corriente A | 400.000,00 |            |
| 1.1.4.01 Mercadería de Reventa    | 300.000,00 |            |
| 2.1.1.01 Proveedores Nacionales   |            | 120.000,00 |
| 3.1 Capital Social                |            | 630.000,00 |

**18. Amortización de bienes de uso**

*Amortización mensual de un rodado u otro bien de uso.*

| **Cuenta**                                    | **Debe** | **Haber** |
|-----------------------------------------------|----------|-----------|
| 5.7 Amortizaciones                            | 8.500,00 |           |
| 1.2.1.04 Amortización Acumulada Bienes de Uso |          | 8.500,00  |

**19. Cierre de cuentas de resultado**

*Cierre de ejercicio: se cancelan todas las cuentas de resultado contra Resultado del Ejercicio.*

| **Cuenta**                        | **Debe**   | **Haber**  |
|-----------------------------------|------------|------------|
| 4.1 Ventas                        | 600.000,00 |            |
| 4.2 Intereses Ganados             | 10.000,00  |            |
| 4.3 Diferencia de Cambio Positiva | 2.200,00   |            |
| 5.1 Costo de Mercadería Vendida   |            | 340.000,00 |
| 5.2 Sueldos y Cargas Sociales     |            | 185.400,00 |
| 5.3 Gastos de Administración      |            | 23.500,00  |
| 3.4 Resultado del Ejercicio       |            | 63.300,00  |

## Gestionar Plan de Cuentas

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Gestionar Plan de Cuentas**

**Nombre:** *CUU-005 - \<Gestionar Plan de Cuentas\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Gestionar las cuentas contables que conforman el Plan de Cuentas mediante su alta, modificación, baja lógica y consulta, asegurando la integridad de la estructura contable utilizada por el sistema.

**Actor Primario (dueño de la meta):** Contador

**Actor Iniciador:** Contador

**Disparador:**

- El usuario accede a la gestión del Plan de Cuentas.

- Se invoca desde *CUU-001 - \<Registrar venta\> y CUU-002 - \<Registrar compra\>* cuando se requiere dar de alta una cuenta.

**Precondiciones:**

- El usuario se encuentra autenticado y posee permisos sobre el Plan de Cuentas.

- El Plan de Cuentas se encuentra configurado y disponible para su gestión.

> **CAMINO BÁSICO**

1.  El usuario accede al Plan de Cuentas. El sistema muestra el listado de cuentas vigentes, su código, denominación, tipo, naturaleza, cuenta padre y estado.

2.  El usuario selecciona la opción **alta de cuenta**.

3.  El sistema solicita los datos necesarios para registrar la nueva cuenta: código, denominación, tipo, naturaleza(deudora o acreedora) y cuenta padre. El usuario ingresa los datos correspondientes.

4.  El sistema valida que el código no se encuentre duplicado y que la cuenta padre y la jerarquía sean consistentes.

5.  El sistema muestra al usuario los datos ingresados y el resultado de las validaciones. El usuario confirma el alta de la cuenta.

6.  El sistema registra la nueva cuenta, la incorpora al Plan de Cuentas y informa que la cuenta fue creada correctamente.

> **CAMINO ALTERNATIVO**

**2.a. \<Durante\> El usuario selecciona la opción modificación de cuenta:**

> **2.a.1.** El usuario selecciona la cuenta que desea modificar. El sistema muestra los datos actuales de la cuenta.
>
> **2.a.2.** El usuario modifica los datos correspondientes. El sistema valida que los cambios mantengan la consistencia de la estructura del Plan de Cuentas.
>
> **2.a.3**. El sistema valida que los datos obligatorios estén completos y que los cambios mantengan la consistencia de la estructura del Plan de Cuentas.
>
> **2.a.4**. El sistema muestra los datos modificados y el resultado de las validaciones.
>
> **2.a.5**. El usuario confirma la modificación. El sistema actualiza la cuenta e informa que la operación fue realizada correctamente.
>
> **2.a.6.** El sistema registra la modificación en el historial de auditoría, incluyendo la cuenta contable afectada, los cambios realizados, el usuario responsable y la fecha y hora de la operación.
>
> **2.a.6.** FCU.

**2.b. \<Durante\> El usuario selecciona la opción baja lógica de cuenta:**

> **2.a.1.** El usuario selecciona la cuenta que desea dar de baja. El sistema verifica que la cuenta no posea movimientos vigentes ni cuentas dependientes activas.
>
> **2.a.2**. Si las validaciones son satisfactorias, el sistema informa que la cuenta puede darse de baja. El usuario confirma la baja.
>
> **2.a.3.** El sistema marca la cuenta como inactiva y conserva su información histórica.
>
> **2.a.4**. El sistema marca la cuenta como inactiva y conserva su información histórica.
>
> **2.a.5**. El sistema registra la baja en el historial de auditoría, incluyendo la cuenta contable afectada, los cambios realizados, el usuario responsable y la fecha y hora de la operación.
>
> **2.a.5.** FCU.

***2.c. \<Durante\> El usuario selecciona la opción consulta de cuenta:***

> ***2.c.1.*** El usuario selecciona la cuenta que desea consultar. El sistema muestra el detalle de la cuenta, incluyendo código, denominación, naturaleza, tipo, cuenta padre, estado y ubicación dentro de la estructura jerárquica.
>
> ***2.c.2.*** El sistema muestra el historial de movimientos asociados a la cuenta.
>
> **2.c.3.** FCU

***4.a. \<Durante\> El código ingresado ya se encuentra registrado:***

> ***4.a.1.*** El sistema informa que el código se encuentra duplicado.
>
> ***4.a.2.*** El usuario modifica el código ingresado.
>
> ***4.a.3.*** El sistema vuelve a validar la información
>
> **4.a.4** Continúa en el Paso 4.

***4.b. \<Durante\> La cuenta padre o la jerarquía ingresada no es válida:***

> ***4.b.1.*** El sistema informa los datos faltantes o la inconsistencia detectada.
>
> ***4.b.2.*** El usuario corrige los datos correspondientes.
>
> ***4.b.3.*** El sistema vuelve a validar la información
>
> **4.b.4** Continúa en el Paso 4.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** El Plan de Cuentas es actualizado mediante el alta, modificación o baja lógica de una cuenta, o la cuenta es consultada correctamente.

**Éxito alternativo:** \<Omitido\>

**Fracaso:** La operación no se realiza debido a una validación, dependencia o falta de permisos.

**Poscondición de sistema**

**Éxito:** La cuenta queda creada, modificada o marcada como inactiva según la operación realizada, manteniendo la integridad de la estructura del Plan de Cuentas.

**Éxito alternativo:** \<Omitido\>

**Fracaso:** La operación es rechazada y no se producen modificaciones en la información existente.

### Diagramas de actividad y estado



### Ejemplo de Plan de Cuentas

Se presenta un Plan de Cuentas genérico como estructura contable de referencia para el sistema. Se encuentra organizado en cinco rubros principales: Activo, Pasivo, Patrimonio Neto, Resultados Positivos y Resultados Negativos, cada uno compuesto por sus correspondientes sub-rubros y cuentas.

Este Plan de Cuentas permite establecer una estructura común sobre la cual se pueden imputar contablemente las operaciones registradas en el sistema y sirve como base para que los comprobantes digitalizados mediante OCR/NLP puedan ser asociados a las cuentas contables correspondientes.

| **Código** | **Cuenta** | **Naturaleza** |
|----|----|----|
| **1** | **ACTIVO** |  |
| 1.1 | Activo Corriente | — |
| 1.1.1 | Caja y Bancos | — |
| 1.1.1.01 | Caja | Deudora |
| 1.1.1.02 | Moneda extranjera | Deudora |
| 1.1.1.03 | Banco Cuenta Corriente A | Deudora |
| 1.1.1.04 | Banco Cuenta Corriente B | Deudora |
| 1.1.2 | Créditos por Ventas | — |
| 1.1.2.01 | Deudores por Ventas | Deudora |
| 1.1.2.02 | Documentos a Cobrar | Deudora |
| 1.1.2.03 | Previsión para Deudores Incobrables | Acreedora (regularizadora) |
| 1.1.3 | Otros Créditos | — |
| 1.1.3.01 | Anticipo a Proveedores | Deudora |
| 1.1.3.02 | Saldo a Favor de IVA | Deudora |
| 1.1.3.03 | Percepciones de IVA Sufridas | Deudora |
| 1.1.3.04 | Retenciones de IVA Sufridas | Deudora |
| 1.1.3.05 | Retenciones de Ingresos Brutos Sufridas | Deudora |
| 1.1.3.06 | Anticipo de Impuesto a las Ganancias | Deudora |
| 1.1.3.07 | Saldo a Favor de Impuesto a las Ganancias | Deudora |
| 1.1.3.08 | Retenciones de Impuesto a las Ganancias Sufridas | Deudora |
| 1.1.4 | Bienes de Cambio | — |
| 1.1.4.01 | Mercadería de Reventa | Deudora |
| 1.1.4.02 | Bienes de Cambio recibidos en canje (a confirmar) | Deudora |
| 1.1.5 | Otras Inversiones | — |
| 1.1.5.01 | Inversiones Financieras Corrientes | Deudora |
| 1.2 | Activo No Corriente | — |
| 1.2.1 | Bienes de Uso | — |
| 1.2.1.01 | Rodados | Deudora |
| 1.2.1.02 | Muebles y Útiles | Deudora |
| 1.2.1.03 | Instalaciones | Deudora |
| 1.2.1.04 | Amortización Acumulada Bienes de Uso | Acreedora (regularizadora) |
| 1.2.2 | Inversiones a Largo Plazo | — |
| **2** | **PASIVO** |  |
| 2.1 | Pasivo Corriente | — |
| 2.1.1 | Deudas Comerciales | — |
| 2.1.1.01 | Proveedores Nacionales | Acreedora |
| 2.1.1.02 | Proveedores del Exterior | Acreedora |
| 2.1.2 | Remuneraciones y Cargas Sociales | — |
| 2.1.2.01 | Sueldos y Jornales a Pagar | Acreedora |
| 2.1.2.02 | Cargas Sociales a Pagar | Acreedora |
| 2.1.2.03 | ART a Pagar | Acreedora |
| 2.1.2.04 | Cuota Sindical a Pagar | Acreedora |
| 2.1.3 | Cargas Fiscales | — |
| 2.1.3.01 | IVA Débito Fiscal | Acreedora |
| 2.1.3.02 | Retenciones a Depositar (terceros) | Acreedora |
| 2.1.3.03 | Impuesto a las Ganancias a Pagar | Acreedora |
| 2.1.3.04 | Ingresos Brutos a Pagar | Acreedora |
| 2.1.4 | Anticipos de Clientes | — |
| 2.1.4.01 | Anticipo de Clientes | Acreedora |
| 2.2 | Pasivo No Corriente | — |
| 2.2.1.01 | Préstamos a Largo Plazo | Acreedora |
| **3** | **PATRIMONIO NETO** |  |
| 3.1 | Capital Social | Acreedora |
| 3.2 | Ajustes al Capital | Acreedora |
| 3.3 | Resultados Acumulados | Acreedora |
| 3.4 | Resultado del Ejercicio | Acreedora / Deudora |
| **4** | **RESULTADOS POSITIVOS** |  |
| 4.1 | Ventas | Acreedora |
| 4.2 | Intereses Ganados | Acreedora |
| 4.3 | Diferencia de Cambio Positiva | Acreedora |
| **5** | **RESULTADOS NEGATIVOS** |  |
| 5.1 | Costo de Mercadería Vendida | Deudora |
| 5.2 | Sueldos y Cargas Sociales | Deudora |
| 5.3 | Gastos de Administración | Deudora |
| 5.4 | Gastos de Comercialización | Deudora |
| 5.5 | Impuestos y Tasas | Deudora |
| 5.6 | Diferencia de Cambio Negativa | Deudora |
| 5.7 | Amortizaciones | Deudora |

## Consultar Libro Mayor

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Consultar Libro Mayor**

**Nombre:** *CUU-006 - \<Consultar Libro Mayor\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Consultar los movimientos y saldos, históricos y actuales, de cada cuenta contable.

**Actor Primario (dueño de la meta):** Contador / Administrativo contable

**Actor Iniciador:** Contador / Administrativo contable

**Disparador: El usuario selecciona la opción “Libro Mayor”.**

**Precondiciones:**

- El usuario se encuentra autenticado y posee permisos sobre el Libro Mayor.

- Existen cuentas configuradas en el Plan de Cuentas.

> **CAMINO BÁSICO**

1.  El usuario selecciona una cuenta o grupo de cuentas y define el período a consultar.

2.  El sistema recupera automáticamente los movimientos registrados en el período, provenientes de ventas, compras, asientos manuales, modificaciones y anulaciones, y calcula el saldo inicial acumulado, los movimientos del Debe y Haber y el saldo final.

3.  El sistema muestra el detalle de los movimientos y los saldos calculados.

> **CAMINO ALTERNATIVO**

**2.a. *\<Durante\>* La cuenta no registra movimientos en el período**

> **2.a.1.**El sistema informa que no existen movimientos y muestra el saldo inicial arrastrado.
>
> **2.a.2.** FCU.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** Consulta realizada exitosamente.

**Éxito alternativo:** \<Omitido\>

**Fracaso:** No fue posible realizar la consulta.

**Poscondición de sistema**

**Éxito:** El sistema muestra los movimientos y saldos actualizados de la o las cuentas consultadas.

**Éxito alternativo:** \<Omitido\>

**Fracaso:** Se informa un error de acceso a los datos o falta de permisos.

### Diagramas de actividad y estado



### Ejemplo de Libro Mayor

A continuación, se presenta un ejemplo genérico de la visualización de una cuenta en el Libro Mayor del sistema. En este caso, se muestra la cuenta Cargas Sociales a Pagar, junto con sus movimientos, comprobantes, conceptos e importes correspondientes.

| **Fecha** | **Comprobante** | **N°** | **Concepto** | **Debe** | **Haber** |
|----|----|----|----|----|----|
| 01/01/25 | — | — | Saldo anterior |  | 0,00 |
| 31/01/25 | Minuta | 12 | Devengamiento cargas sociales |  | 58.200,00 |
| 15/02/25 | Pago | 1.045 | Depósito cargas sociales | 58.200,00 |  |
| 28/02/25 | Minuta | 13 | Devengamiento cargas sociales |  | 59.750,00 |
| 17/03/25 | Pago | 1.098 | Depósito cargas sociales | 59.750,00 |  |
| 31/03/25 | Minuta | 14 | Devengamiento cargas sociales |  | 61.100,00 |
| 16/04/25 | Pago | 1.152 | Depósito cargas sociales | 61.100,00 |  |
| 30/04/25 | Minuta | 15 | Devengamiento cargas sociales |  | 60.400,00 |
| 15/05/25 | Pago | 1.201 | Convenio de pago — cuota 1 | 30.200,00 |  |
| 30/05/25 | Pago | 1.244 | Convenio de pago — cuota 2 | 30.200,00 |  |
| **Totales del período** |  |  |  | 239.450,00 | 239.450,00 |

## Gestionar Clientes

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Gestionar Clientes**

**Nombre:** *CUU-007 - \<Gestionar Clientes\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Gestionar de forma integral los datos de los clientes

**Actor Primario (dueño de la meta):** Contador / Administrativo contable

**Actor Iniciador:** Contador / Administrativo contable

**Disparador:**

- El usuario accede a la gestión de clientes,

- Se invoca desde *CUU-001 - \<Registrar venta\>* cuando se requiere dar de alta un cliente

**Precondiciones:**

- El usuario se encuentra autenticado y posee permisos sobre la gestión de clientes.

> **CAMINO BÁSICO**

1.  El usuario accede a la gestión de clientes.

2.  El usuario selecciona la opción de alta.

3.  El usuario ingresa el CUIT del cliente. El sistema consulta el padrón de ARCA y completa automáticamente los datos disponibles.

4.  El sistema valida que no exista un cliente registrado con el mismo CUIT.

5.  El usuario confirma los datos y completa la información faltante, si corresponde.

6.  El sistema registra el cliente y le asigna un código.

> **CAMINO ALTERNATIVO**

**2.a. *\<Durante\>* Modificación**

**2.a.1.** El usuario selecciona un cliente existente y solicita modificar sus datos

**2.a.2.** El sistema muestra la información actual del cliente.

**2.a.3.** El usuario realiza los cambios y el sistema valida y actualiza los datos.

**2.a.4.** FCU.

**2.b. *\<Durante\>* Consulta**

**2.b.1.** El usuario selecciona un cliente existente y solicita consultar sus datos.

> **2.b.2.** El sistema muestra los datos del cliente y el historial de comprobantes asociados.

**2.b.3.** FCU.

**2.c. *\<Durante\>* Baja**

**2.c.1.** El usuario selecciona un cliente existente y solicita su desactivación.

> **2.c.2.** El sistema valida que el cliente no tenga comprobantes pendientes de procesamiento.
>
> **2.c.3.** Si se cumplen las condiciones, el sistema marca al cliente como inactivo.

**2.c.4.** FCU.

**4.a. *\<Posterior\>* Cliente duplicado (mismo CUIT)**

> **4.a.1.** El sistema detecta que ya existe un cliente registrado con el CUIT ingresado.
>
> **4.a.2.** El sistema informa el conflicto y ofrece asociar el comprobante al cliente existente.
>
> **4.a.3.** FCU.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** Gestión del cliente realizada exitosamente.

**Éxito alternativo:** \<Omitido\>

**Fracaso:** Operación no realizada.

**Poscondición de sistema**

**Éxito:** El cliente queda creado, actualizado o marcado como inactivo, disponible para su uso en el registro automático de ventas.

**Éxito alternativo:** \<Omitido\>

**Fracasó:** Operación rechazada por validación, falta de permisos u otra condición que impida completar la operación.

### Diagramas de actividad y estado



## Gestionar Proveedores

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Gestionar Proveedores**

**Nombre:** *CUU-008 - \<Gestionar Proveedores\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Gestionar de forma integral los datos de los proveedores

**Actor Primario (dueño de la meta):** Contador / Administrativo contable

**Actor Iniciador:** Contador / Administrativo contable

**Disparador:**

- El usuario accede a la gestión de proveedores

- Se invoca desde *CUU-002 - \<Registrar compra\>* el sistema detecta que el proveedor no se encuentra registrado y solicita su alta.

**Precondiciones:**

- El usuario se encuentra autenticado y posee permisos sobre la gestión de proveedores.

> **CAMINO BÁSICO**

1.  El usuario accede a la gestión de proveedores.

2.  El usuario selecciona la opción de alta.

3.  El usuario ingresa el CUIT del proveedor. El sistema consulta el padrón de ARCA y completa automáticamente los datos disponibles.

4.  El sistema valida que no exista un proveedor registrado con el mismo CUIT.

5.  El usuario confirma los datos y completa la información faltante, si corresponde.

6.  El sistema registra el proveedor y le asigna un código.

> **CAMINO ALTERNATIVO**

**2.a. *\<Durante\>* Modificación**

> **2.a.1.** El usuario selecciona un proveedor existente y solicita modificar sus datos.  
> **2.a.2.** El sistema muestra la información actual del proveedor.  
> **2.a.3.** El usuario realiza los cambios y el sistema valida y actualiza los datos.
>
> **2.a.4.** FCU.

**2.b. *\<Durante\>* Baja**

> **2.b.1.** El usuario selecciona un proveedor existente y solicita su desactivación.
>
> **2.b.2.** El sistema valida que el proveedor no tenga comprobantes pendientes de procesamiento.
>
> **2.b.3.** Si se cumplen las condiciones, el sistema marca al proveedor como inactivo.
>
> **2.b.4.** FCU.

**2.c. *\<Durante\>* Consulta**

> **2.c.1.** El usuario selecciona un proveedor existente y solicita consultar sus datos.
>
> **2.c.2.** El sistema muestra los datos del proveedor y el historial de comprobantes asociados.
>
> **2.c.3.** FCU.

**4.a. *\<Posterior\>* Proveedor duplicado (mismo CUIT)**

> **4.a.1.** El sistema detecta que ya existe un proveedor registrado con el CUIT ingresado.
>
> **4.a.2.** El sistema informa el conflicto y ofrece asociar el comprobante al proveedor existente.
>
> **4.a.3.** FCU.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** Gestión del proveedor realizada exitosamente.

**Éxito alternativo:** \<Omitido\>

**Fracaso:** Operación no realizada.

**Poscondición de sistema**

**Éxito:** El proveedor queda creado, actualizado o marcado como inactivo, disponible para su uso en el registro automático de compras.

**Éxito alternativo:** \<Omitido\>

**Fracasó:** Operación rechazada por validación, falta de permisos u otra condición que impida completar la operación.

### Diagramas de actividad y estado



## Generar Balance General

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Generar Balance General**

**Nombre:** *CUU-009 - \<Generar Balance General\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Generar automáticamente el Balance General (Estado Patrimonial) de la empresa a partir de los saldos del Libro Mayor, a una fecha de corte determinada.

**Actor Primario (dueño de la meta):** Contador

**Actor Iniciador:** Contador

**Disparador:** El usuario solicita la generación del Balance para una fecha de corte

**Precondiciones:**

- El Plan de Cuentas se encuentra configurado con la clasificación patrimonial (Activo / Pasivo / Patrimonio Neto) de cada cuenta.

- El Libro Mayor se encuentra actualizado a la fecha de corte solicitada.

> **CAMINO BÁSICO**

1.  El sistema recupera automáticamente los saldos actualizados de todas las cuentas patrimoniales del Libro Mayor a la fecha de corte solicitada.

2.  El sistema clasifica automáticamente cada cuenta según la naturaleza patrimonial definida en el Plan de Cuentas.

3.  El sistema calcula automáticamente los subtotales por rubro y los totales de Activo, Pasivo y Patrimonio Neto.

4.  El sistema valida automáticamente que se cumpla la igualdad **Activo = Pasivo + Patrimonio Neto.**

5.  El sistema genera el reporte del Balance General y lo pone a disposición del usuario para su consulta o exportación.

> **CAMINO ALTERNATIVO**

**2.a. *\<Posterior\>* Cuentas sin clasificación patrimonial**

> **2.a.1.** El sistema detecta cuentas sin clasificación patrimonial definida en el Plan de Cuentas.
>
> **2.a.2.** El sistema informa cuáles son las cuentas pendientes de clasificación y solicita al usuario completar su clasificación mediante *CUU-005 - \<Gestionar Plan de Cuentas\>*
>
> **2.a.3.** Una vez completada la clasificación, el sistema reprocesa. automáticamente la generación del Balance.

**4.a. *\<Posterior\>* Balance desbalanceado**

> **4.a.1.** El sistema detecta que no se cumple la igualdad Activo = Pasivo + Patrimonio Neto.
>
> **4.a.2.** El sistema informa la diferencia patrimonial detectada.
>
> **4.a.3.** El sistema no emite el reporte hasta que se identifique y corrija el origen de la diferencia, por ejemplo, un asiento pendiente o mal clasificado mediante *CUU-003 - \<Gestionar Libro Diario\>.*
>
> ***4.a.4.*** Continua en el paso 5.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** Balance General generado y con igualdad patrimonial verificada.

**Éxito alternativo:** Generación pendiente por existencia de cuentas sin clasificación patrimonial.

**Fracaso:** Balance no generado por desbalance patrimonial.

**Poscondición de sistema**

**Éxito:** Reporte disponible para consulta y exportación.

**Éxito alternativo:**

**Fracaso:** Reporte no emitido; el sistema informa el detalle de la diferencia patrimonial detectada.

### Diagramas de actividad y estado



## Generar Estado de Resultados

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Generar Estado de Resultados**

**Nombre:** *CUU-010 - \<Generar Estado de Resultados \>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Generar automáticamente el Estado de Resultados (pérdidas y ganancias) del período a partir de los saldos de las cuentas de resultado del Libro Mayor.

**Actor Primario (dueño de la meta):** Contador

**Actor Iniciador:** Contador

**Disparador:** El usuario solicita la generación del Estado de Resultados para un período

**Precondiciones:**

- El Plan de Cuentas se encuentra configurado con la clasificación patrimonial (Activo / Pasivo / Patrimonio Neto) de cada cuenta.

- El Libro Mayor se encuentra actualizado a la fecha de corte solicitada.

> **CAMINO BÁSICO**

1.  El sistema recupera automáticamente los saldos del período de las cuentas de Ingresos, Costos y Gastos del Libro Mayor.

2.  El sistema clasifica y agrupa automáticamente las cuentas según su naturaleza (ingresos operativos, costos, gastos y resultados financieros).

3.  El sistema calcula automáticamente los subtotales correspondientes y el Resultado del Ejercicio.

4.  El sistema genera el reporte del Estado de Resultados y lo pone a disposición del usuario para su consulta o exportación.

> **CAMINO ALTERNATIVO**

**2.a. *\<Posterior\>* Cuentas de resultado sin clasificación definida**

> **2.a.1.** El sistema detecta cuentas de resultado sin clasificación definida en el Plan de Cuentas.
>
> **2.a.2.** El sistema informa cuáles son las cuentas pendientes de clasificación y solicita al usuario completar su clasificación mediante CUU-05 *- \<Gestionar Plan de Cuentas\>*
>
> **2.a.3.** Continua en el Paso 3.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** Estado de Resultados generado correctamente.

**Éxito alternativo:** Generación pendiente por existencia de cuentas sin clasificar.

**Fracaso:** Estado de Resultados no generado.

**Poscondición de sistema**

**Éxito:** Reporte disponible para consulta y exportación.

**Éxito alternativo:**

**Fracaso:** Reporte no emitido por error en el cálculo o falta de datos del período.

### Diagramas de actividad y estado



## Exportar Libro Diario

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Exportar Libro Diario**

**Nombre:** *CUU-011 - \<Exportar Libro Diario \>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Exportar los asientos contables registrados en el Libro Diario para un período determinado, en un formato descargable (PDF o Excel).

**Actor Primario (dueño de la meta):** Contador / Administrativo contable

**Actor Iniciador:** Contador / Administrativo contable

**Disparador:** El usuario solicita la exportación del Libro Diario.

**Precondiciones:**

- El usuario se encuentra autenticado y posee permisos sobre el Libro Diario.

> **CAMINO BÁSICO**

1.  El usuario selecciona el período y el formato de exportación (PDF o Excel).

2.  El sistema recupera automáticamente los asientos contables registrados en el período y genera el archivo en el formato solicitado.

3.  El sistema pone el archivo a disposición del usuario para su descarga.

> **CAMINO ALTERNATIVO**

**2.a. *\<Posterior\>* No existen asientos para el período seleccionado**

> **2.a.1.** El sistema informa la situación y no genera el archivo.
>
> **2.a.2.** FCU.

**2.b. *\<Posterior\>* Error durante la generación del archivo**

**2.b.1.** El sistema detecta un error durante la generación del archivo.

**2.b.2.** El sistema informa el error y no genera el archivo.

> **2.b.3.** FCU.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** Exportación del Libro Diario realizada exitosamente.

**Éxito alternativo:** Exportación no realizada por ausencia de asientos o error durante la generación.

**Fracaso:** Exportación no realizada.

**Poscondición de sistema**

**Éxito:** Archivo generado en el formato solicitado y disponible para su descarga.

**Éxito alternativo:** Archivo no generado; el sistema informa la ausencia de datos o el error ocurrido durante la generación.

**Fracaso:** Exportación no realizada.

### Diagramas de actividad y estado



## Exportar Libro Mayor

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Exportar Libro Mayor**

**Nombre:** *CUU- 012 - \<Exportar Libro Mayor \>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Exportar los movimientos y saldos del Libro Mayor para una o varias cuentas y un período determinado, en un formato descargable (PDF o Excel).

**Actor Primario (dueño de la meta):** Contador / Administrativo contable

**Actor Iniciador:** Contador / Administrativo contable

**Disparador:** El usuario solicita la exportación del Libro Mayor.

**Precondiciones:**

- El usuario se encuentra autenticado y posee permisos sobre el Libro Mayor.

> **CAMINO BÁSICO**

1.  El usuario selecciona la cuenta o cuentas, el período y el formato de exportación (PDF o Excel).

2.  El sistema recupera automáticamente los movimientos y saldos correspondientes y genera el archivo en el formato solicitado.

3.  El sistema pone el archivo a disposición del usuario para su descarga.

> **CAMINO ALTERNATIVO**

**2.a. *\<Posterior\>* No existen movimientos para las cuentas y el período seleccionados**

> **2.a.1.** El sistema informa la situación y no genera el archivo.

**2.a.2.** FCU.

**2.b. *\<Posterior\>* Error durante la generación del archivo**

**2.b.1.** El sistema detecta un error durante la generación del archivo.

**2.b.2.** El sistema informa el error y no genera el archivo.

**2.b.3.** FCU.

> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** Exportación del Libro Mayor realizada exitosamente.

**Éxito alternativo:** Exportación no realizada por ausencia de movimientos o error durante la generación.

**Fracaso:** Exportación no realizada.

**Poscondición de sistema**

**Éxito:** Archivo generado en el formato solicitado y disponible para su descarga.

**Éxito alternativo:** Archivo no generado; el sistema informa la ausencia de datos o el error ocurrido durante la generación.

**Fracaso:** Exportación no realizada.

### Diagramas de actividad y estado



## Consultar historial de auditoría

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Consultar historial de auditoría**

**Nombre:** *CUU-013 - \<Consultar Historial de auditoría\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Consultar el historial de altas, modificaciones y anulaciones realizadas sobre la información contable (asientos, cuentas, clientes y proveedores), registrado automáticamente por el sistema en cada operación, a fines de auditoría y trazabilidad.

**Actor Primario (dueño de la meta):** Contador.

**Actor Iniciador:** Contador.

**Disparador:** El usuario accede al historial de auditoría.

**Precondiciones:**

- El usuario se encuentra autenticado y posee permisos de auditoría.

> **CAMINO BÁSICO**

1.  El usuario accede al historial de auditoría y aplica filtros (usuario responsable, entidad afectada, tipo de operación y rango de fechas).

2.  El sistema recupera y muestra automáticamente los registros de auditoría correspondientes a los filtros aplicados, incluyendo la entidad afectada, tipo de operación, usuario responsable, fecha y hora, y valores anteriores y nuevos cuando corresponda.

> **CAMINO ALTERNATIVO**

**2.a. *\<Posterior\>* No existen registros para los filtros aplicados**

> **2.a.1.** El sistema verifica que no existen registros de auditoría que coincidan con los filtros seleccionados.

**2.a.2.** El sistema informa la ausencia de registros.

**2.a.3.** FCU.

> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** Consulta del historial realizada exitosamente.

**Éxito alternativo:** Sin registros para los filtros aplicados.

**Fracaso:** No fue posible realizar la consulta.

**Poscondición de sistema**

**Éxito:** El sistema muestra los registros de auditoría correspondientes a los filtros aplicados.

**Éxito alternativo:** El sistema informa la ausencia de registros para los filtros aplicados.

**Fracaso:** Error de acceso a los datos o falta de permisos

### Diagramas de actividad y estado



## Exportar Libro IVA a ARCA

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Exportar Libro IVA a ARCA**

**Nombre:** *CUU-014 - \<Exportar Libro IVA a ARCA\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Generar los archivos de comprobantes y alícuotas correspondientes al Libro IVA Ventas o Libro IVA Compras, con el formato y la información requerida para su presentación ante ARCA.

**Actor Primario (dueño de la meta):** Contador / Administrativo contable

**Actor Iniciador:** Contador / Administrativo contable

**Disparador:** El usuario solicita la exportación del Libro IVA Ventas o Libro IVA Compras para un período determinado.

**Precondiciones:**

- El usuario se encuentra autenticado y posee permisos para consultar y exportar los Libros IVA.

- Los comprobantes del período se encuentran registrados en el sistema.

- La información necesaria para la exportación se encuentra disponible.

> **CAMINO BÁSICO**

1.  El usuario selecciona el Libro IVA Ventas o Libro IVA Compras y el período a exportar.

2.  El sistema recupera los comprobantes correspondientes al período seleccionado.

3.  El sistema genera el archivo de comprobantes con los datos requeridos por ARCA.

4.  El sistema identifica las distintas alícuotas de IVA correspondientes a cada comprobante y genera el archivo de alícuotas, registrando una línea por cada alícuota diferente.

5.  Si se trata del Libro IVA Compras, el sistema incorpora además las retenciones y percepciones sufridas por la empresa.

6.  El sistema valida que los archivos cumplan con la estructura y los datos requeridos.

7.  El sistema pone a disposición del usuario los archivos generados para su presentación ante ARCA.

> **CAMINO ALTERNATIVO**

***2.a. \<Posterior\> No existen comprobantes para el período seleccionado***

> ***2.a.1.*** El sistema informa la situación y no genera los archivos.
>
> ***2.a.2.*** FCU.

***3.a. \<Durante\> Falta información obligatoria en un comprobante***

> ***3.a.1.*** El sistema detecta que uno o más comprobantes no poseen información necesaria para la exportación.
>
> ***3.a.2.*** El sistema informa los comprobantes afectados y los datos faltantes.
>
> ***3.a.3.*** El sistema no genera los archivos hasta que la información sea completada o corregida.
>
> **3.a.4.** Continúa en el Paso 4.

***6.a. \<Posterior\> Error de validación del formato***

> ***6.a.1.*** El sistema detecta que alguno de los archivos no cumple con la estructura requerida.
>
> ***6.a.2.*** El sistema informa el error y no pone el archivo a disposición para su presentación.
>
> ***6.a.3.*** FCU.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** Exportación del Libro IVA realizada correctamente para el período seleccionado.

**Éxito alternativo:** Exportación no realizada debido a ausencia de comprobantes, falta de información obligatoria o errores de validación.

**Fracaso:** Exportación no realizada.

**Poscondición de sistema**

**Éxito:** Archivos de comprobantes y alícuotas generados y disponibles para su descarga.

**Éxito alternativo:** Archivos no generados; el sistema informa la causa que impide la exportación.

**Fracaso:** Exportación no realizada.

### Diagramas de actividad y estado



### Ejemplo de Exportación del Libro IVA a ARCA

Para la presentación del Libro IVA ante ARCA, el sistema genera los archivos correspondientes a los comprobantes y a las alícuotas de IVA. Para cada libro, tanto Ventas como Compras, se generan dos archivos: uno con los datos generales de los comprobantes y otro con las alícuotas de IVA aplicadas, generando una línea por cada alícuota diferente que tenga el comprobante.

En el caso del Libro IVA Compras, también se informa la información correspondiente a las retenciones y percepciones sufridas por la empresa.

Los archivos generados contienen la información requerida para la presentación ante ARCA, pero no incluyen el detalle de los productos o servicios incluidos en cada factura. Este detalle se mantiene disponible dentro del sistema de gestión interno.

A continuación, se muestra un ejemplo ilustrativo de la estructura del archivo de comprobantes correspondiente al Libro IVA Ventas y el significado de cada uno de sus campos.

**VENTAS archivo de comprobante**



| **Campo** | **Qué representa** | **Ejemplo genérico** |
|----|----|----|
| Fecha del comprobante | Fecha de emisión, formato AAAAMMDD. | 20250307 |
| Tipo de comprobante | Código de ARCA para el tipo de documento (001=Fact. A, 006=Fact. B, 003=NC A). | 006 |
| Punto de venta | Punto de venta habilitado desde el que se emitió. | 00003 |
| N° de comprobante (desde/hasta) | Numeración del comprobante. | 00004521 |
| Código de documento del receptor | Identifica si el cliente se informa con CUIT, CUIL o DNI. | 80 (CUIT) |
| N° de documento del receptor | CUIT o documento, completado con ceros a la izquierda hasta 20 posiciones. | 00000000020111111112 |
| Denominación del receptor | Nombre o razón social, hasta 30 posiciones. | Cliente Genérico S.R.L. |
| Importe total de la operación | Total del comprobante, IVA incluido. | 000000072600000 |
| Importe de conceptos no gravados | Parte del total no alcanzada por IVA. | 000000000000000 |
| Percepción a no categorizados | Percepción específica prevista por ARCA. | 000000000000000 |
| Importe de operaciones exentas | Parte del total correspondiente a operaciones exentas. | 000000000000000 |
| Percepciones/retenciones informadas | Otros impuestos nacionales, IIBB o municipales. | 000000000000000 |
| Código de moneda y tipo de cambio | Moneda de emisión y cotización. | PES 0001000000 |
| Cantidad de alícuotas de IVA | Cuántas alícuotas distintas contiene el comprobante. | 1 |
| CAE / CAI y fecha de vencimiento | Código de autorización otorgado por ARCA y su vencimiento. | 71234567890123 / 20250317 |

**VENTAS archivo de alícuota**



| **Campo** | **Qué representa** | **Ejemplo genérico** |
|----|----|----|
| Tipo, punto de venta y N° de comprobante | Identifican a qué comprobante del archivo CBTE corresponde. | 006 / 00003 / 00000000000000004521 |
| Importe neto gravado | Base imponible sobre la que se calculó el IVA de esa alícuota. | 000000060000000 |
| Alícuota de IVA (código) | Código de ARCA para la alícuota (5=21%, 4=10,5%, 6=27%). | 0005 |
| Impuesto liquidado | Monto de IVA calculado sobre el importe neto gravado. | 000000012600000 |

## Iniciar Sesión 

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Iniciar Sesión**

**Nombre:** *CUU-015 - \<Iniciar Sesión\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Permitir que un usuario registrado acceda al sistema mediante autenticación de múltiples factores.

**Actor Primario (dueño de la meta):** Usuario registrado

**Actor Iniciador:** Usuario registrado

**Disparador:** El usuario selecciona la opción "Iniciar sesión".

**Precondiciones:**

- El usuario se encuentra registrado en la base de datos.

- El usuario posee una cuenta corporativa asignada.

- El sistema de autenticación se encuentra disponible.

> **CAMINO BÁSICO**

1.  El usuario ingresa su correo corporativo y contraseña.

2.  El sistema verifica que el correo electrónico exista en la base de datos.

3.  El sistema valida la contraseña ingresada.

4.  El sistema genera y envía un token de autenticación mediante SMS o el mecanismo 2FA configurado.

5.  El usuario ingresa el token recibido.

6.  El sistema valida el token ingresado.

7.  El sistema autentica al usuario y le concede acceso al sistema.

> **CAMINO ALTERNATIVO**

**1.a. \<Durante\> El usuario olvidó su contraseña:**

> **1.a.1.** El usuario selecciona la opción "Restablecer contraseña".
>
> **1.a.2.** El sistema solicita el correo corporativo asociado.
>
> **1.a.3.** El usuario ingresa el correo corporativo.
>
> **1.a.4.** El sistema verifica que el correo exista en la base de datos.
>
> **1.a.5.** El sistema solicita validación de identidad mediante alguno de los mecanismos habilitados: código enviado por SMS, código enviado por correo electrónico o método 2FA configurado.
>
> **1.a.6.** El usuario completa la validación de identidad.
>
> **1.a.7.** El sistema habilita el cambio de contraseña.
>
> **1.a.8.** El usuario ingresa una nueva contraseña.
>
> **1.a.9.** El sistema valida que la contraseña cumpla las políticas de seguridad establecidas.
>
> **1.a.10.** El caso de uso continúa en el Paso 1.
>
> **1.a.9.a. \<Posterior\> La contraseña ingresada no cumple las políticas de seguridad:**
>
> **1.a.9.a.1.** El sistema informa al usuario las restricciones incumplidas.
>
> **1.a.9.a.2.** El sistema solicita el ingreso de una nueva contraseña.
>
> **1.a.9.a.3.** El caso de uso continúa en el paso 1.a.8.

**2.a. \<Posterior\> El correo ingresado no se encuentra registrado en la base de datos:**

> **2.a.1.** El sistema informa que el usuario no posee una cuenta asignada.
>
> **2.a.2.** El sistema solicita al usuario que contacte al administrador.
>
> **2.a.3.** FCU.

**3.a. \<Posterior\> La contraseña ingresada es incorrecta:**

**3.a.1**. El sistema informa que la contraseña es inválida.

**3.a.2**. El sistema verifica la cantidad de intentos fallidos de autenticación.

**3.a.3**. Si la cantidad de intentos fallidos es menor a tres, el sistema solicita un nuevo intento de autenticación.

**3.a.4.** Continúa en el paso 1.

**3.b. \<Posterior\> La contraseña ingresada es incorrecta por tercera vez consecutiva:**

> **3.b.1.** El sistema detecta que el usuario alcanzó el límite de tres intentos fallidos consecutivos.
>
> **3.b.2.** El sistema bloquea temporalmente la cuenta del usuario.
>
> **3.b.3.**El sistema informa al usuario que su cuenta ha sido bloqueada temporalmente y le indica el tiempo restante para poder volver a intentar iniciar sesión.
>
> **3.b.4.** FCU sin conceder acceso al sistema.

**6.a. \<Posterior\> El token ingresado es inválido o se encuentra vencido:**

> **6.a.1.** El sistema informa el motivo del rechazo.
>
> **6.a.2.** El sistema ofrece generar un nuevo token.
>
> **6.a.3.** El usuario solicita un nuevo token.
>
> **6.a.4.** Continúa en el paso 4.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** Usuario autenticado exitosamente.

**Éxito alternativo:** Contraseña restablecida y usuario habilitado para autenticarse nuevamente.

**Fracaso:** Usuario no autenticado.

**Poscondición de sistema**

**Éxito:** Sesión iniciada y acceso habilitado conforme a los permisos del usuario.

**Éxito alternativo:** Contraseña actualizada correctamente.

**Fracaso:** No se crea una sesión de usuario y no se concede acceso al sistema.

### Diagramas de actividad y estado



## Registrar comprobante con OCR

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Registrar comprobante con OCR**

**Nombre:** *CUU-016 - \<Registrar comprobante con OCR\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Registrar un comprobante digital mediante procesamiento OCR y NLP, obteniendo automáticamente los datos relevantes para su posterior contabilización.

**Actor Primario (dueño de la meta):** Contador / Administrativo contable

**Actor Iniciador:** Contador / Administrativo contable

**Disparador:**

- El usuario selecciona la opción de cargar un comprobante digital.

- *El usuario solicita leer un comprobante mediante OCR durante la registración de una venta CUU-001 - \<Registrar venta\> o una compra CUU-002 - \<Registrar compra\>*

**Precondiciones:**

- El usuario se encuentra autenticado.

- El usuario posee permisos para registrar comprobantes.

- El comprobante se encuentra disponible en formato PDF o imagen.

> **CAMINO BÁSICO**

1.  El usuario selecciona un comprobante para procesar.

2.  El sistema recibe el documento y ejecuta el proceso OCR/NLP.

3.  El sistema extrae e interpreta la información relevante del comprobante.

4.  El sistema calcula el nivel de confianza de los datos extraídos y ejecuta validaciones automáticas de consistencia (formato, fechas, CUIT, alícuotas e igualdad entre importe neto, IVA e importe total).

5.  El sistema presenta la información extraída, las validaciones realizadas y los niveles de confianza obtenidos.

6.  El usuario revisa la información presentada.

7.  El usuario confirma o corrige los datos extraídos.

8.  El sistema registra los datos definitivos del comprobante.

9.  El sistema registra la trazabilidad entre el documento original, los datos extraídos, las correcciones realizadas y el asiento contable asociado.

10. El sistema almacena el comprobante para su posterior utilización en los procesos contables.

11. El sistema informa que el comprobante fue registrado exitosamente.

> **CAMINO ALTERNATIVO**

***2.a. \<Durante\>** **El archivo cargado posee un formato no soportado***

> ***2.a.1.** El sistema informa que el formato del documento no es válido.*
>
> ***2.a.2.** El usuario selecciona otro archivo.*
>
> ***2.a.3.** Continua en el Paso 2.*

***3.a. \<Durante\> El OCR no puede extraer correctamente la información***

> **3.a.1.** El sistema informa que algunos campos no pudieron ser reconocidos.
>
> **3.a.2.** El sistema asigna nivel de confianza nulo o insuficiente a los campos afectados.
>
> **3.a.3.** El usuario completa o corrige los datos faltantes.
>
> **3.a.4.** Continúa en el Paso 10.

**4.a *\<Posterior\>* El nivel de confianza es inferior al umbral definido**

> **4.a.1** El sistema identifica los campos con nivel de confianza inferior al umbral mínimo configurado.  
> **4.a.2** El sistema marca dichos campos para revisión obligatoria.  
> **4.a.3** El sistema impide la confirmación automática del comprobante.  
> **4.a.4** El usuario revisa y corrige los campos señalados.  
> **4.a.5** El sistema registra la intervención manual realizada.  
> **4.a.6** Continúa en el Paso 10.

**6.a *\<Durante\>* Se detectan inconsistencias aritméticas o fiscales**  
**6.a.1.** El sistema detecta errores de consistencia en la información extraída.  
**6.a.2.** El sistema identifica los campos involucrados.  
**6.a.3.** El sistema impide la registración automática.  
**6.a.4.** El usuario corrige la información.  
**6.a.5.** Continúa en el Paso 10.

**7.a *\<Durante\>* El usuario rechaza la información extraída**

> **7.a.1** El usuario considera incorrectos los datos propuestos.  
> **7.a.2** El usuario modifica los datos necesarios.  
> **7.a.3** El sistema registra las correcciones efectuadas para fines de auditoría y trazabilidad.  
> **7.a.4** Continúa en el paso 10.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** El comprobante fue registrado y digitalizado correctamente.

**Éxito alternativo:** El comprobante queda parcialmente cargado para su corrección posterior.

**Fracaso:** El comprobante no está registrado.

**Poscondición de sistema**

**Éxito:**

- El documento queda almacenado junto con los datos estructurados obtenidos mediante OCR/NLP.

- Quedan registrados los niveles de confianza calculados.

- Queda almacenada la trazabilidad entre comprobante, extracción OCR/NLP, correcciones manuales y asiento contable generado.

**Éxito alternativo:** El comprobante queda en estado**"Pendiente de validación"** cuando existan campos con confianza inferior al umbral definido.

**Fracaso:** No se almacena información en el sistema.

### Diagramas de actividad y estado



## Validar comprobante con ARCA

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Validar comprobante con ARCA**

**Nombre:** *CUU-017 - \<Validar comprobante con ARCA\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Validar la autenticidad y vigencia de un comprobante fiscal mediante la integración con los servicios de ARCA.

**Actor Primario (dueño de la meta):** Contador / Administrativo contable

**Actor Iniciador:** Contador / Administrativo contable

**Disparador:** El usuario solicita validar un comprobante cargado en el sistema.

**Precondiciones:**

- El usuario se encuentra autenticado.

- Existe un comprobante registrado en el sistema.

- La integración con ARCA se encuentra configurada.

- Los servicios de ARCA se encuentran disponibles.

> **CAMINO BÁSICO**

1.  El usuario selecciona el comprobante a validar.

2.  El sistema recupera los datos fiscales necesarios.

3.  El sistema envía la consulta a ARCA.

4.  ARCA devuelve la información correspondiente al comprobante.

5.  El sistema verifica la vigencia del CAE y la consistencia de los datos recibidos.

6.  El sistema informa el resultado de la validación.

7.  El usuario confirma la visualización del resultado.

8.  El sistema actualiza el estado fiscal del comprobante

> **CAMINO ALTERNATIVO**

**3.a. *\<Durante\>* El servicio de ARCA no responde**

> **3.a.1.** El sistema informa que no fue posible establecer conexión.
>
> **3.a.2.** El comprobante queda pendiente de validación.
>
> **3.a.3.** FCU.

**4.a. *\<Durante\>* ARCA informa que el comprobante no existe**

> **4.a.1.** El sistema informa la inconsistencia detectada.
>
> **4.a.2.** El comprobante se marca como no válido.
>
> **4.a.3.** FCU.

**5.a. *\<Posterior\>* El CAE se encuentra vencido**

> **5.a.1.** El sistema muestra una alerta de advertencia.
>
> **5.a.2.** El comprobante es marcado como observado.
>
> **5.a.3.** FCU.

**6.a. *\<Posterior\>* Los datos recibidos difieren de los registrados**

> **6.a.1.** El sistema muestra las diferencias detectadas.
>
> **6.a.2.** El usuario revisa la información.
>
> **6.a.3.** El comprobante queda pendiente de auditoría.
>
> **6.a.4.** FCU.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** El comprobante fue validado satisfactoriamente.

**Éxito alternativo:** El comprobante queda pendiente de revisión o validación.

**Fracaso:** No fue posible validar el comprobante.

**Poscondición de sistema**

**Éxito:** El estado fiscal del comprobante queda actualizado con la información obtenida desde ARCA.

**Éxito alternativo:** El sistema registra la incidencia y deja el comprobante pendiente.

**Fracaso:** No se actualiza el estado de validación.

### Diagramas de actividad y estado



## Gestionar Usuarios

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Gestionar Usuarios**

**Nombre:** *CUU-018 - \<Gestionar Usuarios\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Permitir al Administrador del Sistema gestionar usuarios mediante operaciones de alta, modificación y baja

**Actor Primario (dueño de la meta):** Administrador del Sistema.

**Actor Iniciador:** Administrador del Sistema.

**Disparador:** El administrador accede al módulo Administración de Usuarios y selecciona una operación de gestión.

**Precondiciones:**

- El administrador se encuentra autenticado.

- El administrador posee permisos para gestionar usuarios.

> **CAMINO BÁSICO**

1.  El administrador accede al módulo Administración de Usuarios.

2.  El administrador selecciona la opción "Crear Usuario".

3.  El sistema solicita los datos requeridos.

4.  El administrador ingresa la información del nuevo usuario.

5.  El sistema valida la información ingresada.

6.  El sistema registra el nuevo usuario.

7.  El sistema genera las credenciales iniciales de acceso.

8.  El sistema informa que el usuario fue creado correctamente

> **CAMINO ALTERNATIVO**

**2.a. *\<Durante\>* Modificación de Usuario**

> **2.a.1.** El administrador selecciona un usuario existente.
>
> **2.a.2.** El sistema muestra la información actual del usuario.
>
> **2.a.3.** El administrador modifica datos y/o permisos.
>
> **2.a.4.** El sistema valida la información ingresada.
>
> **2.a.5.** El sistema actualiza la información del usuario.
>
> **2.a.6.** El sistema registra la modificación realizada en la auditoría.
>
> **2.a.7.** El sistema informa que la modificación fue realizada correctamente.
>
> **2.a.8.** FCU.

**2.b.*\<Durante\>* Baja de Usuario**

> **2.b.1.** El administrador selecciona un usuario existente.
>
> **2.b.2.** El sistema muestra la información del usuario.
>
> **2.b.3.** El administrador selecciona la opción "Dar de Baja".
>
> **2.b.4.** El sistema solicita confirmación de la operación.
>
> **2.b.5.** El administrador confirma la operación.
>
> **2.b.6.** El sistema desactiva al usuario.
>
> **2.b.7.** El sistema registra la operación en la auditoría.
>
> **2.b.8.** El sistema informa que el usuario fue dado de baja correctamente.
>
> **2.b.9.** FCU

**5.a. *\<Posterior\>* Datos inválidos o incompletos**

> **5.a.1.** El sistema detecta información inválida, incompleta o duplicada.
>
> **5.a.2.** El sistema informa el error encontrado.
>
> **5.a.3.** El administrador corrige la información.
>
> **5.a.4.** Continua en el paso 6.

**\*.a. *\<Durante\>* Error de procesamiento**

> **\*.1.** Ocurre un error al registrar, actualizar o desactivar el usuario.
>
> **\*.2.** El sistema informa que no fue posible completar la operación.
>
> **\*.3.** El sistema registra el incidente.
>
> **\*.4.** FCU.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** El usuario fue creado, actualizado o desactivado según la operación seleccionada.

**Éxito alternativo:** \<Omitido\>

**Fracaso:** : No se realizaron modificaciones sobre la información del usuario.

**Poscondición de sistema**

**Éxito:** Los cambios quedan almacenados y registrados en la auditoría del sistema.

**Éxito alternativo:** \<Omitido\>

**Fracaso:** No se realizan modificaciones sobre los datos persistidos.

### Diagramas de actividad y estado



## Gestionar Alertas de Auditoría

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Gestionar Alertas de Auditoría**

**Nombre:** *CUU-019 - \<Gestionar Alertas de Auditoría\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Identificar, consultar y gestionar alertas generadas automáticamente por el sistema ante posibles inconsistencias contables o fiscales.

**Actor Primario (dueño de la meta):** Contador

**Actor Iniciador:** Contador

**Disparador:** El usuario accede al módulo de auditoría para revisar alertas generadas por el sistema.

**Precondiciones:**

- El usuario se encuentra autenticado.

- Existen comprobantes y movimientos registrados en el sistema.

- El motor de auditoría se encuentra operativo

> **CAMINO BÁSICO**

1.  El usuario accede al módulo de auditoría.

2.  El sistema muestra el listado de alertas pendientes.

3.  El usuario selecciona una alerta.

4.  El sistema presenta el detalle de la inconsistencia detectada.

5.  El usuario analiza la información presentada.

6.  El usuario registra una acción sobre la alerta.

7.  El sistema actualiza el estado de la alerta.

8.  El sistema registra la acción realizada en el historial de auditoría.

9.  El sistema informa que la gestión fue realizada exitosamente.

> **CAMINO ALTERNATIVO**

**2.a. \<Durante\>** **No existen alertas pendientes**

> **2.a.1.** El sistema informa que no existen alertas para revisar.
>
> **2.a.2.** FCU.

**4.a. \<Durante\> La alerta corresponde a un comprobante duplicado**

> **4.a.1.** El sistema muestra los registros involucrados.
>
> **4.a.2.** El usuario decide continuar con la revisión.
>
> **4.a.3.** Continúa en paso 5.

**6.a. \<Durante\> El usuario descarta la alerta**

> **6.a.1.** El usuario indica que la alerta no representa una inconsistencia.
>
> **6.a.2.** El sistema registra la observación.
>
> **6.a.3.** El sistema marca la alerta como resuelta.
>
> **6.a.4.** FCU.

**6.b. \<Posterior\> El usuario requiere una revisión posterior**

> **6.b.1.** El usuario deja la alerta en estado pendiente.
>
> **6.b.2.** El sistema registra la observación correspondiente.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** La alerta fue gestionada correctamente.

**Éxito alternativo:** La alerta permanece pendiente para futuras revisiones.

**Fracaso:** No se realiza ninguna acción sobre la alerta.

**Poscondición de sistema**

**Éxito:** El estado de la alerta y el historial de auditoría son actualizados.

**Éxito alternativo:** La alerta queda registrada como pendiente.

**Fracaso:** No se producen modificaciones en el sistema.

### Diagramas de actividad y estado



## Generar Reportes Automáticos

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Generar Reportes Automáticos**

**Nombre:** *CUU-020 - \<Generar Reportes Automáticos\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Generar automáticamente reportes contables, financieros y fiscales a partir de la información registrada en el sistema.

**Actor Primario (dueño de la meta):** Contador

**Actor Iniciador:** Contador

**Disparador:** El usuario solicita la generación de un reporte.

**Precondiciones:**

- El usuario se encuentra autenticado.

- Existen registros contables almacenados en el sistema.

- El usuario posee permisos para consultar reportes.

> **CAMINO BÁSICO**

1.  El usuario accede al módulo de reportes.

2.  El sistema muestra los tipos de reportes disponibles.

3.  El usuario selecciona el reporte deseado.

4.  El usuario indica el período a analizar.

5.  El sistema recupera la información correspondiente.

6.  El sistema procesa los datos y genera el reporte.

7.  El sistema presenta una vista previa del reporte.

8.  El usuario confirma la generación.

9.  El sistema emite el reporte en el formato seleccionado.

10. El sistema informa que el reporte fue generado exitosamente.

> **CAMINO ALTERNATIVO**

**4.a. \<Durante\> El período seleccionado es inválido**

> **4.a.1**. El sistema informa el error.
>
> **4.a.2.** El usuario selecciona un nuevo período.
>
> **4.a.3.** Continua en el paso 4.

**5.a. \<Durante\> No existen registros para el período solicitado**

> **5.a.1.** El sistema informa que no hay datos disponibles.
>
> **5.a.2.** FCU.

**9.a. \<Durante\> El formato de exportación no está disponible**

> **9.a.1.** El sistema informa la situación.
>
> **9.a.2.** El usuario selecciona otro formato.
>
> **9.a.3**. Continua en el paso 9.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** El reporte solicitado es generado y puesto a disposición del usuario.

**Éxito alternativo:** Se genera un reporte parcial con la información disponible.

**Fracaso:** El reporte no puede ser generado.

**Poscondición de sistema**

**Éxito:** El reporte queda generado y almacenado para su consulta o descarga.

**Éxito alternativo:** Se registra la incidencia correspondiente.

**Fracaso:** No se genera ningún archivo ni salida de información.

### Diagramas de actividad y estado



## Consultar Dashboard Financiero

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Consultar Dashboard Financiero**

**Nombre:** *CUU-021 - \<Consultar Dashboard Financiero\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Visualizar indicadores financieros y contables consolidados para apoyar el análisis y la toma de decisiones.

**Actor Primario (dueño de la meta):** Contador

**Actor Iniciador:** Contador

**Disparador: El usuario solicita visualizar el panel de control financiero.**

**Precondiciones:**

- El usuario se encuentra autenticado.

- Existen registros contables en el sistema.

- Los indicadores financieros han sido calculados.

> **CAMINO BÁSICO**

1.  El usuario accede al dashboard financiero.

2.  El sistema recupera la información contable registrada.

3.  El sistema calcula los indicadores correspondientes.

4.  El sistema muestra gráficos y métricas financieras.

5.  El usuario consulta los indicadores presentados.

6.  El usuario aplica filtros de búsqueda o período.

7.  El sistema actualiza la información visualizada.

8.  El usuario finaliza la consulta.

> **CAMINO ALTERNATIVO**

**2.a. \<Posteriore\> No existen datos suficientes para generar indicadores**

> **2.a.1.** El sistema informa que no hay información disponible.
>
> **2.a.2.** FCU.

**6.a. \<Posterior\> El período seleccionado no contiene registros**

> **6.a.1.** El sistema informa que no existen movimientos para el período indicado.
>
> **6.a.2.** El usuario selecciona otro período.
>
> **6.a.3.** Continua en el paso 6.

**7.a. \<Durante\> Se produce un error al calcular indicadores**

> **7.a.1.** El sistema informa la imposibilidad de generar algunos indicadores.
>
> ***7.a.2.*** Se muestran únicamente los datos disponibles.
>
> ***7.a.3.*** FCU.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** El usuario obtiene una visión consolidada de la situación financiera de la organización.

**Éxito alternativo:** Se visualiza información parcial.

**Fracaso:** No es posible generar el dashboard.

**Poscondición de sistema**

**Éxito:** Los indicadores son calculados y presentados correctamente.

**Éxito alternativo:** El sistema registra los errores detectados y presenta los datos disponibles.

**Fracaso:** No se generan indicadores ni visualizaciones.

### Diagramas de actividad y estado



## Consultar estado de comprobante

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Consultar estado de comprobante**

**Nombre:** *CUU-022 - \<Consultar estado de comprobante\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Consultar el estado de procesamiento, validación y contabilización de un comprobante registrado en el sistema.

**Actor Primario (dueño de la meta):** Contador

**Actor Iniciador:** Contador

**Disparador:** El usuario solicita consultar el estado de un comprobante.

**Precondiciones:**

- El usuario se encuentra autenticado.

- Existe al menos un comprobante registrado en el sistema.

> **CAMINO BÁSICO**

1.  El usuario accede al módulo de comprobantes.

2.  El sistema muestra los comprobantes registrados.

3.  El usuario selecciona un comprobante.

4.  El sistema recupera la información asociada.

5.  El sistema muestra el estado actual del comprobante.

6.  El sistema presenta el historial de validaciones realizadas.

7.  El usuario consulta la información.

8.  El usuario finaliza la consulta.

> **CAMINO ALTERNATIVO**

**3.a. \<Durante\> El comprobante no existe**

> **3.a.1.** El sistema informa que el comprobante solicitado no fue encontrado.
>
> **3.a.2.** FCU.

**5.a. \<Durante\> El comprobante se encuentra pendiente de validación**

> **5.a.1.** El sistema muestra el estado "Pendiente de validación".
>
> **5.a.2.** Continua en el Paso 7.

**5.b. \<Durante\> El comprobante presenta observaciones**

> **5.b.1.** El sistema muestra las inconsistencias detectadas.
>
> **5.b.2.** El usuario revisa la información presentada.
>
> **5.b.3.** Continua en el Paso 6.

**6.a. No existen validaciones registradas**

> **6.a.1.** El sistema informa que el comprobante aún no fue validado.
>
> **6.a.2.** FCU.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** El usuario obtiene información completa sobre el estado del comprobante.

**Éxito alternativo:** Se visualiza información parcial debido a procesos pendientes.

**Fracaso:** No se puede acceder a la información solicitada.

**Poscondición de sistema**

**Éxito:** Se presentan correctamente el estado y el historial del comprobante.

**Éxito alternativo:** Se registran las incidencias detectadas durante la consulta.

**Fracaso:** No se recupera información del comprobante.

### Diagramas de actividad y estado



## Obtener recomendaciones financieras inteligentes

### Caso de uso

> **CASO DE USO - NIVEL USUARIO - Obtener recomendaciones Financieras Inteligentes**

**Nombre:** *CUU-023 - \<Obtener recomendaciones Financieras Inteligentes\>*

| **Alcance** | **Nivel** | **Estructura** | **Interacción** | **Caja** | **Instanciación** |
|----|----|----|----|----|----|
| Sistema | Usuario | Sin-estructura | Semántica | Negra | Real |

**Meta:** Obtener recomendaciones financieras inteligentes generadas mediante técnicas de análisis de datos e inteligencia artificial, con el fin de asistir al usuario en la toma de decisiones financieras y contables.

**Actor Primario (dueño de la meta):** Contador

**Actor Iniciador:** Contador

**Disparador:** El usuario solicita un análisis financiero inteligente desde el módulo de recomendaciones.

**Precondiciones:**

- El usuario se encuentra autenticado.

- Existen movimientos contables registrados en el sistema.

- Los datos financieros se encuentran actualizados.

- El módulo de análisis inteligente se encuentra operativo.

- El usuario posee permisos para acceder a información financiera.

> **CAMINO BÁSICO**

1.  El usuario accede al módulo de recomendaciones financieras.

2.  El sistema solicita el período a analizar.

3.  El usuario selecciona el período deseado.

4.  El sistema recupera la información contable, financiera y fiscal correspondiente.

5.  El sistema analiza los datos históricos registrados.

6.  El sistema calcula indicadores financieros relevantes.

7.  El sistema identifica tendencias, patrones y comportamientos significativos.

8.  El sistema genera recomendaciones basadas en los resultados obtenidos.

9.  El sistema clasifica las recomendaciones según su nivel de prioridad.

10. El sistema presenta las recomendaciones generadas junto con la justificación correspondiente.

11. El usuario consulta el análisis presentado.

12. El usuario finaliza la consulta.

> **CAMINO ALTERNATIVO**

**4.a. \<Posterior\> No existe información suficiente para realizar el análisis**

> **4.a.1.** El sistema detecta una cantidad insuficiente de datos históricos.
>
> **4.a.2.** El sistema informa que no es posible generar recomendaciones confiables.
>
> **4.a.3.** FCU.

**4.b. \<Durante\> Información histórica inaccesible**

> **4.b.1.** El sistema no puede acceder a los datos requeridos.
>
> **4.b.2.** El sistema informa la situación.
>
> **4.b.3.** FCU.

**5.a. \<Durante\> Se detectan registros incompletos**

> **5.a.1.** El sistema identifica información faltante o inconsistente.
>
> **5.a.2.** El sistema informa la situación al usuario.
>
> **5.a.3.** El sistema continúa el análisis utilizando únicamente los datos válidos.
>
> **5.a.4.** Continua en el Paso 6.

**5.b. \<Durante\> Error durante el procesamiento**

> **5.b.1.** El sistema detecta una falla durante el análisis.
>
> **5.b.2.** El sistema registra el incidente.
>
> **5.b.3.** El sistema informa al usuario que no fue posible completar la operación.
>
> **5.b.4.** FCU.

**7.a. \<Durante\> No se identifican anomalías ni tendencias relevantes**

> **7.a.1.** El sistema informa que no se detectaron situaciones que requieran atención inmediata.
>
> **7.a.2.** El sistema genera únicamente indicadores descriptivos.
>
> **7.a.3.** Continua en el Paso 10.

**8.a. \<Durante\> Se detecta riesgo financiero significativo**

> **8.a.1.** El sistema identifica una condición financiera potencialmente riesgosa.
>
> **8.a.2.** El sistema genera una alerta de alta prioridad.
>
> **8.a.3.** Continua en el Paso 9.

**8.b. \<Durante\> Se detectan oportunidades de mejora**

> **8.b.1.** El sistema identifica patrones favorables o posibilidades de optimización.
>
> **8.b.2.** El sistema genera recomendaciones preventivas o estratégicas.
>
> **8.b.3.** Continua en el Paso 9.

**10.a. \<Posterior\> El usuario solicita ampliar el detalle de una recomendación**

> **10.a.1.** El usuario selecciona una recomendación específica.
>
> **10.a.2**. El sistema presenta el análisis utilizado para generarla.
>
> **10.a.3.** El sistema muestra los indicadores y tendencias asociadas.
>
> **10.a.4.** Continúa en paso 11.
>
> **POSTCONDICIONES**

**Poscondición de negocio**

**Éxito:** El usuario obtiene recomendaciones financieras fundamentadas que le permiten evaluar riesgos, detectar oportunidades y mejorar la toma de decisiones.

**Éxito alternativo:** El usuario obtiene únicamente indicadores y tendencias descriptivas debido a limitaciones en los datos disponibles.

**Fracaso:** No es posible generar recomendaciones financieras.

**Poscondición de sistema**

**Éxito:** El sistema genera y muestra recomendaciones utilizando información histórica y modelos de análisis financiero.

**Éxito alternativo:** El sistema registra las limitaciones encontradas y presenta resultados parciales.

**Fracaso:** No se generan recomendaciones ni se producen modificaciones sobre los datos almacenados.

### Diagramas de actividad y estado



# Análisis de riesgos

En esta sección se analizan los riesgos identificados, teniendo en cuenta la probabilidad de que ocurran y el impacto que podrían generar en la organización. A partir de estos dos factores, se determina el nivel de severidad de cada riesgo, lo que permite establecer cuáles representan una mayor amenaza y cuáles requieren medidas de tratamiento prioritarias.

Para realizar este análisis, primero se identifican los riesgos asociados a los activos de la organización y se elabora un inventario de estos, considerando su importancia y los posibles efectos que tendría su pérdida, daño o indisponibilidad. Luego, los riesgos se clasifican según su severidad, con el objetivo de contar con un criterio que permita compararlos y definir cuáles deben abordarse con mayor urgencia.

La siguiente tabla presenta la clasificación de los riesgos según su nivel de severidad, considerando la probabilidad de ocurrencia y el impacto asociado a cada uno.



Una vez realizada esta clasificación, se profundiza en los tres riesgos que presentan los niveles de severidad más altos, ya que son los que requieren mayor atención. Para cada uno, se desarrolla una tabla de identificación del riesgo y se definen las medidas para su tratamiento. Además, se establecen los planes de contingencia, recuperación y continuidad del negocio, con el fin de determinar cómo actuar ante su ocurrencia, reducir sus consecuencias y mantener las actividades de la organización.

Para la identificación y el análisis de los riesgos se toma como referencia el enfoque FAIR (*Factor Analysis of Information Risk*), mientras que para definir las medidas de tratamiento se utiliza la norma ISO/IEC 27002:2022, que proporciona lineamientos para la implementación de controles de seguridad de la información.

## Identificación de riesgos

| **Id** | **Riesgo** | **Categoría** | **Probabilidad** | **Impacto** | **Severidad** |
|----|----|----|----|----|----|
| **R-01** | Un usuario del módulo contable EugenIA recibe un correo electrónico malicioso que contiene un archivo adjunto o enlace fraudulento. Al interactuar con él, se instala un malware o se comprometen sus credenciales, permitiendo posteriormente el acceso no autorizado al módulo y la modificación o eliminación de información contable. | Fallas de Sistemas y Tecnología | Probable (4) | Mayor (4) | **Muy alto (16)** |
| **R-03** | Una vulnerabilidad de seguridad en la aplicación expone datos comerciales y contables sensibles (clientes, proveedores, montos de operaciones). | Software / Ciberseguridad | Moderado (3) | Severo (5) | **Muy alto (15)** |
| **R-02** | El motor de OCR/IA interpreta incorrectamente un comprobante (monto, cuenta, IVA) y genera un asiento erróneo que pasa inadvertido en la revisión del usuario. | Software / Precisión del Motor de IA | Probable (4) | Significativo (3) | **Alto (12)** |
| **R-04** | La integración con los servicios de ARCA presenta fallas de conectividad, cambios de API o indisponibilidad temporal, impidiendo la validación automática de comprobantes fiscales y generando retrasos en los procesos contables. | Integraciones Externas | Moderado (3) | Significativo (3) | **Medio (9)** |
| **R-05** | El motor de análisis predictivo genera recomendaciones financieras incorrectas o poco confiables debido a datos históricos insuficientes, incompletos o inconsistentes, provocando decisiones de negocio basadas en información errónea. | Inteligencia Artificial / Calidad de Datos | Moderado (3) | Significativo (3) | **Medio (9)** |
| **R-06** | Un usuario carga un comprobante ilegible, incompleto o con baja calidad de imagen, impidiendo su procesamiento automático y requiriendo intervención manual. | Operación / Calidad de Datos | Probable (4) | Menor (2) | **Medio (8)** |
| **R-07** | Una actualización del navegador utilizado por los usuarios provoca problemas de visualización o funcionamiento en algunos módulos de EugenIA. | Software / Compatibilidad | Moderado (3) | Menor (2) | **Medio (6)** |
| **R-08** | Errores involuntarios de configuración de parámetros contables o fiscales generan resultados incorrectos en reportes y consultas hasta que son detectados y corregidos. | Personas / Operación | Moderado (3) | Menor (2) | **Medio (6)** |
| **R-09** | El usuario configura filtros o parámetros de busqueda incorrectos al consultar dashboards o reportes, obteniendo información incompleta o poco representativa | Personas / Operación | Moderado (3) | Menor (2) | **Baja (6)** |
| **R-10** | La generación de reportes o dashboards presenta demoras ocasionales durante períodos de alta carga del sistema, afectando temporalmente la experiencia del usuario. | Rendimiento / Operación | Poco probable (2) | Menor (2) | **Baja (4)** |

## Inventario activos

<table>
<colgroup>
<col style="width: 10%" />
<col style="width: 18%" />
<col style="width: 9%" />
<col style="width: 9%" />
<col style="width: 8%" />
<col style="width: 4%" />
<col style="width: 3%" />
<col style="width: 3%" />
<col style="width: 22%" />
<col style="width: 10%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Activos</strong></th>
<th style="text-align: center;"><strong>Descripción</strong></th>
<th style="text-align: center;"><strong>Tipo</strong></th>
<th style="text-align: center;"><strong>Dueño</strong></th>
<th style="text-align: center;"><strong>Custodio</strong></th>
<th style="text-align: center;"><strong>C</strong></th>
<th style="text-align: center;"><strong>I</strong></th>
<th style="text-align: center;"><strong>D</strong></th>
<th style="text-align: center;"><strong>Relación con otros activos</strong></th>
<th style="text-align: center;"><strong>Riesgos asociados</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>EugenIA</strong></th>
<th style="text-align: left;">Módulo contable utilizado para la carga de comprobantes y generación de asientos contables.</th>
<th>Software</th>
<th>Área Contable</th>
<th>Sistemas / TI</th>
<th>5</th>
<th>5</th>
<th>4</th>
<th style="text-align: left;"><p><strong>Hardware:</strong> Computadora del usuario, servidor.</p>
<p><strong>Servicios</strong>: Servicio de conectividad a Internet.</p>
<p><strong>Activos de información:</strong> Comprobantes contables, asientos contables, credenciales de acceso, registros de auditoría y archivos originales de comprobantes.</p>
<p><strong>Software:</strong> Motor de base de datos, motor OCR/IA, integración con ARCA y APIs externas.</p></th>
<th><strong>R-01, R-02, R-03, R-04, R-07, R-08, R-09, R-10</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>Base de datos contable</strong></th>
<th style="text-align: left;">Base de datos donde se almacena la información generada por el módulo contable, incluyendo comprobantes y asientos.</th>
<th>Soporte</th>
<th>Área Contable</th>
<th>Sistemas / TI</th>
<th>5</th>
<th>5</th>
<th>4</th>
<th style="text-align: left;"><p><strong>Software:</strong> EugenIA, motor de base de datos.</p>
<p><strong>Hardware:</strong> Servidor.</p>
<p><strong>Activos de información:</strong> Comprobantes contables, asientos contables, datos de clientes y proveedores, datos históricos contables y copias de seguridad.</p></th>
<th><strong>R-01, R-02, R-03, R-05</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>Comprobantes contables</strong></th>
<th style="text-align: left;">Información correspondiente a los comprobantes que se cargan en EugenIA para registrar las operaciones contables.</th>
<th>Activo de Información</th>
<th>Área Contable</th>
<th>Personal Contable</th>
<th>5</th>
<th>5</th>
<th>3</th>
<th style="text-align: left;"><p><strong>Software:</strong> EugenIA, motor OCR/IA.</p>
<p><strong>Soporte:</strong> Base de datos contable, copias de seguridad.</p>
<p><strong>Hardware:</strong> Computadora del usuario.</p>
<p><strong>Activos de información:</strong> Archivos originales de comprobantes, datos de clientes y proveedores.</p></th>
<th><strong>R-01, R-02, R-06</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>Asientos contables</strong></th>
<th style="text-align: left;">Registros generados a partir de los comprobantes y utilizados para representar las operaciones contables.</th>
<th>Activo de Información</th>
<th>Área Contable</th>
<th>Personal Contable</th>
<th>5</th>
<th>5</th>
<th>4</th>
<th style="text-align: left;"><p><strong>Software:</strong> EugenIA, motor OCR/IA.</p>
<p><strong>Soporte:</strong> Base de datos contable, copias de seguridad.</p>
<p><strong>Activos de información:</strong> Comprobantes contables, registros de auditoría, datos históricos contables.</p></th>
<th><strong>R-01, R-02</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>Computadora del usuario</strong></th>
<th style="text-align: left;">Equipo utilizado por el personal contable para acceder a EugenIA y realizar la carga de comprobantes.</th>
<th>Hardware</th>
<th>Área Contable</th>
<th>Personal Contable</th>
<th>4</th>
<th>4</th>
<th>4</th>
<th style="text-align: left;"><p><strong>Software:</strong> EugenIA, sistema operativo, antivirus/EDR, motor OCR/IA (mediante acceso al sistema).</p>
<p><strong>Servicios</strong>: Servicio de conectividad a Internet, correo electrónico.</p>
<p><strong>Activos de información:</strong> Credenciales de acceso, archivos originales de comprobantes.</p></th>
<th><strong>R-01, R-03, R-06, R-07</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>Credenciales de acceso</strong></th>
<th style="text-align: left;">Datos de autenticación utilizados por los usuarios autorizados para acceder al módulo contable.</th>
<th>Activo de Información</th>
<th>Área Contable</th>
<th>Sistemas / TI</th>
<th>5</th>
<th>5</th>
<th>4</th>
<th style="text-align: left;"><p><strong>Software:</strong> EugenIA.</p>
<p><strong>Activos:</strong> Usuarios del sistema.registros de auditoría.</p>
<p><strong>Hardware:</strong> Computadora del usuario.</p></th>
<th><strong>R-01, R-03</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>Servidor</strong></th>
<th style="text-align: left;">Equipo que aloja o permite procesar los servicios necesarios para el funcionamiento de EugenIA y el almacenamiento de la información contable.</th>
<th>Hardware</th>
<th>Sistemas / TI</th>
<th>Sistemas / TI</th>
<th>5</th>
<th>5</th>
<th>5</th>
<th style="text-align: left;"><p><strong>Software:</strong> EugenIA, motor de base de datos, motor OCR/IA.</p>
<p><strong>Activos de información:</strong> Base de datos contable, registros de auditoría, copias de seguridad.</p>
<p><strong>Servicios:</strong> Servicio de conectividad a Internet.</p></th>
<th><strong>R-01, R-03, R-10</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>Motor de base de datos</strong></th>
<th style="text-align: left;">Software encargado de gestionar y almacenar la información utilizada por EugenIA.</th>
<th>Software</th>
<th>Sistemas / TI</th>
<th>Sistemas / TI</th>
<th>5</th>
<th>5</th>
<th>5</th>
<th style="text-align: left;"><p><strong>Software:</strong> EugenIA.</p>
<p><strong>Hardware:</strong> Servidor.</p>
<p><strong>Soporte:</strong> Base de datos contable.</p>
<p><strong>Activos de información:</strong> Comprobantes contables, asientos contables, datos de clientes y proveedores, datos históricos contables.</p></th>
<th><strong>R-01, R-03, R-05, R-10</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>Correo electrónico</strong></th>
<th style="text-align: left;">Medio utilizado por el personal contable para recibir y enviar comunicaciones con clientes, proveedores y otras entidades.</th>
<th>Servicio</th>
<th>Área Contable</th>
<th>Sistemas / TI</th>
<th>4</th>
<th>4</th>
<th>4</th>
<th style="text-align: left;"><p><strong>Hardware:</strong> Computadora.</p>
<p><strong>Act. Información:</strong> Comprobantes y comunicaciones.</p></th>
<th><strong>R-01</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>Registros de auditoría (Logs)</strong></th>
<th style="text-align: left;">Registros de accesos y actividades realizadas sobre EugenIA, utilizados para detectar y analizar modificaciones o accesos no autorizados.</th>
<th>Activo de Información</th>
<th>Sistemas / TI</th>
<th>Sistemas / TI</th>
<th>4</th>
<th>5</th>
<th>4</th>
<th style="text-align: left;"><p><strong>Software:</strong> EugenIA.</p>
<p><strong>Soporte:</strong> Servidor / Base de datos.</p></th>
<th><strong>R-01, R-02, R-03</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>Copias de seguridad</strong></th>
<th style="text-align: left;">Respaldos periódicos de la información contable utilizados para recuperar los datos ante incidentes.</th>
<th>Activo de Información</th>
<th>Sistemas / TI</th>
<th>Sistemas /</th>
<th>4</th>
<th>5</th>
<th>5</th>
<th style="text-align: left;"><p><strong>Hardware:</strong> Servidor o repositorio de respaldo. <strong>Soporte:</strong> Base de datos contable.</p>
<p><strong>Act. Información:</strong> Comprobantes contables, Asientos contables, Datos históricos contables.</p></th>
<th><strong>R-01</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>Motor OCR/IA</strong></th>
<th style="text-align: left;">Componente que interpreta los comprobantes y extrae datos como montos, cuentas contables e IVA para generar registros.</th>
<th>Software</th>
<th>Sistemas / TI</th>
<th>Sistemas / TI</th>
<th>4</th>
<th>5</th>
<th>4</th>
<th style="text-align: left;"><p><strong>Software</strong>: EugenIA.</p>
<p><strong>Soporte:</strong> Base de datos contable.</p>
<p><strong>Activos de apoyo:</strong> Registros de auditoría.</p>
<p><strong>Act. Información:</strong> Archivos originales de comprobantes, Comprobantes contables, Asientos contables.</p></th>
<th><strong>R-02, R-06</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>Datos de clientes y proveedores</strong></th>
<th style="text-align: left;">Información comercial y contable de clientes y proveedores, incluyendo los datos sensibles mencionados en el riesgo de exposición.</th>
<th>Activo de Información</th>
<th>Área Contable</th>
<th>Personal Contable</th>
<th>5</th>
<th>5</th>
<th>4</th>
<th style="text-align: left;"><p><strong>Software:</strong> EugenIA.</p>
<p><strong>Soporte:</strong> Base de datos contable.</p>
<p><strong>Act. Información:</strong> Comprobantes contables.</p>
<p><strong>Servicios:</strong> Integración con ARCA y APIs externas, cuando corresponda.</p></th>
<th><strong>R-03</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>Integración con ARCA y APIs externas</strong></th>
<th style="text-align: left;">Interfaces y servicios utilizados para validar comprobantes fiscales y comunicarse con sistemas externos.</th>
<th>Software</th>
<th>Sistemas / TI</th>
<th>Sistemas / TI</th>
<th>4</th>
<th>5</th>
<th>4</th>
<th style="text-align: left;"><p><strong>Software:</strong> EugenIA.</p>
<p><strong>Servicios</strong>: ARCA, APIs externas, Internet.</p>
<p><strong>Act. Información:</strong> Comprobantes contables.</p></th>
<th><strong>R-03, R-04</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>Datos históricos contables</strong></th>
<th style="text-align: left;">Información histórica utilizada por el análisis predictivo para generar recomendaciones financieras.</th>
<th>Activo de Información</th>
<th>Área Contable</th>
<th>Personal Contable</th>
<th>3</th>
<th>5</th>
<th>4</th>
<th style="text-align: left;"><p><strong>Soporte:</strong> Base de datos contable.</p>
<p><strong>Software:</strong> Motor de análisis predictivo, EugenIA.</p>
<p><strong>Act. Información:</strong> Asientos contables, Informes financieros.</p></th>
<th><strong>R-05</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>Archivos originales de comprobantes</strong></th>
<th style="text-align: left;">Imágenes o documentos originales cargados por los usuarios y utilizados para verificar los datos extraídos.</th>
<th>Activo de Información</th>
<th>Área Contable</th>
<th>Personal Contable</th>
<th>4</th>
<th>5</th>
<th>4</th>
<th style="text-align: left;"><p><strong>Hardware:</strong> Computadora del usuario.</p>
<p><strong>Software:</strong> EugenIA, Motor OCR/IA.</p>
<p><strong>Act. Información:</strong> Comprobantes contables, Registros de auditoría.</p>
<p><strong>Soporte:</strong> Base de datos contable y copias de seguridad</p></th>
<th><strong>R-02, R-06</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>Informes y dashboards</strong></th>
<th style="text-align: left;">Informes y tableros que presentan información contable y financiera a partir de consultas y filtros.</th>
<th>Software</th>
<th>Área Contable</th>
<th>Personal Contable</th>
<th>4</th>
<th>4</th>
<th>3</th>
<th style="text-align: left;"><p><strong>Software</strong>: EugenIA, Motor de base de datos.</p>
<p><strong>Soporte:</strong> Base de datos contable.</p>
<p><strong>Act. Información:</strong> Datos históricos contables, Parámetros contables y fiscales.</p></th>
<th><strong>R-05, R-09, R-10</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>Servicio de conectividad a Internet</strong></th>
<th style="text-align: left;">Servicio de red necesario para acceder al módulo web y comunicarse con servicios externos.</th>
<th>Servicio</th>
<th>Sistemas / TI</th>
<th>Sistemas / TI</th>
<th>3</th>
<th>3</th>
<th>4</th>
<th style="text-align: left;"><p><strong>Hardware:</strong> Computadora del usuario,</p>
<p><strong>Servidor.</strong> Software: EugenIA.</p>
<p><strong>Servicios:</strong> Correo electrónico, Integración con ARCA y APIs externas.</p></th>
<th><strong>R-04, R-07</strong></th>
</tr>
<tr>
<th style="text-align: left;"><strong>Software antivirus/EDR</strong></th>
<th style="text-align: left;">Herramienta de protección del equipo frente a malware y otras amenazas. Su instalación y configuración deben confirmarse.</th>
<th>Software</th>
<th>Sistemas / TI</th>
<th>Sistemas / TI</th>
<th>3</th>
<th>4</th>
<th>4</th>
<th style="text-align: left;"><p><strong>Hardware:</strong> Computadora del usuario.</p>
<p><strong>Software:</strong> Sistema operativo.</p></th>
<th><strong>R-01</strong></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## Riesgo 1: Phishing y acceso no autorizado

### Identificación de riesgo

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 14%" />
<col style="width: 20%" />
<col style="width: 30%" />
</colgroup>
<thead>
<tr>
<th>Id. 01</th>
<th colspan="4"></th>
</tr>
<tr>
<th><strong>Identificador</strong></th>
<th colspan="4"></th>
</tr>
<tr>
<th><strong>Especificación</strong></th>
<th colspan="4">Un usuario del módulo contable EugenIA recibe un correo electrónico malicioso que contiene un archivo adjunto o enlace fraudulento. Al interactuar con él, se instala un malware o se comprometen sus credenciales, permitiendo posteriormente el acceso no autorizado al módulo y la modificación o eliminación de información contable.</th>
</tr>
<tr>
<th><strong>Clasificación</strong></th>
<th colspan="2">Fallas de Sistemas y Tecnología</th>
<th>Software</th>
<th>Parámetros de seguridad</th>
</tr>
<tr>
<th colspan="5"><strong>Descripción ampliada del Contexto del Riesgo</strong></th>
</tr>
<tr>
<th colspan="5"><p>Se detecta un incidente de seguridad a partir de la recepción de un correo electrónico malicioso por parte de un usuario autorizado al módulo contable Eugenia. El mensaje aparenta provenir de un cliente, proveedor o entidad bancaria habitual.</p>
<p>El usuario interactúa con un archivo adjunto o enlace, provocando la ejecución de software malicioso o el ingreso de sus credenciales en un sitio fraudulento. Como consecuencia, el atacante obtiene acceso al equipo o a las credenciales del usuario y utiliza la cuenta comprometida para consultar, modificar o eliminar información contable.</p>
<p>El incidente afecta principalmente la integridad de la información, ya que se modifican registros contables sin autorización. También se compromete la confidencialidad de la información y, dependiendo del malware, su disponibilidad.</p></th>
</tr>
<tr>
<th colspan="5" style="text-align: center;"><strong>VALORACIÓN DEL RIESGO</strong></th>
</tr>
<tr>
<th colspan="5"><p><strong>ACTIVOS</strong> involucrados y dimensión de <strong>valor de su criticidad</strong>:</p>
<p>En la planilla de activos se ha establecido el nivel de criticidad de los activos afectados.</p></th>
</tr>
<tr>
<th colspan="5"><p><strong>F<em>actores analizados para el cálculo de la probabilidad del riesgo inherente:</em></strong></p>
<p><strong>Frecuencia de amenaza:</strong></p>
<ul>
<li><p><strong>Contacto:</strong></p></li>
</ul>
<blockquote>
<p>Aleatorio: No</p>
<p>Intencional: Si</p>
<p>Regular: No</p>
</blockquote>
<ul>
<li><p><strong>Acción:</strong> Materializada la amenaza de este riesgo, el proceso se ve afectado en su operatoria normal.</p>
<ul>
<li><p><strong>Beneficio:</strong> El atacante podría obtener información financiera, modificar registros o utilizar las credenciales comprometidas para realizar acciones dentro del sistema.</p></li>
<li><p><strong>Nivel de esfuerzo:</strong> Medio-Alto.</p></li>
<li><p><strong>Riesgo de detección:</strong> Medio-Alto. Si el atacante utiliza credenciales válidas, determinadas acciones podrían parecer realizadas por el usuario legítimo y no ser detectadas inmediatamente.</p></li>
</ul></li>
</ul>
<ul>
<li><p><strong>Capacidad de la Amenaza:</strong> Alto. El phishing puede facilitar el robo de credenciales y la ejecución de malware, que podría comprometer los sistemas y afectar la disponibilidad e integridad de la base de datos contable de EugenIA.</p></li>
<li><p><strong>Capacidad de Resistencia:</strong> Media-Baja<strong>.</strong> Si bien existen mecanismos de seguridad, el usuario continúa siendo un punto vulnerable frente a técnicas de ingeniería social. La falta de capacitación específica, controles sobre enlaces y archivos adjuntos o mecanismos de monitoreo podría facilitar la materialización del riesgo.</p></li>
</ul>
<p><strong>Utilizando la escala de valores se puede decir que la probabilidad es: Probable (4).</strong></p>
<p><em>Factores analizados para el cálculo del <strong>impacto</strong> del riesgo inherente:</em></p>
<p><strong>Activos:</strong> En la planilla de activos se ha establecido el nivel de criticidad de los activos afectados. Además se puede considerar:</p>
<ul>
<li><p><strong>Productividad:</strong> La productividad puede verse afectada debido a la necesidad de revisar los registros contables, identificar cuáles fueron modificados y realizar nuevamente las operaciones que hayan quedado inconsistentes. Además, si el incidente genera indisponibilidad del sistema o bloqueo de información, las tareas contables podrían tener que realizarse temporalmente de manera manual.</p></li>
</ul>
<ul>
<li><p><strong>Costo de reemplazo:</strong> Este costo estará dado por</p>
<ul>
<li><p>Tiempo necesario para identificar y solucionar el incidente.</p></li>
<li><p>Recuperación de la información mediante copias de seguridad.</p></li>
<li><p>Revisión de los registros afectados.</p></li>
<li><p>Reprocesamiento de operaciones contables.</p></li>
<li><p>Tiempo de indisponibilidad del sistema.</p></li>
<li><p>Posibles costos asociados a la recuperación del equipo comprometido.</p></li>
</ul></li>
</ul>
<ul>
<li><p><strong>Sensibilidad:</strong> En este riesgo se trata la divulgación de información confidencial.</p>
<ul>
<li><p><strong>Reputación:</strong> La organización podría perder confianza por parte de clientes, proveedores y otros actores si se conoce que su información contable fue comprometida.</p></li>
<li><p><strong>Ventaja competitiva:</strong> La exposición de información financiera podría proporcionar información útil para terceros, dependiendo del tipo de datos que haya sido obtenido.</p></li>
<li><p><strong>Legal / Regulatoria:</strong> El incumplimiento de las normativas vigentes de protección de datos personales y seguridad de la información puede derivar en sanciones impuestas por la ley.</p></li>
</ul></li>
<li><p><strong>Volumen</strong>:</p>
<ul>
<li><p>El impacto dependerá de la cantidad de registros que hayan sido modificados, eliminados o expuestos desde el momento en que se comprometieron las credenciales hasta la detección del incidente.</p></li>
<li><p>También se deberá considerar la cantidad de operaciones realizadas durante ese período que deban ser revisadas para determinar si fueron afectadas.</p></li>
</ul></li>
</ul>
<p><strong>Amenazas:</strong> La amenaza es Phishing dirigido al usuario del módulo contable, con el objetivo de obtener credenciales o introducir malware en el equipo desde el cual se accede a Eugenia.</p>
<ul>
<li><p><strong>Competencias:</strong> El personal no cuenta con formación suficiente en ciberseguridad, lo que dificulta la identificación de correos maliciosos y la correcta actuación ante amenazas. Además, no existen políticas claras ni controles técnicos adecuados para prevenir la ejecución de software dañino o detectar intrusiones a tiempo</p></li>
<li><p><strong>Internas/Externas:</strong> el agente es <strong>externo.</strong></p></li>
<li><p><strong>Acción</strong>:</p>
<ul>
<li><p><strong>Acceso</strong>: Acceso no autorizado.</p></li>
<li><p><strong>Uso indebido</strong>: Sí aplica.</p></li>
<li><p><strong>Divulgación</strong>: Existe riesgo de acceso y extracción de información contable.</p></li>
<li><p><strong>Modificación</strong>: El atacante podría modificar registros contables utilizando la cuenta comprometida.</p></li>
<li><p><strong>Denegación de acceso</strong>: Podría producirse si el malware bloquea archivos o impide el acceso al sistema.</p></li>
</ul></li>
</ul>
<p><strong>Organización:</strong></p>
<ul>
<li><p><strong>Momento:</strong> Los back-up se realizan solo una vez a la semana por lo que tendrá un impacto de pérdida mayor dependiendo del día que se presenta.</p></li>
<li><p><strong>Debido al cuidado</strong>: No se conocen medidas preventivas.</p></li>
<li><p><strong>Detección:</strong> Se conoce cuando los empleados informan modificaciones inesperadas o cuando el propio usuario detecta que realizó una acción sobre un correo sospechoso</p></li>
<li><p><strong>Respuesta:</strong></p>
<ul>
<li><p><strong>Contención:</strong> Bloquear la cuenta comprometida y aislar el equipo afectado.</p></li>
<li><p><strong>Remediación:</strong> No existe.</p></li>
<li><p><strong>Recuperación:</strong> No existe.</p></li>
</ul></li>
</ul>
<p><strong>Factores externos:</strong> Es un riesgo que puede ser utilizado por una entidad externa para aumentar el impacto de la pérdida o alteración de información</p>
<ul>
<li><p><strong>Detección</strong>: El ataque podría ser detectado rápidamente si existen mecanismos de monitoreo y registro de las actividades realizadas en Eugenia. Sin estos controles, un atacante que utilice credenciales válidas podría permanecer sin ser detectado durante un período de tiempo.</p></li>
<li><p><strong>Legal/Regulatorio</strong>: Existe un riesgo elevado si además de modificar información contable se produce una exposición de datos financieros o personales almacenados en el sistema.</p></li>
<li><p><strong>Competidores</strong>: La información obtenida podría ser utilizada por terceros para obtener información sobre la situación económica o comercial de la organización.</p></li>
<li><p><strong>Medios de comunicación</strong>: En caso de que el incidente provoque una filtración importante de información, su conocimiento público podría afectar negativamente la imagen y confianza en la organización.</p></li>
</ul>
<p><strong>Utilizando la escala de valores se puede decir que el impacto es: Mayor (4).</strong></p>
<p><strong>Para concluir, podemos considerar que la severidad es: Muy Alto (16)</strong></p></th>
</tr>
<tr>
<th><strong>Consecuencias</strong></th>
<th colspan="4"><ul>
<li><p>Modificación o eliminación de registros contables.</p></li>
<li><p>Pérdida de integridad de la información.</p></li>
<li><p>Exposición de información financiera.</p></li>
<li><p>Posible robo de credenciales.</p></li>
<li><p>Errores en reportes y saldos contables.</p></li>
<li><p>Necesidad de revisar y procesar operaciones.</p></li>
<li><p>Interrupción parcial de las actividades contables.</p></li>
<li><p>Costos asociados a la recuperación del sistema.</p></li>
<li><p>Posibles consecuencias legales o regulatorias.</p></li>
<li><p>Pérdida de confianza de clientes y proveedores.</p></li>
</ul></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

### Tratamiento de riesgos

<table>
<colgroup>
<col style="width: 5%" />
<col style="width: 14%" />
<col style="width: 16%" />
<col style="width: 63%" />
</colgroup>
<thead>
<tr>
<th colspan="2">Id. 01</th>
<th colspan="2"></th>
</tr>
<tr>
<th colspan="2"><strong>Identificador</strong></th>
<th colspan="2"></th>
</tr>
<tr>
<th colspan="2"><strong>Especificación</strong></th>
<th colspan="2">Un usuario del módulo contable EugenIA recibe un correo electrónico malicioso que contiene un archivo adjunto o enlace fraudulento. Al interactuar con él, se instala un malware o se comprometen sus credenciales, permitiendo posteriormente el acceso no autorizado al módulo y la modificación o eliminación de información contable.</th>
</tr>
<tr>
<th rowspan="6" style="text-align: center;"><blockquote>
<p><strong>ESTRATEGIAS</strong></p>
</blockquote></th>
<th colspan="3" style="text-align: center;"><strong>EVITAR</strong></th>
</tr>
<tr>
<th colspan="3"><mark>No se puede evitar.</mark></th>
</tr>
<tr>
<th colspan="3" style="text-align: center;"><strong>TRANSFERIR</strong></th>
</tr>
<tr>
<th colspan="3"><mark>No se puede transferir.</mark></th>
</tr>
<tr>
<th colspan="3" style="text-align: center;"><strong>MITIGAR</strong></th>
</tr>
<tr>
<th colspan="3"><p><strong>En cuanto a mitigar la probabilidad de materialización del riesgo:</strong></p>
<ol type="1">
<li><p>Contratar a un especialista en ciberseguridad.</p></li>
<li><p>Capacitar de forma continua al personal en ciberseguridad para que puedan detectar correos sospechosos.</p></li>
<li><p>Implementar y mantener un antivirus/EDR actualizado</p></li>
<li><p>Implementar mecanismos de detección y prevención de intrusos (IDS/IPS).</p></li>
<li><p>Implementar políticas de seguridad sobre el uso del correo, contraseñas y gestión de incidentes.</p></li>
<li><p>Reforzar la autenticación multifactor (2MFA) y segmentar la red para limitar el acceso a los sistemas críticos.</p></li>
</ol>
<p><strong>En cuanto a mitigar el impacto de materialización del riesgo</strong></p>
<ol start="7" type="1">
<li><p>Implementar copias de seguridad automáticas y periódicas de la información contable.</p></li>
<li><p>Realizar pruebas de restauración y procedimientos de respuesta ante incidentes para reducir los tiempos de recuperación.</p></li>
<li><p>Mantener registros y trazabilidad de las operaciones para identificar modificaciones o accesos no autorizados.</p></li>
</ol></th>
</tr>
<tr>
<th style="text-align: center;"><blockquote>
<p><strong>CONTROLES</strong></p>
</blockquote></th>
<th colspan="3"><p>Considerando la ISO/IEC 27002:2022, se seleccionan los siguientes controles para las estrategias de mitigación planteadas:</p>
<p><strong><mark>Para la estrategia 1:</mark></strong></p>
<p><strong>Controles organizacionales:</strong></p>
<ul>
<li><p><mark>5.2 Roles y responsabilidades de seguridad de la información.</mark></p></li>
</ul>
<p><mark><strong>Evidencia objetiva</strong>: Descripción formal del puesto, asignación de responsabilidades y documentación que acredite la incorporación del especialista.</mark></p>
<p><strong>Para la estrategia 2:<br />
</strong> <strong>Personas:</strong></p>
<ul>
<li><p>6.03 Concientización, educación y entrenamiento en seguridad de la información</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Registro de capacitaciones realizadas.</p>
<p><strong>Para la estrategia 3:<br />
Controles tecnológicos:</strong></p>
<ul>
<li><p>8.07 Protección contra malware</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Licencia y registros de actualización del antivirus/EDR.</p>
<p><strong>Para la estrategia 4:<br />
Controles tecnológicos:</strong></p>
<ul>
<li><p>8.16 Actividades de seguimiento</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Logs y registros de monitoreo.</p>
<p><strong>Para la estrategia 5:<br />
Organización:</strong></p>
<ul>
<li><p>5.01 Políticas para la seguridad de la información</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Documento de políticas aprobado y difundido.</p>
<p><strong>Para la estrategia 6:<br />
Controles tecnológicos:</strong></p>
<ul>
<li><p>8.05 Autenticación segura</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Configuración y registros de autenticación multifactor.</p>
<p><strong>Para la estrategia 7:<br />
</strong> <strong>Controles tecnológicos:</strong></p>
<ul>
<li><p>8.13 Copias de seguridad de la información</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Logs de ejecución de los respaldos.</p>
<p><strong>Para la estrategia 8:</strong></p>
<p><strong>Organización:</strong></p>
<ul>
<li><p>5.24 Planificación y preparación de la gestión de incidentes de seguridad de la información</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Procedimientos documentados y reportes de pruebas de restauración.</p>
<p><strong>Para la estrategia 9:<br />
</strong> <strong>Controles tecnológicos:</strong></p>
<ul>
<li><p>8.15 Gestión de eventos (Log)</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Logs de auditoría y registros de actividad del módulo contable</p></th>
</tr>
<tr>
<th colspan="4" style="text-align: center;"><strong>RIESGO RESIDUAL</strong></th>
</tr>
<tr>
<th colspan="4" style="text-align: left;"><p>Con las estrategias de mitigación la probabilidad baja de Probable (4) a Poco Probable (2) y el impacto de Mayor (4) a Significativo (3). Quedándonos una severidad residual de 6 (Medio)</p>
<p>Sin embargo, el riesgo no puede eliminarse completamente, debido a que los correos maliciosos evolucionan constantemente y existe la posibilidad de que un usuario interactúe con un mensaje fraudulento o no cumpla con las políticas de seguridad establecidas.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

### Planes de Contingencia, Recuperación y Continuidad de Negocio

<table>
<colgroup>
<col style="width: 21%" />
<col style="width: 14%" />
<col style="width: 63%" />
</colgroup>
<thead>
<tr>
<th>Id. 01</th>
<th colspan="2"></th>
</tr>
<tr>
<th><strong>Identificador</strong></th>
<th colspan="2"></th>
</tr>
<tr>
<th><strong>Especificación</strong></th>
<th colspan="2">Un usuario del módulo contable EugenIA recibe un correo electrónico malicioso que contiene un archivo adjunto o enlace fraudulento. Al interactuar con él, se instala un malware o se comprometen sus credenciales, permitiendo posteriormente el acceso no autorizado al módulo y la modificación o eliminación de información contable.</th>
</tr>
<tr>
<th><strong>Disparadores</strong></th>
<th colspan="2">El usuario intenta acceder al módulo contable EugenIA y detecta comportamientos anómalos, accesos no reconocidos o modificaciones y eliminación de información contable. También puede detectar actividad sospechosa mediante los mecanismos de monitoreo.</th>
</tr>
<tr>
<th><strong>Contingencia</strong></th>
<th colspan="2"><p>Ante la detección del incidente, se realizan los siguientes pasos:</p>
<ol type="1">
<li><p>Notificar al personal responsable del Área Desarrollo sobre el incidente.</p></li>
<li><p>Analizar el equipo y los registros para determinar el origen y alcance del incidente.</p></li>
<li><p>Suspender temporalmente el acceso del usuario comprometido y, si es necesario, aislar el equipo afectado.</p></li>
<li><p>Registrar y conservar las evidencias relacionadas con el incidente.</p></li>
</ol></th>
</tr>
<tr>
<th><strong>Recuperación</strong></th>
<th colspan="2"><ol type="1">
<li><p><mark>Se procede a realizar una limpieza del equipo con herramientas especializadas para remover el malware.</mark></p></li>
<li><p><mark>Verificar que el malware haya sido completamente eliminado y que el equipo se encuentre seguro.</mark></p></li>
<li><p><mark>Restaurar la información contable desde la copia de seguridad más reciente disponible.</mark></p></li>
<li><p><mark>Verificar la integridad y coherencia de la información recuperada.</mark></p></li>
<li><p><mark>Restablecer los accesos del usuario una vez verificado que el equipo y las credenciales sean seguros.</mark></p></li>
<li><p><mark>Actualizar el registro del incidente con las acciones realizadas y los resultados obtenidos.</mark></p></li>
</ol></th>
</tr>
<tr>
<th><strong>Continuidad<br />
de Negocio</strong></th>
<th colspan="2">Mientras el módulo contable EugenIA se encuentre fuera de servicio, se suspende temporalmente la carga de comprobantes y la generación de asientos contables. Una vez restablecido el sistema y verificada su seguridad e integridad, se retoma el funcionamiento normal del módulo.</th>
</tr>
<tr>
<th><strong>Controles de Garantía de los Planes</strong></th>
<th colspan="2"><p><em><strong>Controles para el plan de contingencia:</strong></em></p>
<p><strong>Paso 1:<br />
Organización:</strong></p>
<ul>
<li><p>5.24 Planificación y preparación de la gestión de incidentes de seguridad de la información</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Mail o ticket de notificación del incidente.</p>
<p><strong>Paso 2:<br />
</strong> <strong>Organización:</strong></p>
<ul>
<li><p>5.25 Evaluación y decisión sobre los eventos de seguridad de información</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Informe de diagnóstico del incidente.</p>
<p><strong>Paso 3:<br />
</strong> <strong>Controles tecnológicos:</strong></p>
<ul>
<li><p>8.15 Gestión de eventos (Log)</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Logs de acceso y registro de bloqueo o suspensión de la cuenta.</p>
<p><strong>Paso 4:<br />
</strong> <strong>Organización:</strong></p>
<ul>
<li><p>5.28 Recopilación de evidencias</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Evidencias técnicas recolectadas (logs, capturas y reportes).</p>
<p><em><strong>Controles para el plan de recuperación</strong></em></p>
<p><strong>Paso 1:<br />
Controles tecnológicos:</strong></p>
<ul>
<li><p>8.07 Protección contra malware</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Informe de limpieza y eliminación del malware.</p>
<p><strong>Paso 2:<br />
Organización:</strong></p>
<ul>
<li><p>5.25 Evaluación y decisión sobre los eventos de seguridad de información</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Resultado del análisis o escaneo posterior a la limpieza.</p>
<p><strong>Paso 3:<br />
Controles tecnológicos:</strong></p>
<ul>
<li><p>8.13 Copias de seguridad de la información</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Log de restauración de la copia de seguridad.</p>
<p><strong>Paso 4:<br />
Controles tecnológicos:</strong></p>
<ul>
<li><p>8.15 Gestión de eventos (Log)</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Registros de auditoría utilizados para verificar accesos y modificaciones realizadas sobre la información contable.</p>
<p><strong>Paso 5:<br />
Organización:</strong></p>
<ul>
<li><p>5.24 Planificación y preparación de la gestión de incidentes de seguridad de la información</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Registro de restablecimiento de accesos y documentación del procedimiento de recuperación.</p>
<p><strong>Paso 6:<br />
Organización:</strong></p>
<ul>
<li><p>5.27 Aprendizaje de los incidentes de seguridad de la información</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Documento de lecciones aprendidas y acciones de mejora</p>
<p><em><strong>Controles para el plan de Continuidad de Negocio:</strong></em></p>
<p><strong>Paso 1:<br />
Organización:</strong></p>
<ul>
<li><p>5.29 Seguridad de la información durante interrupciones</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Procedimientos documentados para continuar las operaciones contables mediante registros manuales durante la interrupción del sistema.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## Riesgo 2: Error de interpretación OCR/IA

### Identificación de riesgo

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 14%" />
<col style="width: 20%" />
<col style="width: 30%" />
</colgroup>
<thead>
<tr>
<th>Id 02</th>
<th colspan="4"></th>
</tr>
<tr>
<th><strong>Identificador</strong></th>
<th colspan="4"><strong>R02 - Error de interpretación OCR/IA</strong></th>
</tr>
<tr>
<th><strong>Especificación</strong></th>
<th colspan="4">El motor de OCR/IA interpreta incorrectamente un comprobante (monto, cuenta, IVA) y genera un asiento contable erróneo que pasa inadvertido durante la revisión del usuario.</th>
</tr>
<tr>
<th><strong>Clasificación</strong></th>
<th colspan="2">Fallas de Sistemas y Tecnología</th>
<th>Sistemas</th>
<th>Especificaciones</th>
</tr>
<tr>
<th colspan="5"><strong>Descripción ampliada del Contexto del Riesgo</strong></th>
</tr>
<tr>
<th colspan="5"><p>Se presenta durante el procesamiento automático de comprobantes mediante las funcionalidades de OCR e inteligencia artificial implementadas en EugenIA. El sistema analiza imágenes o documentos digitalizados para extraer información relevante y generar automáticamente los asientos contables correspondientes.</p>
<p>Debido a errores de reconocimiento de caracteres, baja calidad de las imágenes, formatos de comprobantes no contemplados o limitaciones propias del modelo de IA, pueden producirse interpretaciones incorrectas de datos críticos como importes, cuentas contables, porcentajes de IVA, fechas o conceptos. Si estos errores no son detectados durante la revisión realizada por el usuario, el sistema registrará información contable incorrecta en la base de datos.</p></th>
</tr>
<tr>
<th colspan="5" style="text-align: center;"><strong>VALORACIÓN DEL RIESGO</strong></th>
</tr>
<tr>
<th colspan="5"><p><strong>ACTIVOS</strong> involucrados y dimensión de <strong>valor de su criticidad</strong>:</p>
<p>En la planilla de activos se ha establecido el nivel de criticidad de los activos afectados.</p></th>
</tr>
<tr>
<th colspan="5"><p><strong>F<em>actores analizados para el cálculo de la probabilidad del riesgo inherente:</em></strong></p>
<p><strong>Frecuencia de amenaza:</strong></p>
<ul>
<li><p><strong>Contacto:</strong></p></li>
</ul>
<blockquote>
<p>Aleatorio: No.</p>
<p>Intencional: No.</p>
<p>Regular: Sí. El procesamiento automático de comprobantes mediante OCR e IA constituye una actividad habitual dentro de la operatoria normal del sistema.</p>
</blockquote>
<ul>
<li><p><strong>Acción:</strong></p>
<ul>
<li><p><strong>Beneficio:</strong> No existe un actor que obtenga un beneficio directo, ya que la amenaza surge por limitaciones técnicas, errores de reconocimiento o interpretaciones incorrectas realizadas por el motor de IA.</p></li>
<li><p><strong>Nivel de esfuerzo:</strong> Bajo. El error puede producirse automáticamente ante documentos de baja calidad, formatos no contemplados o situaciones no previstas durante el entrenamiento del modelo.</p></li>
<li><p><strong>Riesgo de detección:</strong> Medio-Alto. Si el usuario deposita excesiva confianza en la automatización o realiza una revisión superficial, el error puede permanecer sin ser detectado durante un período considerable.</p></li>
</ul></li>
</ul>
<ul>
<li><p><strong>Capacidad de la Amenaza:</strong> Alta. Un error sistemático del motor OCR/IA puede afectar múltiples comprobantes y generar numerosos registros incorrectos antes de ser identificado.</p></li>
<li><p><strong>Capacidad de Resistencia:</strong> Media. Existen controles de revisión por parte de los usuarios, pero dependen de la experiencia, capacitación y atención de quienes validan la información generada.</p></li>
</ul>
<p><strong>Utilizando la escala de valores se puede decir que la probabilidad es: Probable (4).</strong></p>
<p><em>Factores analizados para el cálculo del <strong>impacto</strong> del riesgo inherente:</em></p>
<p><strong>Activos:</strong> En la planilla de activos se ha establecido el nivel de criticidad de los activos afectados. Además se puede considerar:</p>
<ul>
<li><p><strong>Productividad:</strong> La productividad puede verse afectada debido a la necesidad de revisar comprobantes procesados, identificar errores, corregir asientos contables y realizar conciliaciones adicionales para garantizar la integridad de la información.</p></li>
</ul>
<ul>
<li><p><strong>Costo de reemplazo:</strong> Este costo estará dado por</p>
<ul>
<li><p>Tiempo necesario para identificar los comprobantes afectados.</p></li>
<li><p>Revisión manual de la documentación original.</p></li>
<li><p>Corrección de asientos contables erróneos.</p></li>
<li><p>Reprocesamiento de comprobantes.</p></li>
<li><p>Verificación de balances, reportes e impuestos afectados.</p></li>
<li><p>Horas de trabajo adicionales del personal contable y administrativo.</p></li>
</ul></li>
</ul>
<ul>
<li><p><strong>Sensibilidad:</strong></p>
<ul>
<li><p><strong>Reputación:</strong> La recurrencia de errores contables generados automáticamente podría disminuir la confianza de los usuarios en el sistema y en los procesos automatizados implementados por la organización.</p></li>
<li><p><strong>Ventaja competitiva:</strong> La pérdida de confiabilidad en la automatización reduce los beneficios esperados del proyecto y puede afectar la percepción de calidad de la solución desarrollada.</p></li>
<li><p><strong>Legal / Regulatoria:</strong> Errores en la registración contable o en la liquidación de impuestos pueden derivar en inconsistencias regulatorias, observaciones de auditoría o sanciones por incumplimientos normativos.</p></li>
</ul></li>
<li><p><strong>Volumen</strong>:</p>
<ul>
<li><p>El impacto dependerá de la cantidad de comprobantes procesados incorrectamente antes de la detección del incidente. Si el error afecta reglas generales de reconocimiento, el volumen de registros comprometidos puede ser considerable.</p></li>
</ul></li>
</ul>
<p><strong>Amenazas:</strong></p>
<ul>
<li><p><strong>Competencias:</strong> Los usuarios podrían no poseer la capacitación necesaria para detectar inconsistencias contables generadas automáticamente, especialmente cuando estas presentan valores aparentemente coherentes.</p></li>
<li><p><strong>Internas/Externas:</strong> El agente es interno, ya que el origen del riesgo proviene de componentes tecnológicos propios del sistema y de las limitaciones del modelo de inteligencia artificial.</p></li>
<li><p><strong>Acción</strong>:</p>
<ul>
<li><p><strong>Acceso</strong>: No aplica</p></li>
<li><p><strong>Divulgación</strong>: No existe exposición de información por la materialización directa del riesgo.</p></li>
<li><p><strong>Modificación</strong>: Se generan modificaciones incorrectas sobre registros contables mediante la creación automática de asientos erróneos.</p></li>
<li><p><strong>Denegación de acceso</strong>: No aplica</p></li>
</ul></li>
</ul>
<p><strong>Organización:</strong></p>
<ul>
<li><p><strong>Momento:</strong> El riesgo puede materializarse cada vez que se procese un comprobante mediante OCR e IA, especialmente cuando se reciben documentos con baja calidad, formatos no estándar o información ambigua.</p></li>
<li><p><strong>Debido al cuidado</strong>: No existen garantías absolutas de exactitud en los modelos OCR e IA. La ausencia de validaciones automáticas adicionales o revisiones exhaustivas puede favorecer la materialización del riesgo.</p></li>
<li><p><strong>Detección:</strong> Se detecta normalmente durante conciliaciones contables, controles administrativos, auditorías internas o cuando el usuario identifica diferencias entre el comprobante original y el asiento generado.</p></li>
<li><p><strong>Respuesta:</strong></p>
<ul>
<li><p><strong>Contención:</strong> Suspender temporalmente el procesamiento automático del tipo de comprobante afectado e identificar todos los registros potencialmente impactados.</p></li>
<li><p><strong>Remediación:</strong>Corregir los asientos erróneos, ajustar reglas de validación y mejorar los parámetros de entrenamiento o configuración del modelo.</p></li>
<li><p><strong>Recuperación:</strong> Reprocesar la documentación afectada y verificar nuevamente la integridad de la información contable obtenida.</p></li>
</ul></li>
</ul>
<p><strong>Factores externos:</strong></p>
<ul>
<li><p><strong>Detección</strong>: Los errores pueden ser detectados por auditorías externas, organismos de control o durante procesos de conciliación con terceros.</p></li>
<li><p><strong>Legal/Regulatorio</strong>: La presentación de información contable o impositiva incorrecta puede generar observaciones, sanciones o requerimientos de rectificación por parte de organismos regulatorios.</p></li>
<li><p><strong>Competidores</strong>: No existe un impacto directo asociado a competidores, aunque errores frecuentes pueden afectar la percepción de calidad de la solución frente a otras alternativas del mercado.</p></li>
<li><p><strong>Medios de comunicación</strong>: El impacto es bajo, aunque errores significativos que afecten información financiera podrían perjudicar la imagen institucional si alcanzan difusión pública.</p></li>
</ul>
<p><strong>Utilizando la escala de valores se puede decir que el impacto es: Significativo (3).</strong></p>
<p><strong>Para concluir, podemos considerar que la severidad es: Alto (12)</strong></p></th>
</tr>
<tr>
<th><strong>Consecuencias</strong></th>
<th colspan="4"><ul>
<li><p>Generación de asientos contables incorrectos debido a errores en la interpretación de montos, IVA, cuentas contables o conceptos.</p></li>
<li><p>Pérdida de integridad y confiabilidad de la información contable almacenada en el sistema.</p></li>
<li><p>Distorsión de balances, estados financieros y reportes gerenciales.</p></li>
<li><p>Errores en la liquidación de impuestos y en el cumplimiento de obligaciones fiscales.</p></li>
<li><p>Necesidad de realizar revisiones, conciliaciones y correcciones manuales de los registros afectados.</p></li>
<li><p>Incremento de los tiempos operativos del personal administrativo y contable.</p></li>
<li><p>Costos adicionales asociados a tareas de control, auditoría y reprocesamiento de documentación.</p></li>
<li><p>Retrasos en los cierres contables y en la generación de información financiera.</p></li>
<li><p>Disminución de la confianza de los usuarios en los resultados generados por el motor OCR/IA.</p></li>
</ul></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

### Tratamiento de riesgos

<table>
<colgroup>
<col style="width: 5%" />
<col style="width: 14%" />
<col style="width: 16%" />
<col style="width: 63%" />
</colgroup>
<thead>
<tr>
<th colspan="2">Id. 02</th>
<th colspan="2"></th>
</tr>
<tr>
<th colspan="2"><strong>Identificador</strong></th>
<th colspan="2"></th>
</tr>
<tr>
<th colspan="2"><strong>Especificación</strong></th>
<th colspan="2">El motor de OCR/IA interpreta incorrectamente un comprobante (monto, cuenta, IVA) y genera un asiento contable erróneo que pasa inadvertido en la revisión del usuario.</th>
</tr>
<tr>
<th rowspan="6" style="text-align: center;"><blockquote>
<p><strong>ESTRATEGIAS</strong></p>
</blockquote></th>
<th colspan="3" style="text-align: center;"><strong>EVITAR</strong></th>
</tr>
<tr>
<th colspan="3"><mark>No se puede evitar.</mark></th>
</tr>
<tr>
<th colspan="3" style="text-align: center;"><strong>TRANSFERIR</strong></th>
</tr>
<tr>
<th colspan="3"><mark>No se puede transferir.</mark></th>
</tr>
<tr>
<th colspan="3" style="text-align: center;"><strong>MITIGAR</strong></th>
</tr>
<tr>
<th colspan="3"><p>En cuanto a mitigar la probabilidad de materialización del riesgo:</p>
<ol type="1">
<li><p>Implementar validaciones automáticas sobre montos, IVA, fechas y cuentas contables extraídas del comprobante.</p></li>
<li><p>Definir umbrales mínimos de confianza para que los resultados sean aceptados automáticamente.</p></li>
<li><p>Exigir revisión y aprobación manual para comprobantes cuyo nivel de confianza sea inferior al valor establecido.</p></li>
<li><p>Realizar pruebas periódicas de precisión y rendimiento del motor OCR/IA.</p></li>
<li><p>Capacitar a los usuarios para detectar inconsistencias entre los comprobantes originales y la información extraída.</p></li>
<li><p>Mantener trazabilidad entre el documento procesado y el asiento contable generado</p></li>
</ol>
<p>En cuanto a mitigar el impacto de materialización del riesgo:</p>
<ol start="7" type="1">
<li><p>Implementar registros de auditoría para identificar rápidamente los comprobantes procesados incorrectamente.</p></li>
<li><p>Realizar conciliaciones contables periódicas.</p></li>
<li><p>Establecer procedimientos de corrección y reprocesamiento de comprobantes erróneos.</p></li>
<li><p>Conservar los documentos originales para permitir verificaciones posteriores.</p></li>
<li><p>Implementar controles de aprobación previa para operaciones consideradas críticas.</p></li>
</ol></th>
</tr>
<tr>
<th style="text-align: center;"><blockquote>
<p><strong>CONTROLES</strong></p>
</blockquote></th>
<th colspan="3"><p>Considerando la ISO/IEC 27002:2022, se seleccionan los siguientes controles para las estrategias de mitigación planteadas:</p>
<p><strong>Para la estrategia 1</strong></p>
<p><strong>Controles tecnológicos:</strong></p>
<ul>
<li><p>8.26 Requisitos de seguridad de las aplicaciones</p></li>
</ul>
<p><strong>Evidencia objetiva</strong>: Configuración de reglas de validación y pruebas funcionales.</p>
<p><strong>Para la estrategia 2</strong></p>
<p><strong>Controles tecnológicos:</strong></p>
<ul>
<li><p>8.16 Actividades de monitoreo</p></li>
</ul>
<p><strong>Evidencia objetiva</strong>: Reportes de niveles de confianza y métricas de precisión del OCR/IA.</p>
<p><strong>Para la estrategia 3</strong></p>
<p><strong>Controles tecnológicos:</strong></p>
<ul>
<li><p>8.15 Gestión de eventos (Log)</p></li>
</ul>
<p><strong>Evidencia objetiva</strong>: Registros de revisión y aprobación de comprobantes.</p>
<p><strong>Para la estrategia 4</strong></p>
<p><strong>Controles tecnológicos:</strong></p>
<ul>
<li><p>8.29 Pruebas de seguridad</p></li>
</ul>
<p><strong>Evidencia objetiva</strong>: Informes de pruebas de precisión y resultados de validación del modelo.</p>
<p><strong>Para la estrategia 5</strong></p>
<p><strong>Personas:</strong></p>
<ul>
<li><p>6.03 Concientización, educación y entrenamiento en seguridad de la información</p></li>
</ul>
<p><strong>Evidencia objetiva</strong>: Registro de capacitaciones y evaluaciones realizadas.</p>
<p><strong>Para la estrategia 6</strong></p>
<p><strong>Controles tecnológicos:</strong></p>
<ul>
<li><p>8.15 Gestión de eventos (Log)</p></li>
</ul>
<p><strong>Evidencia objetiva</strong>: Trazabilidad completa entre comprobantes, datos extraídos y asientos generados.</p>
<p><strong>Para la estrategia 7</strong></p>
<p><strong>Organización:</strong></p>
<ul>
<li><p>5.27 Aprendizaje de incidentes de seguridad de la información</p></li>
</ul>
<p><strong>Evidencia objetiva</strong>: Informes de errores detectados y acciones correctivas implementadas.</p>
<p><strong>Para la estrategia 8</strong></p>
<p><strong>Controles tecnológicos:</strong></p>
<ul>
<li><p>8.16 Actividades de monitoreo</p></li>
</ul>
<p><strong>Evidencia objetiva</strong>: Informes de conciliaciones contables</p>
<p><strong>Para la estrategia 9</strong></p>
<p><strong>Controles organizacionales:</strong></p>
<ul>
<li><p>5.37 Procedimientos operativos documentados</p></li>
</ul>
<p><strong>Evidencia objetiva</strong>: Procedimientos documentados para identificar, corregir y reprocesar comprobantes afectados, incluyendo la verificación de los asientos contables corregidos.</p>
<p><strong>Para la estrategia 10</strong></p>
<p><strong>Controles organizacionales:</strong></p>
<ul>
<li><p>5.33 Protección de registros</p></li>
</ul>
<p><strong>Evidencia objetiva</strong>: Documentos originales conservados.</p>
<p><strong>Para la estrategia 11</strong></p>
<p><strong>Controles organizacionales:</strong></p>
<ul>
<li><p>5.3 Segregación de funciones</p></li>
</ul>
<p><strong>Evidencia objetiva</strong>: Procedimientos de autorización previa, registros de aprobación y asignación documentada de responsabilidades para las operaciones críticas, cuando corresponda la separación de funciones.</p></th>
</tr>
<tr>
<th colspan="4" style="text-align: center;"><strong>RIESGO RESIDUAL</strong></th>
</tr>
<tr>
<th colspan="4" style="text-align: left;">Con las estrategias de mitigación propuestas se reduce la probabilidad de materialización del riesgo de Probable(4) a Poco Probable(2) y el impacto de Significativo(3) a Menor(2). Sin embargo, el riesgo no puede eliminarse completamente debido a las limitaciones inherentes de las tecnologías OCR e Inteligencia Artificial, la posible existencia de documentos con formatos no contemplados y la dependencia de la revisión realizada por los usuarios antes de confirmar los registros contables generados automáticamente.</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

### 

### Planes de Contingencia, Recuperación y Continuidad de Negocio

<table>
<colgroup>
<col style="width: 21%" />
<col style="width: 14%" />
<col style="width: 63%" />
</colgroup>
<thead>
<tr>
<th>Id. 02</th>
<th colspan="2"></th>
</tr>
<tr>
<th><strong>Identificador</strong></th>
<th colspan="2">R02</th>
</tr>
<tr>
<th><strong>Especificación</strong></th>
<th colspan="2">El motor de OCR/IA interpreta incorrectamente un comprobante (monto, cuenta, IVA) y genera un asiento contable erróneo que pasa inadvertido en la revisión del usuario.</th>
</tr>
<tr>
<th><strong>Disparadores</strong></th>
<th colspan="2"><ul>
<li><p>Se detectan diferencias entre la información contenida en el comprobante original y el asiento contable generado.</p></li>
<li><p>Se identifican inconsistencias durante conciliaciones contables.</p></li>
<li><p>Se detectan errores en liquidaciones impositivas o reportes financieros.</p></li>
<li><p>Los usuarios informan resultados incorrectos generados por el módulo OCR/IA.</p></li>
<li><p>Auditorías internas o externas detectan registros contables inconsistentes originados por el procesamiento automático.</p></li>
</ul></th>
</tr>
<tr>
<th><strong>Contingencia</strong></th>
<th colspan="2"><p>Ante la detección del incidente se realizan los siguientes pasos:</p>
<ol type="1">
<li><p>Notificar al personal responsable del Área de Desarrollo Y al responsable funcional contable.</p></li>
<li><p>Identificar los comprobantes procesados mediante la misma configuración o modelo de OCR/IA para determinar el alcance del incidente.</p></li>
<li><p>Suspender temporalmente el procesamiento automático de comprobantes afectados hasta identificar la causa raíz.</p></li>
<li><p>Registrar y conservar evidencias relacionadas con el incidente, incluyendo documentos originales, resultados OCR, registros de auditoría y asientos generados.</p></li>
</ol></th>
</tr>
<tr>
<th><strong>Recuperación</strong></th>
<th colspan="2"><ol type="1">
<li><p>Analizar la causa del error y verificar si corresponde a problemas de configuración, calidad documental o limitaciones del modelo.</p></li>
<li><p>Revisar y corregir los asientos contables afectados.</p></li>
<li><p>Reprocesar los comprobantes utilizando configuraciones corregidas o mediante validación manual.</p></li>
<li><p>Verificar la integridad y consistencia de la información recuperada.</p></li>
<li><p>Actualizar reglas de validación, parámetros de reconocimiento o modelos de IA para evitar reincidencias.</p></li>
<li><p>Documentar el incidente y las acciones correctivas implementadas.</p></li>
</ol></th>
</tr>
<tr>
<th><strong>Continuidad<br />
de Negocio</strong></th>
<th colspan="2"><p>Mientras el procesamiento automático mediante OCR/IA se encuentre limitado o suspendido, los comprobantes serán registrados mediante revisión y carga manual asistida por los usuarios responsables.</p>
<p>Una vez restablecida la precisión y confiabilidad del sistema, y verificadas las correcciones implementadas, se retomará el procesamiento automático normal de comprobantes y generación de asientos contables.</p></th>
</tr>
<tr>
<th><strong>Controles de Garantía de los Planes</strong></th>
<th colspan="2"><p><em><strong>Controles para el plan de contingencia:</strong></em></p>
<p><strong>Paso 1:</strong></p>
<p><strong>Organización:</strong></p>
<ul>
<li><p>5.24 Planificación y preparación de la gestión de incidentes de seguridad de la información.</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Registro de notificación del incidente, ticket de soporte o correo electrónico emitido.</p>
<p><strong>Paso 2:</strong></p>
<p><strong>Controles tecnológicos:</strong></p>
<ul>
<li><p>8.15 Gestión de eventos (Log).</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Registros de auditoría utilizados para identificar los comprobantes afectados.</p>
<p><strong>Paso 3:</strong></p>
<p><strong>Organización:</strong></p>
<ul>
<li><p>5.25 Evaluación y decisión sobre los eventos de seguridad de la información.</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Informe de análisis de impacto y autorización para suspensión temporal del procesamiento.</p>
<p><strong>Paso 4:</strong></p>
<p><strong>Organización:</strong></p>
<ul>
<li><p>5.28 Recopilación de evidencias.</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Evidencias técnicas, comprobantes originales, capturas y registros de procesamiento.</p>
<p><em><strong>Controles para el plan de recuperación</strong></em></p>
<p><strong>Paso 1:</strong></p>
<p><strong>Controles tecnológicos:</strong></p>
<ul>
<li><p>8.20 Seguridad de redes y aplicaciones.</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Informe técnico de análisis y corrección del problema detectado.</p>
<p><strong>Paso 2:</strong></p>
<p><strong>Controles tecnológicos:</strong></p>
<ul>
<li><p>8.15 Gestión de eventos (Log).</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Registros de las correcciones realizadas sobre los asientos afectados.</p>
<p><strong>Paso 3:</strong></p>
<p><strong>Controles tecnológicos:</strong></p>
<ul>
<li><p>8.16 Actividades de seguimiento.</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Resultados de las verificaciones posteriores al reprocesamiento.</p>
<p><strong>Paso 4:</strong></p>
<p><strong>Controles tecnológicos:</strong></p>
<ul>
<li><p>8.29 Pruebas de seguridad.</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Resultados de pruebas funcionales y de precisión realizadas al motor OCR/IA luego de las correcciones.</p>
<p><strong>Paso 5:</strong></p>
<p><strong>Organización:</strong></p>
<ul>
<li><p>5.27 Aprendizaje de los incidentes de seguridad de la información.</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Documento de lecciones aprendidas y acciones de mejora implementadas.</p>
<p><em><strong>Controles para el plan de Continuidad de Negocio:</strong></em></p>
<p><strong>Paso 1:</strong></p>
<p><strong>Organización:</strong></p>
<ul>
<li><p>5.29 Seguridad de la información durante interrupciones.</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Procedimientos documentados para la registración manual de comprobantes y generación controlada de asientos contables durante la interrupción del procesamiento automático.</p>
<p><strong>Paso 2:</strong></p>
<p><strong>Controles tecnológicos:</strong></p>
<ul>
<li><p>8.15 Gestión de eventos (Log).</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Registros de las operaciones realizadas manualmente durante el período de contingencia.</p>
<p><strong>Paso 3:</strong> <strong>Organización:</strong></p>
<ul>
<li><p>5.37 Procedimientos operativos documentados.</p></li>
</ul>
<p><strong>Evidencia objetiva:</strong> Instructivos y registros de ejecución de los procedimientos alternativos de operación.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## Riesgo 3: Vulnerabilidad de seguridad en la aplicación y exposición de información sensible

### Identificación de riesgo

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 13%" />
<col style="width: 14%" />
<col style="width: 20%" />
<col style="width: 30%" />
</colgroup>
<thead>
<tr>
<th>Id. 03</th>
<th colspan="4"></th>
</tr>
<tr>
<th><strong>Identificador</strong></th>
<th colspan="4"></th>
</tr>
<tr>
<th><strong>Especificación</strong></th>
<th colspan="4">Una vulnerabilidad de seguridad en la aplicación expone datos comerciales y contables sensibles, incluyendo información de clientes, proveedores y montos de operaciones. Un usuario no autorizado podría explotar dicha vulnerabilidad para consultar, extraer o alterar información, afectando la confidencialidad, integridad y, eventualmente, disponibilidad de los datos.</th>
</tr>
<tr>
<th><strong>Clasificación</strong></th>
<th colspan="2">Fallas de Sistemas y Tecnología</th>
<th>Software</th>
<th>Ciberseguridad</th>
</tr>
<tr>
<th colspan="5"><strong>Descripción ampliada del Contexto del Riesgo</strong></th>
</tr>
<tr>
<th colspan="5">Se detecta una falla de seguridad en el diseño, desarrollo o configuración de la aplicación del módulo contable EugenIA (como vulnerabilidades de inyección, control de acceso roto, exposición de APIs o fallas en la validación de entradas). Un atacante explota este fallo técnico para acceder de manera no autorizada a bases de datos o interfaces internas del sistema. Como consecuencia, se produce la exfiltración o consulta indebida de información comercial y contable confidencial (nóminas de clientes, proveedores, montos transaccionados y estados financieros). El incidente compromete principalmente la <strong>confidencialidad</strong> de los datos sensibles y la <strong>reputación</strong> de la organización.</th>
</tr>
<tr>
<th colspan="5" style="text-align: center;"><strong>VALORACIÓN DEL RIESGO</strong></th>
</tr>
<tr>
<th colspan="5"><p>ACTIVOS involucrados y dimensión de valor de su criticidad:</p>
<p>En la planilla de activos se ha establecido el nivel de criticidad de los activos afectados (Base de Datos Contable, Módulo Web EugenIA, Registros de Clientes/Proveedores).</p></th>
</tr>
<tr>
<th colspan="5"><p><strong>Factores analizados para el cálculo de la probabilidad del riesgo inherente:</strong></p>
<p><strong>Frecuencia de amenaza:</strong></p>
<ul>
<li><p><strong>Contacto:</strong></p></li>
</ul>
<p><em>Aleatorio:</em> Sí (escaneos automáticos de vulnerabilidades web).</p>
<p><em>Intencional:</em> Sí.</p>
<p><em>Regular:</em> No.</p>
<ul>
<li><p><strong>Acción:</strong> Materializada la amenaza de este riesgo, el proceso se ve afectado en su operatoria normal y se expone información crítica.</p>
<ul>
<li><p><strong>Beneficio:</strong> El atacante podría obtener información financiera confidencial, realizar extorsión, espionaje industrial o vender datos comerciales.</p></li>
<li><p><strong>Nivel de esfuerzo:</strong> Medio.</p></li>
<li><p><strong>Riesgo de detección:</strong> Medio-Bajo (si no existen registros de auditoría detallados en la capa de aplicación o API).</p></li>
</ul></li>
</ul>
<ul>
<li><p><strong>Capacidad de la Amenaza:</strong> Alto. Existen herramientas automatizadas capaces de explotar vulnerabilidades conocidas o de día cero para extraer bases de datos completas.</p></li>
<li><p><strong>Capacidad de Resistencia:</strong> Media-Baja. La falta de pruebas de seguridad (pentesting), auditorías de código o controles sobre la validación de entradas facilita la explotación.</p></li>
</ul>
<blockquote>
<p><strong>Utilizando la escala de valores se puede decir que la probabilidad es: Moderado(3)</strong></p>
</blockquote>
<p>Factores analizados para el cálculo del <strong>impacto</strong> del riesgo inherente:</p>
<ul>
<li><p><strong>Activos:</strong> En la planilla de activos se ha establecido el nivel de criticidad de los activos afectados. Además se puede considerar:</p>
<ul>
<li><p><strong>Productividad:</strong> La productividad puede verse afectada por la suspensión temporal del servicio para aplicar parches de emergencia y llevar a cabo auditorías forenses.</p></li>
<li><p><strong>Costo de reemplazo / remediación:</strong> Tiempo necesario para identificar, parchear y desplegar la solución; costos asociados a la auditoría forense digital; sanciones o multas por incumplimiento de normativas de protección de datos personales.</p></li>
<li><p><strong>Sensibilidad:</strong> En este riesgo se trata la divulgación de información comercial y contable confidencial de alta sensibilidad.</p></li>
<li><p><strong>Reputación:</strong> Daño severo a la imagen institucional y pérdida de confianza por parte de clientes y proveedores.</p></li>
<li><p><strong>Ventaja competitiva:</strong> La exposición de estrategias de precios, clientes y montos transaccionados otorga ventaja a competidores.</p></li>
<li><p><strong>Legal / Regulatoria:</strong> Incumplimiento de normativas e implicancias contractuales legales.</p></li>
<li><p><strong>Volumen:</strong> Puede comprometer la totalidad de los datos comerciales y contables almacenados en la aplicación.</p></li>
</ul></li>
<li><p><strong>Amenazas:</strong> Explotación de vulnerabilidades de seguridad en el código, APIs o infraestructura del módulo contable EugenIA.</p>
<ul>
<li><p><strong>Competencias:</strong> Insuficientes prácticas de desarrollo seguro (SDLC) y falta de análisis continuo de vulnerabilidades.</p></li>
<li><p><strong>Internas/Externas:</strong> Agente externo o interno no autorizado.</p></li>
</ul></li>
</ul>
<ul>
<li><p><strong>Acción:</strong></p>
<ul>
<li><p><strong>Acceso:</strong> Acceso no autorizado a repositorios de datos.</p></li>
<li><p><strong>Uso indebido:</strong> Sí aplica.</p></li>
<li><p><strong>Divulgación:</strong> Exfiltración y filtración de información sensible.</p></li>
<li><p><strong>Modificación:</strong> Posible alteración de datos dependiendo de la vulnerabilidad.</p></li>
<li><p><strong>Denegación de acceso</strong><em>:</em> Podría producirse si la vulnerabilidad afecta la disponibilidad del servicio.</p></li>
</ul></li>
</ul>
<ul>
<li><p><strong>Organización:</strong></p>
<ul>
<li><p><strong>Momento:</strong> La vulnerabilidad permanece activa mientras el código afectado esté en producción.</p></li>
<li><p><strong>Debido al cuidado:</strong> Ausencia de pruebas de penetración previas a la liberación de cambios.</p></li>
<li><p><strong>Detección:</strong> Se conoce mediante reportes de auditoría, alertas de tráfico anómalo en logs o notificaciones públicas de filtración.</p></li>
<li><p><strong>Respuesta:</strong> <em>Contención:</em> Aislar el módulo o endpoint afectado. <em>Remediación:</em> Aplicación urgente de parches de seguridad (hotfix). <em>Recuperación:</em> Restablecimiento del servicio y notificación a afectados.</p></li>
</ul></li>
<li><p><strong>Factores externos:</strong></p>
<ul>
<li><p><strong>Detección:</strong> Puede ser detectado por herramientas de monitoreo o terceros.</p></li>
<li><p><strong>Legal/Regulatorio:</strong> Riesgo elevado de acciones legales y sanciones regulatorias por filtración de datos sensibles.</p></li>
<li><p><strong>Competidores:</strong> La información filtrada puede ser aprovechada comercialmente por la competencia.</p></li>
<li><p><strong>Medios de comunicación:</strong> Impacto mediático negativo que deteriora la reputación de la empresa.</p></li>
</ul></li>
</ul>
<p><strong>Utilizando la escala de valores se puede decir que el impacto es: Severo(5)</strong></p>
<p><strong>Para concluir, podemos considerar que la severidad es: Muy Alto (15)</strong></p></th>
</tr>
<tr>
<th><strong>Consecuencias</strong></th>
<th colspan="4"><ul>
<li><p>Exfiltración y fuga de datos comerciales y contables sensibles.</p></li>
<li><p>Pérdida de confidencialidad sobre clientes, proveedores y operaciones.</p></li>
<li><p>Sanciones legales y regulatorias por violación de leyes de privacidad.</p></li>
<li><p>Severo daño reputacional y pérdida de clientes.</p></li>
<li><p>Costos financieros por peritajes forenses y desarrollo de parches de emergencia.</p></li>
<li><p>Interrupción temporal del servicio del módulo EugenIA</p></li>
</ul></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

### Tratamiento de riesgos

<table>
<colgroup>
<col style="width: 5%" />
<col style="width: 14%" />
<col style="width: 16%" />
<col style="width: 63%" />
</colgroup>
<thead>
<tr>
<th colspan="2">Id. 03</th>
<th colspan="2"></th>
</tr>
<tr>
<th colspan="2"><strong>Identificador</strong></th>
<th colspan="2"></th>
</tr>
<tr>
<th colspan="2"><strong>Especificación</strong></th>
<th colspan="2">Una vulnerabilidad de seguridad en la aplicación expone datos comerciales y contables sensibles (clientes, proveedores, montos de operaciones).</th>
</tr>
<tr>
<th rowspan="6" style="text-align: center;"><blockquote>
<p><strong>ESTRATEGIAS</strong></p>
</blockquote></th>
<th colspan="3" style="text-align: center;"><strong>EVITAR</strong></th>
</tr>
<tr>
<th colspan="3"><mark>No se puede evitar.</mark></th>
</tr>
<tr>
<th colspan="3" style="text-align: center;"><strong>TRANSFERIR</strong></th>
</tr>
<tr>
<th colspan="3"><mark>No se puede transferir.</mark></th>
</tr>
<tr>
<th colspan="3" style="text-align: center;"><strong>MITIGAR</strong></th>
</tr>
<tr>
<th colspan="3"><p><strong>En cuanto a mitigar la probabilidad de materialización del riesgo:</strong></p>
<ol type="1">
<li><p>Realizar pruebas de penetración (pentesting) periódicas y escaneos automáticos de vulnerabilidades (SAST/DAST).</p></li>
<li><p>Implementar prácticas de desarrollo seguro de software (SDLC) y revisiones de código enfocadas en el top 10 de OWASP.</p></li>
<li><p>Establecer una política de gestión de parches para mantener librerías, marcos de trabajo y componentes actualizados.</p></li>
<li><p>Implementar un Firewall de Aplicaciones Web (WAF) y controles estrictos de autenticación y autorización (RBAC).</p></li>
</ol>
<p><strong>En cuanto a mitigar el impacto de materialización del riesgo:</strong></p>
<ol start="5" type="1">
<li><p>Cifrar la información sensible tanto en tránsito (TLS/HTTPS) como en reposo (AES-256 en base de datos).</p></li>
<li><p>Implementar técnicas de enmascaramiento de datos (data masking) en entornos de prueba e interfaces de consulta.</p></li>
<li><p>Implementar un sistema centralizado de registros (logs) y monitoreo en tiempo real de accesos inusuales.</p></li>
<li><p>Elaborar y mantener actualizado un plan de respuesta a incidentes de brechas de datos e información confidencial.</p></li>
</ol></th>
</tr>
<tr>
<th style="text-align: center;"><blockquote>
<p><strong>CONTROLES</strong></p>
</blockquote></th>
<th colspan="3"><p><strong>CONTROLES (ISO/IEC 27002:2022)</strong></p>
<p>Considerando la ISO/IEC 27002:2022, se seleccionan los siguientes controles para las estrategias de mitigación planteadas:</p>
<p><strong>Para la estrategia 1:</strong></p>
<p><strong><em>Controles tecnológicos:</em></strong></p>
<ul>
<li><p>8.29 Pruebas de seguridad en el desarrollo y la aceptación.</p></li>
</ul>
<p><em><strong>Evidencia objetiva:</strong></em> Informes ejecutivos de pentesting y reportes de escaneos SAST/DAST.</p>
<p><strong>Para la estrategia 2:</strong></p>
<p><strong><em>Controles tecnológicos:</em></strong></p>
<ul>
<li><p>8.28 Codificación segura.</p></li>
</ul>
<p><em><strong>Evidencia objetiva:</strong></em> Guía documentada de desarrollo seguro y registros de revisión de código (peer review).</p>
<p><strong>Para la estrategia 3:</strong></p>
<p><strong><em>Controles tecnológicos:</em></strong></p>
<ul>
<li><p>8.8 Gestión de vulnerabilidades técnicas.</p></li>
</ul>
<p><strong><em>Evidencia objetiva:</em></strong> Registro de parches aplicados e historial de actualizaciones del software.</p>
<p><strong>Para la estrategia 4:</strong></p>
<p><em><strong>Controles tecnológicos:</strong></em></p>
<ul>
<li><p>8.20 Seguridad de las redes</p></li>
<li><p>8.02 Imperativos de control de acceso.</p></li>
</ul>
<p><strong><em>Evidencia objetiva:</em></strong> Reglas activas configuradas en el WAF y matriz de permisos RBAC.</p>
<p><strong>Para la estrategia 5:</strong></p>
<p><strong><em>Controles tecnológicos:</em></strong></p>
<ul>
<li><p>8.24 Uso de criptografía.</p></li>
</ul>
<p><em><strong>Evidencia objetiva:</strong></em> Certificado SSL/TLS válido y parámetros de cifrado habilitados en base de datos.</p>
<p><strong>Para la estrategia 6:</strong></p>
<p><em><strong>Controles tecnológicos:</strong></em></p>
<ul>
<li><p>8.11 Enmascaramiento de datos.</p></li>
</ul>
<p><strong><em>Evidencia objetiva:</em></strong> Configuración y políticas de anonimización/enmascaramiento aplicadas.</p>
<p><strong>Para la estrategia 7:</strong></p>
<p><strong><em>Controles tecnológicos:</em></strong></p>
<ul>
<li><p>8.15 Gestión de eventos (Log).</p></li>
</ul>
<p><em><strong>Evidencia objetiva:</strong></em> Logs de auditoría de la aplicación y alertas de comportamiento anómalo.</p>
<p><strong>Para la estrategia 8:</strong></p>
<p><strong><em>Organización:</em></strong></p>
<ul>
<li><p>5.24 Planificación y preparación de la gestión de incidentes de seguridad de la información.</p></li>
</ul>
<p><em><strong>Evidencia objetiva</strong>:</em> Plan de respuesta ante fugas de datos documentado y probado.</p></th>
</tr>
<tr>
<th colspan="4" style="text-align: center;"><strong>RIESGO RESIDUAL</strong></th>
</tr>
<tr>
<th colspan="4"><p>Con las estrategias de mitigación se reduce la probabilidad de materialización del riesgo de Moderado (3) a Poco Probable (2) y el impacto de Severo (5) a Significativo (3), logrando un nivel de riesgo residual de valor 6 (Medio).</p>
<p>Sin embargo, el riesgo no puede eliminarse completamente, debido a la aparición constante de vulnerabilidades de día cero (Zero-Day) y la complejidad inherente al desarrollo continuo de software.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

### Planes de Contingencia, Recuperación y Continuidad de Negocio

<table>
<colgroup>
<col style="width: 21%" />
<col style="width: 14%" />
<col style="width: 63%" />
</colgroup>
<thead>
<tr>
<th>Id. 03</th>
<th colspan="2"></th>
</tr>
<tr>
<th><strong>Identificador</strong></th>
<th colspan="2"></th>
</tr>
<tr>
<th><strong>Especificación</strong></th>
<th colspan="2">Una vulnerabilidad de seguridad en la aplicación expone datos comerciales y contables sensibles (clientes, proveedores, montos de operaciones).</th>
</tr>
<tr>
<th><strong>Disparadores</strong></th>
<th colspan="2"><mark>Detección de patrones inusuales de tráfico/exfiltración por parte del SIEM o WAF, alertas emitidas por herramientas de monitoreo, reportes de vulnerabilidades externas o identificación de datos expuestos en fuentes no autorizadas.</mark></th>
</tr>
<tr>
<th><strong>Contingencia</strong></th>
<th colspan="2"><p>Ante la detección del incidente, se realizan los siguientes pasos:</p>
<blockquote>
<p>1. Notificar inmediatamente al equipo de Ciberseguridad y Desarrollo de Sistemas.</p>
<p>2. Aislar el componente/módulo afectado o activar reglas de bloqueo inmediato en el WAF.</p>
<p>3. Revocar tokens de sesión o accesos sospechosos.</p>
<p>4. Preservar los logs del sistema web y de la base de datos como evidencia.</p>
</blockquote></th>
</tr>
<tr>
<th><strong>Recuperación</strong></th>
<th colspan="2"><ol type="1">
<li><p>Desarrollar e implementar el parche de seguridad (hotfix) que corrige la vulnerabilidad.</p></li>
<li><p>Realizar pruebas de seguridad para verificar la correcta eliminación del fallo.</p></li>
<li><p>Determinar el alcance exacto de la información sensible expuesta</p></li>
<li><p>Realizar las notificaciones legales pertinentes según la normativa vigente.</p></li>
<li><p>Restablecer el funcionamiento normal del módulo EugenIA.</p></li>
<li><p>Actualizar el informe del incidente y definir acciones correctivas.</p></li>
</ol></th>
</tr>
<tr>
<th><strong>Continuidad<br />
de Negocio</strong></th>
<th colspan="2">Mientras se aplique el parche y el módulo contable EugenIA permanezca fuera de línea o restringido, la carga de comprobantes se realiza de manera temporal mediante registros manuales o diferidos. Una vez validada la seguridad de la aplicación, se sincroniza la información y se retoma la operación normal.</th>
</tr>
<tr>
<th><strong>Controles de Garantía de los Planes</strong></th>
<th colspan="2"><p><em><strong>Controles para el plan de contingencia:</strong></em></p>
<p><strong>Paso 1:</strong></p>
<p><strong><em>Organización:</em></strong></p>
<ul>
<li><p>5.24 Planificación y preparación de la gestión de incidentes de seguridad de la información.</p></li>
</ul>
<p><strong><em>Evidencia objetiva:</em></strong> Ticket o correo de notificación de la brecha.</p>
<p><strong>Paso 2:</strong></p>
<p><em><strong>Controles tecnológicos:</strong></em></p>
<ul>
<li><p>8.20 Seguridad de las redes.</p></li>
</ul>
<p><em><strong>Evidencia objetiva:</strong></em> Logs de aislamiento del endpoint o reglas aplicadas en WAF.</p>
<p><strong>Paso 3:</strong></p>
<p><strong><em>Controles tecnológicos:</em></strong></p>
<ul>
<li><p>8.05 Autenticación segura.</p></li>
</ul>
<p><strong><em>Evidencia objetiva:</em></strong> Registros de invalidación masiva/individual de tokens y sesiones.</p>
<p><strong>Paso 4:</strong></p>
<p><strong><em>Organización:</em></strong></p>
<ul>
<li><p>5.28 Recopilación de evidencias.</p></li>
</ul>
<p><strong><em>Evidencia objetiva:</em></strong> Copia forense guardada de los logs de auditoría.</p>
<p><em><strong>Controles para el plan de recuperación</strong></em></p>
<p><strong>Paso 1:</strong></p>
<p><em><strong>Controles tecnológicos:</strong></em></p>
<ul>
<li><p>8.25 Codificación segura</p></li>
<li><p>8.8 Gestión de vulnerabilidades.</p></li>
</ul>
<p><em><strong>Evidencia objetiva:</strong></em> Registro de cambios (commit / release notes) con la solución aplicada.</p>
<p><strong>Paso 2:</strong></p>
<p><strong><em>Controles tecnológicos:</em></strong></p>
<ul>
<li><p>8.29 Pruebas de seguridad en el desarrollo y la aceptación.</p></li>
</ul>
<p><em><strong>Evidencia objetiva:</strong></em> Reporte de re-testing de vulnerabilidades sin hallazgos.</p>
<p><strong>Paso 3:</strong></p>
<p><em><strong>Organización:</strong></em></p>
<ul>
<li><p>5.25 Evaluación y decisión sobre los eventos de seguridad de información.</p></li>
</ul>
<p><em><strong>Evidencia objetiva:</strong></em> Informe técnico con el análisis forense de la información expuesta.</p>
<p><strong>Paso 4:</strong></p>
<p><strong><em>Organización:</em></strong></p>
<ul>
<li><p>5.34 Cumplimiento de requisitos legales y reglamentarios.</p></li>
</ul>
<p><strong><em>Evidencia objetiva:</em></strong> Documentación de notificación a autoridades y afectados.</p>
<p><strong>Paso 5:</strong></p>
<p><strong><em>Organización:</em></strong></p>
<ul>
<li><p>5.24 Planificación y preparación de la gestión de incidentes de seguridad de la información.</p></li>
</ul>
<p><em><strong>Evidencia objetiva:</strong></em> Acta de restablecimiento y habilitación del servicio.</p>
<p><strong>Paso 6:</strong></p>
<p><strong><em>Organización:</em></strong></p>
<ul>
<li><p>5.27 Aprendizaje de los incidentes de seguridad de la información.</p></li>
</ul>
<p><em><strong>Evidencia objetiva:</strong></em> Documento de lecciones aprendidas y plan de mejora continua.</p>
<p><em><strong>Controles para el plan de Continuidad de Negocio:</strong></em></p>
<p><strong>Paso 1:</strong></p>
<p><strong><em>Organización:</em></strong></p>
<ul>
<li><p>5.29 Seguridad de la información durante interrupciones.</p></li>
</ul>
<p><strong><em>Evidencia objetiva:</em></strong> Procedimiento documentado de registro contable en contingencia operativa durante la indisponibilidad del módulo.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# Anexo I - Gantt actualizado



# Anexo II - Tabla comparativa de las alternativas 

| **Criterio** | **Tango** | **Megacontable** | **Nexito** | **Evolutiva IA** | **Dijit.app** |
|----|----|----|----|----|----|
| **País / Origen** | Argentina | Argentina | EE.UU. / Latam | Costa Rica / Latam | España / Europa |
| **Foco principal** | ERP contable integral | Estudio contable + IA | OCR fiscal y documental | Automatización IA para PYMES | OCR + gestión de facturas |
| **Tecnología OCR** | No nativo(requiere integración) | No especificada | OCR con IA avanzado | Sí (proceso documental) | OCR + IA (GPT, Claude, Llama) |
| **Compatibilidad ARCA** | Muy alta: IVA, IIBB, factura ARCA, libros fiscales | Sí (cumplimiento fiscal AR) | Alta: CAE, CITI, retenciones IIBB, todos los tipos de comprobante | No específica para AR | No específica para AR |
| **Reducción de errores** | No cuantificado, validación normativa integrada | 90% menos errores | Validación automática contra ARCA | No cuantificado | 99% precisión extracción |
| **Inteligencia de negocio / Analytics** | Tango Live: tablas dinámicas, informes multidimensionale | Análisis predictivo con IA | No | Analítica prescriptiva, pronóstico ventas | No |
| **Multicanal de ingreso de docs** | Excel, XML, módulos propio | No detallado | Email, WhatsApp, plataforma web | No detallado | PDF / imagen (carga manual o portal) |
| **Modelo de servicio** | On-premise / nube, licencia modular | BPO + plataforma propia | SaaS / licencia | Consultoría + implementación a medida | SaaS |
| **Relevancia para nuestro proyecto** | **Alta (ERP con contexto local AR)** | **Media (contexto local AR, sin OCR detallado)** | **Alta (OCR fiscal AR, APIs contables locales)** | **Media-Baja (sin foco en AR ni normativa ARCA)** | **Media (OCR sólido, sin adaptación AR)** |

# Anexo III - Apartado Legal 

- **[<u>Ley 25.326 – Protección de Datos Personales</u>](https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/texact.htm?utm_source=chatgpt.com)  
  **Regula el tratamiento de datos personales y exige medidas de seguridad, confidencialidad y registro de bases de datos.Recuperado el 23 de mayo de 2026.

- **[<u>Decreto 1558/2001 – Reglamentación de la Ley 25.326</u>](https://servicios.infoleg.gob.ar/infolegInternet/anexos/70000-74999/70368/norma.htm)  
  **Establece cómo deben implementarse los controles y medidas de protección de datos, bajo supervisión de la AAIP. Recuperado el 23 de mayo de 2026.

- **[<u>Ley 11.683 – Procedimiento Tributario</u>](https://biblioteca.afip.gob.ar/dcp/TOR_C_011683_1998_07_13)  
  **Define las obligaciones fiscales y el marco de interacción con organismos como AFIP/ARCA. Recuperado el 23 de mayo de 2026

- **[<u>Resoluciones Generales AFIP (Facturación Electrónica)</u>](https://www.afip.gob.ar/fe/ayuda/normativa.asp)  
  **Regulan la emisión, validación (CAE) y gestión de comprobantes electrónicos. Recuperado el 23 de mayo de 2026

- **[<u>Ley 25.506 – Firma Digital</u>](https://www.afip.gob.ar/fe/ayuda/normativa.asp)  
  **Regula la validez jurídica de documentos electrónicos y firmas digitales.Recuperado el 23 de mayo de 2026

- **[<u>Ley 27.078 – Argentina Digital</u>](https://servicios.infoleg.gob.ar/infolegInternet/anexos/235000-239999/239771/texact.htm?utm_source=chatgpt.com)  
  **Marco regulatorio de servicios TIC y uso de infraestructura digital.Recuperado el 23 de mayo de 2026

- **[<u>Código Civil y Comercial de la Nación</u>](https://servicios.infoleg.gob.ar/infolegInternet/anexos/235000-239999/235975/texact.htm?utm_source=chatgpt.com)  
  **Regula contratos, responsabilidades y relaciones comerciales con clientes.Recuperado el 23 de mayo de 2026

- **[<u>Ley 24.240 – Defensa del Consumidor</u>](https://servicios.infoleg.gob.ar/infolegInternet/anexos/0-4999/638/texact.htm?utm_source=chatgpt.com)  
  **Protege derechos de usuarios en la contratación de servicios.Recuperado el 23 de mayo de 2026

- [**<u>Ley 11.723 – Propiedad Intelectual  
  </u>**](https://servicios.infoleg.gob.ar/infolegInternet/anexos/40000-44999/42755/texact.htm?utm_source=chatgpt.com)Protege los derechos sobre el software y desarrollos tecnológicos.Recuperado el 23 de mayo de 2026

- **[<u>Marco normativo BCRA</u>](https://www.bcra.gob.ar/archivos/Pdfs/SistemasFinancierosYdePagos/marco%20normativo.pdf) (DIC 2025)  
  **Regula operaciones financieras y posibles integraciones con sistemas bancarios.

# Anexo IV - Bibliografía

Federación Argentina de Consejos Profesionales de Ciencias Económicas \[FACPCE\]. (2026). *Índices FACPCE para ajuste por inflación (Res. JG 539/18, RT 6/RT 54).* Recuperado el 22 de junio de 2026, de [<u>https://www.facpce.org.ar/indices-facpce/</u>](https://www.facpce.org.ar/indices-facpce/)

Contadores en Red. (2026). *Ajuste por inflación contable e impositivo: Índices mayo 2026.* Recuperado el 22 de junio de 2026, de [<u>https://contadoresenred.com/ajuste-por-inflacion-contable-e-impositivo-indices-mayo-2026/</u>](https://contadoresenred.com/ajuste-por-inflacion-contable-e-impositivo-indices-mayo-2026/)

Consejo Profesional de Ciencias Informáticas de la Provincia de Córdoba \[CPCIPC\]. (2026). *Honorarios recomendados.* Recuperado el 22 de junio de 2026, de [<u>https://cpcipc.org.ar/honorarios-recomendados/</u>](https://cpcipc.org.ar/honorarios-recomendados/)

**Medición funcional y puntos de función**

International Function Point Users Group \[IFPUG\]. (2010). *Function Point Counting Practices Manual (CPM), Release 4.3.1.* Recuperado el 22 de junio de 2026, de [<u>https://ifpug.org/</u>](https://ifpug.org/)

International Organization for Standardization \[ISO\]. (2009). *ISO/IEC 20926:2009. Software and systems engineering—Software measurement—IFPUG functional size measurement method.* Recuperado el 22 de junio de 2026, de [<u>https://cdn.standards.iteh.ai/samples/51717/46988316f2e1414eae0caae9bca6f621/ISO-IEC-20926-2009.pdf</u>](https://cdn.standards.iteh.ai/samples/51717/46988316f2e1414eae0caae9bca6f621/ISO-IEC-20926-2009.pdf)

Abran, A. (2010). *Software Metrics and Software Metrology.* Wiley-IEEE Computer Society Press.

Facultad de Ingeniería, Universidad de la República. (s. f.). *Instructivo para la cuenta de puntos función.* Recuperado el 22 de junio de 2026, de [<u>https://www.fing.edu.uy/tecnoinf/mvd/cursos/ingsoft/material/teorico/is05-PuntosFuncionComp.pdf</u>](https://www.fing.edu.uy/tecnoinf/mvd/cursos/ingsoft/material/teorico/is05-PuntosFuncionComp.pdf)

**Normativa argentina e integración con ARCA**

Administración Federal de Ingresos Públicos \[AFIP\]. (2019). *Resolución General 4597/2019: Procedimiento. Libro de IVA Digital.* Boletín Oficial de la República Argentina. Recuperado el 22 de junio de 2026, de [<u>https://www.boletinoficial.gob.ar/detalleAviso/primera/217644/20191001</u>](https://www.boletinoficial.gob.ar/detalleAviso/primera/217644/20191001)

Agencia de Recaudación y Control Aduanero \[ARCA\]. (s. f.). *Libro IVA Digital: Diseño de registros.* Recuperado el 22 de junio de 2026, de [<u>https://arca.gob.ar/iva/documentos/libro-iva-digital-diseno-registros.pdf</u>](https://arca.gob.ar/iva/documentos/libro-iva-digital-diseno-registros.pdf)

Administración Federal de Ingresos Públicos \[AFIP\]. (s. f.). *Libro de IVA Digital.* Recuperado el 22 de junio de 2026, de [<u>https://www.afip.gob.ar/iva/libro-iva-digital/</u>](https://www.afip.gob.ar/iva/libro-iva-digital/)

Administración Federal de Ingresos Públicos \[AFIP\]. (s. f.). *Web Services de factura electrónica.* Recuperado el 22 de junio de 2026, de [<u>https://www.afip.gob.ar/ws/</u>](https://www.afip.gob.ar/ws/)

**Casos de uso y modelado**

Booch, G., Rumbaugh, J., y Jacobson, I. (2006). *El lenguaje unificado de modelado* (2.ª ed.). Addison-Wesley.

Cockburn, A. (2001). *Writing Effective Use Cases.* Addison-Wesley Professional.

Larman, C. (2005). Applying UML and Patterns: An Introduction to Object-Oriented Analysis and Design and Iterative Development (3.ª ed.). Prentice Hall.

**Riesgos y seguridad de la información**

International Organization for Standardization \[ISO\], e International Electrotechnical Commission \[IEC\]. (2022). *ISO/IEC 27002:2022. Information security, cybersecurity and privacy protection—Information security controls.*

The Open Group. (s. f.). *Open FAIR™ Risk Analysis Standard.* Recuperado el 22 de junio de 2026, de [<u>https://www.opengroup.org/open-fair</u>](https://www.opengroup.org/open-fair)

**Inteligencia artificial, OCR y calidad de datos**

Russell, S., y Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4.ª ed.). Pearson.

European Union Agency for Cybersecurity \[ENISA\]. (2023). *Threat Landscape: Artificial Intelligence and Cybersecurity.* Recuperado el 22 de junio de 2026, de [<u>https://www.enisa.europa.eu/</u>](https://www.enisa.europa.eu/)

International Organization for Standardization \[ISO\], e International Electrotechnical Commission \[IEC\]. (2023). *ISO/IEC 42001:2023. Information technology—Artificial intelligence—Management system.*
