from . import Connection
from Models import Marca

class MarcaRepository:
    def __init__(self):
        
        self.con = Connection()


    def verify(self, description):

        result = self.get_by_description(description)
        if not result:
            return False
        else 
            return True


    def insert(self, param):

        cur = self.con.estoque.cursor()
        cur.execute("insert into marca (descricao) values (%s)", (param))
        id_marca = cur.insert_id()
        marca  = Marca(id_marca, param[0])
        return marca

    def get_by_description(self, description):

        cur = self.con.estoque.cursor()
        cur.execute("select * from marca where descricao = %s", (description) )
        data_marca = cur.fetchone()
        cur.close()
        marca = Marca(data_marca[0], data_marca[1])
        return marca