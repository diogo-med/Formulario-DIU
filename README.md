# Formulario-DIU


## Informações Coletadas

### IDENTIFICAÇÃO
- Nome completo 
- Data de nascimento 
- Telefone 
- CPF 
- SUS
- Cor
- Religião
- Profissão
- Escolaridade
- Endereço 
- Local de atendimento 

### MOTIVAÇÃO PARA INSERÇÃO DO DIU
- 1 Contracepção
- 2 Pós aborto
- 3 SUA
- 4 Doença hematológica
- 5 Transplantada
- 6 Mioma
- 7 Endometriose
- 8 Dor pélvica
- 9 TPM
- 10 Terapia pós menopausa
- Outro:(string descrição)

### DADOS GINEGOLÓGICOS
- Data da última menstruação (DUM)
- Última C.O
- C.M(regular/irregular) + Duração(dias)
- Já teve IST (sim/não)
- Possui parceiro fixo(sim/não)
- Alto risco de IST(sim/não)
- Uso de MAC(s/n) + Qual
- Anemia(s/n)
- Sangramento uterino aumentado na menstruação(s/n)
- DIPA nos ultimos 3 meses(s/n)
- IST ativa(s/n)+ qual
- HIV/AIDS (S/N)
- Uso de antirretrovirais(s/n) +quais
- Sangramento uterino não investigado(s/n)
- Câncer cervical(s/n)

### HISTÓRIA OBSTÉTRICA
- Gesta
- Para
- Cesárea
- Abortos
- Data do último parto
- Data do último aborto
- Teve infecção pós-parto ou pós-aborto(s/n)

### INSERÇÃO DO DIU
- Foi informada sobre contraindicações e efeitos do DIU sobre o sangramento e possíveis efeotps colaterais(s/n)
- DIU escolhido (TCU/Levonorgestrel)
- Peso kg
- Altura cm
- PA(mmHg)
- Data de inserção
- Data da primeira revisão
- Exame pélvico (normal/anormal)
- Cervicite purulenta(s/n)
- Confirma elegimilidade para o DIU(s/n)
- Inserção (fácil/difícil/ não realizada)+motivo
- Posição uterina(AVF/MVF/RVF)
- Refelexo vaginal(s/n)
- Uso de analgesia(s/n)+qual
- Uso de dilatadores cervicais (s/n)
- Histerometria(cm)
- Nota de dor na inserção(1-10) em qual momento (Histerometria/Liberação do DIU/Fixação do colo do útero(pinça de pozzi)/ Outro(recebe string))
- Dificuldade na inserção(sem dificuldade/dificuldade esperada/mais difícil que o esperado/não foi possível inserir)
- Qual o motivo da dificuldade(Estenose de orifício interno ou externo/ curvatura uterina acentuada/cicatriz de cesárea/deformação da cavidade)
- inserido por ()staff/residente()ano/enfermeira/estudante()periodo/MFC()/supervisor())



## Como Usar

### Requisitos
- Python 3.6 ou superior
- Nenhuma biblioteca externa necessária (usa apenas bibliotecas padrão)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/diogo-med/Formulario-DIU.git
cd Formulario-DIU
```

2. Execute o programa:
```bash
python3 formulario_diu.py
```

### Uso do Sistema

Ao iniciar o programa, você verá o menu principal com as seguintes opções:

```
1. Novo Registro - Criar um novo registro de paciente
2. Listar Registros - Ver os últimos registros salvos
3. Buscar Paciente - Buscar registros por nome
4. Exportar para CSV - Exportar todos os dados para arquivo CSV
5. Sair - Encerrar o sistema
```

**Nota:** Todos os dados são armazenados automaticamente em um banco de dados SQLite offline (`formulario_diu.db`). A opção "Exportar para CSV" permite exportar uma cópia dos dados para análise externa, mas o armazenamento principal é no arquivo .db.

### Funcionalidades Detalhadas

#### 1. Novo Registro
Guia o usuário através de todas as seções do formulário:
- **Identificação**: Nome, CPF, SUS, endereço, etc.
- **Motivação**: Razões para inserção do DIU (pode selecionar múltiplas)
- **Dados Ginecológicos**: DUM, histórico de IST, uso de MAC, etc.
- **História Obstétrica**: Gesta, para, cesáreas, abortos, etc.
- **Inserção do DIU**: Dados do procedimento, tipo de DIU, dificuldades, etc.

#### 2. Listar Registros
Exibe os 10 registros mais recentes com informações resumidas (nome, telefone, data de inserção).

#### 3. Buscar Paciente
Permite buscar pacientes por nome (busca parcial) e visualizar detalhes completos do registro.

#### 4. Exportar para CSV
Gera um arquivo CSV com timestamp contendo todos os registros e campos do banco de dados.

### Armazenamento de Dados

O sistema cria automaticamente um arquivo `formulario_diu.db` na pasta do programa. Este arquivo contém:
- Todos os registros de pacientes
- 73 campos de dados conforme especificado
- Histórico completo com timestamps

**Importante:** Faça backup regular do arquivo `formulario_diu.db` para não perder os dados!

