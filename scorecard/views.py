# Create your views here.
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import Http404, HttpResponse
from forms import MisionForm, PerspectivaForm, CategoriaIndicadorForm, UnidadMedidaForm, IndicadorForm
from models import Mision, Perspectiva, CategoriaIndicador, UnidadMedida, Indicador, CategoriaXIndicador
from django.shortcuts import render_to_response
from django.core import serializers
from django.http import QueryDict
import json
import socket

import pdb

def main(request):
    t=get_template('base.html')
    html= t.render(Context({'title':'BSC GPA'}))
    return HttpResponse(html)

def showUnidad(request):
    unidades=UnidadMedida.objects.all()
    data={'title':'BSC GPA'}
    csrfContext=RequestContext(request,data)
    return render_to_response('unidades.html', data, csrfContext)

def showMision(request):
    t=get_template('mision.html')
    data={'title':'BSC GPA'}
    misiones=Mision.objects.all()
    if misiones.count()>0:
        data={'title':'BSC GPA', 'empresa':misiones[0].getEmpresa(), 'descripcion':misiones[0].getDescripcion()}
    else:
        data={'title':'BSC GPA', 'empresa':'','descripcion':''}
    csrfContext=RequestContext(request,data)
    #html= t.render(Context(data,csrfContext))
    #return HttpResponse(html)
    return render_to_response('mision.html', data, csrfContext)
def ingresarMision(request):
    if request.is_ajax() and request.POST:
        form=MisionForm(request.POST)
        if form.is_valid():
            misiones=Mision.objects.all()
            n=misiones.count()
            if n>0:
                mensaje="actualizar"
                resultado=Mision.objects.filter(id=1).update(empresa=form.cleaned_data['empresa'], descripcion=form.cleaned_data['descripcion'])
                #form.save()
            else:
                 mensaje='crear'
                 form.save()   
            #valor-mision.objects.all()
            #form.save()
            data={'message':mensaje}
        else:
            data={'message':'Error'}
        return HttpResponse(json.dumps(data),content_type='application/json')
    else:
        raise Http404
def editarUnidad(request):
    if request.is_ajax() and request.POST:
        mydict=QueryDict.dict(request.POST)
        if mydict['oper'] == 'add':
            form = UnidadMedidaForm({'nombre':mydict['fields.nombre'], 'abreviatura':mydict['fields.abreviatura']})
            if form.is_valid():
                unidades=UnidadMedida.objects.all()
                mensaje='crear'
                form.save()           
                data={'message':mensaje}
            else:
                data={'message':'Error'}    
        elif  mydict['oper'] == 'del':
            mensaje="eliminar"
            aux_obj=UnidadMedida.objects.get(id=mydict['selrow'])
            aux_obj.delete()    
            data={'message':mensaje}
        else:
            data={'message':'Error'}
        return HttpResponse(json.dumps(data),content_type='application/json')
    else:
        raise Http404    
def editarCategoria(request):
    if request.is_ajax() and request.POST:
        mydict=QueryDict.dict(request.POST)
        if mydict['oper'] == 'add':
            form = CategoriaIndicadorForm({'nombre':mydict['fields.nombre'], 'descripcion':mydict['fields.descripcion']})
            if form.is_valid():
                categorias=CategoriaIndicador.objects.all()
                mensaje='crear'
                form.save()           
                data={'message':mensaje}
            else:
                data={'message':'Error'}    
        elif  mydict['oper'] == 'del':
            mensaje="eliminar"
            aux_obj=CategoriaIndicador.objects.get(id=mydict['selrow'])
            aux_obj.delete()    
            data={'message':mensaje}
        else:
            data={'message':'Error'}
        return HttpResponse(json.dumps(data),content_type='application/json')
    else:
        raise Http404

def editIndicador(request):
    if request.is_ajax() and request.POST:
        mydict=QueryDict.dict(request.POST)
        if mydict['oper'] == 'add':
            #categoria=CategoriaIndicador.objects.get(nombre=mydict['fields.categoria'])
            unidad=UnidadMedida.objects.get(abreviatura=mydict['fields.unidad'])
            form=IndicadorForm({'nombre':mydict['fields.nombre'], 'numerador':mydict['fields.numerador'], 'denominador':mydict['fields.denominador'], 'unidad':unidad.id})
            print form.errors
            
            if form.is_valid():
                form.save()
                data={'message':'Correcto'}
            else:
                data={'message':'Error'}
            return HttpResponse(json.dumps(data),content_type='application/json')
    else:
        raise Http404  

def loadSelectUnidades(request):
    data = "<select>"
    unidades = UnidadMedida.objects.all()
    n=0
    for i in unidades:
        data+='<option value="'+unidades[n].abreviatura+'">'+unidades[n].nombre+'</option>'
        n += 1
    data+="</select>"    
    return HttpResponse(data,content_type='application/json')
def loadSelectCategorias(request):
    data = "<select>"
    categorias = CategoriaIndicador.objects.all()
    n=0
    for i in categorias:
        data+='<option value="'+categorias[n].nombre+'">'+categorias[n].nombre+'</option>'
        n += 1
    data+="</select>"    
    return HttpResponse(data,content_type='application/json')

def loadSelectPerspectivas(request):
    data=serializers.serialize( "json",Perspectiva.objects.all())
    return HttpResponse(data, content_type="application/json")

def loadSelectCategoria(request):
    data=serializers.serialize( "json",CategoriaIndicador.objects.all())
    return HttpResponse(data, content_type="application/json")

def editPerspectiva(request):
    
    if request.is_ajax() and request.POST:
        mydict=QueryDict.dict(request.POST)
        if mydict['oper'] == 'edit':
            form=PerspectivaForm({'nombre':mydict['fields.nombre'], 'descripcion':mydict['fields.descripcion'], 'color':mydict['fields.color'], 'icono':mydict['fields.icono']})
            if form.is_valid():
                aux_obj=Perspectiva.objects.get(id=request.POST['pk'])
                aux_obj.nombre=mydict['fields.nombre']
                aux_obj.descripcion=mydict['fields.descripcion']
                aux_obj.color=mydict['fields.color']
                aux_obj.icono=mydict['fields.icono']
                aux_obj.save()
                data={'message':'Correcto'}
            else:    
                data={'message':'Error'}
        elif  mydict['oper'] == 'del':
            aux_obj=Perspectiva.objects.get(id=mydict['id'])
            aux_obj.delete()     
            data={'message':'Correcto'}
        elif mydict['oper'] == 'add':
            form=PerspectivaForm({'nombre':mydict['fields.nombre'], 'descripcion':mydict['fields.descripcion'], 'color':mydict['fields.color'], 'icono':mydict['fields.icono']})
            if form.is_valid():
                form.save()
                data={'message':'Correcto'}
            else:
                data={'message':'Error'}
        return HttpResponse(json.dumps(data),content_type='application/json')
    else:
        raise Http404    
def loadPerspectiva(request):
    data = serializers.serialize("json", Perspectiva.objects.all())
    #pdb.set_trace()
    return HttpResponse(data,content_type='application/json')

def loadUnidades(request):
    data = serializers.serialize("json", UnidadMedida.objects.all())
    #pdb.set_trace()
    return HttpResponse(data,content_type='application/json')

def showCategoria(request):
    t=get_template('categorias.html')
    html= t.render(Context({'title':'BSC GPA', 'empresa':'Gobierno Provincial del Azuay'}))
    return HttpResponse(html)

def showEstrategia(request):
    t=get_template('estrategia.html')
    data={'title':'BSC GPA', 'empresa':'Gobierno Provincial del Azuay'}
    csrfContext=RequestContext(request,data)
    html= t.render(csrfContext)
    return HttpResponse(html)

def showIndicador(request):
    t=get_template('indicadores.html')

    data={'title':'BSC GPA', 'empresa':'Gobierno Provincial del Azuay'}
    csrfContext=RequestContext(request,data)
    html= t.render(csrfContext)
    return HttpResponse(html)
def loadSelectCategoriaTipo(request):
    mydict=QueryDict.dict(request.POST)
    aux=CategoriaXIndicador.objects.all().distinct('categoria')
    indicadores=[]
    data=""
    for i in aux:
        aux_categoria=CategoriaIndicador.objects.get(pk=i.categoria_id)
        if mydict['tipo']=="Todos":
            data= Indicador.objects.all().values_list()
            n=0
            array=[]
            for i in data:
                unidad=UnidadMedida.objects.get(pk=i[4]) 
                aux={'id':i[0], 'nombre':i[1], 'numerador':i[2], 'denominador':i[3], 'unidad':unidad.nombre}
                array.append(aux)
            #pdb.set_trace()
            data=json.dumps(array)
        elif mydict['tipo']==aux_categoria.nombre:
            aux_indicadores=CategoriaXIndicador.objects.all().filter(categoria=aux_categoria.id)
            for j in aux_indicadores:
                aux_indicador=Indicador.objects.get(pk=j.indicador_id)
                aux_unidad=UnidadMedida.objects.get(pk=aux_indicador.unidad_id) 
                aux1={'id':aux_indicador.id, 'nombre':aux_indicador.nombre, 'numerador':aux_indicador.numerador, 'denominador':aux_indicador.denominador, 'unidad':aux_unidad.nombre}
                indicadores.append(aux1)
            data=json.dumps(indicadores)
            break
    return HttpResponse(data, content_type='application/json')

def loadIndicadores(request):
    try:
        data= Indicador.objects.all().values_list()
        n=0
        array=[]
        for i in data:
            unidad=UnidadMedida.objects.get(pk=i[4]) 
            aux={'id':i[0], 'nombre':i[1], 'numerador':i[2], 'denominador':i[3], 'unidad':unidad.nombre}
            array.append(aux)
        #pdb.set_trace()
        data=json.dumps(array)
        #data=serializers.serialize("json", data)
        return HttpResponse(data, content_type='application/json')
    except:
        return HttpResponse("", content_type='application/json')
def opcionesSelectCategorias():
    data= CategoriaIndicador.objects.all().values_list()
    aux=""
    for i in data:
        aux+='<option value="'+i[1]+'">'+i[1]+"</option>"
    return aux

def loadCategorias(request):
    data= serializers.serialize("json", CategoriaIndicador.objects.all())
    return HttpResponse(data, content_type='application/json')

def showPerspectiva(request):
    t=get_template('perspectiva.html')
    html= t.render(Context({'title':'BSC GPA', 'empresa':'Gobierno Provincial del Azuay'}))
    return HttpResponse(html)
def ingresarCategoriasXIndicador(request):
    t=get_template('ingreso_categorias.html')
    opciones=opcionesSelectCategorias()
    data={'title':'BSC GPA', 'empresa':'Gobierno Provincial del Azuay', 'opciones_select':opciones}
    csrfContext=RequestContext(request,data)
    html= t.render(csrfContext)
    return HttpResponse(html)
