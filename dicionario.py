#importando o json
import json

# Carregando os Exercícios
exerciciosJson = open("exercicios.json", "r")
exerciciosDisponiveis = json.load(exerciciosJson)
