from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LugarForm
from .models import Categoria, LugarPatrimonial


def home(request):
    return render(request, 'core/home.html')


def catalogo(request, categoria_id=None):
    lugares = LugarPatrimonial.objects.select_related('categoria')
    categoria_actual = None
    if categoria_id is not None:
        categoria_actual = get_object_or_404(Categoria, pk=categoria_id)
        lugares = lugares.filter(categoria=categoria_actual)
    return render(request, 'core/catalogo.html', {
        'lugares': lugares,
        'categorias': Categoria.objects.all(),
        'categoria_actual': categoria_actual,
    })


def detalle(request, lugar_id):
    lugar = get_object_or_404(
        LugarPatrimonial.objects.select_related('categoria'), pk=lugar_id
    )
    return render(request, 'core/detalle.html', {'lugar': lugar})


@login_required
def gestion(request):
    return render(request, 'core/gestion.html', {
        'lugares': LugarPatrimonial.objects.select_related('categoria'),
    })


@login_required
@permission_required('core.add_lugarpatrimonial', raise_exception=True)
def agregar_lugar(request):
    form = LugarForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        lugar = form.save()
        return redirect('detalle', lugar_id=lugar.pk)
    return render(request, 'core/lugar_form.html', {'form': form, 'titulo': 'Agregar lugar'})


@login_required
@permission_required('core.change_lugarpatrimonial', raise_exception=True)
def editar_lugar(request, lugar_id):
    lugar = get_object_or_404(LugarPatrimonial, pk=lugar_id)
    form = LugarForm(request.POST if request.method == 'POST' else None, instance=lugar)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('detalle', lugar_id=lugar.pk)
    return render(request, 'core/lugar_form.html', {'form': form, 'titulo': 'Editar lugar'})
