"""
Configurações - Orca Interiores SaaS
Configurações centralizadas do sistema
"""

import os
from datetime import datetime

class Config:
    """Configurações centralizadas da aplicação"""
    
    # Informações da aplicação
    APP_NAME = "Orca Interiores SaaS"
    APP_VERSION = "2.0"
    APP_DESCRIPTION = "Sistema Inteligente de Orçamento para Marcenaria"
    
    # Configurações de banco de dados
    DATABASE_PATH = "usuarios.db"
    
    # Configurações de upload
    MAX_UPLOAD_SIZE_MB = 500
    ALLOWED_EXTENSIONS = ['.obj', '.dae', '.stl', '.ply']
    
    # Configurações de planos
    PLANOS = {
        'gratuito': {
            'nome': 'Gratuito',
            'preco': 0.00,
            'projetos_mes': 3,
            'upload_max_mb': 50,
            'recursos': [
                'upload_basico',
                'orcamento_simples',
                'suporte_email'
            ]
        },
        'basico': {
            'nome': 'Básico',
            'preco': 49.90,
            'projetos_mes': 50,
            'upload_max_mb': 200,
            'recursos': [
                'upload_basico',
                'orcamento_simples',
                'visualizacao_3d',
                'precos_atualizados',
                'relatorios_pdf',
                'suporte_prioritario'
            ]
        },
        'profissional': {
            'nome': 'Profissional',
            'preco': 99.90,
            'projetos_mes': 200,
            'upload_max_mb': 500,
            'recursos': [
                'upload_basico',
                'orcamento_simples',
                'visualizacao_3d',
                'precos_atualizados',
                'relatorios_pdf',
                'api_integracao',
                'white_label',
                'suporte_prioritario'
            ]
        },
        'empresarial': {
            'nome': 'Empresarial',
            'preco': 299.90,
            'projetos_mes': 999999,
            'upload_max_mb': 1000,
            'recursos': [
                'upload_basico',
                'orcamento_simples',
                'visualizacao_3d',
                'precos_atualizados',
                'relatorios_pdf',
                'api_integracao',
                'white_label',
                'multi_usuarios',
                'dashboard_avancado',
                'consultoria_inclusa',
                'suporte_24h'
            ]
        }
    }
    
    # Configurações de materiais
    MATERIAIS_DISPONIVEIS = {
        'mdf_15mm': {
            'nome': 'MDF 15mm',
            'descricao': 'Medium Density Fiberboard 15mm',
            'categoria': 'mdf'
        },
        'mdf_18mm': {
            'nome': 'MDF 18mm',
            'descricao': 'Medium Density Fiberboard 18mm',
            'categoria': 'mdf'
        },
        'compensado_15mm': {
            'nome': 'Compensado 15mm',
            'descricao': 'Compensado multilaminado 15mm',
            'categoria': 'compensado'
        },
        'compensado_18mm': {
            'nome': 'Compensado 18mm',
            'descricao': 'Compensado multilaminado 18mm',
            'categoria': 'compensado'
        },
        'melamina_15mm': {
            'nome': 'Melamina 15mm',
            'descricao': 'MDF revestido com melamina 15mm',
            'categoria': 'melamina'
        },
        'melamina_18mm': {
            'nome': 'Melamina 18mm',
            'descricao': 'MDF revestido com melamina 18mm',
            'categoria': 'melamina'
        }
    }
    
    # Configurações de qualidade
    QUALIDADES_ACESSORIOS = {
        'comum': {
            'nome': 'Comum',
            'descricao': 'Acessórios padrão de boa qualidade',
            'multiplicador': 1.0
        },
        'premium': {
            'nome': 'Premium',
            'descricao': 'Acessórios de alta qualidade e durabilidade',
            'multiplicador': 1.5
        }
    }
    
    # Configurações de complexidade
    COMPLEXIDADES = {
        'simples': {
            'nome': 'Simples',
            'descricao': 'Projeto básico com poucos detalhes',
            'multiplicador': 1.0
        },
        'media': {
            'nome': 'Média',
            'descricao': 'Projeto com complexidade moderada',
            'multiplicador': 1.2
        },
        'complexa': {
            'nome': 'Complexa',
            'descricao': 'Projeto com muitos detalhes e acabamentos',
            'multiplicador': 1.5
        },
        'premium': {
            'nome': 'Premium',
            'descricao': 'Projeto de alta complexidade e acabamento',
            'multiplicador': 2.0
        }
    }
    
    # Configurações de fornecedores
    FORNECEDORES = {
        'leo_madeiras': {
            'nome': 'Léo Madeiras',
            'url': 'https://www.leomadeiras.com.br/',
            'descricao': 'Fornecedor principal de materiais',
            'ativo': True,
            'ultima_atualizacao': '30/06/2025'
        }
    }
    
    # Configurações de interface
    CORES_TEMA = {
        'primaria': '#667eea',
        'secundaria': '#764ba2',
        'sucesso': '#28a745',
        'aviso': '#ffc107',
        'erro': '#dc3545',
        'info': '#17a2b8'
    }
    
    # Configurações de email (para futuras implementações)
    EMAIL_CONFIG = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'use_tls': True,
        'from_email': 'noreply@orcainteriores.com',
        'from_name': 'Orca Interiores SaaS'
    }
    
    # Configurações de API (para futuras implementações)
    API_CONFIG = {
        'rate_limit': 100,  # requests por minuto
        'timeout': 30,      # segundos
        'max_retries': 3
    }
    
    # Configurações de segurança
    SECURITY_CONFIG = {
        'session_timeout_hours': 24,
        'max_login_attempts': 5,
        'password_min_length': 6,
        'require_email_verification': False
    }
    
    # Configurações de logs
    LOG_CONFIG = {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file_path': 'orca_saas.log',
        'max_size_mb': 10,
        'backup_count': 5
    }
    
    @classmethod
    def get_plano_info(cls, plano: str) -> dict:
        """Retorna informações do plano"""
        return cls.PLANOS.get(plano, cls.PLANOS['gratuito'])
    
    @classmethod
    def get_material_info(cls, material: str) -> dict:
        """Retorna informações do material"""
        return cls.MATERIAIS_DISPONIVEIS.get(material, {})
    
    @classmethod
    def get_qualidade_info(cls, qualidade: str) -> dict:
        """Retorna informações da qualidade"""
        return cls.QUALIDADES_ACESSORIOS.get(qualidade, cls.QUALIDADES_ACESSORIOS['comum'])
    
    @classmethod
    def get_complexidade_info(cls, complexidade: str) -> dict:
        """Retorna informações da complexidade"""
        return cls.COMPLEXIDADES.get(complexidade, cls.COMPLEXIDADES['media'])
    
    @classmethod
    def is_recurso_disponivel(cls, plano: str, recurso: str) -> bool:
        """Verifica se recurso está disponível no plano"""
        plano_info = cls.get_plano_info(plano)
        return recurso in plano_info.get('recursos', [])
    
    @classmethod
    def get_limite_upload(cls, plano: str) -> int:
        """Retorna limite de upload em MB para o plano"""
        plano_info = cls.get_plano_info(plano)
        return plano_info.get('upload_max_mb', 50)
    
    @classmethod
    def get_limite_projetos(cls, plano: str) -> int:
        """Retorna limite de projetos por mês para o plano"""
        plano_info = cls.get_plano_info(plano)
        return plano_info.get('projetos_mes', 3)
    
    @classmethod
    def get_app_info(cls) -> dict:
        """Retorna informações da aplicação"""
        return {
            'nome': cls.APP_NAME,
            'versao': cls.APP_VERSION,
            'descricao': cls.APP_DESCRIPTION,
            'data_build': datetime.now().strftime('%d/%m/%Y %H:%M')
        }
    
    @classmethod
    def get_cores_tema(cls) -> dict:
        """Retorna cores do tema"""
        return cls.CORES_TEMA.copy()
    
    @classmethod
    def get_fornecedores_ativos(cls) -> dict:
        """Retorna fornecedores ativos"""
        return {k: v for k, v in cls.FORNECEDORES.items() if v.get('ativo', False)}

