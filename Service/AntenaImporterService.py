import pymysql
from modulos import Provider
from Repository import MarcaRepository, ModeloRepository, ProdutoRepository, ItemRepository, ProdutoItemRepository, ClienteRepository


class AntenaImporterService:
    def __init__(self):
        pass
    
    
    def importar(self):
        try:
            antenas = model_antena.get_antenas()
            for antena in antenas:
                ## Verifying marca antena[3]
                marca = MarcaRepository.get_by_description(antena[3]) 
                if not marca:
                    marca = MarcaRepository.insert(antena[3])
                    id_marca = marca.id
                else:
                    id_marca = marca.id

                ## VERIFYING MODELO
                modelo = ModeloRepository.get_by_description(antena[4])
                if not modelo:
                    modelo = ModeloRepository.insert(antena[4])
                    id_modelo = modelo.id
                else:
                    id_modelo = modelo.id

                ## VERIFYING PRODUTO
                produto = ProdutoRepository.get_by_modelo(id_modelo)
                if not produto:
                    data_produto = (id_modelo, 'UN', antena[9], 0)
                    produto = ProdutoRepository.insert(data_produto)
                    id_produto = produto.id
                else:
                    id_produto = produto.id

                ## GETING ALL ITENS OF THIS PRODUTO -- Itens of default deposit
                itens = Provider.get_itens(id_produto)
                for item in itens:
                    item_exists = ItemRepository.get_by_serie(item[0])
                    if not item_exists:
                        id_deposito = 2 ## default deposit 
                        data_pitem = (id_produto, id_deposito, 1, null)
                        produtoItem = ProdutoItemRepository.insert(data_pitem)
                        ## creating item
                        data_item = (item[0], item[1], 'A', produtoItem.id, item[2], item[3], null, null)
                        item_new = ItemRepository.insert(data_item)
                    else:
                        print('Item já existe.')

                ## GEETING ALL ITENS WITH CUSTOMERS
                itens_customers = Provider.get_itens_cliente(id_produto)
                for item_customer in itens_customers:
                    item_customer_exists = ItemRepository.get_by_serie(item_customer[0])
                    if not item_customer_exists:
                        ## verifying if the customer exists
                        cliente = ClienteRepository.get_by_login(item_customer[4])
                        id_cliente = cliente.id

                        if not cliente:
                            cliente_provider = Provider.get_cliente_by_login(item_customer[4])
                            cliente_new = ClienteRepository.insert(cliente_provider[0], cliente_provider[1], cliente_provider[2], cliente_provider[3], 'A', cliente_provider[4])
                            id_cliente = cliente_new.id

                        data_pitem = (id_produto, null, 1, id_cliente)
                        produtoItem = ProdutoItemRepository.insert(data_pitem)
                        ## creating item
                        data_item = (item_customer[0], item_customer[1], 'A', produtoItem.id, item_customer[2], item_customer[3], null, null)
                        item_new = ItemRepository.insert(data_item)

            self.con.estoque.commit()

        except Exception as e:
            self.con.estoque.rollback()
            print("Error during the importation.")
