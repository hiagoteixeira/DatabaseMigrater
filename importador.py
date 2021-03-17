import pymysql

CATEGORIAS = {}
TECNICOS = {}
CLIENTES = {}

# ========================= CONNECTIONS ====================

def connection_origem():
    return pymysql.connect(user='usuario_origem', password='senha_origem', database='database_origem', host='host_origem')

def connection_destino():
    return pymysql.connect(user='user_destino', password='senha_destino', database='database_destino', host='host_destino')

# ======================= GETS INTEGRA ==========================

def get_tecnico(con_origem, id):
    cur = con_origem.cursor()
    cur.execute("SELECT nome, id FROM operador WHERE id = %s", (id))
    tecnicos = cur.fetchone()
    cur.close()
    return tecnicos

def get_produtos(con_origem):
    cur = con_origem.cursor()
    cur.execute('SELECT * FROM produto WHERE marca is not null')
    produtos = cur.fetchall()
    cur.close()
    return produtos

def get_itens(con_origem, id_produto):
    cur = con_origem.cursor()
    cur.execute('SELECT * FROM produto_estoque WHERE id_produto = %s', (id_produto))
    itens = cur.fetchall()
    cur.close()
    return itens

def get_cliente(con_origem, adesao):
    cur = con_origem.cursor()
    cur.execute('SELECT cli.id, cli.nome, cli.cpfcnpj, cli.email , ade.login FROM clientes as cli join adesao as ade on ade.cliente = cli.id WHERE ade.status in ("A", "I") and ade.login = %s', (adesao))
    clientes = cur.fetchone()
    cur.close()
    return clientes

def get_adesao(con_origem):
    cur = con_origem.cursor()
    cur.execute('SELECT cliente, login FROM adesao')
    adesao = cur.fetchall()
    cur.close()
    return adesao

def get_fornecedores(con_origem):
    cur = con_origem.cursor()
    cur.execute('SELECT * FROM fornecedor')
    fornecedores = cur.fetchall()
    cur.close()
    return fornecedores

def get_categorias(con_origem):
    cur = con_origem.cursor()
    cur.execute('SELECT * FROM produto_categoria')
    categorias = cur.fetchall()
    cur.close()
    return categorias

def get_categoria(con_origem, id):
    cur = con_origem.cursor()
    cur.execute("SELECT cat.* FROM produto_categoria AS cat JOIN produto as prod ON prod.categoria = cat.id WHERE prod.id = %s", (id))
    categoria = cur.fetchone()
    cur.close()
    return categoria

def get_itens_deposito(con_origem, produto):
    cur = con_origem.cursor()
    cur.execute("SELECT pe.serie, pe.mac, pe.wifi, pe.senha, adesao.login, pe.status_produto FROM produto_estoque pe left join (select * from mov_estoque where id in (SELECT max(id) FROM mov_estoque mov group by id_estoque)) mov on mov.id_estoque = pe.id left join adesao_equipamento adesao on adesao.serie = pe.serie where pe.status_produto in ('D') and pe.id_produto = %s", (produto))
    itens_deposito = cur.fetchall()
    cur.close()
    return itens_deposito

def get_itens_tecnico(con_origem, produto):
    cur = con_origem.cursor()
    cur.execute("SELECT pe.serie, pe.mac, pe.wifi, pe.senha, mov.id_operador, pe.status_produto FROM produto_estoque pe join (select * from mov_estoque where id in (SELECT max(id) FROM mov_estoque mov where id_operador != 0 group by id_estoque)) mov on mov.id_estoque = pe.id where pe.status_produto in ('R') and pe.id_produto = %s", (produto))
    itens_tecnico = cur.fetchall()
    cur.close()
    return itens_tecnico

def get_itens_cliente(con_origem, produto):
    cur = con_origem.cursor()
    cur.execute("SELECT pe.serie, pe.mac, pe.wifi, pe.senha, adesao.login, pe.status_produto FROM produto_estoque pe join adesao_equipamento adesao on adesao.serie = pe.serie where adesao.status = 'A' and adesao.tipo in ('onu', 'roteador-preset') and pe.status_produto in ('U') and pe.id_produto = %s", (produto))
    itens_cliente = cur.fetchall()
    cur.close()
    return itens_cliente

## =================== CREATE =================================

def create_tecnico(con_destino, tecnico):
    with con_destino.cursor() as cursor:
        cursor.execute('INSERT INTO deposito (nome, tecnico) VALUES (%s, %s)', (tecnico[0], 1))
        TECNICOS[tecnico[1]] = con_destino.insert_id()

def create_categoria(con_destino, categoria):
    with con_destino.cursor() as cursor:
        cursor.execute('insert into categoria (descricao, controleSerial) values (%s, %s)', (categoria[1], 1 if categoria[2] == 'S' else 0 ))
        CATEGORIAS[categoria[0]] = con_destino.insert_id()

def create_cliente(con_destino, cliente):
    with con_destino.cursor() as cursor:
        cursor.execute("INSERT INTO cliente (nome, cpf, email, login) VALUES (%s, %s, %s, %s)", (cliente[1], cliente[2], cliente[3], cliente[4]))
        CLIENTES[cliente[0]] = con_destino.insert_id()

def create_fornecedores(con_destino, fornecedor):
    with con_destino.cursor() as cursor:
        cursor.execute("INSERT INTO fornecedor (nome, cep, uf, cidade, bairro, endereco, cnpj, site, email, vendedor, empresa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (fornecedor[1], fornecedor[2], fornecedor[3], fornecedor[4], fornecedor[5], fornecedor[6], fornecedor[7], fornecedor[9], fornecedor[10], fornecedor[11], fornecedor[8]))

# ========================== CREATE PRODUTO COM SEUS RELACIONAMENTOS ===================

def create_produtos(con_destino, con_origem, produto):
    with con_destino.cursor() as cursor:
        #CADASTRANDO MARCA
        cursor.execute("SELECT * FROM marca WHERE descricao = %s", (produto[2]))
        marca = cursor.fetchone()
        if not marca:
            cursor.execute("INSERT INTO marca (descricao) VALUES (%s)", (produto[2]))
            id_marca = con_destino.insert_id()
        else:
            id_marca = marca[0]

        #CADASTRANDO MODELO
        print('========== MODELO =========')
        print(produto[3])
        cursor.execute("SELECT * FROM modelo WHERE descricao = %s", (produto[3]))
        modelo = cursor.fetchone()
        if not modelo:
            cursor.execute("INSERT INTO modelo (descricao, id_marca) VALUES (%s, %s)", (produto[3], id_marca))
            id_modelo = con_destino.insert_id()
        else:
            id_modelo = modelo[0]

        #CADASTRANDO CATEGORIA
        id_categoria = 0
        if produto[13] in CATEGORIAS:
            id_categoria = CATEGORIAS[produto[13]]
        else:
            categoria = get_categoria(con_origem, produto[0])
            create_categoria(con_destino, categoria)
            id_categoria = CATEGORIAS[categoria[0]]

        #CADASTRANDO PRODUTO
        cursor.execute("INSERT INTO produto (id_modelo, unidade, preco, estoqueMin, id_categoria, venda, frequencia, limite_velocidade, velocidade_minima) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (id_modelo, produto[4], produto[8], produto[10], id_categoria, 0 ,produto[15], produto[16], produto[17]))
        id_produto = con_destino.insert_id()
       
        #CADASTRANDO ITENS

        #NO DEPOSITO
        itens_deposito = get_itens_deposito(con_origem, produto[0])
        for item_deposito in itens_deposito:
            # CRIANDO PRODUTO ITEM
            cursor.execute("insert into produtoItem (id_produto, id_deposito, quantidade) values (%s, %s, 1)", (id_produto, 2))
            id_pitem = con_destino.insert_id()
            # CRIANDO ITEM
            cursor.execute("insert into item (serie, mac, wifi, senha, id_produtoItem) values (%s, %s, %s, %s, %s)", (item_deposito[0], item_deposito[1], item_deposito[2], item_deposito[3], id_pitem))

        #COM CLIENTES
        itens_cliente = get_itens_cliente(con_origem, produto[0])
        for item_cliente in itens_cliente:
            cliente_origem = get_cliente(con_origem, item_cliente[4])
            id_cliente_origem = cliente_origem[0]
            if id_cliente_origem in CLIENTES:
                id_cliente = CLIENTES[id_cliente_origem]
            else:
                create_cliente(con_destino, cliente_origem)
                id_cliente = CLIENTES[id_cliente_origem]
            # CRIANDO PITEM
            cursor.execute("insert into produtoItem (id_produto, id_cliente, quantidade) values (%s, %s, 1)", (id_produto, id_cliente))
            id_pitem = con_destino.insert_id()
            # CRIANDO ITEM
            cursor.execute("insert into item (serie, mac, wifi, senha, id_produtoItem) values (%s, %s, %s, %s, %s)", (item_cliente[0], item_cliente[1], item_cliente[2], item_cliente[3], id_pitem))

        #COM TECNICO
        itens_tecnico = get_itens_tecnico(con_origem, produto[0])
        for item_tecnico in itens_tecnico:
            id_tecnico = 0
            if item_tecnico[4] in TECNICOS:
                id_tecnico = TECNICOS[item_tecnico[4]]
            else:
                tecnico = get_tecnico(con_origem, item_tecnico[4])
                create_tecnico(con_destino, tecnico)
                id_tecnico = TECNICOS[item_tecnico[4]]
            # CRIANDO PITEM
            cursor.execute("insert into produtoItem (id_produto, id_deposito, quantidade) values (%s, %s, 1)", (id_produto, id_tecnico))
            id_pitem = con_destino.insert_id()
            # CRIANDO ITEM
            cursor.execute("insert into item (serie, mac, wifi, senha, id_produtoItem) values (%s, %s, %s, %s, %s)", (item_tecnico[0], item_tecnico[1], item_tecnico[2], item_tecnico[3], id_pitem))
                
                

# ====================== MAIN =============================

def main():
    con_origem = connection_origem()
    con_destino = connection_destino()

    try:
      
        #========== CADASTRANDO FORNECEDORES ============
        list_fornecedores = get_fornecedores(con_origem)
        for fornecedor in list_fornecedores:
            create_fornecedores(con_destino, fornecedor)
        #=========== CADASTRO DE PRODUTOS ============
        list_produto = get_produtos(con_origem)
        for produto in list_produto:
            create_produtos(con_destino,con_origem, produto)
       
   
    
        con_destino.commit()
        # con_destino.rollback()
    
    except Exception as e:
        con_destino.rollback()
    con_origem.close()
    con_destino.close()

main()


