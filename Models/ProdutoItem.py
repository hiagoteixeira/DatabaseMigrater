class ProdutoItem :


    def __init__ (self, id, id_produto, quantidade, id_deposito=None, id_cliente=None) :
        
        self.id = id
        self.id_produto = id_produto
        self.id_deposito = id_deposito
        self.quantidade = quantidade
        self.id_cliente = id_cliente
