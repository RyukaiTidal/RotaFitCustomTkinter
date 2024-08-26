import csv
import dicionario
import tkinter as tk
from tkinter import filedialog

import re

# Criar o Primeiro CSV

fields = ['Nome', 'grupo', 'tempo', 'id','qtd']
exercicios = dicionario.exerciciosDisponiveis
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
