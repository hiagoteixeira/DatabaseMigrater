from modulos.Connection import Connection
from Models.Modelo import Modelo


class ModeloRepository:

    def __init__(self):
        
        self.con = Connection()

    
    def verify(self, param):
        
        modelo = self.get_by_description(param)
        if not modelo:
            return False
        else:
            return True 


    def insert(self, modelo):

        print("Iniciando inserção do Modelo => ", modelo[0])        
        cur = self.con.estoque.cursor()
        cur.execute("insert into modelo (descricao, id_marca) values (%s, %s)", (modelo[0], modelo[1]))
        id_modelo = self.con.estoque.insert_id()
        modelo = Modelo(id_modelo, modelo[0], modelo[1])
        print("Modelo inserido com sucesso!")
        return modelo
    

    def get_by_description(self, param):

        print("Iniciando busca da marca => ", param)
        cur = self.con.estoque.cursor()
        cur.execute("select * from modelo where descricao = %s", (param) )
        data_modelo = cur.fetchone()
        cur.close()
        if not data_modelo:
            print("Modelo não encontrado")
            return None
        else:
            print("Modelo já existe!")
            modelo = Modelo(data_modelo[0], data_modelo[1], data_modelo[2])
            return modelo