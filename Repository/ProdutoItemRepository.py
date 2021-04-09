from Models import ProdutoItem
from Modelos import Connection


class ProdutoItem:

    def __init__(self):
        self.con = Connection()
    
    def insert(self, params):
        
        cur = self.con.estoque.cursor()
        cur.execute("insert into produtoItem (id_produto, id_deposito, quantidade, id_cliente) values (%s, %s, %s, %s)", (params[0], params[1] ,params[2], params[3]))
        id_pitem  = cur.insert_id()
        cur.close()
        produtoItem = ProdutoItem(id_pitem, params[0], params[1], params[2], params[3])
        return produtoItem

