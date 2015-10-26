from django import forms
from localflavor.br.forms import BRZipCodeField
from .models import *
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
import datetime

class UserForm(forms.ModelForm):
	email = forms.CharField(label='Email', 
                    widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class':'form-control placeholder-no-fix'}))
	username = forms.CharField(label='Usuário', 
					widget=forms.TextInput(attrs={'placeholder': 'Usuário', 'class':'form-control placeholder-no-fix'}))
	password = forms.CharField(label='Senha', 
                    widget=forms.PasswordInput(attrs={'placeholder': 'Senha', 'class':'form-control placeholder-no-fix'}))
	class Meta:
		model = User
		fields = ['email','username', 'password']
		
class EnderecoForm(forms.ModelForm):
	logradouro = forms.CharField(label='Logradouro', 
                    widget=forms.TextInput(attrs={'placeholder': 'Logradouro', 'class':'form-control placeholder-no-fix'}))
	bairro = forms.CharField(label='Bairro', 
                    widget=forms.TextInput(attrs={'placeholder': 'Bairro', 'class':'form-control placeholder-no-fix'}))
	cidade = forms.CharField(label='Cidade', 
                    widget=forms.TextInput(attrs={'placeholder': 'Cidade', 'class':'form-control placeholder-no-fix'}))
	estado = forms.CharField(label='Estado', 
                    widget=forms.TextInput(attrs={'placeholder': 'Estado', 'class':'form-control placeholder-no-fix'}))
	cep = BRZipCodeField(label='Cep', 
                    widget=forms.TextInput(attrs={'placeholder': 'CEP', 'class':'form-control placeholder-no-fix'}))
	
	class Meta:
		model = Endereco
		fields = '__all__'
		
class CandidatoForm(forms.ModelForm):	
	FORMACAO_CHOICES = (
	('','Qual sua formação?'),	
	('Ens. Fundamental','Ensino Fundamental'),
	('Ens. Médio','Ens. Médio'),
	('Ens. Superior','Ens. Superior'),
	)
	
	formacao = forms.ChoiceField(widget = forms.Select(attrs={'class':'form-control'}), choices = FORMACAO_CHOICES, )
	
	areaAtuacao = forms.CharField(label='Área de Atuação', widget=forms.TextInput(attrs={'placeholder': 'Área de Atuação', 'class':'form-control placeholder-no-fix'}))
	
	SEXO_CHOICES = (
	('','Qual seu sexo?'),	
	('Masculino','Masculino'),
	('Feminino','Feminino'),
	('Outro','Outro'),
	)
	sexo = forms.ChoiceField(widget = forms.Select(attrs={'class':'form-control'}), choices = SEXO_CHOICES, )
	
	class Meta:
		model = Candidato
		fields = '__all__'
		exclude = ['usuario']
		
class UsuarioForm(forms.ModelForm):
	nomeCompleto = forms.CharField(label='nome Completo', widget=forms.TextInput(attrs={'placeholder': 'Nome Completo', 'class':'form-control placeholder-no-fix'}))
	tipoUser = forms.TypedChoiceField(
                   coerce=lambda x: x == 'candidato',
                   choices=(('candidato', 'Candidato'), ('empresa', 'Empresa')),
                   widget=forms.RadioSelect(attrs={'name':'perfil', 'onclick':'checkPerfil()'}),
                   label='Escolha seu perfil'
                )
	class Meta:
		model = Usuario
		fields = ['nomeCompleto', 'tipoUser']
		exclude = ['user', 'endereco']

class VagaForm(forms.ModelForm):
	dataFechamento = forms.DateField(label='Data de Fechamento', widget=SelectDateWidget(
			years=range(datetime.date.today().year, datetime.date.today().year+3), attrs={'placeholder': 'Data de Fechamento', 'class':'form-control'}), initial=timezone.now(), input_formats=['%d/%m/%Y'])
	cargaHoraria = forms.CharField(label='Carga Horária (horas)', widget=forms.NumberInput(attrs={'placeholder': 'Carga Horária', 'class':'form-control'}))
	salario = forms.DecimalField(label='Salário (R$)', widget=forms.NumberInput(attrs={'placeholder': 'Salário', 'class':'form-control'}))
	funcao = forms.CharField(label='Fução Disponível', widget=forms.TextInput(attrs={'placeholder': 'Fução Desejada', 'class':'form-control'}))
	descricao = forms.CharField(label='Descrição das Atividades', widget=forms.Textarea(attrs={'placeholder': 'Descreva as atividades da vaga', 'class':'form-control'}))
	enderecoImagem = forms.URLField(label='Endreço da Imagem de Destaque', widget=forms.TextInput(attrs={'placeholder': 'Endreço da Imagem de Destaque', 'class':'form-control'}))
	
	
	class Meta:
		model = Vaga
		fields = '__all__'
		exclude = ['empresa', 'dataAbertura']