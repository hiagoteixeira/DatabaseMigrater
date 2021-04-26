import pymysql
from modulos.Connection import Connection
from Repository.ItemRepository import ItemRepository
from modulos.Provider import Provider

class ItemService:

    def __init__(self):
        self.con = Connection()
        self.itemRepository = ItemRepository()
        self.provider = Provider()

    def fix_pppoe(self):
        try:
            print("Iniciando execução!")
            itens = self.provider.get_all_presets()
            # print(len(itens))
            for item in itens:
                print("Item => ", item)
                print("Iniciando processo de update")
                self.itemRepository.update_pppoe(item)
                print("Item n° serie: ", item[0], " atualizado")

            self.con.estoque.commit()
        except Exception as e:
            self.con.estoque.rollback()
            print("Erro durante a execução!")
