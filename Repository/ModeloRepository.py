from modulos import Connection
from Models import Modelo


class ModeloRepository:

    def __init__(self):
        
        self.con = Connection()

    
    def verify(self, param):
        
        modelo = self.get_by_description(param)
        if not modelo:
            return False
        else
            return True 


    def insert(self, modelo):
        
        cur = self.con.estoque.cursor()
        cur.execute("insert into modelo (descricao, id_marca) values (%s, %s)", (modelo[0], modelo[1]))
        id_modelo = cur.insert_id()
        modelo = Modelo(id_modelo, modelo[0], modelo[1])
        return id_modelo
    

    def get_by_description(self, param):

        cur = self.con.estoque.cursor()
        cur.execute("select * from modelo where descricao = %s", (param) )
        data_modelo = cur.fetchone()
        cur.close()
        modelo = Modelo(data_modelo[0], data_modelo[1], data_modelo[2])
        return modelo