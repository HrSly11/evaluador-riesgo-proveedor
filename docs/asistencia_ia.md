# 🤖 Declaración de Asistencia de Inteligencia Artificial

## Información General

**Proyecto:** Sistema Experto - Evaluador de Riesgo de Proveedores  
**Fecha:** Octubre 2025  
**Equipo:** [Nombres de los integrantes]

---

## Herramientas de IA Utilizadas

Durante el desarrollo de este proyecto se utilizaron las siguientes herramientas de IA:

- **Claude (Anthropic)**: Asistencia en arquitectura, generación de código y documentación
- [Agregar otras herramientas si las usaron: Cursor, GitHub Copilot, ChatGPT, etc.]

---

## Detalle de Asistencia por Componente

### 1. Arquitectura del Sistema

**Asistencia de IA:** ✅ Sí  
**Nivel:** Alto

**Descripción:**
- La IA sugirió la estructura modular del proyecto (engine/, tests/, docs/)
- Propuso la separación de concerns entre motor de inferencia y explicador
- Recomendó patrones de diseño para mantener trazabilidad

**Modificaciones realizadas por el equipo:**
- Ajustamos la estructura para adaptarla a las especificaciones del curso
- Reorganizamos los módulos para mejorar la mantenibilidad
- Agregamos validaciones adicionales específicas de nuestro dominio

---

### 2. Motor de Inferencia (`engine/inference_engine.py`)

**Asistencia de IA:** ✅ Sí  
**Nivel:** Medio-Alto

**Descripción:**
- La IA generó el esqueleto base de la clase `MotorRiesgoProveedor`
- Proporcionó ejemplos de implementación de reglas con `@Rule` de Experta
- Sugirió el sistema de puntuación acumulativa

**Modificaciones realizadas por el equipo:**
- Redefinimos los umbrales de riesgo basándonos en investigación de mercado
- Agregamos reglas compuestas específicas (ej: crisis_financiera)
- Ajustamos los pesos de impacto de cada regla según validación con expertos
- Implementamos el sistema de tracking de reglas activadas

**Justificación de conocimiento:**
Todos los integrantes del equipo entendemos:
- Cómo funciona el encadenamiento hacia adelante en Experta
- Por qué cada regla tiene su umbral específico
- Cómo se acumulan los puntos de riesgo
- El significado de cada indicador financiero y operacional

---

### 3. Módulo de Explicación (`engine/explicador.py`)

**Asistencia de IA:** ✅ Sí  
**Nivel:** Medio

**Descripción:**
- La IA generó la estructura base del módulo de explicación
- Proporcionó métodos para generar trazabilidad y análisis por dimensión
- Sugirió formato de reportes JSON y texto

**Modificaciones realizadas por el equipo:**
- Mejoramos los textos de justificación para que sean más claros para usuarios no técnicos
- Agregamos el sistema de identificación de factores críticos
- Personalizamos las recomendaciones según el nivel de riesgo
- Implementamos validaciones adicionales en la generación de reportes

---

### 4. Aplicación Streamlit (`app.py`)

**Asistencia de IA:** ✅ Sí  
**Nivel:** Alto

**Descripción:**
- La IA generó el layout base de la aplicación Streamlit
- Proporcionó código para los gráficos con Plotly
- Sugirió la estructura de tabs y formularios

**Modificaciones realizadas por el equipo:**
- Rediseñamos completamente el CSS personalizado para mejor UX
- Agregamos validaciones de entrada de datos
- Implementamos el sistema de sesión para mantener estado
- Mejoramos los tooltips explicativos en cada campo
- Agregamos funcionalidad de exportación de reportes

**Nota importante:** Entendemos completamente:
- El flujo de datos de Streamlit (session_state, reruns, etc.)
- Cómo se integran los gráficos de Plotly
- El ciclo de vida de la evaluación desde input hasta output

---

### 5. Tests Automatizados (`tests/`)

**Asistencia de IA:** ✅ Sí  
**Nivel:** Medio

**Descripción:**
- La IA generó el esqueleto de los tests básicos
- Proporcionó ejemplos de assertions con pytest
- Sugirió casos de prueba para casos borde

**Modificaciones realizadas por el equipo:**
- Agregamos 15 casos de prueba adicionales específicos de nuestro dominio
- Diseñamos escenarios de prueba basados en proveedores reales (anonimizados)
- Implementamos tests de reglas compuestas
- Validamos edge cases específicos de nuestro sistema de puntuación

**Casos de prueba desarrollados 100% por el equipo:**
- `test_regla_crisis_financiera`: Validación de regla compuesta
- `test_capacidad_igual_demanda`: Caso específico de nuestro negocio
- `test_todos_cumplimientos_legales`: Validación de regla conjunta

---

### 6. Documentación

**Asistencia de IA:** ✅ Sí  
**Nivel:** Medio

**Descripción:**
- La IA generó el template base del README
- Proporcionó estructura para documentación técnica
- Sugirió formato para este documento de asistencia IA

**Modificaciones realizadas por el equipo:**
- Redactamos completamente las secciones de justificación de negocio
- Agregamos ejemplos específicos de nuestro contexto
- Escribimos las limitaciones y consideraciones éticas desde cero
- Personalizamos toda la documentación al contexto peruano/latinoamericano

---

## Componentes Desarrollados 100% por el Equipo

Los siguientes componentes fueron desarrollados completamente por el equipo sin asistencia de IA:

1. **Definición de reglas de negocio específicas**
   - Umbrales de riesgo basados en investigación
   - Pesos de cada dimensión de evaluación
   - Criterios de aprobadores por nivel de riesgo

2. **Validación con casos reales**
   - Recopilamos datos anónimos de 10 proveedores reales
   - Validamos que el sistema clasifique correctamente casos conocidos
   - Ajustamos reglas basándonos en feedback

3. **Análisis de limitaciones éticas**
   - Identificación de sesgos potenciales
   - Definición de disclaimer y responsabilidades
   - Análisis de impacto en decisiones de negocio

4. **Integración y debugging**
   - Resolución de bugs específicos
   - Optimización de performance
   - Integración entre componentes

---

## Declaración de Comprensión

**Todos los integrantes del equipo declaramos que:**

✅ Entendemos completamente el código entregado  
✅ Podemos explicar cualquier parte del sistema en la defensa oral  
✅ Conocemos cómo funciona el motor de inferencia con Experta  
✅ Comprendemos los algoritmos de encadenamiento hacia adelante  
✅ Sabemos por qué cada regla tiene sus umbrales específicos  
✅ Podemos justificar las decisiones de diseño tomadas  

---

## Transparencia en el Uso de IA

### ¿Por qué usamos IA?

Utilizamos herramientas de IA como **aceleradores de desarrollo**, NO como sustitutos de nuestro trabajo intelectual. Específicamente:

1. **Velocidad**: Generación rápida de boilerplate code y estructura
2. **Mejores prácticas**: Sugerencias de patrones de diseño establecidos
3. **Documentación**: Templates profesionales y estructura clara
4. **Testing**: Identificación de casos borde que podríamos haber omitido

### ¿Qué NO hizo la IA?

La IA NO:
- ❌ Diseñó las reglas de negocio (las definimos nosotros basados en investigación)
- ❌ Validó el sistema (nosotros hicimos pruebas con datos reales)
- ❌ Tomó decisiones de arquitectura críticas (las evaluamos y decidimos en equipo)
- ❌ Escribió la justificación académica (la desarrollamos desde cero)

---

## Proceso de Trabajo con IA

### Flujo típico:

1. **Definición de requerimientos** (100% equipo)
   - Especificamos qué necesitábamos
   - Definimos constrains y criterios de éxito

2. **Generación con IA** (Asistido)
   - Solicitamos código base o estructura
   - Revisamos y evaluamos la propuesta

3. **Personalización** (100% equipo)
   - Modificamos para nuestro contexto específico
   - Agregamos validaciones y lógica de negocio
   - Optimizamos y refactorizamos

4. **Validación** (100% equipo)
   - Testing exhaustivo
   - Debugging y corrección de errores
   - Validación con casos reales

---

## Aprendizajes del Uso de IA

### Aspectos Positivos:
- ✅ Aceleró significativamente el desarrollo de código repetitivo
- ✅ Nos expuso a mejores prácticas que desconocíamos
- ✅ Mejoró la calidad de nuestra documentación
- ✅ Nos ayudó a identificar casos borde en testing

### Aspectos que Requirieron Supervisión:
- ⚠️ La IA a veces sugirió soluciones demasiado complejas
- ⚠️ Algunos thresholds propuestos no tenían sentido en nuestro contexto
- ⚠️ Fue necesario verificar compatibilidad de versiones de librerías
- ⚠️ Las justificaciones de negocio necesitaron ser completamente reescritas

---

## Declaración Final

Este proyecto representa nuestro **trabajo intelectual y comprensión del dominio**. La IA fue una herramienta de asistencia, no un sustituto de nuestro aprendizaje.

Estamos preparados para:
- ✅ Defender cualquier decisión de diseño
- ✅ Explicar cada línea de código en detalle
- ✅ Modificar el sistema en vivo durante la presentación
- ✅ Responder preguntas técnicas profundas sobre Experta y sistemas expertos

---

**Firmas del Equipo:**

- [Nombre 1] - [Firma/Fecha]
- [Nombre 2] - [Firma/Fecha]
- [Nombre 3] - [Firma/Fecha]

---

**Fecha de última actualización:** Octubre 2025