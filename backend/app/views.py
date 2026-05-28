from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib import messages
from urllib3 import request
from app.models import Categoria, Contato, Produto
from app.forms import FormCategoria, FormContato, ProdutoForm, FormUsuario, FormEditarUsuario

def index(request):
    return render(request, 'index.html')

def quemSomos(request):
    usuarios = User.objects.all()[:3]
    return render(request, 'quem-somos.html', {'usuarios': usuarios})

def loja(request):
   produtos = Produto.objects.exclude(time__icontains='Palmeiras').exclude(nome__icontains='Palmeiras')
   return render(request, 'loja.html', {'produtos': produtos})

def cadastrarUsuario(request):
    formulario = FormUsuario(request.POST or None)
    if request.method == 'POST':
        if formulario.is_valid():
            usuario = formulario.save()
            grupo_cliente = Group.objects.get(name="Cliente")
            usuario.groups.add(grupo_cliente)
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('login')
    return render(request, 'cadastro.html', {'form': formulario})

def loginUsuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('index')
        else:
            return render(request, 'login.html', {'erro': 'Usuário ou senha inválidos.'})
    return render(request, 'login.html')

def logoutUsuario(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def editarUsuario(request):
    formulario = FormEditarUsuario(request.POST or None, instance=request.user)
    if request.method == 'POST':
        if formulario.is_valid():
            formulario.save()
            return redirect('index')
    return render(request, 'edit-usuario.html', {'form': formulario})


# ─── Categoria ───

@login_required
@staff_member_required
def listarCategoria(request):
    _categorias = Categoria.objects.all().values()
    return render(request, 'categoria.html', {'categorias': _categorias})

@login_required
@staff_member_required
def delCategoria(request, id_cat):
    _categoria = Categoria.objects.get(id=id_cat)
    _categoria.delete()
    return redirect('categoria')

@login_required
@staff_member_required
def addCategoria(request):
    formulario = FormCategoria(request.POST or None)
    if request.POST:
        if formulario.is_valid():
            formulario.save()
            return redirect('categoria')
    return render(request, 'add-categoria.html', {'form': formulario})

@login_required
@staff_member_required
def editCategoria(request, id_cat):
    _categoria = Categoria.objects.get(id=id_cat)
    formulario = FormCategoria(request.POST or None, instance=_categoria)
    if request.POST:
        if formulario.is_valid():
            formulario.save()
            return redirect('categoria')
    return render(request, 'edit-categoria.html', {'form': formulario})


# ─── Contato ───

@login_required
@staff_member_required
def listarContato(request):
    contatos = Contato.objects.all()
    return render(request, 'contato.html', {'contatos': contatos})

@login_required
@staff_member_required
def delContato(request, id_contato):
    _contato = Contato.objects.get(id=id_contato)
    _contato.delete()
    return redirect('contato')

def addContato(request):
    formulario = FormContato(request.POST or None)
    if request.POST:
        if formulario.is_valid():
            formulario.save()
            return redirect('contato')
    return render(request, 'add-contato.html', {'form': formulario})


# ─── Produto ───

@login_required
@staff_member_required
def listarProduto(request):
    _produtos = Produto.objects.all()
    return render(request, 'produto.html', {'produtos': _produtos})

@login_required
@staff_member_required
def addProduto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('produto')
        else:
            # Isso vai imprimir o erro no seu terminal do VS Code
            print("ERROS DO FORMULÁRIO:", form.errors)
            # Isso vai renderizar a página com os erros visíveis
            return render(request, 'add-produto.html', {'form': form}) 
    else:
        form = ProdutoForm()
    return render(request, 'add-produto.html', {'form': form})

@login_required
@staff_member_required
def editProduto(request, id_prod):
    _produto = get_object_or_404(Produto, id=id_prod)
    form = ProdutoForm(request.POST or None, request.FILES or None, instance=_produto)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('produto')
    return render(request, 'edit-produto.html', {'form': form, 'produto': _produto})

@login_required
@staff_member_required
def delProduto(request, id_prod):
    _produto = get_object_or_404(Produto, id=id_prod)
    _produto.delete()
    return redirect('produto')


# ─── Dashboard ───

@login_required
@staff_member_required
def dashboard(request):
    total_produtos = Produto.objects.count()
    total_categorias = Categoria.objects.count()
    total_contatos = Contato.objects.count()
    total_usuarios = User.objects.count()

    context = {
        'total_produtos': total_produtos,
        'total_categorias': total_categorias,
        'total_contatos': total_contatos,
        'total_usuarios': total_usuarios,
        # 'total_vendas': 0, # Placeholder por enquanto
        # 'total_avaliacoes': 3, # As 3 que colocamos no HTML
    }
    return render(request, 'dashboard.html', context)

@login_required
@staff_member_required
def listarUsuarios(request):
    usuarios = User.objects.all().order_by('date_joined')
    return render(request, 'usuarios.html', {'usuarios': usuarios})

@login_required
@staff_member_required
def editUsuarioAdmin(request, id_user):
    _usuario = get_object_or_404(User, id=id_user)
    formulario = FormEditarUsuario(request.POST or None, instance=_usuario)
    if request.method == 'POST':
        if formulario.is_valid():
            formulario.save()
            return redirect('usuarios')
    return render(request, 'edit-usuario-admin.html', {'form': formulario, 'usuario': _usuario})

@login_required
@staff_member_required
def delUsuario(request, id_user):
    _usuario = get_object_or_404(User, id=id_user)
    _usuario.delete()
    return redirect('usuarios')

# ─── Carrinho ───

def _get_carrinho(request):
    return request.session.get('carrinho', {})

def add_to_cart(request, produto_id):
    carrinho = _get_carrinho(request)
    carrinho[str(produto_id)] = carrinho.get(str(produto_id), 0) + 1
    request.session['carrinho'] = carrinho
    messages.success(request, "Camisa adicionada ao carrinho!")
    return redirect('carrinho')

def carrinho_view(request):
    carrinho = _get_carrinho(request)
    itens = []
    total = 0
    for pid, qtd in carrinho.items():
        prod = get_object_or_404(Produto, id=pid)
        subtotal = prod.preco * qtd
        total += subtotal
        itens.append({'produto': prod, 'qtd': qtd, 'subtotal': subtotal})
    return render(request, 'carrinho.html', {'itens': itens, 'total': total})

def remover_item(request, produto_id):
    carrinho = _get_carrinho(request)
    carrinho.pop(str(produto_id), None)
    request.session['carrinho'] = carrinho
    return redirect('carrinho')

def atualizar_qtd(request, produto_id, acao):
    carrinho = _get_carrinho(request)
    pid = str(produto_id)
    if pid in carrinho:
        if acao == 'mais':
            carrinho[pid] += 1
        elif acao == 'menos' and carrinho[pid] > 1:
            carrinho[pid] -= 1
    request.session['carrinho'] = carrinho
    return redirect('carrinho')

def finalizar_compra(request):
    request.session['carrinho'] = {}
    messages.success(request, "✅ Pagamento realizado com sucesso! Obrigado pela compra.")
    return redirect('carrinho')