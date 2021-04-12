from modulos.Connection import Connection
from Models.Marca import Marca

class MarcaRepository:
    def __init__(self):
        
        self.con = Connection()


    def verify(self, description):

        result = self.get_by_description(description)
        if not result:
            return False
        else:
            return True


    def insert(self, param):

        cur = self.con.estoque.cursor()
        cur.execute("insert into marca (descricao) values (%s)", (param))
        id_marca = cur.insert_id()
        marca  = Marca(id_marca, param[0])
        return marca

    def get_by_description(self, description):
        print('Iniciando busca da marca pela descricao')
        cur = self.con.estoque.cursor()
        cur.execute("select * from marca where descricao = %s", (description) )
        data_marca = cur.fetchone()
        cur.close()
        print('data_marca ==>', data_marca)
        marca = Marca(data_marca[0], data_marca[1])
        print(marca)
        return marca