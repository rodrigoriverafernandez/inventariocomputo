from django import forms
from .models import Empleado, InventarioEquipo, AsignacionEquipo

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'

class InventarioEquipoForm(forms.ModelForm):
    class Meta:
        model = InventarioEquipo
        fields = '__all__'

class AsignacionEquipoForm(forms.ModelForm):
    class Meta:
        model = AsignacionEquipo
        fields = '__all__'


from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()
