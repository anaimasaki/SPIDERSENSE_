from tkinter import *
import time
import random

# Variáveis para contar jogadas e armazenar tempos de reação
jogadas = 0
tempos_de_reacao = []
cronometro_inicio = 0
executando = False  # Controla o estado do cronômetro

# Função para atualizar o cronômetro
def atualizar_cronometro():
    if executando:  # Se o cronômetro estiver ativo
        tempo_atual = time.time() - cronometro_inicio
        cronometro_label['text'] = f"Cronômetro: {tempo_atual:.1f} s"
        janela.after(100, atualizar_cronometro)  # Atualiza o cronômetro a cada 100ms

# Função para calcular o tempo de reação
def contar_tempo_reacao():
    global jogadas, tempos_de_reacao, cronometro_inicio, executando
    jogadas = 0
    tempos_de_reacao = []  # Zera as jogadas e tempos quando o jogo é reiniciado
    texto_resposta['text'] = ""  # Limpa o texto da rodada anterior
    texto_media['text'] = ""  # Limpa a média anterior
    botao['text'] = "Reset"  # Muda o botão para "Reset"
    botao['command'] = contar_tempo_reacao  # Redefine para resetar o jogo ao ser clicado de novo
    cronometro_inicio = time.time()  # Inicia o cronômetro
    executando = True
    atualizar_cronometro()  # Chama a função para começar a atualizar o cronômetro
    colocar_circulo()  # Chama a função para criar o círculo em uma posição aleatória

# Função para criar o círculo em posição aleatória
def colocar_circulo():
    global tempo_inicial, jogadas  # Marca o tempo inicial e controla as rodadas
    tempo_inicial = time.time()  # Atualiza o tempo inicial ao aparecer o círculo

    # Gera coordenadas aleatórias para o círculo
    x = random.randint(50, janela.winfo_screenwidth() - 150)
    y = random.randint(50, janela.winfo_screenheight() - 150)

    # Cores diferentes para cada jogada
    cores = ["red", "blue", "green", "yellow", "purple"]
    
    # Desenha o círculo em uma posição aleatória e altera a cor
    canvas.place(x=x, y=y)
    canvas.itemconfig(circulo, fill=cores[jogadas % len(cores)])  # Altera a cor do círculo
    canvas.coords(circulo, 10, 10, 110, 110)  # Define a posição e tamanho do círculo
    canvas.tag_bind(circulo, "<Button-1>", medir_tempo_reacao)  # Liga o clique ao círculo

# Função chamada quando o círculo é clicado para medir o tempo de reação
def medir_tempo_reacao(event):
    global jogadas, tempos_de_reacao, executando
    tempo_final = time.time()  # Marca o tempo final
    tempo_reacao = tempo_final - tempo_inicial  # Calcula o tempo de reação
    tempos_de_reacao.append(tempo_reacao)  # Adiciona o tempo à lista de tempos
    
    # Mostra o tempo de reação na interface
    texto_resposta['text'] += f"Rodada {jogadas + 1}: {tempo_reacao:.2f} segundos\n"

    jogadas += 1

    # Se ainda não chegamos a 5 rodadas, cria outro círculo
    if jogadas < 5:
        colocar_circulo()
    else:
        # Calcula a média dos tempos de reação
        media_reacao = sum(tempos_de_reacao) / len(tempos_de_reacao)
        texto_media['text'] = f"Média do tempo de reação: {media_reacao:.2f} segundos"
        canvas.place_forget()  # Esconde o círculo após a última jogada
        executando = False  # Para o cronômetro quando o jogo termina

# Função para fechar a janela
def fechar_janela():
    janela.destroy()

# Cria a janela e configura tela cheia
janela = Tk()
janela.title("Spider Sense")
janela.attributes('-fullscreen', True)

# Botão "Fechar" no canto superior direito
botao_fechar = Button(janela, text="Fechar", command=fechar_janela, bg="red", fg="white")
botao_fechar.place(x=janela.winfo_screenwidth() - 100, y=10)

# Título do jogo
titulo = Label(janela, text="Spider Sense", font=("Arial", 36), fg="black")
titulo.place(relx=0.5, rely=0.1, anchor=CENTER)

# Cronômetro no canto superior esquerdo
cronometro_label = Label(janela, text="Cronômetro: 0.0 s", font=("Arial", 16))
cronometro_label.place(x=10, y=10)

# Frame central para o primeiro botão e a instrução
frame_central = Frame(janela)
frame_central.place(relx=0.5, rely=0.4, anchor=CENTER)

# Label com instrução
texto = Label(frame_central, text="Clique no botão para iniciar o teste", font=("Arial", 16))
texto.grid(column=0, row=0, padx=10, pady=10)

# Botão que inicia o teste e depois vira reset
botao = Button(frame_central, text="Iniciar", command=contar_tempo_reacao, font=("Arial", 16))
botao.grid(column=0, row=1, padx=10, pady=10)

# Label para mostrar os tempos de reação em cada rodada
texto_resposta = Label(janela, text="", font=("Arial", 16), justify=LEFT)
texto_resposta.place(relx=0.5, rely=0.55, anchor=CENTER)

# Label para mostrar a média final dos tempos de reação
texto_media = Label(janela, text="", font=("Arial", 16), justify=CENTER)
texto_media.place(relx=0.5, rely=0.7, anchor=CENTER)

# Canvas para desenhar o círculo
canvas = Canvas(janela, width=120, height=120, bg="white", highlightthickness=0)
circulo = canvas.create_oval(10, 10, 110, 110, fill="red", outline="")

janela.mainloop()
