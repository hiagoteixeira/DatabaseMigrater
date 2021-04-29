from modulos.Connection import Connection
from Models.Item import Item


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
        cur.execute("SELECT pe.serie, pe.mac, pe.wifi, pe.senha, adesao.login, pe.status_produto FROM produto_estoque pe join adesao_equipamento adesao on adesao.serie = pe.serie where adesao.status = 'A' and pe.status_produto in ('U') and pe.id_produto = %s", (id_produto))
        itens_cliente = cur.fetchall()
        cur.close()
        return itens_cliente

    def get_cliente_by_login(self, login):

        cur = self.con.integra.cursor()
        cur.execute("select c.nome, c.cpfcnpj, c.email, t.telefone, a.login from clientes as c join adesao as a on a.cliente = c.id join telefones as t on t.id_cliente = c.id where a.login =  %s group by c.nome", (login))
        cliente = cur.fetchone()
        cur.close()
        return cliente

    def get_all_presets(self):
        
        cur = self.con.integra.cursor()
        cur.execute("select	serie, login_pppoe, senha_pppoe from produto_estoque as item join produto as p on p.id = item.id_produto join produto_categoria as c on c.id = p.categoria where c.id in (3,21) AND login_pppoe is not null;")
        itens = cur.fetchall()
        cur.close()
        return itens
        