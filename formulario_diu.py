#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Formulário DIU
Gerencia informações de pacientes para inserção de DIU
"""

import sqlite3
import csv
import os
from datetime import datetime

class FormularioDIU:
    def __init__(self, db_name="formulario_diu.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados e cria as tabelas necessárias"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
        # Criar tabela de pacientes
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                -- IDENTIFICAÇÃO
                nome_completo TEXT NOT NULL,
                data_nascimento TEXT,
                telefone TEXT,
                cpf TEXT,
                sus TEXT,
                cor TEXT,
                religiao TEXT,
                profissao TEXT,
                escolaridade TEXT,
                endereco TEXT,
                local_atendimento TEXT,
                
                -- MOTIVAÇÃO PARA INSERÇÃO DO DIU
                motivo_contracepcao INTEGER DEFAULT 0,
                motivo_pos_aborto INTEGER DEFAULT 0,
                motivo_sua INTEGER DEFAULT 0,
                motivo_doenca_hematologica INTEGER DEFAULT 0,
                motivo_transplantada INTEGER DEFAULT 0,
                motivo_mioma INTEGER DEFAULT 0,
                motivo_endometriose INTEGER DEFAULT 0,
                motivo_dor_pelvica INTEGER DEFAULT 0,
                motivo_tpm INTEGER DEFAULT 0,
                motivo_terapia_pos_menopausa INTEGER DEFAULT 0,
                motivo_outro TEXT,
                
                -- DADOS GINECOLÓGICOS
                dum TEXT,
                ultima_co TEXT,
                cm_regularidade TEXT,
                cm_duracao_dias INTEGER,
                teve_ist TEXT,
                parceiro_fixo TEXT,
                alto_risco_ist TEXT,
                uso_mac TEXT,
                uso_mac_qual TEXT,
                anemia TEXT,
                sangramento_aumentado TEXT,
                dipa_3meses TEXT,
                ist_ativa TEXT,
                ist_ativa_qual TEXT,
                hiv_aids TEXT,
                uso_antirretrovirais TEXT,
                antirretrovirais_quais TEXT,
                sangramento_nao_investigado TEXT,
                cancer_cervical TEXT,
                
                -- HISTÓRIA OBSTÉTRICA
                gesta INTEGER,
                para INTEGER,
                cesarea INTEGER,
                abortos INTEGER,
                data_ultimo_parto TEXT,
                data_ultimo_aborto TEXT,
                infeccao_pos_parto_aborto TEXT,
                
                -- INSERÇÃO DO DIU
                informada_contraindicacoes TEXT,
                diu_escolhido TEXT,
                peso_kg REAL,
                altura_cm REAL,
                pa_mmhg TEXT,
                data_insercao TEXT,
                data_primeira_revisao TEXT,
                exame_pelvico TEXT,
                cervicite_purulenta TEXT,
                confirma_elegibilidade TEXT,
                insercao_resultado TEXT,
                insercao_motivo TEXT,
                posicao_uterina TEXT,
                reflexo_vaginal TEXT,
                uso_analgesia TEXT,
                analgesia_qual TEXT,
                uso_dilatadores TEXT,
                histerometria_cm REAL,
                dor_nota INTEGER,
                dor_momento TEXT,
                dificuldade_insercao TEXT,
                motivo_dificuldade TEXT,
                inserido_por TEXT,
                
                data_registro TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        
        # Obter lista de colunas válidas da tabela
        self.cursor.execute("PRAGMA table_info(pacientes)")
        self.valid_columns = set([col[1] for col in self.cursor.fetchall()])
    
    def get_input(self, prompt, required=False, tipo="texto", min_val=None, max_val=None):
        """Obtém input do usuário com validação"""
        while True:
            valor = input(prompt).strip()
            
            if not valor and required:
                print("Este campo é obrigatório!")
                continue
            
            if not valor:
                return None
            
            if tipo == "numero":
                try:
                    num = int(valor)
                    if min_val is not None and num < min_val:
                        print(f"Por favor, digite um número maior ou igual a {min_val}!")
                        continue
                    if max_val is not None and num > max_val:
                        print(f"Por favor, digite um número menor ou igual a {max_val}!")
                        continue
                    return num
                except ValueError:
                    print("Por favor, digite um número válido!")
                    continue
            elif tipo == "decimal":
                try:
                    return float(valor)
                except ValueError:
                    print("Por favor, digite um número decimal válido!")
                    continue
            elif tipo == "sim_nao":
                if valor.lower() in ['s', 'sim', 'n', 'não', 'nao']:
                    return 's' if valor.lower() in ['s', 'sim'] else 'n'
                else:
                    print("Por favor, digite 's' ou 'n'!")
                    continue
            
            return valor
    
    def coletar_identificacao(self):
        """Coleta dados de identificação do paciente"""
        print("\n" + "="*60)
        print("IDENTIFICAÇÃO")
        print("="*60)
        
        dados = {}
        dados['nome_completo'] = self.get_input("Nome completo: ", required=True)
        dados['data_nascimento'] = self.get_input("Data de nascimento (DD/MM/AAAA): ")
        dados['telefone'] = self.get_input("Telefone: ")
        dados['cpf'] = self.get_input("CPF: ")
        dados['sus'] = self.get_input("SUS: ")
        dados['cor'] = self.get_input("Cor: ")
        dados['religiao'] = self.get_input("Religião: ")
        dados['profissao'] = self.get_input("Profissão: ")
        dados['escolaridade'] = self.get_input("Escolaridade: ")
        dados['endereco'] = self.get_input("Endereço: ")
        dados['local_atendimento'] = self.get_input("Local de atendimento: ")
        
        return dados
    
    def coletar_motivacao(self):
        """Coleta dados sobre motivação para inserção do DIU"""
        print("\n" + "="*60)
        print("MOTIVAÇÃO PARA INSERÇÃO DO DIU")
        print("="*60)
        print("Marque as opções aplicáveis (s/n):")
        
        dados = {}
        dados['motivo_contracepcao'] = 1 if self.get_input("1. Contracepção (s/n): ", tipo="sim_nao") == 's' else 0
        dados['motivo_pos_aborto'] = 1 if self.get_input("2. Pós aborto (s/n): ", tipo="sim_nao") == 's' else 0
        dados['motivo_sua'] = 1 if self.get_input("3. SUA (s/n): ", tipo="sim_nao") == 's' else 0
        dados['motivo_doenca_hematologica'] = 1 if self.get_input("4. Doença hematológica (s/n): ", tipo="sim_nao") == 's' else 0
        dados['motivo_transplantada'] = 1 if self.get_input("5. Transplantada (s/n): ", tipo="sim_nao") == 's' else 0
        dados['motivo_mioma'] = 1 if self.get_input("6. Mioma (s/n): ", tipo="sim_nao") == 's' else 0
        dados['motivo_endometriose'] = 1 if self.get_input("7. Endometriose (s/n): ", tipo="sim_nao") == 's' else 0
        dados['motivo_dor_pelvica'] = 1 if self.get_input("8. Dor pélvica (s/n): ", tipo="sim_nao") == 's' else 0
        dados['motivo_tpm'] = 1 if self.get_input("9. TPM (s/n): ", tipo="sim_nao") == 's' else 0
        dados['motivo_terapia_pos_menopausa'] = 1 if self.get_input("10. Terapia pós menopausa (s/n): ", tipo="sim_nao") == 's' else 0
        dados['motivo_outro'] = self.get_input("Outro motivo (descreva): ")
        
        return dados
    
    def coletar_dados_ginecologicos(self):
        """Coleta dados ginecológicos"""
        print("\n" + "="*60)
        print("DADOS GINECOLÓGICOS")
        print("="*60)
        
        dados = {}
        dados['dum'] = self.get_input("Data da última menstruação (DUM) (DD/MM/AAAA): ")
        dados['ultima_co'] = self.get_input("Última C.O: ")
        dados['cm_regularidade'] = self.get_input("C.M (regular/irregular): ")
        dados['cm_duracao_dias'] = self.get_input("Duração em dias: ", tipo="numero")
        dados['teve_ist'] = self.get_input("Já teve IST? (s/n): ", tipo="sim_nao")
        dados['parceiro_fixo'] = self.get_input("Possui parceiro fixo? (s/n): ", tipo="sim_nao")
        dados['alto_risco_ist'] = self.get_input("Alto risco de IST? (s/n): ", tipo="sim_nao")
        dados['uso_mac'] = self.get_input("Uso de MAC? (s/n): ", tipo="sim_nao")
        if dados['uso_mac'] == 's':
            dados['uso_mac_qual'] = self.get_input("Qual MAC: ")
        else:
            dados['uso_mac_qual'] = None
        dados['anemia'] = self.get_input("Anemia? (s/n): ", tipo="sim_nao")
        dados['sangramento_aumentado'] = self.get_input("Sangramento uterino aumentado na menstruação? (s/n): ", tipo="sim_nao")
        dados['dipa_3meses'] = self.get_input("DIPA nos últimos 3 meses? (s/n): ", tipo="sim_nao")
        dados['ist_ativa'] = self.get_input("IST ativa? (s/n): ", tipo="sim_nao")
        if dados['ist_ativa'] == 's':
            dados['ist_ativa_qual'] = self.get_input("Qual IST: ")
        else:
            dados['ist_ativa_qual'] = None
        dados['hiv_aids'] = self.get_input("HIV/AIDS? (s/n): ", tipo="sim_nao")
        dados['uso_antirretrovirais'] = self.get_input("Uso de antirretrovirais? (s/n): ", tipo="sim_nao")
        if dados['uso_antirretrovirais'] == 's':
            dados['antirretrovirais_quais'] = self.get_input("Quais antirretrovirais: ")
        else:
            dados['antirretrovirais_quais'] = None
        dados['sangramento_nao_investigado'] = self.get_input("Sangramento uterino não investigado? (s/n): ", tipo="sim_nao")
        dados['cancer_cervical'] = self.get_input("Câncer cervical? (s/n): ", tipo="sim_nao")
        
        return dados
    
    def coletar_historia_obstetrica(self):
        """Coleta história obstétrica"""
        print("\n" + "="*60)
        print("HISTÓRIA OBSTÉTRICA")
        print("="*60)
        
        dados = {}
        dados['gesta'] = self.get_input("Gesta: ", tipo="numero")
        dados['para'] = self.get_input("Para: ", tipo="numero")
        dados['cesarea'] = self.get_input("Cesárea: ", tipo="numero")
        dados['abortos'] = self.get_input("Abortos: ", tipo="numero")
        dados['data_ultimo_parto'] = self.get_input("Data do último parto (DD/MM/AAAA): ")
        dados['data_ultimo_aborto'] = self.get_input("Data do último aborto (DD/MM/AAAA): ")
        dados['infeccao_pos_parto_aborto'] = self.get_input("Teve infecção pós-parto ou pós-aborto? (s/n): ", tipo="sim_nao")
        
        return dados
    
    def coletar_insercao_diu(self):
        """Coleta dados sobre inserção do DIU"""
        print("\n" + "="*60)
        print("INSERÇÃO DO DIU")
        print("="*60)
        
        dados = {}
        dados['informada_contraindicacoes'] = self.get_input("Foi informada sobre contraindicações e efeitos? (s/n): ", tipo="sim_nao")
        dados['diu_escolhido'] = self.get_input("DIU escolhido (TCU/Levonorgestrel): ")
        dados['peso_kg'] = self.get_input("Peso (kg): ", tipo="decimal")
        dados['altura_cm'] = self.get_input("Altura (cm): ", tipo="decimal")
        dados['pa_mmhg'] = self.get_input("PA (mmHg): ")
        dados['data_insercao'] = self.get_input("Data de inserção (DD/MM/AAAA): ")
        dados['data_primeira_revisao'] = self.get_input("Data da primeira revisão (DD/MM/AAAA): ")
        dados['exame_pelvico'] = self.get_input("Exame pélvico (normal/anormal): ")
        dados['cervicite_purulenta'] = self.get_input("Cervicite purulenta? (s/n): ", tipo="sim_nao")
        dados['confirma_elegibilidade'] = self.get_input("Confirma elegibilidade para o DIU? (s/n): ", tipo="sim_nao")
        dados['insercao_resultado'] = self.get_input("Inserção (fácil/difícil/não realizada): ")
        if dados['insercao_resultado'] in ['difícil', 'dificil', 'não realizada', 'nao realizada']:
            dados['insercao_motivo'] = self.get_input("Motivo: ")
        else:
            dados['insercao_motivo'] = None
        dados['posicao_uterina'] = self.get_input("Posição uterina (AVF/MVF/RVF): ")
        dados['reflexo_vaginal'] = self.get_input("Reflexo vaginal? (s/n): ", tipo="sim_nao")
        dados['uso_analgesia'] = self.get_input("Uso de analgesia? (s/n): ", tipo="sim_nao")
        if dados['uso_analgesia'] == 's':
            dados['analgesia_qual'] = self.get_input("Qual analgesia: ")
        else:
            dados['analgesia_qual'] = None
        dados['uso_dilatadores'] = self.get_input("Uso de dilatadores cervicais? (s/n): ", tipo="sim_nao")
        dados['histerometria_cm'] = self.get_input("Histerometria (cm): ", tipo="decimal")
        dados['dor_nota'] = self.get_input("Nota de dor na inserção (1-10): ", tipo="numero", min_val=1, max_val=10)
        dados['dor_momento'] = self.get_input("Em qual momento (Histerometria/Liberação do DIU/Fixação do colo do útero/Outro): ")
        dados['dificuldade_insercao'] = self.get_input("Dificuldade na inserção (sem dificuldade/dificuldade esperada/mais difícil que o esperado/não foi possível inserir): ")
        if 'dificuldade' in dados['dificuldade_insercao'].lower() or 'difícil' in dados['dificuldade_insercao'].lower():
            dados['motivo_dificuldade'] = self.get_input("Motivo da dificuldade: ")
        else:
            dados['motivo_dificuldade'] = None
        dados['inserido_por'] = self.get_input("Inserido por (staff/residente/enfermeira/estudante/MFC/supervisor): ")
        
        return dados
    
    def novo_registro(self):
        """Cria um novo registro completo de paciente"""
        print("\n" + "#"*60)
        print("NOVO REGISTRO DE PACIENTE")
        print("#"*60)
        
        # Coletar todos os dados
        dados = {}
        dados.update(self.coletar_identificacao())
        dados.update(self.coletar_motivacao())
        dados.update(self.coletar_dados_ginecologicos())
        dados.update(self.coletar_historia_obstetrica())
        dados.update(self.coletar_insercao_diu())
        
        # Confirmar salvamento
        print("\n" + "-"*60)
        confirma = self.get_input("Deseja salvar este registro? (s/n): ", tipo="sim_nao")
        
        if confirma == 's':
            # Validar que todas as colunas são válidas
            invalid_columns = set(dados.keys()) - self.valid_columns
            if invalid_columns:
                print(f"\n✗ Erro: Colunas inválidas detectadas: {invalid_columns}")
                return
            
            # Montar query de inserção com colunas validadas
            colunas = ', '.join(dados.keys())
            placeholders = ', '.join(['?' for _ in dados])
            query = f"INSERT INTO pacientes ({colunas}) VALUES ({placeholders})"
            
            self.cursor.execute(query, list(dados.values()))
            self.conn.commit()
            
            print("\n✓ Registro salvo com sucesso!")
            print(f"ID do registro: {self.cursor.lastrowid}")
        else:
            print("\n✗ Registro cancelado.")
    
    def listar_registros(self, limite=10):
        """Lista os últimos registros salvos"""
        print("\n" + "="*60)
        print(f"ÚLTIMOS {limite} REGISTROS")
        print("="*60)
        
        self.cursor.execute('''
            SELECT id, nome_completo, data_nascimento, telefone, data_insercao, data_registro
            FROM pacientes
            ORDER BY id DESC
            LIMIT ?
        ''', (limite,))
        
        registros = self.cursor.fetchall()
        
        if not registros:
            print("Nenhum registro encontrado.")
            return
        
        for reg in registros:
            print(f"\nID: {reg[0]}")
            print(f"Nome: {reg[1]}")
            print(f"Data Nascimento: {reg[2] or 'N/A'}")
            print(f"Telefone: {reg[3] or 'N/A'}")
            print(f"Data Inserção DIU: {reg[4] or 'N/A'}")
            print(f"Data Registro: {reg[5]}")
            print("-"*60)
    
    def buscar_paciente(self):
        """Busca pacientes por nome"""
        print("\n" + "="*60)
        print("BUSCAR PACIENTE")
        print("="*60)
        
        nome = self.get_input("Digite o nome (ou parte do nome) para buscar: ", required=True)
        
        self.cursor.execute('''
            SELECT id, nome_completo, data_nascimento, telefone, cpf, data_insercao
            FROM pacientes
            WHERE nome_completo LIKE ?
            ORDER BY nome_completo
        ''', (f'%{nome}%',))
        
        registros = self.cursor.fetchall()
        
        if not registros:
            print(f"\nNenhum paciente encontrado com o nome '{nome}'.")
            return
        
        print(f"\n{len(registros)} paciente(s) encontrado(s):\n")
        
        for reg in registros:
            print(f"ID: {reg[0]}")
            print(f"Nome: {reg[1]}")
            print(f"Data Nascimento: {reg[2] or 'N/A'}")
            print(f"Telefone: {reg[3] or 'N/A'}")
            print(f"CPF: {reg[4] or 'N/A'}")
            print(f"Data Inserção DIU: {reg[5] or 'N/A'}")
            print("-"*60)
        
        # Opção de ver detalhes
        ver_detalhes = self.get_input("\nDeseja ver os detalhes completos de algum registro? (s/n): ", tipo="sim_nao")
        if ver_detalhes == 's':
            id_registro = self.get_input("Digite o ID do registro: ", tipo="numero")
            self.ver_detalhes_registro(id_registro)
    
    def ver_detalhes_registro(self, id_registro):
        """Exibe todos os detalhes de um registro específico"""
        self.cursor.execute('SELECT * FROM pacientes WHERE id = ?', (id_registro,))
        registro = self.cursor.fetchone()
        
        if not registro:
            print(f"\nRegistro com ID {id_registro} não encontrado.")
            return
        
        # Obter nomes das colunas
        colunas = [desc[0] for desc in self.cursor.description]
        
        print("\n" + "="*60)
        print(f"DETALHES DO REGISTRO #{id_registro}")
        print("="*60)
        
        for i, coluna in enumerate(colunas):
            if registro[i] is not None:
                print(f"{coluna}: {registro[i]}")
    
    def exportar_csv(self):
        """Exporta todos os registros para um arquivo CSV"""
        print("\n" + "="*60)
        print("EXPORTAR PARA CSV")
        print("="*60)
        
        nome_arquivo = self.get_input("Nome do arquivo (sem extensão) [export]: ")
        if not nome_arquivo:
            nome_arquivo = "export"
        
        nome_arquivo = f"{nome_arquivo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        self.cursor.execute('SELECT * FROM pacientes')
        registros = self.cursor.fetchall()
        
        if not registros:
            print("Nenhum registro para exportar.")
            return
        
        # Obter nomes das colunas
        colunas = [desc[0] for desc in self.cursor.description]
        
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            writer.writerow(colunas)
            writer.writerows(registros)
        
        print(f"\n✓ {len(registros)} registro(s) exportado(s) com sucesso!")
        print(f"Arquivo: {nome_arquivo}")
    
    def menu_principal(self):
        """Exibe o menu principal do sistema"""
        while True:
            print("\n" + "="*60)
            print("SISTEMA DE FORMULÁRIO DIU")
            print("="*60)
            print("1. Novo Registro - Criar um novo registro de paciente")
            print("2. Listar Registros - Ver os últimos registros salvos")
            print("3. Buscar Paciente - Buscar registros por nome")
            print("4. Exportar para CSV - Exportar todos os dados para arquivo CSV")
            print("5. Sair - Encerrar o sistema")
            print("="*60)
            
            opcao = self.get_input("Escolha uma opção (1-5): ")
            
            if opcao == '1':
                self.novo_registro()
            elif opcao == '2':
                self.listar_registros()
            elif opcao == '3':
                self.buscar_paciente()
            elif opcao == '4':
                self.exportar_csv()
            elif opcao == '5':
                print("\nEncerrando o sistema...")
                break
            else:
                print("\n✗ Opção inválida! Tente novamente.")
    
    def __del__(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()


def main():
    """Função principal"""
    print("="*60)
    print("BEM-VINDO AO SISTEMA DE FORMULÁRIO DIU")
    print("="*60)
    
    app = FormularioDIU()
    app.menu_principal()
    
    print("\nObrigado por usar o Sistema de Formulário DIU!")


if __name__ == "__main__":
    main()
