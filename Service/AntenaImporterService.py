import pymysql
from modulos.Provider import *
from modulos.Connection import Connection
from Repository.MarcaRepository import * 
from Repository.ModeloRepository import * 
from Repository.ProdutoRepository import * 
from Repository.ProdutoItemRepository import * 
from Repository.ItemRepository import * 
from Repository.ClienteRepository import * 


class AntenaImporterService:
    def __init__(self):
        self.con = Connection()
        self.provider = Provider()
        self.marcaRepository = MarcaRepository()  
        self.modeloRepository = ModeloRepository()  
        self.produtoRepository = ProdutoRepository()  
        self.itemRepository = ItemRepository()  
        self.produtoItemRepository = ProdutoItemRepository()  
        self.clienteRepository= ClienteRepository() 
    
    def importar(self):
        try:
            print('Getting antenas.')
            antenas = self.provider.get_antenas()
            for antena in antenas:
                ## Verifying marca antena[3]
                print('Marcas')
                marca = self.marcaRepository.get_by_description(antena[3]) 
                if not marca:
                    print('Inserindo Marcas')
                    marca = self.marcaRepository.insert(antena[3])
                    id_marca = marca.id
                else:
                    print('Marca já Existe!! <===')
                    id_marca = marca.id

                ## VERIFYING MODELO
                print('Modelos')
                modelo = self.modeloRepository.get_by_description(antena[4])
                if not modelo:
                    print('Inserindo Modelo')
                    modelo = self.modeloRepository.insert(antena[4])
                    id_modelo = modelo.id
                else:
                    print('Modelo já Existe <====')
                    id_modelo = modelo.id

                ## VERIFYING PRODUTO
                print('Produtos')
                produto = self.produtoRepository.get_by_modelo(id_modelo)
                if not produto:
                    print('Inserindo Produto')
                    data_produto = (id_modelo, 'UN', antena[9], 0)
                    produto = self.produtoRepository.insert(data_produto)
                    id_produto = produto.id
                else:
                    id_produto = produto.id

                ## GETING ALL ITENS OF THIS PRODUTO -- Itens of default deposit
                print('Listando Itens')
                itens = self.provider.get_itens(id_produto)
                for item in itens:
                    print('Verificando se Item existe')
                    item_exists = self.itemRepository.get_by_serie(item[0])
                    if not item_exists:
                        id_deposito = 2 ## default deposit 
                        print('Dando Certo até aqui <==')
                        data_pitem = (id_produto, id_deposito, 1)
                        print('Inserindo produtoItem')
                        produtoItem = self.produtoItemRepository.insert(data_pitem)
                        ## creating item
                        data_item = (item[0], item[1], 'A', produtoItem.id, item[2], item[3], None, None)
                        print('Inserindo Item')
                        item_new = self.itemRepository.insert(data_item)
                    else:
                        print('Item já existe.')

                ## GEETING ALL ITENS WITH CUSTOMERS
                print('Listando Itens com Cliente')
                itens_customers = self.provider.get_itens_cliente(id_produto)
                for item_customer in itens_customers:
                    print('Verificando se Item existe')
                    item_customer_exists = self.itemRepository.get_by_serie(item_customer[0])
                    if not item_customer_exists:
                        ## verifying if the customer exists
                        print('Verificando se o cliente existe')
                        cliente = self.clienteRepository.get_by_login(item_customer[4])
                        id_cliente = cliente.id

                        if not cliente:
                            print('Inserindo Cliente')
                            cliente_provider = self.provider.get_cliente_by_login(item_customer[4])
                            cliente_new = self.clienteRepository.insert(cliente_provider[0], cliente_provider[1], cliente_provider[2], cliente_provider[3], 'A', cliente_provider[4])
                            id_cliente = cliente_new.id

                        data_pitem = (id_produto, None, 1, id_cliente)
                        print('Inserindo produtoItem')
                        produtoItem = self.produtoItemRepository.insert_cliente(data_pitem)
                        ## creating item
                        print('Inserindo Item')
                        data_item = (item_customer[0], item_customer[1], 'A', produtoItem.id, item_customer[2], item_customer[3], None, None)
                        item_new = self.itemRepository.insert(data_item)

            # self.con.estoque.commit()
            self.con.estoque.rollback()
            print('Processo finalizado com sucesso!')

        except Exception as e:
            self.con.estoque.rollback()
            print("Error during the importation.")
