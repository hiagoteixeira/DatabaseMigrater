from Models.Cliente import Cliente
from modulos.Connection import Connection


class ClienteRepository:

    def __init__(self):

        self.con = Connection()

    def get_by_login(self, login):

        print("Iniciando Busca do Cliente")
        cur = self.con.estoque.cursor()
        cur.execute("select * from cliente where login = %s", (login))
        data_cliente = cur.fetchone()
        cur.close()
        if not data_cliente:
            print("Cliente não encontrado!")
            return None;
        else:
            cliente = Cliente(data_cliente[0], data_cliente[1], data_cliente[2], data_cliente[3], data_cliente[4], data_cliente[5], data_cliente[6])
            print("Cliente ", cliente.nome, " encontrado!")
            return cliente

    def insert(self, data):

        print("Iniciando inserção de cliente!")
        cur = self.con.estoque.cursor()
        print("teste")
        cur.execute("insert into cliente (nome, cpf, email, telefone, status, login) values (%s, %s, %s, %s, %s, %s)", (data[0], data[1], data[2], data[3], data[4], data[5]))
        id_cliente = self.con.estoque.insert_id()
        cur.close()
        cliente = Cliente(id_cliente, data[0], data[1], data[2], data[3], data[4], data[5])
        print("Cliente ", cliente.nome, " inserido!")
        return cliente
