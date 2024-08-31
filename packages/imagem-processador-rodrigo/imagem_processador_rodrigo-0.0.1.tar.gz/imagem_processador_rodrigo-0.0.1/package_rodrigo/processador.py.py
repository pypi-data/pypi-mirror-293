from PIL import Image, ImageFilter
import numpy as np

def carregar_imagem(caminho):
    """Carrega uma imagem do caminho especificado."""
    return Image.open(caminho)

def converter_para_escala_cinza(imagem):
    """Converte uma imagem para escala de cinza."""
    return imagem.convert('L')

def redimensionar_imagem(imagem, tamanho):
    """Redimensiona a imagem para o tamanho especificado."""
    return imagem.resize(tamanho)

def salvar_imagem(imagem, caminho):
    """Salva a imagem no caminho especificado."""
    imagem.save(caminho)

def aplicar_filtro_media(imagem, tamanho_kernel):
    """Aplica um filtro de média à imagem."""
    return imagem.filter(ImageFilter.BoxBlur(tamanho_kernel))