import csv
import tkinter as tk
from tkinter import filedialog

import re

# Criar o Primeiro CSV

fields = ['Nome', 'grupo', 'tempo', 'id','qtd']

exercicios = {"agachamentoLivre": {"grupo": "perna", "tempo": 10, "id":1},
                "legPress": {"grupo": "perna", "tempo": 30, "id":2},
                "supinoReto": {"grupo": "peito", "tempo": 30, "id":3},
                "supinoInclinado": {"grupo": "peito", "tempo": 30, "id":4},
                "puxadaFrontal": {"grupo": "costas", "tempo": 30, "id":5},
                "remadaCurva": {"grupo": "costas", "tempo": 30, "id":6},
                "roscaDireta": {"grupo": "biceps", "tempo": 30, "id":7},
                "roscaMartelo": {"grupo": "biceps", "tempo": 30, "id":8},
                "tricepsPulley": {"grupo": "triceps", "tempo": 30, "id":9},
                "tricepsCorda": {"grupo": "triceps", "tempo": 30, "id":10},
                "abdominalSupra": {"grupo": "abdomen", "tempo": 10, "id":11},
                "abdominalInfra": {"grupo": "abdomen", "tempo": 10, "id":12},
                "esteira": {"grupo": "cardio", "tempo": 300, "id":13},
                "bicicleta": {"grupo": "cardio", "tempo": 300, "id":14}}

qtd_Lista = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def create_csv():
    exercicios_dict = {}
    for nome, detalhes in exercicios.items():
        exercicios_dict[nome] = {
            'Nome': nome,
            'grupo': detalhes.get('grupo'),
            'tempo': detalhes.get('tempo'),
            'id': detalhes.get('id'),
            'qtd': detalhes.get('qtd',0)
        }

    return exercicios_dict

# Função para abrir a janela de seleção de arquivo e carregar o CSV (R = Read)
def read_csv():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    file_path = filedialog.askopenfilename(defaultextension=".csv",
                                           filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])

    if file_path:  # Se o usuário não cancelar
        treinos = {}
        with open(file_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                nome = row['Nome']
                # Converte os valores para o tipo apropriado
                row['tempo'] = int(row['tempo'])
                row['id'] = int(row['id'])
                row['qtd'] = int(row['qtd'])
                treinos[nome] = row  # Adiciona o dicionário ao dicionário aninhado

        return treinos
# Atualiza o treino (U = Update)

def update_csv(treinos):
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")])

    if file_path:  # Se o usuário não cancelar
        # Transformar o dicionário aninhado em uma lista de dicionários
        data_to_write = []
        for nome, detalhes in treinos.items():
            detalhes['Nome'] = nome  # Adiciona o nome do exercício ao dicionário
            data_to_write.append(detalhes)  # Adiciona o dicionário à lista

        with open(file_path, 'w', newline='') as f:
            fields = ['Nome', 'grupo', 'tempo', 'id', 'qtd']  # Campos esperados no CSV
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data_to_write)


def formatar_nome(nome):
    # Substitui as letras maiúsculas por espaços seguidos da letra maiúscula
    nome_formatado = ''.join([' ' + c if c.isupper() else c for c in nome]).strip()
    # Capitaliza a primeira letra de cada palavra
    return nome_formatado.title()
