from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

class Endereco(models.Model):
    logradouro = models.CharField(max_length=50)
    bairro =  models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    cep = models.CharField(max_length=10)
	
class Usuario(models.Model):
	
	user = models.ForeignKey(User)
	endereco = models.ForeignKey(Endereco)
	tipoUser = models.CharField(max_length=9)
	nomeCompleto = models.CharField(max_length=30)
    
class Candidato(models.Model):
	usuario = models.ForeignKey(Usuario)
	formacao = models.CharField(max_length=30, null=True)
	areaAtuacao = models.CharField(max_length=30, null=True)
	sexo = models.CharField(max_length=10, null=True)
    
class Empresa(models.Model):
	usuario = models.ForeignKey(Usuario)
	status = models.BooleanField(default=False)

    
class Vaga(models.Model):
	empresa = models.ForeignKey(Empresa)
	dataAbertura = models.DateField(default=timezone.now)
	dataFechamento = models.DateField()
	salario = models.DecimalField(decimal_places=2, max_digits=8)
	cargaHoraria = models.CharField(max_length=25)
	funcao = models.CharField(max_length=100)
	descricao =  models.CharField(max_length=255)
	enderecoImagem = models.CharField(max_length=255, null=True)
	
	@property
	def is_past_due(self):
		if date.today() > self.dataFechamento:
			return True
		return False
	
	def qntCandidatos(self):
		candidatos = VagaTemCandidatos.objects.filter(vaga=self)
		return len(candidatos)
    
    
class VagaTemCandidatos(models.Model):
    vaga = models.ForeignKey(Vaga)
    candidato = models.ForeignKey(Candidato)
    dataCandidatura = models.DateField(default=timezone.now)
    aprovado = models.BooleanField(default=False)