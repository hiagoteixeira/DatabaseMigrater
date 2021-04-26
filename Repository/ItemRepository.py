from Models.Item import Item
from modulos.Connection import Connection


class ItemRepository:
    def __init__(self):
        self.con = Connection()

    def get_by_serie(self, serie):
        print('Iniciando busca de item')
        cur = self.con.estoque.cursor()
        cur.execute("select * from item where serie = %s", (serie))
        data_item = cur.fetchone()
        cur.close()
        if not data_item:
            (print('Item nao encontrado!'))
            return data_item
        else:
            print('Item Existente => ', data_item)
            item = Item(data_item[0], data_item[1], data_item[2], data_item[3], data_item[4], data_item[5], data_item[6], data_item[7], data_item[8])
            return item

    def exists(self, serie):

        item = self.get_by_serie(serie)
        if not item :
            return False
        else:
            return True

    def insert(self, params):

        print('Inserindo item Serie => ', params[0])
        cur  = self.con.estoque.cursor()
        cur.execute("insert into item (serie, mac, status, id_produtoItem, wifi, senha, login_pppoe, senha_pppoe) values (%s , %s, %s, %s, %s, %s, %s, %s)", (params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7]))
        id_item = self.con.estoque.insert_id()
        item = Item(id_item, params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7])
        return item
    
    def update_pppoe(self, item):
        cur = self.con.estoque.cursor()
        print("Executando Query.")
        cur.execute("update item set login_pppoe = %s, senha_pppoe = %s where serie = %s", (item[1], item[2], item[0]))
        print("Item n° Serie: ", item[0], " atualizado.")
        cur.close()
        return 