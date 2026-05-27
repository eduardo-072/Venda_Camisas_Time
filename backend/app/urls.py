from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),

    # ─── Páginas Públicas ───
    path('quem-somos', views.quemSomos, name="quemsomos"),
    path('loja', views.loja, name="loja"),

    # ─── Usuário ───
    path('cadastro', views.cadastrarUsuario, name="cadastro"),
    path('login', views.loginUsuario, name="login"),
    path('editar-usuario', views.editarUsuario, name="editarusuario"),

    # ─── Categoria ───
    path('Categoria', views.listarCategoria, name="categoria"),
    path('del-categoria/<int:id_cat>', views.delCategoria, name="delcategoria"),
    path('add-categoria', views.addCategoria, name="addcategoria"),
    path('edit-categoria/<int:id_cat>', views.editCategoria, name="editcategoria"),

    # ─── Contato ───
    path('contato', views.listarContato, name="contato"),
    path('del-contato/<int:id_contato>', views.delContato, name="delcontato"),
    path('add-contato', views.addContato, name="addcontato"),

    # ─── Produto ───
    path('add-produto', views.addProduto, name="addproduto"),
    path('produto', views.listarProduto, name="produto"),
    path('edit-produto/<int:id_prod>', views.editProduto, name="editproduto"),
    path('del-produto/<int:id_prod>', views.delProduto, name="delproduto"),

    # ─── Dashboard ───
    path('dashboard', views.dashboard, name="dashboard"),
    path('dashboard/usuarios', views.listarUsuarios, name="usuarios"),
    path('dashboard/usuarios/edit/<int:id_user>', views.editUsuarioAdmin, name="editusuarioadmin"),
    path('dashboard/usuarios/del/<int:id_user>', views.delUsuario, name="delusuario"),

    # ─── Carrinho ───
    path('carrinho/', views.carrinho_view, name='carrinho'),
    path('carrinho/add/<int:produto_id>/', views.add_to_cart, name='add_to_cart'),
    path('carrinho/remover/<int:produto_id>/', views.remover_item, name='remover_item'),
    path('carrinho/<int:produto_id>/<str:acao>/', views.atualizar_qtd, name='atualizar_qtd'),
    path('carrinho/finalizar/', views.finalizar_compra, name='finalizar_compra'),
]
