"""
Sistema de Autenticação - Orca Interiores SaaS
Gerenciamento completo de usuários e planos de assinatura
"""

import sqlite3
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import os

class AuthManager:
    def __init__(self, db_path: str = "usuarios.db"):
        """Inicializa o gerenciador de autenticação"""
        self.db_path = db_path
        self.inicializar_banco()
        self.criar_usuarios_demo()
    
    def inicializar_banco(self):
        """Cria as tabelas necessárias no banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL,
                plano TEXT NOT NULL DEFAULT 'gratuito',
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_ultimo_login TIMESTAMP,
                ativo BOOLEAN DEFAULT 1,
                projetos_mes INTEGER DEFAULT 0,
                ultimo_reset_projetos DATE
            )
        ''')
        
        # Tabela de sessões
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                token TEXT UNIQUE NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_expiracao TIMESTAMP,
                ativo BOOLEAN DEFAULT 1,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        # Tabela de projetos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projetos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                nome_arquivo TEXT NOT NULL,
                dados_analise TEXT,
                dados_orcamento TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def criar_usuarios_demo(self):
        """Cria usuários demo para teste"""
        usuarios_demo = [
            {
                'nome': 'Demo Orca Interiores',
                'email': 'demo@orcainteriores.com',
                'senha': 'demo123',
                'plano': 'profissional'
            },
            {
                'nome': 'Arquiteto Teste',
                'email': 'arquiteto@teste.com',
                'senha': 'arq123',
                'plano': 'basico'
            },
            {
                'nome': 'Marceneiro Teste',
                'email': 'marceneiro@teste.com',
                'senha': 'marc123',
                'plano': 'empresarial'
            }
        ]
        
        for usuario in usuarios_demo:
            if not self.usuario_existe(usuario['email']):
                self.criar_usuario(
                    usuario['nome'],
                    usuario['email'],
                    usuario['senha'],
                    usuario['plano']
                )
    
    def hash_senha(self, senha: str) -> str:
        """Gera hash seguro da senha"""
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def usuario_existe(self, email: str) -> bool:
        """Verifica se usuário já existe"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
        resultado = cursor.fetchone()
        
        conn.close()
        return resultado is not None
    
    def criar_usuario(self, nome: str, email: str, senha: str, plano: str = 'gratuito') -> bool:
        """Cria novo usuário"""
        try:
            if self.usuario_existe(email):
                return False
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            senha_hash = self.hash_senha(senha)
            
            cursor.execute('''
                INSERT INTO usuarios (nome, email, senha_hash, plano, ultimo_reset_projetos)
                VALUES (?, ?, ?, ?, ?)
            ''', (nome, email, senha_hash, plano, datetime.now().date()))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return False
    
    def fazer_login(self, email: str, senha: str) -> Optional[Dict]:
        """Realiza login do usuário"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            senha_hash = self.hash_senha(senha)
            
            cursor.execute('''
                SELECT id, nome, email, plano, projetos_mes, ultimo_reset_projetos
                FROM usuarios 
                WHERE email = ? AND senha_hash = ? AND ativo = 1
            ''', (email, senha_hash))
            
            resultado = cursor.fetchone()
            
            if resultado:
                usuario_id, nome, email, plano, projetos_mes, ultimo_reset = resultado
                
                # Verificar se precisa resetar contador de projetos (novo mês)
                hoje = datetime.now().date()
                if ultimo_reset:
                    ultimo_reset_date = datetime.strptime(ultimo_reset, '%Y-%m-%d').date()
                    if hoje.month != ultimo_reset_date.month or hoje.year != ultimo_reset_date.year:
                        # Resetar contador para novo mês
                        cursor.execute('''
                            UPDATE usuarios 
                            SET projetos_mes = 0, ultimo_reset_projetos = ?
                            WHERE id = ?
                        ''', (hoje, usuario_id))
                        projetos_mes = 0
                
                # Atualizar último login
                cursor.execute('''
                    UPDATE usuarios 
                    SET data_ultimo_login = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (usuario_id,))
                
                conn.commit()
                conn.close()
                
                return {
                    'id': usuario_id,
                    'nome': nome,
                    'email': email,
                    'plano': plano,
                    'projetos_mes': projetos_mes
                }
            
            conn.close()
            return None
            
        except Exception as e:
            print(f"Erro no login: {e}")
            return None
    
    def incrementar_projeto(self, usuario_id: int) -> bool:
        """Incrementa contador de projetos do usuário"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE usuarios 
                SET projetos_mes = projetos_mes + 1
                WHERE id = ?
            ''', (usuario_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Erro ao incrementar projeto: {e}")
            return False
    
    def obter_limites_plano(self, plano: str) -> Dict:
        """Retorna limites do plano"""
        limites = {
            'gratuito': {
                'projetos_mes': 3,
                'upload_max_mb': 50,
                'recursos': ['upload_basico', 'orcamento_simples']
            },
            'basico': {
                'projetos_mes': 50,
                'upload_max_mb': 200,
                'recursos': ['upload_basico', 'orcamento_simples', 'visualizacao_3d', 'precos_atualizados']
            },
            'profissional': {
                'projetos_mes': 200,
                'upload_max_mb': 500,
                'recursos': ['upload_basico', 'orcamento_simples', 'visualizacao_3d', 'precos_atualizados', 'api_integracao', 'white_label']
            },
            'empresarial': {
                'projetos_mes': 999999,
                'upload_max_mb': 1000,
                'recursos': ['upload_basico', 'orcamento_simples', 'visualizacao_3d', 'precos_atualizados', 'api_integracao', 'white_label', 'multi_usuarios', 'dashboard_avancado']
            }
        }
        
        return limites.get(plano, limites['gratuito'])
    
    def salvar_projeto(self, usuario_id: int, nome_arquivo: str, analise: Dict, orcamento: Dict) -> bool:
        """Salva projeto do usuário"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO projetos (usuario_id, nome_arquivo, dados_analise, dados_orcamento)
                VALUES (?, ?, ?, ?)
            ''', (
                usuario_id,
                nome_arquivo,
                json.dumps(analise),
                json.dumps(orcamento)
            ))
            
            conn.commit()
            conn.close()
            
            # Incrementar contador de projetos
            self.incrementar_projeto(usuario_id)
            
            return True
            
        except Exception as e:
            print(f"Erro ao salvar projeto: {e}")
            return False
    
    def listar_projetos_usuario(self, usuario_id: int) -> List[Dict]:
        """Lista projetos do usuário"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, nome_arquivo, data_criacao
                FROM projetos
                WHERE usuario_id = ?
                ORDER BY data_criacao DESC
            ''', (usuario_id,))
            
            projetos = []
            for row in cursor.fetchall():
                projetos.append({
                    'id': row[0],
                    'nome_arquivo': row[1],
                    'data_criacao': row[2]
                })
            
            conn.close()
            return projetos
            
        except Exception as e:
            print(f"Erro ao listar projetos: {e}")
            return []
    
    def obter_estatisticas_usuario(self, usuario_id: int) -> Dict:
        """Obtém estatísticas do usuário"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Contar projetos totais
            cursor.execute('''
                SELECT COUNT(*) FROM projetos WHERE usuario_id = ?
            ''', (usuario_id,))
            total_projetos = cursor.fetchone()[0]
            
            # Contar projetos este mês
            cursor.execute('''
                SELECT COUNT(*) FROM projetos 
                WHERE usuario_id = ? AND strftime('%Y-%m', data_criacao) = strftime('%Y-%m', 'now')
            ''', (usuario_id,))
            projetos_mes = cursor.fetchone()[0]
            
            # Obter dados do usuário
            cursor.execute('''
                SELECT plano, data_criacao FROM usuarios WHERE id = ?
            ''', (usuario_id,))
            usuario_data = cursor.fetchone()
            
            conn.close()
            
            if usuario_data:
                plano, data_criacao = usuario_data
                return {
                    'total_projetos': total_projetos,
                    'projetos_mes': projetos_mes,
                    'plano': plano,
                    'membro_desde': data_criacao
                }
            
            return {}
            
        except Exception as e:
            print(f"Erro ao obter estatísticas: {e}")
            return {}
    
    def validar_limite_projeto(self, usuario_id: int) -> bool:
        """Valida se usuário pode criar novo projeto"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT plano, projetos_mes FROM usuarios WHERE id = ?
            ''', (usuario_id,))
            
            resultado = cursor.fetchone()
            conn.close()
            
            if resultado:
                plano, projetos_mes = resultado
                limites = self.obter_limites_plano(plano)
                return projetos_mes < limites['projetos_mes']
            
            return False
            
        except Exception as e:
            print(f"Erro ao validar limite: {e}")
            return False

