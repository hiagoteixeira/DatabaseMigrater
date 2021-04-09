from Models import Produto
from modulos import Connection


class ProdutoRepository:

    def __init__ (self):
        
        self.con = Connection()

    
    def get_by_modelo (self, id_modelo):

        cur = self.con.estoque.cursor()
        cur.execute("select * from  produto where id_modelo = %s", (id_modelo))
        data_produto = cur.fetchone();
        cur.close()
        produto = Produto(data_produto[0], data_produto[1],data_produto[2],data_produto[3],data_produto[4],data_produto[5],data_produto[6],data_produto[7],data_produto[8],data_produto[9],data_produto[10],data_produto[11])
        return produto

    
    def exists (self, id_modelo):

        produto = self.get_by_modelo(id_modelo)
        if not produto:
            return False
        else:
            return True

    def insert (self, params):

        cur = self.con.estoque.cursor()
        cur.execute("insert into produto (id_modelo, unidade, preco, estoqueMin, id_categoria, status, venda, preco_venda, frequencia, limite_velocidade, velocidade_minima) value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], params[9],params[10]))
        id_produto = cur.insert_id()
        produto = Produto(id_produto, params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], params[9],params[10])
        return produto

