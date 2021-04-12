from . import Connection


class Provider:
    def __init__(self):
        self.con = Connection()


    def get_antenas(self):
        cur = self.con.integra.cursor()
        cur.execute("select * from produto join produto_categoria as cat on cat.id = produto.categoria where categoria = 2 and produto.marca is not null")
        produtos = cur.fetchall()
        cur.close()
        return produtos
    

    def get_itens(self, id_produto):

        cur = self.con.integra.cursor()
        cur.execute("SELECT pe.serie, pe.mac, pe.wifi, pe.senha, adesao.login, pe.status_produto FROM produto_estoque pe left join (select * from mov_estoque where id in (SELECT max(id) FROM mov_estoque mov group by id_estoque)) mov on mov.id_estoque = pe.id left join adesao_equipamento adesao on adesao.serie = pe.serie where pe.status_produto in ('D') and pe.id_produto = %s", (id_produto))
        itens = cur.fetchall()
        cur.close()
        return itens

    def get_itens_cliente (self, id_produto):

        cur = self.con.integra.cursor()
        cur.execute("SELECT pe.serie, pe.mac, pe.wifi, pe.senha, adesao.login, pe.status_produto FROM produto_estoque pe join adesao_equipamento adesao on adesao.serie = pe.serie where adesao.status = 'A' and adesao.tipo in ('onu', 'roteador-preset') and pe.status_produto in ('U') and pe.id_produto = %s", (id_produto))
        itens_cliente = cur.fetchall()
        cur.close()
        return itens_cliente

    def get_cliente_by_login(self, login):

        cur = self.con.integra.cursor()
        cur.execute("select nome, cpf, email, telefone1, login from operador where login = %s", (login))
        cliente = cur.fetchone()
        cur.close()
        return cliente