from Models import Item
from Modelos import Connection


class ItemRepository:
    def __init__(self):
        self.con = Connection()

    def get_by_serie(self, serie):

        cur = self.con.estoque.cursor()
        cur.execute("select * from item where serie = %s", (serie))
        data_item = cur.fetchone()
        cur.close()
        item = Item(data_item[0], data_item[1], data_item[2], data_item[3], data_item[4], data_item[5], data_item[6], data_item[7], data_item[8])
        return item

    def exists(self, serie):

        item = self.get_by_serie(serie)
        if not item :
            return False
        else :
            return True

    def insert(self, params):

        cur  = self.con.estoque.cursor()
        cur.execute("insert into item (serie, mac, status, id_produtoItem, wifi, senha, login_pppoe, senha_pppoe) values (%s , %s, %s, %s, %s, %s, %s, %s)", (params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7]))
        id_item = cur.insert_id()
        item = Item(id_item, params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7])
        return item
