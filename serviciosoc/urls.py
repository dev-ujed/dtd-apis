from django.urls import path

from .apiviews import getDatosAlumno, getCiclosEgreso, searchAlumnos, countAlumnos, getEstadistica


urlpatterns = [
	path('alumno/<int:escuela>/<str:matricula>/', 	getDatosAlumno.as_view(), 	name='getDatosAlumno'),
	path('ciclos/<int:escuela>/', 					getCiclosEgreso.as_view(), 	name='getCiclosEgreso'),
	path('alumnos/<int:escuela>', 					searchAlumnos.as_view(), 	name='searchAlumnos'),
	path('contar/<int:escuela>/', 					countAlumnos.as_view(), 	name='countAlumnos'),
	path('estadistica/<int:escuela>', 				getEstadistica.as_view(), 	name='getEstadistica'),
]
