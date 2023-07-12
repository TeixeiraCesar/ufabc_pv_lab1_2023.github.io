import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Função para equalizar o histograma
def equalizar_histograma(imagem):
    imagem_equalizada = cv2.equalizeHist(imagem)
    return imagem_equalizada

# Caminho da pasta para salvar as imagens
caminho_pasta = '/home/ufabc/Documentos/cesarabt/Lab4'

# Carregar a imagem
imagem = cv2.imread('/home/ufabc/Documentos/cesarabt/Lab1/Parte3/cesar.png')

# Converter a imagem para tons de cinza
imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

# Calcular o histograma da imagem em tons de cinza
histograma_antes = cv2.calcHist([imagem_cinza], [0], None, [256], [0, 256])

# Equalizar o histograma
imagem_equalizada = equalizar_histograma(imagem_cinza)

# Calcular o histograma da imagem equalizada
histograma_depois = cv2.calcHist([imagem_equalizada], [0], None, [256], [0, 256])

# Exibir os gráficos de histograma antes e depois da equalização
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(histograma_antes)
plt.title('Histograma Antes da Equalização')
plt.subplot(1, 2, 2)
plt.plot(histograma_depois)
plt.title('Histograma Depois da Equalização')
plt.show()

# Salvar a imagem original em tons de cinza
caminho_imagem_cinza = os.path.join(caminho_pasta, 'cesar_cinza.png')
cv2.imwrite(caminho_imagem_cinza, imagem_cinza)

# Salvar a imagem equalizada em tons de cinza
caminho_imagem_equalizada = os.path.join(caminho_pasta, 'cesar_equalizada.png')
cv2.imwrite(caminho_imagem_equalizada, imagem_equalizada)

# Salvar a imagem original em cores
caminho_imagem_colorida = os.path.join(caminho_pasta, 'cesar_colorida.png')
cv2.imwrite(caminho_imagem_colorida, imagem)

