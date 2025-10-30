"""
Motor de inferencia para evaluación de riesgo de proveedores
Utiliza experta para encadenamiento hacia adelante
"""

from experta import KnowledgeEngine, Rule, Fact, MATCH, OR, AND, NOT
from typing import List, Dict, Any
from datetime import datetime


class DatosProveedor(Fact):
    """Representa los datos y características de un proveedor"""
    pass


class Conclusion(Fact):
    """Representa conclusiones intermedias y finales"""
    pass


class MotorEvaluacionRiesgo(KnowledgeEngine):
    """
    Motor de inferencia que evalúa el riesgo de un proveedor
    basándose en criterios financieros, operacionales, legales y reputacionales
    """
    
    def __init__(self):
        super().__init__()
        self.explicaciones = []
        self.alertas = []
        self.puntuacion_total = 100
        self.riesgo_final = "NO DETERMINADO"
        self.recomendacion = ""
        self.factores_criticos = []
        
    def registrar_explicacion(self, regla: str, razonamiento: str, impacto: int):
        """Registra la activación de una regla para trazabilidad"""
        self.explicaciones.append({
            'regla': regla,
            'razonamiento': razonamiento,
            'impacto': impacto,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
        self.puntuacion_total -= impacto
        
    def registrar_alerta(self, nivel: str, mensaje: str):
        """Registra alertas de riesgo"""
        self.alertas.append({
            'nivel': nivel,
            'mensaje': mensaje
        })
        
    # ========== REGLAS FINANCIERAS ==========
    
    @Rule(DatosProveedor(liquidez_corriente=MATCH.lc & (lambda lc: lc < 1.0)))
    def liquidez_critica(self, lc):
        """Liquidez corriente menor a 1.0 indica problemas de solvencia inmediata"""
        self.registrar_explicacion(
            "RF-001: Liquidez Crítica",
            f"Ratio de liquidez corriente de {lc:.2f} está por debajo del mínimo aceptable (1.0). "
            "El proveedor puede tener dificultades para cumplir obligaciones a corto plazo.",
            25
        )
        self.registrar_alerta("CRÍTICO", "Liquidez insuficiente - Alto riesgo de incumplimiento")
        self.declare(Conclusion(riesgo_financiero="ALTO"))
        self.factores_criticos.append("Liquidez crítica")
        
    @Rule(DatosProveedor(liquidez_corriente=MATCH.lc & (lambda lc: 1.0 <= lc < 1.5)))
    def liquidez_moderada(self, lc):
        """Liquidez corriente entre 1.0 y 1.5 es aceptable pero requiere monitoreo"""
        self.registrar_explicacion(
            "RF-002: Liquidez Moderada",
            f"Ratio de liquidez de {lc:.2f} es aceptable pero limitado. Se recomienda monitoreo.",
            10
        )
        self.declare(Conclusion(riesgo_financiero="MEDIO"))
        
    @Rule(DatosProveedor(liquidez_corriente=MATCH.lc & (lambda lc: lc >= 1.5)))
    def liquidez_saludable(self, lc):
        """Liquidez corriente mayor a 1.5 indica buena salud financiera"""
        self.registrar_explicacion(
            "RF-003: Liquidez Saludable",
            f"Ratio de liquidez de {lc:.2f} es saludable. Buen indicador de solvencia.",
            0
        )
        self.declare(Conclusion(riesgo_financiero="BAJO"))
        
    @Rule(DatosProveedor(endeudamiento=MATCH.end & (lambda end: end > 0.7)))
    def endeudamiento_alto(self, end):
        """Endeudamiento superior al 70% es crítico"""
        self.registrar_explicacion(
            "RF-004: Endeudamiento Excesivo",
            f"Nivel de endeudamiento de {end*100:.1f}% excede el límite prudente (70%). "
            "Alta dependencia de financiamiento externo.",
            20
        )
        self.registrar_alerta("ALTO", "Endeudamiento excesivo - Riesgo de insolvencia")
        self.factores_criticos.append("Endeudamiento excesivo")
        
    @Rule(DatosProveedor(rentabilidad=MATCH.rent & (lambda rent: rent < 0)))
    def rentabilidad_negativa(self, rent):
        """Rentabilidad negativa indica pérdidas operativas"""
        self.registrar_explicacion(
            "RF-005: Pérdidas Operativas",
            f"Rentabilidad negativa de {rent*100:.1f}% indica que el proveedor está operando con pérdidas. "
            "Riesgo de discontinuidad del negocio.",
            30
        )
        self.registrar_alerta("CRÍTICO", "Proveedor operando con pérdidas")
        self.factores_criticos.append("Pérdidas operativas")
        
    @Rule(DatosProveedor(historial_pagos=MATCH.hp & (lambda hp: hp < 60)))
    def morosidad_alta(self, hp):
        """Tasa de pago puntual menor a 60% es inaceptable"""
        self.registrar_explicacion(
            "RF-006: Historial de Pagos Deficiente",
            f"Solo {hp:.0f}% de pagos puntuales a sus proveedores. Indica problemas de flujo de caja.",
            25
        )
        self.registrar_alerta("ALTO", "Historial de morosidad significativo")
        self.factores_criticos.append("Morosidad recurrente")
    
    # ========== REGLAS OPERACIONALES ==========
    
    @Rule(DatosProveedor(certificacion_calidad=False))
    def sin_certificacion_calidad(self):
        """Falta de certificación de calidad aumenta riesgo operacional"""
        self.registrar_explicacion(
            "RO-001: Sin Certificación de Calidad",
            "El proveedor no cuenta con certificaciones de calidad (ISO 9001 u otras). "
            "Mayor riesgo de incumplimiento de estándares.",
            15
        )
        self.declare(Conclusion(riesgo_operacional="MEDIO"))
        
    @Rule(DatosProveedor(tiempo_mercado=MATCH.tm & (lambda tm: tm < 2)))
    def proveedor_nuevo(self, tm):
        """Proveedores con menos de 2 años son de mayor riesgo"""
        self.registrar_explicacion(
            "RO-002: Proveedor Nuevo en el Mercado",
            f"Solo {tm:.1f} años de operación. Falta de historial aumenta incertidumbre.",
            15
        )
        self.registrar_alerta("MEDIO", "Proveedor con experiencia limitada")
        
    @Rule(DatosProveedor(capacidad_produccion=MATCH.cp & (lambda cp: cp < 50)))
    def capacidad_limitada(self, cp):
        """Capacidad de producción menor a 50% indica problemas de escalabilidad"""
        self.registrar_explicacion(
            "RO-003: Capacidad de Producción Limitada",
            f"Capacidad de producción al {cp:.0f}%. Riesgo de no poder atender demanda.",
            20
        )
        self.registrar_alerta("ALTO", "Capacidad insuficiente para escalar")
        self.factores_criticos.append("Capacidad limitada")
        
    @Rule(DatosProveedor(tasa_defectos=MATCH.td & (lambda td: td > 5)))
    def alta_tasa_defectos(self, td):
        """Tasa de defectos superior a 5% es inaceptable"""
        self.registrar_explicacion(
            "RO-004: Alta Tasa de Defectos",
            f"Tasa de defectos de {td:.1f}% excede el estándar aceptable (5%). "
            "Impacto en calidad del producto final.",
            25
        )
        self.registrar_alerta("CRÍTICO", "Control de calidad deficiente")
        self.factores_criticos.append("Problemas de calidad")
        
    @Rule(DatosProveedor(cumplimiento_entregas=MATCH.ce & (lambda ce: ce < 70)))
    def incumplimiento_entregas(self, ce):
        """Cumplimiento de entregas menor a 70% es crítico"""
        self.registrar_explicacion(
            "RO-005: Incumplimiento Sistemático de Entregas",
            f"Solo {ce:.0f}% de entregas a tiempo. Afecta la cadena de suministro.",
            25
        )
        self.registrar_alerta("CRÍTICO", "Retrasos frecuentes en entregas")
        self.factores_criticos.append("Incumplimiento de plazos")
    
    # ========== REGLAS LEGALES ==========
    
    @Rule(DatosProveedor(cumplimiento_legal=False))
    def incumplimiento_legal(self):
        """Incumplimiento de normativas legales es factor crítico"""
        self.registrar_explicacion(
            "RL-001: Incumplimiento Legal",
            "El proveedor tiene antecedentes de incumplimiento legal o normativo. "
            "Riesgo reputacional y legal para la organización.",
            30
        )
        self.registrar_alerta("CRÍTICO", "Antecedentes legales problemáticos")
        self.declare(Conclusion(riesgo_legal="ALTO"))
        self.factores_criticos.append("Problemas legales")
        
    @Rule(DatosProveedor(certificacion_ambiental=False),
          DatosProveedor(industria="manufactura"))
    def sin_certificacion_ambiental(self):
        """Manufactura sin certificación ambiental es riesgoso"""
        self.registrar_explicacion(
            "RL-002: Sin Certificación Ambiental",
            "Proveedor de manufactura sin certificaciones ambientales (ISO 14001). "
            "Riesgo de incumplimiento normativo futuro.",
            15
        )
        self.registrar_alerta("MEDIO", "Falta certificación ambiental")
        
    @Rule(DatosProveedor(seguros_vigentes=False))
    def sin_seguros(self):
        """Falta de seguros aumenta riesgo de responsabilidad"""
        self.registrar_explicacion(
            "RL-003: Seguros No Vigentes",
            "El proveedor no cuenta con seguros de responsabilidad civil vigentes. "
            "Exposición a riesgos no cubiertos.",
            20
        )
        self.registrar_alerta("ALTO", "Sin cobertura de seguros adecuada")
        self.factores_criticos.append("Sin seguros")
    
    # ========== REGLAS REPUTACIONALES ==========
    
    @Rule(DatosProveedor(calificacion_mercado=MATCH.cm & (lambda cm: cm < 3.0)))
    def mala_reputacion(self, cm):
        """Calificación de mercado menor a 3.0 de 5.0 es preocupante"""
        self.registrar_explicacion(
            "RR-001: Reputación Deficiente",
            f"Calificación de mercado de {cm:.1f}/5.0 indica problemas reputacionales. "
            "Posibles conflictos con otros clientes.",
            20
        )
        self.registrar_alerta("ALTO", "Reputación de mercado deficiente")
        self.declare(Conclusion(riesgo_reputacional="ALTO"))
        
    @Rule(DatosProveedor(quejas_clientes=MATCH.qc & (lambda qc: qc > 10)))
    def muchas_quejas(self, qc):
        """Más de 10 quejas recientes es señal de alerta"""
        self.registrar_explicacion(
            "RR-002: Alto Número de Quejas",
            f"{qc:.0f} quejas de clientes en el último año. "
            "Indica problemas recurrentes de servicio o calidad.",
            15
        )
        self.registrar_alerta("MEDIO", "Múltiples quejas de clientes")
        
    @Rule(DatosProveedor(referencias_positivas=MATCH.rp & (lambda rp: rp < 2)))
    def pocas_referencias(self, rp):
        """Menos de 2 referencias positivas es insuficiente"""
        self.registrar_explicacion(
            "RR-003: Referencias Insuficientes",
            f"Solo {rp:.0f} referencias positivas verificables. "
            "Dificulta validar historial del proveedor.",
            10
        )
    
    # ========== REGLAS DE DECISIÓN FINAL ==========
    
    @Rule(OR(
        Conclusion(riesgo_financiero="ALTO"),
        Conclusion(riesgo_legal="ALTO")
    ))
    def decision_riesgo_alto(self):
        """Si hay riesgo financiero o legal alto, el riesgo es ALTO"""
        self.riesgo_final = "ALTO"
        self.recomendacion = "NO APROBAR al proveedor para contratación"
        
    @Rule(
        AND(
            NOT(Conclusion(riesgo_financiero="ALTO")),
            NOT(Conclusion(riesgo_legal="ALTO"))
        ),
        Conclusion(riesgo_operacional="MEDIO")
    )
    def decision_riesgo_medio(self):
        """Riesgo medio si no hay críticos pero sí operacionales"""
        if self.riesgo_final == "NO DETERMINADO":
            self.riesgo_final = "MEDIO"
            self.recomendacion = "APROBAR CON CONDICIONES: Requiere plan de mitigación y monitoreo trimestral"
    
    def evaluar_puntuacion_final(self):
        """Evalúa la puntuación final después de todas las reglas"""
        if self.riesgo_final == "NO DETERMINADO":
            if self.puntuacion_total >= 80:
                self.riesgo_final = "BAJO"
                self.recomendacion = "APROBAR al proveedor para contratación"
            elif self.puntuacion_total >= 60:
                self.riesgo_final = "MEDIO"
                self.recomendacion = "APROBAR CON CONDICIONES: Requiere plan de mitigación"
            else:
                self.riesgo_final = "ALTO"
                self.recomendacion = "NO APROBAR al proveedor"
                
    def obtener_resultado(self) -> Dict[str, Any]:
        """Retorna el resultado completo de la evaluación"""
        self.evaluar_puntuacion_final()
        
        return {
            'riesgo_final': self.riesgo_final,
            'puntuacion': max(0, self.puntuacion_total),
            'recomendacion': self.recomendacion,
            'explicaciones': self.explicaciones,
            'alertas': self.alertas,
            'factores_criticos': self.factores_criticos,
            'total_reglas_activadas': len(self.explicaciones)
        }


def evaluar_proveedor(datos_proveedor: Dict[str, Any]) -> Dict[str, Any]:
    """
    Función de envoltura (wrapper) que recibe un diccionario de datos,
    ejecuta el motor de inferencia y retorna un diccionario de resultados.
    """
    try:
        # 1. Instanciar el motor
        motor = MotorEvaluacionRiesgo()

        # 2. Resetear (limpiar hechos anteriores)
        motor.reset()

        # 3. --- CORRECCIÓN CRÍTICA ---
        # Declarar TODOS los datos como un ÚNICO hecho con múltiples atributos
        motor.declare(DatosProveedor(**datos_proveedor))

        # 4. Correr el motor (encadenamiento hacia adelante)
        motor.run()

        # 5. Obtener el diccionario de resultados
        resultado = motor.obtener_resultado()

        return resultado

    except Exception as e:
        # Manejo de errores
        return {
            'riesgo_final': 'ERROR',
            'puntuacion': 0,
            'recomendacion': 'Error en el motor de inferencia',
            'explicaciones': [],
            'alertas': [{'nivel': 'CRÍTICO', 'mensaje': f"Error interno del motor: {str(e)}"}],
            'factores_criticos': ['Error de ejecución'],
            'total_reglas_activadas': 0
        }