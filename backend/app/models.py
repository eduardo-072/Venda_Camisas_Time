from django.db import models

# Create your models here.

#Models criar todas tabelas aq
class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    assunto = models.CharField(max_length=100)
    mensagem = models.TextField()

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    time = models.CharField(max_length=100, default="Internacional") # Novo campo
    imagem = models.ImageField(upload_to='produtos/')
    quantidade = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True, null=True) # Para detalhes da camisa
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self): return f"{self.nome} - {self.time}"