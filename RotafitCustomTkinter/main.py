# Importar CTK, Crud, Copy, Calculo

import customtkinter
import CRUD
import copy
import calculo

#Importar Sys e OS pra Favicon
import sys
import os

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.treino = None
        self.novoTreino = None

        # Janela
        self.title("Rotafit")
        self.geometry(f"{1280}x{720}")
        customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

        # configurar GRID 4x4
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Obter o diretório do arquivo executável
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, "favicon.ico")

        # Carregar o ícone
        self.iconbitmap(icon_path)


        # Configurar protocolo de fechamento
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.telaInicial()

    def telaInicial(self):

        # Barra lateral

        self.janela_barralateral = customtkinter.CTkFrame(self, width=500, border_width=0)
        self.janela_barralateral.grid(row=0, column=0, rowspan=4, sticky="nsew")

        # Logo ROTAFIT

        self.logo_barralateral = customtkinter.CTkLabel(self.janela_barralateral, text="ROTAFIT",
                                                        font=customtkinter.CTkFont(size=50, weight="bold"))
        self.logo_barralateral.grid(row=0, column=0, padx=200, pady=(100, 50))

        # Botão "Criar um novo Treino"

        self.botao_criar = customtkinter.CTkButton(self.janela_barralateral, command=self.criarTreino,
                                                   text="Criar um novo Treino", font=customtkinter.CTkFont(size=30),
                                                   width=300, height=100)
        self.botao_criar.grid(row=1, column=0, padx=20, pady=100)

        # Botão "Carregar Treinos"

        self.botao_carregar = customtkinter.CTkButton(self.janela_barralateral, command=self.lerTreino,
                                                      text="Carregar Treino", font=customtkinter.CTkFont(size=30),
                                                      width=300, height=100)
        self.botao_carregar.grid(row=2, column=0)

    def criarTreino(self):
        self.treino = CRUD.create_csv()
        self.novoTreino = copy.deepcopy(self.treino)  # Cria uma cópia profunda
        self.frameUpdateEx()

    def lerTreino(self):
        self.treino = CRUD.read_csv()
        if self.treino is not None:
            self.novoTreino = copy.deepcopy(self.treino)  # Cria uma cópia profunda
            self.visualizarTreinos()


    def visualizarTreinos(self):
        # Se a tela de visualização já estiver criada, remova-a
        if hasattr(self, 'visu_Treinos'):
            self.visu_Treinos.destroy()

        self.janela_barralateral.grid_forget()

        # Barra lateral

        self.janela_barralateral = customtkinter.CTkFrame(self, width=500, border_width=0)
        self.janela_barralateral.grid(row=0, column=0, rowspan=4, sticky="nsew")

        # Criar nova tela para visualização de treinos
        self.visu_Treinos = customtkinter.CTkFrame(self, fg_color="transparent")
        self.visu_Treinos.grid(row=0, column=1, sticky="nsew")

        # Adicionar texto e botões na nova tela
        self.tituloVisuT = customtkinter.CTkLabel(self.janela_barralateral, text="Seu Treino:",
                                                  font=customtkinter.CTkFont(size=30, weight="bold"))
        self.tituloVisuT.grid(row=0, column=0, columnspan=2, padx=100, pady=(50, 50))

        # Salvar Treino
        self.BsaveTreino = customtkinter.CTkButton(self.janela_barralateral, text="Salvar",
                                                   font=customtkinter.CTkFont(size=20), width=150, height=50)
        self.BsaveTreino.grid(row=1, column=0, columnspan=2, padx=20, pady=10)
        # Definindo Parâmetros do Botão de Salvar de Treino:
        if self.novoTreino == self.treino:
            self.BsaveTreino.configure(state="Disabled", fg_color="transparent", border_width=2)
        else:
            self.BsaveTreino.configure(state="normal", command=self.BsaveTreino_C, border_width=0)

        # Alterar Exercícios
        self.alterarExercicio = customtkinter.CTkButton(self.janela_barralateral, text="Alterar Rotina", command=self.alterarRotina,
                                                        font=customtkinter.CTkFont(size=20), width=150, height=50)
        self.alterarExercicio.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

        # Voltar
        self.voltarmenu = customtkinter.CTkButton(self.janela_barralateral, command=self.VoltarBotao,
                                                  text="Voltar pro Menu inicial", font=customtkinter.CTkFont(size=20),
                                                  width=300, height=50, border_width=2)
        self.voltarmenu.grid(row=5, column=0, columnspan=2, padx=20, pady=20)

        # Tempo médio de treino
        print(self.novoTreino)
        self.textoTempo = customtkinter.CTkLabel(self.visu_Treinos, text="Tempo Médio:", font=customtkinter.CTkFont(size=30,
                                                                                                                    weight="bold"))
        self.textoTempo.grid(row=7,column=2,padx=20,pady=20)

        self.TempoLabel = customtkinter.CTkLabel(self.visu_Treinos, text=calculo.calculoDeTempo(self.novoTreino),
                                                 font=customtkinter.CTkFont(size=30))
        self.TempoLabel.grid(row=8,column=2)

        # Adicionar exercícios ao frame de exercícios
        column = 0
        row = 1  # Começar a partir da linha 1 para os exercícios
        i = 0 # Contador de Exercícios
        for ex in self.novoTreino:
            exercicios = self.novoTreino[ex]
            if int(exercicios['qtd']) > 0:  # Filtra os exercícios com quantidade maior que 0
                detalhes_str = (f"{CRUD.formatar_nome(exercicios['Nome'])}, {5 * int(exercicios['qtd'])}x\n"
                                f"Tempo médio: {exercicios['tempo']} seg.")
                exercicio_label = customtkinter.CTkLabel(self.visu_Treinos, text=detalhes_str,
                                                         font=customtkinter.CTkFont(size=20))
                exercicio_label.grid(row=row, column=column, padx=20, pady=20, sticky="nw")

                # Ajustar a linha e coluna
                if (i + 1) % 7 == 0:
                    column += 1  # Mudar para a próxima coluna a cada 7 exercícios
                    row = 1  # Reiniciar a linha para a nova coluna
                    i += 1 # Mudar para o próximo Exercício
                else:
                    row += 1  # Mover para a próxima linha
                    i +=1 # Mudar para o próximo Exercício

        # Configurar expansão do grid
        self.visu_Treinos.grid_rowconfigure(4, weight=1)
        self.visu_Treinos.grid_columnconfigure(1, weight=1)
        self.visu_Treinos.grid_columnconfigure(2, weight=1)

        self.janela_barralateral.grid_rowconfigure(4,weight=1)
    def VoltarBotao(self):
        self.janela_barralateral.grid_forget()
        self.visu_Treinos.grid_forget()
        self.telaInicial()


    def alterarRotina(self):
        self.frameUpdateEx()

    def BsaveTreino_C(self):
        CRUD.update_csv(self.novoTreino)


    def frameUpdateEx(self):
        # Se a tela de visualização já estiver criada, remova-a
        if hasattr(self, 'visu_Treinos'):
            self.visu_Treinos.destroy()

        self.janela_barralateral.grid_forget()

        # Barra lateral

        self.janela_barralateral = customtkinter.CTkFrame(self, width=200, border_width=0)
        self.janela_barralateral.grid(row=0, column=0, rowspan=4, sticky="nsew")

        # Label pro grid Lateral

        self.labelFUE = customtkinter.CTkLabel(self.janela_barralateral,text="Alterar\nExercícios",font=customtkinter.CTkFont(size=40,weight="bold"))
        self.labelFUE.grid(row=0,column=0, columnspan=1, padx=50 ,pady=(20,100),sticky='nwe')

        # Botão para Visualizar o treino

        self.fueSaveB = customtkinter.CTkButton(self.janela_barralateral,width=250,height=100,corner_radius=20,text="Visualizar Treino",font=customtkinter.CTkFont(size=30), command= self.salvar_e_voltar)
        self.fueSaveB.grid(row=1,column=0,padx=100,pady=20)

        # Criar tela para visualização de treinos
        self.visu_Treinos = customtkinter.CTkFrame(self, fg_color="transparent")
        self.visu_Treinos.grid(row=0, column=1, padx=50, sticky="nsew")

        # Voltar
        self.voltarmenu = customtkinter.CTkButton(self.janela_barralateral, command=self.VoltarBotao,
                                                  text="Voltar pro Menu inicial", font=customtkinter.CTkFont(size=20),
                                                  width=300, height=50, border_width=2)
        self.voltarmenu.grid(row=5, column=0, columnspan=2, padx=20, pady=200)

        #Adicionar tabview com nomes dos grupos

        self.tabviewExercicios = customtkinter.CTkTabview(self.visu_Treinos, width= 700,corner_radius=10)
        self.tabviewExercicios.grid(row=1,column=0, columnspan=2, rowspan=4, sticky="nsew")

        # Adicionar tabs e botões
        self.tab_buttons = {}  # Para armazenar botões de aumentar/diminuir quantidade
        self.exercise_labels = {}  # Para armazenar labels de quantidade

        grupos = list(set(ex['grupo'] for ex in self.novoTreino.values()))  # Lista dos grupos

        # Adicionar abas para cada grupo
        for grupo in grupos:
            self.tabviewExercicios.add(grupo)

        # Adicionar exercícios às abas
        for grupo in grupos:
            for exercicio in [ex for ex in self.novoTreino.values() if ex['grupo'] == grupo]:
                # Garantir que qtd não seja None
                qtd = exercicio.get('qtd', 0) or 0

                # Exibir exercício
                detalhes_str = f"{CRUD.formatar_nome(exercicio['Nome'])}, {5 * int(qtd)}x\nTempo médio: {exercicio['tempo']} seg."
                exercicio_label = customtkinter.CTkLabel(self.tabviewExercicios.tab(grupo), text=detalhes_str,
                                                         font=customtkinter.CTkFont(size=20))
                exercicio_label.grid(row=len(self.tab_buttons) * 4, column=0, padx=20, pady=(10, 10))

                # Adicionar botão de aumentar quantidade
                aumentar_button = customtkinter.CTkButton(self.tabviewExercicios.tab(grupo), text="+",
                                                          command=lambda e=exercicio: self.aumentarQtd(e))
                aumentar_button.grid(row=len(self.tab_buttons) * 4, column=1, padx=10, pady=20)

                # Adicionar botão de diminuir quantidade
                diminuir_button = customtkinter.CTkButton(self.tabviewExercicios.tab(grupo), text="-",
                                                          command=lambda e=exercicio: self.diminuirQtd(e))
                diminuir_button.grid(row=len(self.tab_buttons) * 4, column=2, padx=10, pady=20)

                # Adicionar label de quantidade
                qtd_label = customtkinter.CTkLabel(self.tabviewExercicios.tab(grupo), text=f"{5 * int(qtd)}x",
                                                   font=customtkinter.CTkFont(size=20))
                qtd_label.grid(row=len(self.tab_buttons) * 4, column=3, padx=10, pady=10)

                self.tab_buttons[exercicio['Nome']] = (aumentar_button, diminuir_button)
                self.exercise_labels[exercicio['Nome']] = qtd_label

        # Definir a primeira aba como ativa
        self.tabviewExercicios.set(grupos[0])

    def aumentarQtd(self, exercicio):
        # Garantir que qtd não seja None e inicializar com 0 se necessário
        if exercicio['qtd'] is None:
            exercicio['qtd'] = 0


        # Aumenta a quantidade do exercício específico
        exercicio['qtd'] += 1
        self.atualizarQuantidades()  # Atualiza a exibição de quantidades

    def diminuirQtd(self, exercicio):
        # Garantir que qtd não seja None e inicializar com 0 se necessário
        if exercicio['qtd'] is None:
            exercicio['qtd'] = 0

        # Diminui a quantidade do exercício específico, mas não deixa abaixo de 0
        if exercicio['qtd'] > 0:
            exercicio['qtd'] -= 1

        self.atualizarQuantidades()  # Atualiza a exibição de quantidades

    def atualizarQuantidades(self):
        # Atualiza os labels de quantidade na interface
        for nome, label in self.exercise_labels.items():
            exercicio = self.novoTreino[nome]
            qtd = exercicio.get('qtd', 0) or 0
            label.configure(text=f"{5 * int(qtd)}x")

    def salvar_e_voltar(self):
        for exercicio in self.novoTreino.values():
            if exercicio['qtd'] is None:
                exercicio['qtd'] = 0
        # Voltar para a tela de visualização de treinos
        self.visualizarTreinos()

    def on_closing(self):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
