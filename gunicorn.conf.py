bind = "127.0.0.1:8000"  # Especifique o endereço IP e a porta onde o Gunicorn irá escutar

workers = 3  # Número de workers que o Gunicorn deve usar

# Especifique o módulo WSGI a ser usado
# Substitua 'roteirizacao_projeto' pelo nome real do seu projeto Django
# e 'wsgi' pelo nome do seu arquivo WSGI
pythonpath = '\roteirizacao_projeto'
wsgi_app = 'roteirizacao_projeto.wsgi:application'

