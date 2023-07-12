import cv2
import numpy as np

# Função para equalizar o histograma
def equalizar_histograma(imagem):
    # Calcula o histograma da imagem
    histograma = cv2.calcHist([imagem], [0], None, [256], [0, 256])

    # Calcula a função de distribuição acumulada do histograma
    cdf = histograma.cumsum()

    # Normaliza a função de distribuição acumulada
    cdf_normalized = cdf * 255 / cdf[-1]

    # Equaliza a imagem utilizando a função de distribuição acumulada
    imagem_equalizada = np.interp(imagem.flatten(), range(256), cdf_normalized.flatten()).reshape(imagem.shape).astype(np.uint8)

    # Retorna a imagem equalizada
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

    # Converte o quadro para tons de cinza
    quadro_cinza = cv2.cvtColor(quadro, cv2.COLOR_BGR2GRAY)

    # Equaliza o histograma do quadro em tons de cinza
    quadro_equalizado = equalizar_histograma(quadro_cinza)

    # Exibe o quadro em tons de cinza e o quadro equalizado em janelas separadas
    cv2.imshow('Quadro em Tons de Cinza', quadro_cinza)
    cv2.imshow('Quadro Equalizado', quadro_equalizado)

    # Sai do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos utilizados pela captura de vídeo e fecha as janelas
captura.release()
cv2.destroyAllWindows()

