def converter_segundos(segundos):
    horas = segundos // 3600  # 1 hora = 3600 segundos
    minutos = (segundos % 3600) // 60  # 1 minuto = 60 segundos
    segundos_restantes = segundos % 60  # Resto dos segundos

    return f"{horas}h {minutos}min {segundos_restantes}seg"

def calculoDeTempo(exercicios):
    tempo = 0.0
    c = 0
    for exer in exercicios:
        i = exercicios[exer]
        tempo += int(i["tempo"]) * int(i['qtd'])
        c +=1

    tempoTotal= converter_segundos(tempo)

    return tempoTotal
