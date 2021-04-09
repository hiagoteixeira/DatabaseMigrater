import pymysql


class Connection:
    def __init__(self):
        self.estoque = self.connection_estoque()
        self.integra = self.connection_integra()

    def connection_integra(self):
        return pymysql.connect(user='hiago', password='hwSrr8sC',database='integra', host='10.0.1.26')


    def connection_estoque(self):
        # return pymysql.connect(user='hiago', password='mserv@0704', database='estoque', host='10.0.1.48')
        return pymysql.connect(user='root', password='root', database='estoque', host='172.17.0.1')
