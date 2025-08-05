# Este arquivo centraliza a importação de todos os modelos SQLAlchemy do projeto.
# Ao importar este módulo, garantimos que o BaseModel.metadata conheça todas as tabelas.
from curso_santander.atleta.models import AtletaModel
from curso_santander.categorias.models import CategoriaModel
from curso_santander.centro_treinamento.models import CentroTreinamentoModel