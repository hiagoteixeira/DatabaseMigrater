import pymysql

CATEGORIAS = {}
TECNICOS = {}
CLIENTES = {}

# ========================= CONNECTIONS ====================

def connection_integra():
    return pymysql.connect(user='hiago', password='hwSrr8sC', database='integra', host='10.0.1.26')

def connection_estoque():
    # return pymysql.connect(user='hiago', password='mserv@0704', database='estoque', host='10.0.1.48')
    return pymysql.connect(user='root', password='root', database='estoque', host='172.17.0.1')


# ======================= GETS INTEGRA ==========================

def get_tecnico(con, id):
    cur = con.cursor()
    cur.execute("SELECT nome, id FROM operador WHERE id = %s", (id))
    tecnicos = cur.fetchone()
    cur.close()
    return tecnicos

def get_produtos(con):
    cur = con.cursor()
    cur.execute('SELECT * FROM produto WHERE marca is not null')
    produtos = cur.fetchall()
    cur.close()
    return produtos

def get_itens(con, id_produto):
    cur = con.cursor()
    cur.execute('SELECT * FROM produto_estoque WHERE id_produto = %s', (id_produto))
    itens = cur.fetchall()
    cur.close()
    return itens

def get_cliente(con, adesao):
    cur = con.cursor()
    cur.execute('SELECT cli.id, cli.nome, cli.cpfcnpj, cli.email , ade.login FROM clientes as cli join adesao as ade on ade.cliente = cli.id WHERE ade.status in ("A", "I") and ade.login = %s', (adesao))
    clientes = cur.fetchone()
    cur.close()
    return clientes

def get_adesao(con):
    cur = con.cursor()
    cur.execute('SELECT cliente, login FROM adesao')
    adesao = cur.fetchall()
    cur.close()
    return adesao

def get_fornecedores(con):
    cur = con.cursor()
    cur.execute('SELECT * FROM fornecedor')
    fornecedores = cur.fetchall()
    cur.close()
    return fornecedores

def get_categorias(con):
    cur = con.cursor()
    cur.execute('SELECT * FROM produto_categoria')
    categorias = cur.fetchall()
    cur.close()
    return categorias

def get_categoria(con, id):
    cur = con.cursor()
    cur.execute("SELECT cat.* FROM produto_categoria AS cat JOIN produto as prod ON prod.categoria = cat.id WHERE prod.id = %s", (id))
    categoria = cur.fetchone()
    cur.close()
    return categoria

def get_itens_micron(con, produto):
    cur = con.cursor()
    cur.execute("SELECT pe.serie, pe.mac, pe.wifi, pe.senha, adesao.login, pe.status_produto FROM produto_estoque pe left join (select * from mov_estoque where id in (SELECT max(id) FROM mov_estoque mov group by id_estoque)) mov on mov.id_estoque = pe.id left join adesao_equipamento adesao on adesao.serie = pe.serie where pe.status_produto in ('D') and pe.id_produto = %s", (produto))
    itens_micron = cur.fetchall()
    cur.close()
    return itens_micron

def get_itens_tecnico(con, produto):
    cur = con.cursor()
    cur.execute("SELECT pe.serie, pe.mac, pe.wifi, pe.senha, mov.id_operador, pe.status_produto FROM produto_estoque pe join (select * from mov_estoque where id in (SELECT max(id) FROM mov_estoque mov where id_operador != 0 group by id_estoque)) mov on mov.id_estoque = pe.id where pe.status_produto in ('R') and pe.id_produto = %s", (produto))
    itens_tecnico = cur.fetchall()
    cur.close()
    return itens_tecnico

def get_itens_cliente(con, produto):
    cur = con.cursor()
    cur.execute("SELECT pe.serie, pe.mac, pe.wifi, pe.senha, adesao.login, pe.status_produto FROM produto_estoque pe join adesao_equipamento adesao on adesao.serie = pe.serie where adesao.status = 'A' and adesao.tipo in ('onu', 'roteador-preset') and pe.status_produto in ('U') and pe.id_produto = %s", (produto))
    itens_cliente = cur.fetchall()
    cur.close()
    return itens_cliente

def get_antenas(con):
    cur = con.cursor()
    cur.execute("select * from produto join produto_categoria as cat on cat.id = produto.categoria where categoria = 2 and produto.marca is not null")
    produtos = cur.fetchall()
    cur.close()
    return produtos


## ================== RETONAR PRODUTO EXISTENTE PELO MODELO =================

def get_produto_existente(con, id_modelo):
    cur = con.cursor()
    cur.execute("SELECT * FROM produto where id_modelo = %s", (id_modelo))
    produto = cur.fetchone()
    cur.close()
    return produto

##==================== RETORNA ITEM EXISTENTE ==========================
def get_item_existente(con, serie):
    cur = con.cursor()
    cur.execute("SELECT * FROM item WHERE serie = %s", (serie))
    item = cur.fetchone()
    cur.close()
    return item

## =================== CREATE =================================

def create_tecnico(con, tecnico):
    with con.cursor() as cursor:
        cursor.execute('INSERT INTO deposito (nome, tecnico) VALUES (%s, %s)', (tecnico[0], 1))
        TECNICOS[tecnico[1]] = con.insert_id()

def create_categoria(con, categoria):
    with con.cursor() as cursor:
        cursor.execute('insert into categoria (descricao, controleSerial) values (%s, %s)', (categoria[1], 1 if categoria[2] == 'S' else 0 ))
        CATEGORIAS[categoria[0]] = con.insert_id()

def create_cliente(con, cliente):
    with con.cursor() as cursor:
        cursor.execute("INSERT INTO cliente (nome, cpf, email, login) VALUES (%s, %s, %s, %s)", (cliente[1], cliente[2], cliente[3], cliente[4]))
        CLIENTES[cliente[0]] = con.insert_id()

def create_fornecedores(con, fornecedor):
    with con.cursor() as cursor:
        cursor.execute("INSERT INTO fornecedor (nome, cep, uf, cidade, bairro, endereco, cnpj, site, email, vendedor, empresa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (fornecedor[1], fornecedor[2], fornecedor[3], fornecedor[4], fornecedor[5], fornecedor[6], fornecedor[7], fornecedor[9], fornecedor[10], fornecedor[11], fornecedor[8]))

# ========================== CREATE PRODUTO COM SEUS RELACIONAMENTOS ===================

def create_produtos(con, con_integra, produto):
    with con.cursor() as cursor:
        print('Inicio')
        #CADASTRANDO MARCA
        print('========== MARCA ==========')
        print(produto[3])

        cursor.execute("SELECT * FROM marca WHERE descricao = %s", (produto[3]))
        marca = cursor.fetchone()
        if not marca:
            cursor.execute("INSERT INTO marca (descricao) VALUES (%s)", (produto[3]))
            id_marca = con.insert_id()
        else:
            id_marca = marca[0]

        #CADASTRANDO MODELO
        print('========== MODELO =========')
        print(produto[4])
        cursor.execute("SELECT * FROM modelo WHERE descricao = %s", (produto[4]))
        modelo = cursor.fetchone()
        if not modelo:
            cursor.execute("INSERT INTO modelo (descricao, id_marca) VALUES (%s, %s)", (produto[4], id_marca))
            id_modelo = con.insert_id()
        else:
            id_modelo = modelo[0]
        
        print ('ID MARCA', id_marca)
        print ('ID MODELO : ', id_modelo)

        #CADASTRANDO CATEGORIA
        id_categoria = 0
        if produto[14] in CATEGORIAS:
            id_categoria = CATEGORIAS[produto[14]]
        else:
            categoria = get_categoria(con_integra, produto[0])
            create_categoria(con, categoria)
            id_categoria = CATEGORIAS[categoria[0]]

        # VERIFICA SE O PRODUTO JA EXISTE
        produto_existente = get_produto_existente(con, id_modelo)
        if produto_existente is None:
            #CADASTRANDO PRODUTO
            print('======= PRODUTO Não Existente =======')
            cursor.execute("INSERT INTO produto (id_modelo, unidade, preco, estoqueMin, id_categoria, venda, frequencia, limite_velocidade, velocidade_minima) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (id_modelo, produto[5], produto[9], produto    [11], id_categoria, 0 ,produto[16], produto[17], produto[18]))
            id_produto = con.insert_id()
        else:
            print('======= PRODUTO já Existente =======')
            id_produto = produto_existente[0]
       
        #CADASTRANDO ITENS

        #NA MICRON
        print('======== ITEM ===========')
        itens_micron = get_itens_micron(con_integra, produto[0])
        for item_micron in itens_micron:
            #Verifica se o item já existe no estoque
            item_existente = get_item_existente(con, item_micron[0])
            if item_existente is None:
                # CRIANDO PRODUTO ITEM
                cursor.execute("insert into produtoItem (id_produto, id_deposito, quantidade) values (%s, %s, 1)", (id_produto, 2))
                id_pitem = con.insert_id()
                # CRIANDO ITEM
                cursor.execute("insert into item (serie, mac, wifi, senha, id_produtoItem) values (%s, %s, %s, %s, %s)", (item_micron[0], item_micron[1], item_micron[2], item_micron[3], id_pitem))
            else:
                print("Item já existe no estoque.")

        #COM CLIENTES
        print('======== COM CLIENTE ===========')
        itens_cliente = get_itens_cliente(con_integra, produto[0])
        for item_cliente in itens_cliente:
           
            print('======== ITEM CLIENTE ============')
            print(item_cliente)
            cliente_integra = get_cliente(con_integra, item_cliente[4])
            print('======>', cliente_integra, 'Login cliente ===>', item_cliente[4])
            id_cliente_integra = cliente_integra[0]
            print('============ CRIA CLIENTE ============ ')
            if id_cliente_integra in CLIENTES:
                id_cliente = CLIENTES[id_cliente_integra]
            else:
                create_cliente(con, cliente_integra)
                id_cliente = CLIENTES[id_cliente_integra]

            #Verifica se o item já existe no estoque
            item_existente = get_item_existente(con, item_cliente[0])
            if item_existente is None:
                # CRIANDO PITEM
                cursor.execute("insert into produtoItem (id_produto, id_cliente, quantidade) values (%s, %s, 1)", (id_produto, id_cliente))
                id_pitem = con.insert_id()
                print('============== ID DO PRODUTO ITEM ==========')
                print('id do produto Item : ',id_pitem)
                # CRIANDO ITEM
                cursor.execute("insert into item (serie, mac, wifi, senha, id_produtoItem) values (%s, %s, %s, %s, %s)", (item_cliente[0], item_cliente[1], item_cliente[2], item_cliente[3], id_pitem))
            else:
                print("Item já existe no estoque.")

        #COM TECNICO
        print('======== COM TECNICO =========== ')
        itens_tecnico = get_itens_tecnico(con_integra, produto[0])
        print('=========== ITENS COM TECNICO ============')
        print(itens_tecnico)
        for item_tecnico in itens_tecnico:
            id_tecnico = 0
            print('=========== ITEM TECNICO ============ ')
            print(item_tecnico)
            if item_tecnico[4] in TECNICOS:
                id_tecnico = TECNICOS[item_tecnico[4]]
            else:
                print('=============== ELSE TECNICO ==========')
                tecnico = get_tecnico(con_integra, item_tecnico[4])
                print('==========> :', tecnico, '===========>' ,item_tecnico[4])
                create_tecnico(con, tecnico)
                id_tecnico = TECNICOS[item_tecnico[4]]
            #Verifica se o item já existe no estoque
            item_existente = get_item_existente(con, item_tecnico[0])
            if item_existente is None:
                # CRIANDO PITEM
                print(id_produto, id_tecnico)
                cursor.execute("insert into produtoItem (id_produto, id_deposito, quantidade) values (%s, %s, 1)", (id_produto, id_tecnico))
                id_pitem = con.insert_id()
                # CRIANDO ITEM
                cursor.execute("insert into item (serie, mac, wifi, senha, id_produtoItem) values (%s, %s, %s, %s, %s)", (item_tecnico[0], item_tecnico[1], item_tecnico[2], item_tecnico[3], id_pitem))
            else:
                print("Item já existe no estoque.")

# ====================== MAIN =============================

def main():
    con_integra = connection_integra()
    con_estoque = connection_estoque()

    try:
      
        #========== CADASTRANDO FORNECEDORES ============
        list_fornecedores = get_fornecedores(con_integra)
        for fornecedor in list_fornecedores:
            create_fornecedores(con_estoque, fornecedor)
        #=========== CADASTRO DE PRODUTOS ============
        list_produto = get_antenas(con_integra)
        for produto in list_produto:
            create_produtos(con_estoque,con_integra, produto)
       
   
    
        # con_estoque.commit()
        con_estoque.rollback()
    
    except Exception as e:
        con_estoque.rollback()
        print('ERRO DE NOVO NESSA PORRA!')
        print(e)
    con_integra.close()
    con_estoque.close()

main()


