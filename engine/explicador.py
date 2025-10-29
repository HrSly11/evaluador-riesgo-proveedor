"""
Módulo de explicación para trazabilidad de decisiones
Proporciona explicaciones legibles sobre cómo el sistema llegó a sus conclusiones
"""

from typing import List, Dict, Any
import pandas as pd


class ExplicadorDecisiones:
    """
    Genera explicaciones claras y estructuradas sobre las decisiones
    del sistema experto
    """
    
    @staticmethod
    def generar_resumen_ejecutivo(resultado: Dict[str, Any]) -> str:
        """
        Genera un resumen ejecutivo de la evaluación
        
        Args:
            resultado: Diccionario con los resultados de la evaluación
            
        Returns:
            str: Resumen ejecutivo en texto
        """
        riesgo = resultado['riesgo_final']
        puntuacion = resultado['puntuacion']
        
        emoji_riesgo = {
            'BAJO': '✅',
            'MEDIO': '⚠️',
            'ALTO': '🚫'
        }
        
        resumen = f"""
### {emoji_riesgo.get(riesgo, '❓')} Nivel de Riesgo: **{riesgo}**
**Puntuación Final:** {puntuacion:.0f}/100

**Recomendación:** {resultado['recomendacion']}

**Reglas Evaluadas:** {resultado['total_reglas_activadas']} reglas activadas
**Factores Críticos Identificados:** {len(resultado['factores_criticos'])}
"""
        return resumen
    
    @staticmethod
    def generar_explicacion_detallada(explicaciones: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Convierte las explicaciones en un DataFrame para visualización
        
        Args:
            explicaciones: Lista de explicaciones de reglas activadas
            
        Returns:
            pd.DataFrame: DataFrame con las explicaciones
        """
        if not explicaciones:
            return pd.DataFrame(columns=['Regla', 'Razonamiento', 'Impacto', 'Hora'])
        
        df = pd.DataFrame(explicaciones)
        df = df.rename(columns={
            'regla': 'Regla',
            'razonamiento': 'Razonamiento',
            'impacto': 'Impacto en Puntuación',
            'timestamp': 'Hora de Evaluación'
        })
        
        # Ordenar por impacto descendente
        df = df.sort_values('Impacto en Puntuación', ascending=False)
        
        return df
    
    @staticmethod
    def generar_cadena_razonamiento(explicaciones: List[Dict[str, Any]]) -> str:
        """
        Genera una narrativa de la cadena de razonamiento
        
        Args:
            explicaciones: Lista de explicaciones
            
        Returns:
            str: Narrativa de razonamiento
        """
        if not explicaciones:
            return "No se activaron reglas críticas. El proveedor cumple con los estándares básicos."
        
        narrativa = "### 🔍 Cadena de Razonamiento\n\n"
        narrativa += "El sistema evaluó al proveedor siguiendo esta secuencia:\n\n"
        
        for i, exp in enumerate(explicaciones, 1):
            narrativa += f"**{i}. {exp['regla']}** _(Impacto: -{exp['impacto']} puntos)_\n"
            narrativa += f"   {exp['razonamiento']}\n\n"
        
        return narrativa
    
    @staticmethod
    def generar_plan_mitigacion(resultado: Dict[str, Any]) -> str:
        """
        Genera recomendaciones para mitigar riesgos identificados
        
        Args:
            resultado: Resultado completo de la evaluación
            
        Returns:
            str: Plan de mitigación sugerido
        """
        if resultado['riesgo_final'] == 'BAJO':
            return """
### ✅ Plan de Acción
El proveedor presenta un perfil de riesgo bajo. Recomendaciones:
- Realizar auditorías anuales de seguimiento
- Mantener comunicación regular sobre cambios en su operación
- Renovar certificaciones antes del vencimiento
"""
        
        factores = resultado['factores_criticos']
        
        if not factores:
            return """
### ⚠️ Plan de Mitigación
Aunque no hay factores críticos, se recomienda:
- Establecer KPIs de desempeño
- Revisión semestral del proveedor
- Cláusulas de mejora continua en el contrato
"""
        
        plan = "### 🔧 Plan de Mitigación Requerido\n\n"
        plan += "Basado en los factores críticos identificados, se requieren las siguientes acciones:\n\n"
        
        mitigaciones = {
            'Liquidez crítica': '- Solicitar garantías financieras o pagos anticipados\n- Establecer límites de crédito más bajos\n- Revisión financiera trimestral',
            'Endeudamiento excesivo': '- Requerir carta de solvencia bancaria actualizada\n- Considerar proveedores alternativos\n- Cláusula de rescisión por insolvencia',
            'Pérdidas operativas': '- Evaluación urgente de viabilidad del negocio\n- Plan de contingencia con proveedor alternativo\n- Pagos contra entrega únicamente',
            'Morosidad recurrente': '- Pagos anticipados obligatorios\n- Garantías bancarias\n- Cláusulas penales por retrasos',
            'Capacidad limitada': '- Auditoría de capacidad instalada\n- Acuerdos de nivel de servicio (SLA) estrictos\n- Desarrollo de proveedores de respaldo',
            'Problemas de calidad': '- Implementar inspecciones de calidad en sitio\n- Certificación de calidad obligatoria\n- Penalizaciones por defectos',
            'Incumplimiento de plazos': '- Buffer de tiempo en planificación\n- Penalizaciones por retrasos\n- Proveedor secundario activo',
            'Problemas legales': '- Auditoría legal completa\n- Seguro de responsabilidad exigido\n- Cláusulas de indemnización',
            'Sin seguros': '- Exigir pólizas de seguro antes de contratación\n- Verificación anual de vigencia\n- Cláusulas de responsabilidad'
        }
        
        for factor in factores:
            if factor in mitigaciones:
                plan += f"\n**{factor}:**\n{mitigaciones[factor]}\n"
        
        plan += "\n\n**Monitoreo Requerido:** Revisión mensual durante los primeros 6 meses."
        
        return plan
    
    @staticmethod
    def generar_metricas_visuales(resultado: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepara datos para visualización gráfica
        
        Args:
            resultado: Resultado de la evaluación
            
        Returns:
            Dict con datos para gráficos
        """
        # Distribución de impacto por categoría
        categorias = {'Financiero': 0, 'Operacional': 0, 'Legal': 0, 'Reputacional': 0}
        
        for exp in resultado['explicaciones']:
            regla = exp['regla']
            impacto = exp['impacto']
            
            if regla.startswith('RF'):
                categorias['Financiero'] += impacto
            elif regla.startswith('RO'):
                categorias['Operacional'] += impacto
            elif regla.startswith('RL'):
                categorias['Legal'] += impacto
            elif regla.startswith('RR'):
                categorias['Reputacional'] += impacto
        
        return {
            'categorias': categorias,
            'puntuacion_final': resultado['puntuacion'],
            'alertas_por_nivel': {
                'CRÍTICO': len([a for a in resultado['alertas'] if a['nivel'] == 'CRÍTICO']),
                'ALTO': len([a for a in resultado['alertas'] if a['nivel'] == 'ALTO']),
                'MEDIO': len([a for a in resultado['alertas'] if a['nivel'] == 'MEDIO'])
            }
        }
    
    @staticmethod
    def generar_informe_completo(resultado: Dict[str, Any], datos_proveedor: Dict[str, Any]) -> str:
        """
        Genera un informe completo de la evaluación
        
        Args:
            resultado: Resultado de la evaluación
            datos_proveedor: Datos originales del proveedor
            
        Returns:
            str: Informe completo en markdown
        """
        informe = "# 📋 INFORME DE EVALUACIÓN DE RIESGO DE PROVEEDOR\n\n"
        informe += f"**Proveedor:** {datos_proveedor.get('nombre', 'No especificado')}\n"
        informe += f"**Fecha de Evaluación:** {datos_proveedor.get('fecha_evaluacion', 'N/A')}\n"
        informe += f"**Evaluador:** Sistema Experto de Riesgo v1.0\n\n"
        informe += "---\n\n"
        
        explicador = ExplicadorDecisiones()
        informe += explicador.generar_resumen_ejecutivo(resultado)
        informe += "\n\n---\n\n"
        informe += explicador.generar_cadena_razonamiento(resultado['explicaciones'])
        informe += "\n\n---\n\n"
        informe += explicador.generar_plan_mitigacion(resultado)
        
        return informe