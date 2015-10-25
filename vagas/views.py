from django.shortcuts import render, render_to_response, RequestContext, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User, Permission
from django.contrib.auth.views import login
import datetime
from vagas.models import *
from vagas.forms import *
from vagas.views import *

# Create your views here.


@login_required
def index(request):
	user = User.objects.get(username=request.user.username)
	if (user.is_staff):
		return redirect ('/administracao')
	else:
		usuario = Usuario.objects.get(user=user)
		if (usuario.tipoUser == 'True'):
			return redirect ('vagas.views.candidato_vagas')
		else:
			return redirect ('vagas.views.list_vagas')


@login_required
@staff_member_required
def administracao(request):
	empresas = Empresa.objects.all()
	return render(request,'admin/admin.html',{'empresas':empresas})
	
@login_required
@staff_member_required
def change_status_empresa(request, idEmpresa):
	empresa = Empresa.objects.get(id=idEmpresa)
	if (empresa.status):
		empresa.status = False
	else:
		empresa.status = True
	empresa.save()

	return redirect('/administracao')

	
	
@login_required
@permission_required('vagas.change_empresa', login_url='/accounts/login')
def change_status(request, idVagaTemCandidato):
	vagaTemCandidato = VagaTemCandidatos.objects.get(id=idVagaTemCandidato)
	if (vagaTemCandidato.aprovado):
		vagaTemCandidato.aprovado = False
	else:
		vagaTemCandidato.aprovado = True
	vagaTemCandidato.save()
	
	vaga = Vaga.objects.get(id=vagaTemCandidato.vaga.id)
	candidatos = VagaTemCandidatos.objects.filter(vaga=vaga)
	
	return render(request,'empresa/candidatos.html',{'candidatos':candidatos})

def delete_candidatura(request, idCandidatura):
	candidatura = get_object_or_404(VagaTemCandidatos, id=idCandidatura)
	candidatura.delete()
	return redirect('/candidato/candidaturas')

@login_required
@permission_required('vagas.change_empresa', login_url='/accounts/login')
def candidatos_vaga(request, idVaga):
	vaga = Vaga.objects.get(id=idVaga)
	candidatos = VagaTemCandidatos.objects.filter(vaga=vaga)
	
	return render(request,'empresa/candidatos.html',{'candidatos':candidatos})
	
@login_required
@permission_required('vagas.change_candidato', login_url='/accounts/login')
def candidaturas(request):
	user = User.objects.get(username=request.user.username)
	usuario = Usuario.objects.get(user=user)
	candidato = Candidato.objects.get(usuario=usuario)
	vagatemcandidatos = VagaTemCandidatos.objects.filter(candidato=candidato)
	return render(request,'candidato/candidaturas.html',{'vagatemcandidatos':vagatemcandidatos})
	
	
@login_required
@permission_required('vagas.change_candidato', login_url='/accounts/login')
def candidatarse(request, idVaga):
	vaga = Vaga.objects.get(id=idVaga)
	user = User.objects.get(username=request.user.username)
	usuario = Usuario.objects.get(user=user)
	candidato = Candidato.objects.get(usuario=usuario)
	VagaTemCandidatos.objects.create(vaga=vaga, candidato=candidato)
	
	return redirect ('vagas.views.candidaturas')
	
	
@login_required
@permission_required('vagas.change_candidato', login_url='/accounts/login')
def candidato_vagas(request):
	user = User.objects.get(username=request.user.username)
	usuario = Usuario.objects.get(user=user)
	candidato = Candidato.objects.get(usuario=usuario)
	vagasPorCandidato = VagaTemCandidatos.objects.values_list('vaga').filter(candidato=candidato)
	empresas = Empresa.objects.filter(status=True)
	vagas = Vaga.objects.filter(dataFechamento__range=[datetime.date.today(), "2050-01-01"], empresa__in=empresas).exclude(id__in=vagasPorCandidato)
	funcoes = Vaga.objects.values('funcao').filter(dataFechamento__range=[datetime.date.today(), "2050-01-01"], empresa__in=empresas).exclude(id__in=vagasPorCandidato).distinct()
	return render(request, 'candidato/ver_vagas.html', {'vagas':vagas, 'funcoes':funcoes})



def register(request):
	if request.method == 'POST':
		formUser = UserForm(request.POST)
		formEndereco = EnderecoForm(request.POST)
		formUsuario = UsuarioForm(request.POST)
		formCandidato = CandidatoForm(request.POST)
		
		if (formUser.is_valid() and formEndereco.is_valid() and formUsuario.is_valid()):
			
			user = formUser.save(commit=False)
			endereco = formEndereco.save(commit=False)
			#necessario para criptografar a senha
			user.set_password(request.POST.get('password'))
			user.save()
			endereco.save()
			usuario = formUsuario.save(commit=False)
			usuario.user = user
			usuario.endereco = endereco
			
			usuario.save()
			print (usuario.tipoUser)
			if (usuario.tipoUser == 'True'):
				permission = Permission.objects.get(name='Can change candidato')
				user.user_permissions.add(permission)
				
				if (formCandidato.is_valid()):
					candidato = formCandidato.save(commit=False)
					candidato.usuario = usuario
					candidato.save()
				else:
					return render_to_response('registration/register.html', {'userForm':formUser, 'enderecoForm':formEndereco, 'candidatoForm':formCandidato, 'usuarioForm':formUsuario}, context_instance=RequestContext(request))
			else:
				permission = Permission.objects.get(name='Can change empresa')
				user.user_permissions.add(permission)
				Empresa.objects.create(usuario=usuario)
				
			return render(request, 'registration/login.html', {})
		else:
			return render_to_response('registration/register.html', {
					'userForm':formUser, 'enderecoForm':formEndereco, 'candidatoForm':formCandidato, 'usuarioForm':formUsuario}, context_instance=RequestContext(request))
	else:
		userForm = UserForm()
		enderecoForm = EnderecoForm()
		candidatoForm = CandidatoForm()
		usuarioForm = UsuarioForm()
		return render(request, 'registration/register.html', {
				'userForm':userForm, 'enderecoForm':enderecoForm,
				'candidatoForm':candidatoForm, 'usuarioForm':usuarioForm})
def login(request):
	return render(request, 'registration/login.html', {})


@login_required
@permission_required('vagas.change_empresa', login_url='/accounts/login')
def new_vaga(request):
	user = request.user
	usuario = Usuario.objects.get(user=user)
	empresa = Empresa.objects.get(usuario=usuario)
	
	if empresa.status:
		if request.method == 'POST':
			formVaga = VagaForm(request.POST)

			if (formVaga.is_valid()):
				print (request.user)
				user = User.objects.get(username=request.user.username)
				print (user.password)
				usuario = Usuario.objects.get(user=user)
				print(usuario.nomeCompleto)
				empresa = Empresa.objects.get(usuario=usuario)

				vaga = formVaga.save(commit=False)
				vaga.empresa = empresa
				vaga.save()

				return redirect('vagas.views.list_vagas')
			else:
				return render_to_response('empresa/new_vaga.html', {'formVaga':formVaga}, context_instance=RequestContext(request))
		else:
			formVaga = VagaForm()	
			return render(request, 'empresa/new_vaga.html', {'formVaga':formVaga})
	else:
		return redirect('vagas.views.list_vagas')

	
@login_required
@permission_required('vagas.change_empresa', login_url='/accounts/login')
def list_vagas(request):
	user = User.objects.get(username=request.user.username)
	usuario = Usuario.objects.get(user=user)
	empresa = Empresa.objects.get(usuario=usuario)
	vagas = Vaga.objects.filter(empresa=empresa)
	return render(request, 'empresa/list_vaga.html', {'vagas':vagas, 'statusEmpresa':empresa.status})

@login_required
@permission_required('vagas.change_empresa', login_url='/accounts/login')
def edit_vaga(request, pk):
	vaga = get_object_or_404(Vaga, pk=pk)
	
	if request.method == 'POST':
		formVaga = VagaForm(request.POST, instance=vaga)
		
		if (formVaga.is_valid()):
			vaga.save()
			
			return redirect('vagas.views.list_vagas')
		else:
			return render_to_response('empresa/new_vaga.html', {'formVaga':formVaga}, context_instance=RequestContext(request))
	else:
		formVaga = VagaForm(instance=vaga)
		return render(request, 'empresa/new_vaga.html', {'formVaga':formVaga})
	
def delete_vaga(request, idVaga):
	vaga = get_object_or_404(Vaga, id=idVaga)
	vaga.delete()
	return redirect('/empresa/vaga/list')