import mysql.connector

class Tarefa:
    def __init__(self, id_tarefa, titulo, descricao, status):
        self.id_tarefa = id_tarefa
        self.titulo = titulo
        self.descricao = descricao
        self.__status = status

    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, novo_status):
        self.__status = novo_status

class Gerenciador_tarefas:
    def __init__(self):
        self.tarefas = []

    def adicionar_tarefa(self, tarefa):
        try:
            self.tarefas.append(tarefa)
            print("Adicionao a Lista de Tarefas.")

        except Exception as e:
            print(f"Erro ao adicionar tarefa: {e}")

    def listar_tarefas(self):
        return self.tarefas

    def atualizar_tarefa(self, id_tarefa, titulo, descricao, status):
        for tarefa in self.tarefas:
            if tarefa.id_tarefa == id_tarefa:
                if titulo:
                    tarefa.titulo = titulo
                if descricao:
                    tarefa.descricao = descricao
                if status:
                    tarefa.status = status
                print("Tarefa atualizada.")
                return
        print("Tarefa não encontrada na lista.")

class Gerenciador_tarefasBD:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="3306",
                user="root",
                password="root",
                database="gerenciamento_tarefas"
            )
            self.criar_tabela()
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.conn = None

    def criar_tabela(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id_tarefa INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(150) NOT NULL,
            descricao TEXT,
            status VARCHAR(30) NOT NULL
        )
        """)
        self.conn.commit()

    def salvar_tarefa(self, tarefa):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO tarefas (titulo, descricao, status) VALUES (%s, %s, %s)",
                       (tarefa.titulo, tarefa.descricao, tarefa.status))
        self.conn.commit()
        print("Tarefa salva no banco de dados.")

    def carregar_tarefas(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tarefas")
        tarefas = cursor.fetchall()
        return [Tarefa(*tarefa) for tarefa in tarefas]

    def atualizar_tarefa(self, id_tarefa, titulo, descricao, status):
        cursor = self.conn.cursor()
        query = "UPDATE tarefas SET "
        params = []

        if titulo:
            query += "titulo = %s, "
            params.append(titulo)

        if descricao:
            query += "descricao = %s, "
            params.append(descricao)

        if status:
            query += "status = %s, "
            params.append(status)

        query = query.rstrip(', ') + " WHERE id_tarefa = %s"
        params.append(id_tarefa)

        cursor.execute(query, tuple(params))
        self.conn.commit()
        print("Tarefa atualizada no banco de dados com sucesso!")

    def remover_tarefa(self, id_tarefa):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tarefas WHERE id_tarefa = %s", (id_tarefa,))
        self.conn.commit()
        print("Tarefa removida do banco de dados com sucesso!")

if __name__ == "__main__":
    gerenciador = Gerenciador_tarefas()  # Agora pode ser usado porque as classes estão definidas acima
    banco = Gerenciador_tarefasBD()      # Agora pode ser usado

    tarefa1 = Tarefa(1, "Fazer Projeto Final", "Elaborar o código do projeto final", "Pendente")
    tarefa2 = Tarefa(2, "Alimentar os gatinhos", "Levar comida aos gatinhos", "Concluído")
    tarefa3 = Tarefa(3, "Ir para o IF", "Ter que ir para o IF estudar", "Em andamento")

    gerenciador.adicionar_tarefa(tarefa1)
    gerenciador.adicionar_tarefa(tarefa2)

    banco.salvar_tarefa(tarefa1)
    banco.salvar_tarefa(tarefa2)

    print("Tarefas cadastradas:")
    for tarefa in banco.carregar_tarefas():
        print(f"ID: {tarefa.id_tarefa}, Título: {tarefa.titulo}, Descrição: {tarefa.descricao}, Status: {tarefa.status}")

    banco.atualizar_tarefa(1, status="Concluída")

    banco.remover_tarefa(3)

    print("Tarefas atualizadas:")
    for tarefa in banco.carregar_tarefas():
        print(f"ID: {tarefa.id_tarefa}, Título: {tarefa.titulo}, Descrição: {tarefa.descricao}, Status: {tarefa.status}")