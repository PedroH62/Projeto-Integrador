from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
DB_CONFIG = {
'host': 'localhost',
'database': 'mybd',
'user':'root', 
'password': '11052003' 
}

def conectar_db():
    """Função para conectar ao banco de dados MySQL."""
    try:
        mydb = mysql.connector.connect(**DB_CONFIG)
        return mydb
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        return None

@app.route("/", methods=["GET"])
def index():
    return render_template("ferramenta.html")

@app.route("/ferramenta", methods=["POST"])
def ferramenta():
    mydb = conectar_db()
    if mydb is None:
        print("Erro: Não foi possível conectar ao banco de dados dentro da função ferramenta()")
        return jsonify({"erro": "Não foi possível conectar ao banco de dados."}), 500
    cursor = mydb.cursor()

    print("Rota /ferramenta acessada (POST)")

    nome = request.form.get("nome")
    profissao = request.form.get("profissao")
    estado_civil = request.form.get("estado_civil")
    nacionalidade = request.form.get("nacionalidade")
    rg = request.form.get("rg")
    uf = request.form.get("uf")
    cpf = request.form.get("cpf")
    cep = request.form.get("cep")
    cidade = request.form.get("cidade")
    endereco = request.form.get("endereco")
    numero = request.form.get("numero")
    bairro = request.form.get("bairro")
    complemento = request.form.get("complemento")
    telefone = request.form.get("telefone")
    email = request.form.get("email")
    objeto_acao = request.form.get("objeto_acao")
    honorario = request.form.get("honorario")
    testemunha1 = request.form.get("testemunha1")
    testemunha2 = request.form.get("testemunha2")
    valor_causa = request.form.get("valor_causa")
    valor_extenso = request.form.get("valor_extenso")
    passivo_nome = request.form.get("passivo_nome")
    passivo_profissao = request.form.get("passivo_profissao")
    passivo_estado_civil = request.form.get("passivo_estado_civil")
    passivo_nacionalidade = request.form.get("passivo_nacionalidade")
    passivo_rg_uf = request.form.get("passivo_rg_uf")
    passivo_cpf_cnpj = request.form.get("passivo_cpf_cnpj")
    passivo_cidade = request.form.get("passivo_cidade")
    passivo_endereco = request.form.get("passivo_endereco")
    numero_autos = request.form.get("numero_autos")
    forma_pagamento = request.form.get("forma_pagamento")
    percentual_penhora = request.form.get("percentual_penhora")
    vara = request.form.get("vara")
    comarca = request.form.get("comarca")
    estado = request.form.get("estado")
    especialidade = request.form.get("especialidade")
    senha_gov_br = request.form.get("senha_gov_br")
    honorario_extenso = request.form.get("honorario_extenso")

    print(f"Dados do formulário recebidos: Nome={nome}, CPF={cpf}, Email={email}, ... (verifique o terminal para todos os campos)")

    residencia_id = None
    if cep and cidade and endereco and numero and bairro:
        sql_residencia = """INSERT INTO `Dados de Residência`
                                    (CEP, Cidade, Endereco, Numero, Bairro, Complemento)
                                    VALUES (%s, %s, %s, %s, %s, %s)"""
        val_residencia = (cep, cidade, endereco, numero, bairro, complemento)
        try:
            cursor.execute(sql_residencia, val_residencia)
            mydb.commit()
            residencia_id = cursor.lastrowid
            print(f"ID de Residência inserido: {residencia_id}")
        except mysql.connector.Error as err:
            print(f"Erro ao inserir em Dados de Residência: {err}")
            mydb.rollback()
            residencia_id = None
    else:
        print("Dados de residência incompletos, ID de residência será None")

    cliente_id = cpf  # Usando o CPF como ID

    sql_atualiza_cliente = "UPDATE `Dados do Cliente` SET Indice = %s WHERE RG_CPF = %s"
    val_atualiza_cliente = (residencia_id, cliente_id)
    print(f"Tentando atualizar Dados do Cliente com Indice: {residencia_id}, CPF: {cliente_id}")
    try:
        cursor.execute(sql_atualiza_cliente, val_atualiza_cliente)
        mydb.commit()
        print("Dados do Cliente atualizados com o Indice de Residência")
    except mysql.connector.Error as err:
        print(f"Erro ao atualizar Dados do Cliente com Indice: {err}")
        mydb.rollback()

    sql_cliente = """INSERT INTO `Dados do Cliente`
                                (NomeCliente, RG_CPF, Email, Profissao, EstadoCivil, Nacionalidade, Telefone)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    val_cliente = (nome, cpf, email, profissao, estado_civil, nacionalidade, telefone)
    print(f"Tentando inserir em Dados do Cliente: {val_cliente}")
    try:
        cursor.execute(sql_cliente, val_cliente)
        mydb.commit()
        print("Dados do Cliente inseridos")
    except mysql.connector.Error as err:
        print(f"Erro ao inserir em Dados do Cliente: {err}")
        mydb.rollback()

    sql_causa = """INSERT INTO Causa
                                (Dados_do_Cliente_RG_CPF_MECH, Objeto_Acao, Numero_dos_Autos, Testemunha1,
                                 Testemunha2, Passivo_Nome, Passivo_Profissao, Passivo_Estado_Civil,
                                 Passivo_Nacionalidade, Passivo_RG_UF, Passivo_CPF_CNPJ, Passivo_Cidade,
                                 Passivo_Endereco, Valor_da_Causa, Valor_por_extenso, Forma_de_Pagamento,
                                 Percentual_Penhora, Vara, Comarca, Estado, Especialidade, Honorario, Honorario_Extenso)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    val_causa = (cliente_id, objeto_acao, numero_autos, testemunha1, testemunha2, passivo_nome,
                  passivo_profissao, passivo_estado_civil, passivo_nacionalidade, passivo_rg_uf,
                  passivo_cpf_cnpj, passivo_cidade, passivo_endereco, valor_causa, valor_extenso,
                  forma_pagamento, percentual_penhora, vara, comarca, estado, especialidade,
                  honorario, honorario_extenso)
    print(f"Tentando inserir em Causa: {val_causa}")
    try:
        cursor.execute(sql_causa, val_causa)
        mydb.commit()
        print("Dados da Causa inseridos")
        return jsonify({"mensagem": "Cliente cadastrado com sucesso!"}), 201
    except mysql.connector.Error as err:
        print(f"Erro ao inserir em Causa: {err}")
        mydb.rollback()
        return jsonify({"erro": f"Erro ao cadastrar cliente: {err}"}), 500
    finally:
        if mydb and mydb.is_connected():
            cursor.close()
            mydb.close()
            print("Conexão com o banco de dados fechada")

@app.route("/buscar_cliente", methods=["POST"])
def buscar_cliente():
    print("A função buscar_cliente() foi acessada!")
    cpf_busca = request.form.get("cpf")
    if not cpf_busca:
        return jsonify({"erro": "CPF não fornecido."}), 400

    mydb = conectar_db()
    if mydb is None:
        return jsonify({"erro": "Não foi possível conectar ao banco de dados."}), 500
    cursor = mydb.cursor()

    try:
        sql = """SELECT dc.NomeCliente, dc.RG_CPF, dc.Email, dc.Profissao, dc.EstadoCivil,
                  dc.Nacionalidade, dc.Telefone, dr.CEP, dr.Cidade, dr.Endereco, dr.Numero,
                  dr.Bairro, dr.Complemento
                  FROM `Dados do Cliente` dc
                  LEFT JOIN `Dados de Residência` dr ON dc.Indice = dr.id
                  WHERE dc.RG_CPF = %s"""
        cursor.execute(sql, (cpf_busca,))
        resultado = cursor.fetchone()

        if resultado:
            cliente = {
                "Nome": resultado[0],
                "RG/CPF": resultado[1],
                "Email": resultado[2],
                "Profissão": resultado[3],
                "Estado Civil": resultado[4],
                "Nacionalidade": resultado[5],
                "Telefone": resultado[6],
                "CEP": resultado[7],
                "Cidade": resultado[8],
                "Endereço": resultado[9],
                "Número": resultado[10],
                "Bairro": resultado[11],
                "Complemento": resultado[12]
            }
            return jsonify(cliente), 200
        else:
            return jsonify({"erro": "Cliente não encontrado."}), 404

    except mysql.connector.Error as err:
        return jsonify({"erro": f"Erro ao buscar cliente: {err}"}), 500
    finally:
        if mydb and mydb.is_connected():
            cursor.close()
            mydb.close()

if __name__ == '__main__':
    app.run(debug=True, port=5001)