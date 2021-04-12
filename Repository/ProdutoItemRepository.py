from Models.ProdutoItem import ProdutoItem
from modulos.Connection import Connection


class ProdutoItemRepository:

    def __init__(self):
        self.con = Connection()
    
    def insert(self, params):
        print('Inicio da inserção der ProdutoItem <==')
        cur = self.con.estoque.cursor()
        print(params)
        cur.execute("insert into produtoItem (id_produto, id_deposito, quantidade) values (%s, %s, %s)", (params[0], params[1] ,params[2]))
        id_pitem  = self.con.estoque.insert_id()
        print('id do ProdutoItem => ', id_pitem)
        cur.close()
        produtoItem = ProdutoItem(id = id_pitem, id_produto = params[0], id_deposito = params[1], quantidade = params[2])
        return produtoItem

    def insert_cliente(self, params):

        print('Inicio da inserção der ProdutoItem com Cliente <==')
        cur = self.con.estoque.cursor()
        print(params)
        cur.execute("insert into produtoItem (id_produto, quantidade, id_cliente) values (%s, %s, %s)", (params[0], params[2], params[3]))
        id_pitem  = self.con.estoque.insert_id()
        cur.close()
        produtoItem = ProdutoItem(id = id_pitem, id_produto = params[0], quantidade = params[2], id_cliente = params[3])
        return produtoItem