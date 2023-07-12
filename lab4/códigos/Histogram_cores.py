import cv2
import numpy as np

# Função para equalizar o histograma em cada canal de cor separadamente
def equalizar_histograma_canais(imagem):
    canais = cv2.split(imagem)
    canais_equalizados = []
    for canal in canais:
        canal_equalizado = cv2.equalizeHist(canal)
        canais_equalizados.append(canal_equalizado)
    imagem_equalizada = cv2.merge(canais_equalizados)
    return imagem_equalizada

# Inicializa a captura de vídeo da webcam
captura = cv2.VideoCapture(0)

# Verifica se a captura de vídeo foi aberta corretamente
if not captura.isOpened():
    print("Não foi possível abrir a câmera.")
    exit()

# Loop para capturar e processar os quadros da webcam
while True:
    # Lê o próximo quadro da webcam
    ret, quadro = captura.read()

    # Verifica se o quadro foi lido corretamente
    if not ret:
        print("Não foi possível receber o quadro da câmera.")
        break

    # Equaliza o histograma em cada canal de cor separadamente
    quadro_equalizado = equalizar_histograma_canais(quadro)

    # Exibe o quadro original e o quadro equalizado em janelas separadas
    cv2.imshow('Quadro Original', quadro)
    cv2.imshow('Quadro Equalizado', quadro_equalizado)

    # Sai do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos utilizados pela captura de vídeo e fecha as janelas
captura.release()
cv2.destroyAllWindows()

