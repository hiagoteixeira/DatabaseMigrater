import pymysql


CACHE_CON = {}

class Connection:
    def __init__(self):
        if 'integra' in CACHE_CON:
            self.integra = CACHE_CON['integra']
        else:
            self.integra = self.connection_integra()
            CACHE_CON['integra'] = self.integra

        if 'estoque' in CACHE_CON:
            self.estoque = CACHE_CON['estoque']
        else:
            self.estoque = self.connection_estoque()

            CACHE_CON['estoque'] = self.estoque

            
    def connection_integra(self):
        return pymysql.connect(user='', password='',database='', host='')


    def connection_estoque(self):
        # return pymysql.connect(user='hiago', password='mserv@0704', database='estoque', host='10.0.1.48')
        return pymysql.connect(user='root', password='root', database='estoque', host='172.17.0.1')
