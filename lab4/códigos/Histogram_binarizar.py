import cv2

# Limiarização simples
def limiarizacao_simples(imagem, limiar):
    _, imagem_limiarizada = cv2.threshold(imagem, limiar, 255, cv2.THRESH_BINARY)
    return imagem_limiarizada

# Inicializa a captura de vídeo da webcam
captura = cv2.VideoCapture(0)

# Verifica se a captura de vídeo foi aberta corretamente
if not captura.isOpened():
    print("Não foi possível abrir a câmera.")
    exit()

# Valor de limiar inicial
limiar = 127

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

    # Aplica a limiarização simples no quadro em tons de cinza
    quadro_limiarizado = limiarizacao_simples(quadro_cinza, limiar)

    # Exibe o quadro em tons de cinza e o quadro limiarizado em janelas separadas
    cv2.imshow('Quadro em Tons de Cinza', quadro_cinza)
    cv2.imshow('Quadro Limiarizado', quadro_limiarizado)

    # Verifica se a tecla 'q' foi pressionada para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Verifica se a tecla '+' foi pressionada para aumentar o limiar
    if cv2.waitKey(1) & 0xFF == ord('+'):
        limiar += 1

    # Verifica se a tecla '-' foi pressionada para diminuir o limiar
    if cv2.waitKey(1) & 0xFF == ord('-'):
        limiar -= 1

# Libera os recursos utilizados pela captura de vídeo e fecha as janelas
captura.release()
cv2.destroyAllWindows()


