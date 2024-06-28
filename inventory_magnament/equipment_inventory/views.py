from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from collections import defaultdict
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Empleado, InventarioEquipo, AsignacionEquipo
from .forms import EmpleadoForm, InventarioEquipoForm, AsignacionEquipoForm, CSVUploadForm
import csv
import chardet
from django.db.models import Q


@login_required
def listar_empleados(request):
    query = request.GET.get('q')
    if query:
        empleados = Empleado.objects.filter(Q(nombre__icontains=query) | Q(rpe__icontains=query))
    else:
        empleados = Empleado.objects.all()
    
    paginator = Paginator(empleados, 10)  # Mostrar 10 empleados por página
    page = request.GET.get('page')
    try:
        empleados = paginator.page(page)
    except PageNotAnInteger:
        empleados = paginator.page(1)
    except EmptyPage:
        empleados = paginator.page(paginator.num_pages)
    
    return render(request, 'equipment_inventory/listar_empleados.html', {'empleados': empleados})


@login_required
def detalle_empleado(request, rpe):
    empleado = get_object_or_404(Empleado, rpe=rpe)
    asignaciones = AsignacionEquipo.objects.filter(empleado=empleado)
    return render(request, 'equipment_inventory/detalle_empleado.html', {'empleado': empleado, 'asignaciones': asignaciones})




@login_required
def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'equipment_inventory/crear_empleado.html', {'form': form})

@login_required
def listar_equipos(request):
    query = request.GET.get('q')
    if query:
        equipos = InventarioEquipo.objects.filter(
            Q(num_serie__icontains=query) | Q(num_inventario__icontains=query) | 
            Q(num_activo__icontains=query) | Q(marca__icontains=query) | 
            Q(modelo__icontains=query) | Q(tipo__icontains=query)
        )
    else:
        equipos = InventarioEquipo.objects.all()
    
    paginator = Paginator(equipos, 10)  # Mostrar 10 equipos por página
    page = request.GET.get('page')
    try:
        equipos = paginator.page(page)
    except PageNotAnInteger:
        equipos = paginator.page(1)
    except EmptyPage:
        equipos = paginator.page(paginator.num_pages)
    
    return render(request, 'equipment_inventory/listar_equipos.html', {'equipos': equipos})


@login_required
def detalle_equipo(request, num_serie):
    equipo = get_object_or_404(InventarioEquipo, num_serie=num_serie)
    asignacion = AsignacionEquipo.objects.filter(equipo=equipo).first()
    return render(request, 'equipment_inventory/detalle_equipo.html', {'equipo': equipo, 'asignacion': asignacion})


@login_required
def crear_equipo(request):
    if request.method == 'POST':
        form = InventarioEquipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_equipos')
    else:
        form = InventarioEquipoForm()
    return render(request, 'equipment_inventory/crear_equipo.html', {'form': form})

@login_required
def listar_asignaciones(request):
    query = request.GET.get('q')
    if query:
        asignaciones = AsignacionEquipo.objects.select_related('empleado', 'equipo').filter(
            Q(empleado__nombre__icontains=query) | Q(empleado__rpe__icontains=query) | 
            Q(equipo__num_serie__icontains=query)
        ).order_by('empleado')
    else:
        asignaciones = AsignacionEquipo.objects.select_related('empleado', 'equipo').order_by('empleado')
    
    paginator = Paginator(asignaciones, 10)  # Mostrar 10 asignaciones por página
    page = request.GET.get('page')
    try:
        asignaciones = paginator.page(page)
    except PageNotAnInteger:
        asignaciones = paginator.page(1)
    except EmptyPage:
        asignaciones = paginator.page(paginator.num_pages)
    
    context = {
        'asignaciones': asignaciones
    }
    return render(request, 'equipment_inventory/listar_asignaciones.html', context)



@login_required
def crear_asignacion(request):
    if request.method == 'POST':
        form = AsignacionEquipoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('listar_asignaciones')
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = AsignacionEquipoForm()
    return render(request, 'equipment_inventory/crear_asignacion.html', {'form': form})


def homepage(request):
    return render(request, 'equipment_inventory/home.html')

def homepage(request):
    return render(request, 'equipment_inventory/home.html')

@login_required
def home(request):
    return render(request, 'equipment_inventory/home.html')
def upload_empleados(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            # Detectar la codificación del archivo
            raw_data = csv_file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            csv_file.seek(0)  # Volver al inicio del archivo después de leerlo
            
            decoded_file = raw_data.decode(encoding).splitlines()
            reader = csv.DictReader(decoded_file)
            try:
                for row in reader:
                    Empleado.objects.create(
                        rpe=row['rpe'],
                        nombre=row['nombre'],
                        adscripcion=row['adscripcion'],
                        ubicacion=row['ubicacion'],
                        email=row['email'],
                        nombramiento=row['nombramiento'],
                    )
                messages.success(request, 'Empleados cargados exitosamente.')
                return redirect('listar_empleados')
            except KeyError as e:
                messages.error(request, f'Error en el archivo CSV: no se encontró la columna {str(e)}.')
                return redirect('upload_empleados')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al procesar el archivo CSV: {str(e)}.')
                return redirect('upload_empleados')
    else:
        form = CSVUploadForm()
    return render(request, 'equipment_inventory/upload_csv.html', {'form': form, 'titulo': 'Empleados'})

def upload_equipos(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            # Detectar la codificación del archivo
            raw_data = csv_file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            csv_file.seek(0)  # Volver al inicio del archivo después de leerlo
            
            decoded_file = raw_data.decode(encoding).splitlines()
            reader = csv.DictReader(decoded_file)
            try:
                for row in reader:
                    InventarioEquipo.objects.create(
                        num_serie=row['num_serie'],
                        num_inventario=row['num_inventario'],
                        num_activo=row['num_activo'],
                        marca=row['marca'],
                        modelo=row['modelo'],
                        tipo=row['tipo'],
                        especificaciones=row['especificaciones'],
                        fecha_adquisicion=row['fecha_adquisicion'],
                        estado=row['estado'],
                        ip=row['ip'],
                        nombre_equipo=row['nombre_equipo'],
                    )
                messages.success(request, 'Equipos cargados exitosamente.')
                return redirect('listar_equipos')
            except KeyError as e:
                messages.error(request, f'Error en el archivo CSV: no se encontró la columna {str(e)}.')
                return redirect('upload_equipos')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al procesar el archivo CSV: {str(e)}.')
                return redirect('upload_equipos')
    else:
        form = CSVUploadForm()
    return render(request, 'equipment_inventory/upload_csv.html', {'form': form, 'titulo': 'Equipos'})


