from django.forms import ModelForm
from django import forms
from models import Mision
from models import Perspectiva
from models import Estrategia
from models import Indicador
from models import CategoriaIndicador
from models import UnidadMedida

class MisionForm(ModelForm):
    class Meta:
        model=Mision
        fields = ('descripcion', 'empresa')


class PerspectivaForm(ModelForm):
	class Meta:
		model=Perspectiva
		fields=('nombre', 'descripcion', 'color', 'icono')

class EstrategiasForm(ModelForm):
	class Meta:
		model=Estrategia
		fields=('nombre','descripcion','perspectivas', 'indicadores')

class IndicadorForm(ModelForm):
	class Meta:
		model=Indicador
		fields=('nombre', 'numerador', 'denominador', 'unidad')

class CategoriaIndicadorForm(ModelForm):
	class Meta:
		model=CategoriaIndicador
		fields=('nombre', 'descripcion')

class UnidadMedidaForm(ModelForm):
	class Meta:
		model=UnidadMedida
		fields=('nombre', 'abreviatura')