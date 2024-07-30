# Arquivo de suporte pra nao colocar Strings hardCoded no codigo
from enum import Enum
class orientation(Enum):
    left = "left"
    bottom = "bottom"
    right = "right"
    top = "top"

class Color(Enum):
    backgroundColor = '#FFFFFF'
    lineColor = '#000000'
    pathColor = '#008000'

class characters(Enum):
    Professor = 'Personagens/professorRafael.png'
    Estrela = 'Personagens/estrelaMario.png'
    codibentinho = 'Personagens/codibentinho.png'

