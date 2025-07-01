"""
Engine de Orçamento - Orca Interiores SaaS
Sistema completo de cálculo de custos para marcenaria
Versão corrigida com compatibilidade Plotly
"""

import json
from typing import Dict, List, Any
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class OrcamentoEngine:
    def __init__(self):
        # Preços atualizados da Léo Madeiras (30/06/2025)
        self.precos_materiais = {
            'mdf_15mm': 69.15,      # R$/m²
            'mdf_18mm': 79.50,      # R$/m²
            'compensado_15mm': 64.00, # R$/m²
            'compensado_18mm': 72.80, # R$/m²
            'melamina_15mm': 89.50,   # R$/m²
            'melamina_18mm': 98.20    # R$/m²
        }
        
        # Custos de acessórios por tipo de móvel
        self.custos_acessorios = {
            'armario': {
                'comum': {'dobradica': 12.50, 'puxador': 8.90, 'corredicao': 25.00},
                'premium': {'dobradica': 18.75, 'puxador': 15.50, 'corredicao': 45.00}
            },
            'gaveta': {
                'comum': {'corredicao_gaveta': 35.00, 'puxador': 8.90},
                'premium': {'corredicao_gaveta': 65.00, 'puxador': 15.50}
            },
            'porta': {
                'comum': {'dobradica': 12.50, 'puxador': 8.90},
                'premium': {'dobradica': 18.75, 'puxador': 15.50}
            },
            'prateleira': {
                'comum': {'suporte': 4.50},
                'premium': {'suporte': 8.00}
            },
            'painel': {
                'comum': {'fixacao': 3.00},
                'premium': {'fixacao': 5.50}
            },
            'fundo': {
                'comum': {'fixacao': 2.50},
                'premium': {'fixacao': 4.00}
            },
            'tampo': {
                'comum': {'suporte': 6.00, 'acabamento': 8.00},
                'premium': {'suporte': 12.00, 'acabamento': 15.00}
            }
        }
        
        # Custos de mão de obra
        self.custos_mao_obra = {
            'corte_reto': 2.50,      # R$/metro linear
            'furo_dobradica': 1.50,   # R$/furo
            'taxa_minima': 15.00      # R$/peça
        }
        
        # Fatores de desperdício por material
        self.desperdicio = {
            'mdf_15mm': 0.15,        # 15%
            'mdf_18mm': 0.15,        # 15%
            'compensado_15mm': 0.12,  # 12%
            'compensado_18mm': 0.12,  # 12%
            'melamina_15mm': 0.18,    # 18%
            'melamina_18mm': 0.18     # 18%
        }

    def detectar_tipo_componente(self, nome_componente: str) -> str:
        """Detecta o tipo de componente baseado no nome"""
        nome_lower = nome_componente.lower()
        
        if any(palavra in nome_lower for palavra in ['armario', 'cabinet', 'wardrobe']):
            return 'armario'
        elif any(palavra in nome_lower for palavra in ['gaveta', 'drawer']):
            return 'gaveta'
        elif any(palavra in nome_lower for palavra in ['porta', 'door']):
            return 'porta'
        elif any(palavra in nome_lower for palavra in ['prateleira', 'shelf']):
            return 'prateleira'
        elif any(palavra in nome_lower for palavra in ['painel', 'panel', 'lateral']):
            return 'painel'
        elif any(palavra in nome_lower for palavra in ['fundo', 'back', 'traseira']):
            return 'fundo'
        elif any(palavra in nome_lower for palavra in ['tampo', 'top', 'superior']):
            return 'tampo'
        else:
            return 'armario'  # Default

    def calcular_area_componente(self, componente: Dict) -> float:
        """Calcula área do componente baseado nos dados 3D"""
        # Usar área já calculada pelo file_analyzer se disponível
        if 'area_m2' in componente:
            return max(componente['area_m2'], 0.1)
        
        # Calcular baseado em dimensões se disponível
        if 'dimensoes_mm' in componente:
            dims = componente['dimensoes_mm']
            if len(dims) >= 3:
                largura, altura, profundidade = dims[0], dims[1], dims[2]
                # Área aproximada (soma das faces principais)
                area = 2 * (largura * altura + largura * profundidade + altura * profundidade)
                return max(area / 1000000, 0.1)  # Converter para m²
        
        # Fallback para área padrão
        return 1.0

    def calcular_custo_componente(self, componente: Dict, material: str, 
                                 qualidade_acessorios: str, complexidade: str) -> Dict:
        """Calcula custo detalhado de um componente"""
        
        # Área do componente
        area_m2 = self.calcular_area_componente(componente)
        
        # Tipo do componente
        tipo = componente.get('tipo', self.detectar_tipo_componente(componente.get('nome', '')))
        
        # Custo do material
        preco_material = self.precos_materiais.get(material, 69.15)
        fator_desperdicio = 1 + self.desperdicio.get(material, 0.15)
        custo_material = area_m2 * preco_material * fator_desperdicio
        
        # Custo dos acessórios
        acessorios = self.custos_acessorios.get(tipo, {}).get(qualidade_acessorios, {})
        custo_acessorios = sum(acessorios.values())
        
        # Multiplicador de complexidade
        multiplicadores = {
            'simples': 1.0,
            'media': 1.2,
            'complexa': 1.5,
            'premium': 2.0
        }
        multiplicador = multiplicadores.get(complexidade, 1.0)
        
        # Custo de mão de obra (estimativa baseada no perímetro)
        perimetro_estimado = 2 * (area_m2 ** 0.5) * 4  # Estimativa grosseira
        custo_corte = max(perimetro_estimado * self.custos_mao_obra['corte_reto'], 
                         self.custos_mao_obra['taxa_minima'])
        
        # Custo total do componente
        custo_base = custo_material + custo_acessorios + custo_corte
        custo_total = custo_base * multiplicador
        
        return {
            'nome': componente.get('nome', f'Componente_{tipo}'),
            'tipo': tipo,
            'area_m2': round(area_m2, 2),
            'custo_material': round(custo_material, 2),
            'custo_acessorios': round(custo_acessorios, 2),
            'custo_corte': round(custo_corte, 2),
            'multiplicador_complexidade': multiplicador,
            'custo_total': round(custo_total, 2),
            'preco_por_m2': round(custo_total / area_m2, 2),
            'vertices': componente.get('vertices', []),
            'faces': componente.get('faces', []),
            'dimensoes_mm': componente.get('dimensoes_mm', [1000, 1000, 20])
        }

    def calcular_orcamento_completo(self, analise_3d: Dict, configuracoes: Dict) -> Dict:
        """Calcula orçamento completo do projeto"""
        
        if not analise_3d or not analise_3d.get('componentes'):
            return {}
            
        componentes = analise_3d['componentes']
        material = configuracoes.get('material', 'mdf_15mm')
        qualidade_acessorios = configuracoes.get('qualidade_acessorios', 'comum')
        complexidade = configuracoes.get('complexidade', 'media')
        margem_lucro = configuracoes.get('margem_lucro', 30) / 100
        
        # Calcular custo de cada componente
        componentes_detalhados = []
        for comp in componentes:
            custo_comp = self.calcular_custo_componente(
                comp, material, qualidade_acessorios, complexidade
            )
            componentes_detalhados.append(custo_comp)
        
        # Totais
        area_total = sum(comp['area_m2'] for comp in componentes_detalhados)
        custo_material_total = sum(comp['custo_material'] for comp in componentes_detalhados)
        custo_acessorios_total = sum(comp['custo_acessorios'] for comp in componentes_detalhados)
        custo_corte_total = sum(comp['custo_corte'] for comp in componentes_detalhados)
        custo_subtotal = custo_material_total + custo_acessorios_total + custo_corte_total
        
        # Margem de lucro
        valor_lucro = custo_subtotal * margem_lucro
        valor_final = custo_subtotal + valor_lucro
        
        return {
            'componentes': componentes_detalhados,
            'resumo': {
                'quantidade_componentes': len(componentes_detalhados),
                'area_total_m2': round(area_total, 2),
                'custo_material': round(custo_material_total, 2),
                'custo_acessorios': round(custo_acessorios_total, 2),
                'custo_corte': round(custo_corte_total, 2),
                'subtotal': round(custo_subtotal, 2),
                'margem_lucro_pct': round(margem_lucro * 100, 1),
                'valor_lucro': round(valor_lucro, 2),
                'valor_final': round(valor_final, 2),
                'preco_por_m2': round(valor_final / area_total, 2) if area_total > 0 else 0
            },
            'configuracoes': configuracoes,
            'data_calculo': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'fonte_precos': 'Léo Madeiras - Atualizado em 30/06/2025'
        }

    def gerar_graficos(self, orcamento: Dict) -> Dict:
        """Gera gráficos interativos do orçamento - VERSÃO CORRIGIDA"""
        if not orcamento or not orcamento.get('componentes'):
            return {'pizza': None, 'barras': None, 'area': None}
        
        componentes = orcamento['componentes']
        nomes = [comp['nome'] for comp in componentes]
        custos = [comp['custo_total'] for comp in componentes]
        
        # Gráfico de pizza - Distribuição de custos
        if componentes:
            fig_pizza = px.pie(
                values=custos,
                names=nomes,
                title="Distribuição de Custos por Componente",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pizza.update_traces(textposition='inside', textinfo='percent+label')
        else:
            fig_pizza = None
        
        # Gráfico de barras - Custo por componente (CORRIGIDO)
        if componentes:
            fig_barras = px.bar(
                x=nomes,
                y=custos,
                title="Custo por Componente",
                labels={'x': 'Componentes', 'y': 'Custo (R$)'},
                color=custos,
                color_continuous_scale='viridis'
            )
            # CORREÇÃO: Usar update_layout ao invés de update_xaxis
            fig_barras.update_layout(
                xaxis={'tickangle': 45},
                xaxis_title="Componentes",
                yaxis_title="Custo (R$)",
                showlegend=False
            )
        else:
            fig_barras = None
        
        # Gráfico de dispersão - Custo por m²
        if componentes:
            areas = [comp['area_m2'] for comp in componentes]
            precos_m2 = [comp['preco_por_m2'] for comp in componentes]
            
            fig_area = px.scatter(
                x=areas,
                y=precos_m2,
                size=[comp['custo_total'] for comp in componentes],
                hover_name=nomes,
                title="Custo por m² vs Área",
                labels={'x': 'Área (m²)', 'y': 'Preço por m² (R$)'},
                color=custos,
                color_continuous_scale='plasma'
            )
            fig_area.update_layout(
                xaxis_title="Área (m²)",
                yaxis_title="Preço por m² (R$)",
                showlegend=False
            )
        else:
            fig_area = None
        
        return {
            'pizza': fig_pizza,
            'barras': fig_barras,
            'area': fig_area
        }

    def gerar_relatorio_detalhado(self, orcamento: Dict, cliente: str, ambiente: str) -> str:
        """Gera relatório detalhado em texto"""
        if not orcamento:
            return ""
        
        resumo = orcamento.get('resumo', {})
        componentes = orcamento.get('componentes', [])
        
        relatorio = f"""
# ORÇAMENTO DETALHADO - ORCA INTERIORES

**Cliente:** {cliente}
**Ambiente:** {ambiente}
**Data:** {orcamento.get('data_calculo', 'N/A')}
**Fonte de Preços:** {orcamento.get('fonte_precos', 'N/A')}

## RESUMO EXECUTIVO

- **Quantidade de Componentes:** {resumo.get('quantidade_componentes', 0)}
- **Área Total:** {resumo.get('area_total_m2', 0)} m²
- **Valor Final:** R$ {resumo.get('valor_final', 0):,.2f}
- **Preço por m²:** R$ {resumo.get('preco_por_m2', 0):,.2f}

## BREAKDOWN DE CUSTOS

- **Material:** R$ {resumo.get('custo_material', 0):,.2f}
- **Acessórios:** R$ {resumo.get('custo_acessorios', 0):,.2f}
- **Corte/Usinagem:** R$ {resumo.get('custo_corte', 0):,.2f}
- **Subtotal:** R$ {resumo.get('subtotal', 0):,.2f}
- **Margem de Lucro ({resumo.get('margem_lucro_pct', 0)}%):** R$ {resumo.get('valor_lucro', 0):,.2f}

## DETALHAMENTO POR COMPONENTE

"""
        
        for i, comp in enumerate(componentes, 1):
            relatorio += f"""
### {i}. {comp.get('nome', 'Componente')}
- **Tipo:** {comp.get('tipo', 'N/A').title()}
- **Área:** {comp.get('area_m2', 0)} m²
- **Material:** R$ {comp.get('custo_material', 0):,.2f}
- **Acessórios:** R$ {comp.get('custo_acessorios', 0):,.2f}
- **Corte:** R$ {comp.get('custo_corte', 0):,.2f}
- **Total:** R$ {comp.get('custo_total', 0):,.2f}
- **Preço/m²:** R$ {comp.get('preco_por_m2', 0):,.2f}

"""
        
        relatorio += """
---
*Orçamento gerado automaticamente pelo sistema Orca Interiores*
*Preços sujeitos a alteração conforme disponibilidade de material*
"""
        
        return relatorio

    def exportar_json(self, orcamento: Dict) -> str:
        """Exporta orçamento em formato JSON"""
        return json.dumps(orcamento, indent=2, ensure_ascii=False)

    def obter_precos_atuais(self) -> Dict:
        """Retorna preços atuais dos materiais"""
        return {
            'materiais': self.precos_materiais,
            'acessorios': self.custos_acessorios,
            'mao_obra': self.custos_mao_obra,
            'desperdicio': self.desperdicio,
            'data_atualizacao': '30/06/2025',
            'fonte': 'Léo Madeiras'
        }

    def calcular_economia_material(self, orcamento: Dict, material_alternativo: str) -> Dict:
        """Calcula economia ao trocar material"""
        if not orcamento or not orcamento.get('componentes'):
            return {}
        
        componentes = orcamento['componentes']
        material_atual = orcamento.get('configuracoes', {}).get('material', 'mdf_15mm')
        
        preco_atual = self.precos_materiais.get(material_atual, 69.15)
        preco_alternativo = self.precos_materiais.get(material_alternativo, 69.15)
        
        area_total = sum(comp['area_m2'] for comp in componentes)
        
        custo_atual = area_total * preco_atual
        custo_alternativo = area_total * preco_alternativo
        economia = custo_atual - custo_alternativo
        
        return {
            'material_atual': material_atual,
            'material_alternativo': material_alternativo,
            'preco_atual': preco_atual,
            'preco_alternativo': preco_alternativo,
            'area_total': area_total,
            'custo_atual': round(custo_atual, 2),
            'custo_alternativo': round(custo_alternativo, 2),
            'economia': round(economia, 2),
            'percentual_economia': round((economia / custo_atual) * 100, 1) if custo_atual > 0 else 0
        }

