from django.db.models import Subquery
# from django.core.serializers import serialize
from rest_framework import generics
from rest_framework.permissions import AllowAny


from .models import DatosAlumno, DatosAlumnos, ContarAlumnos, DBMovAlumnos, DBCiclo
from .serializers import AlumnoSerializer, AlumnosSerializer, ContarSerializer, DBCicloSerializer, EstadisticaSerializer

from datetime import date


class getDatosAlumno(generics.ListAPIView):
	permission_classes=[AllowAny]
	"""
	API que obtiene los datos de los alumno, de una escuela y matrícula específica.
	"""
    
	serializer_class = AlumnoSerializer
	
	def get_queryset(self):
		escuela		= self.kwargs.get('escuela', None)
		matricula	= self.kwargs.get('matricula', None)
		if escuela is not None and matricula is not None:
			queryset = DatosAlumno.objects.using('escolares').raw(
				"""
					with
						datos_alumno as
							(select trim(ta.cve_alumno) as matricula, ta.nombre, ta.paterno, ta.materno, ta.correo as email, ta.telefono
								from desarrollo.alumno ta where trim(ta.cve_alumno) = %s),
						semestre_ingreso as
							(select trim(ta.cve_alumno) as matricula, ta.cve_ciclo as ingreso_cve, 
									substr(tb.desc_ciclo,1,4)||' '||decode(substr(tb.desc_ciclo,6,1),'A','B','E','A') as ingreso_desc
								from desarrollo.mov_alumno ta, desarrollo.ciclo tb
								where ta.cve_ciclo = tb.cve_ciclo
								and ta.cve_escuela = %s
								and trim(ta.cve_alumno) = %s
								and ta.cve_estatus = 1),
						semestre_actual as
							(select trim(ta.cve_alumno) as matricula, ta.cve_ciclo as actual_cve, 
									substr(tb.desc_ciclo,1,4)||' '||decode(substr(tb.desc_ciclo,6,1),'A','B','E','A') as actual_desc,
									ta.semestre as actual_semestre, ta.cve_estatus as actual_estatus, tc.desc_estatus as actual_destatus
								from desarrollo.mov_alumno ta, desarrollo.ciclo tb, desarrollo.estatus tc
								where ta.cve_ciclo = tb.cve_ciclo
								and ta.cve_estatus = tc.cve_estatus
								and ta.cve_escuela = %s
								and trim(ta.cve_alumno) = %s
								and sysdate between tb.f_inicial and tb.f_final
								and ta.fecha_mov =
									(select max(fecha_mov) from desarrollo.mov_alumno tx 
										where tx.cve_escuela = ta.cve_escuela and tx.cve_alumno = ta.cve_alumno 
										and tx.cve_ciclo = ta.cve_ciclo)),
						semestre_egreso as
							(select trim(ta.cve_alumno) as matricula, ta.cve_ciclo as egreso_cve, 
									substr(tb.desc_ciclo,1,4)||' '||decode(substr(tb.desc_ciclo,6,1),'A','B','E','A') as egreso_desc
								from desarrollo.mov_alumno ta, desarrollo.ciclo tb
								where ta.cve_ciclo = tb.cve_ciclo
								and ta.cve_escuela = %s
								and trim(ta.cve_alumno) = %s
								and ta.cve_estatus = 7),
						semestre_ultimo as
							(select trim(ta.cve_alumno) as matricula, ta.cve_ciclo as ultimo_cve, 
									substr(tb.desc_ciclo,1,4)||' '||decode(substr(tb.desc_ciclo,6,1),'A','B','E','A') as ultimo_desc,
									ta.semestre as ultimo_semestre, ta.cve_estatus as ultimo_estatus, tc.desc_estatus as ultimo_destatus
								from desarrollo.mov_alumno ta, desarrollo.ciclo tb, desarrollo.estatus tc
								where ta.cve_ciclo = tb.cve_ciclo
								and ta.cve_estatus = tc.cve_estatus
								and ta.cve_escuela = %s
								and trim(ta.cve_alumno) = %s
								and ta.fecha_mov =
									(select max(fecha_mov) from desarrollo.mov_alumno tx where tx.cve_escuela = ta.cve_escuela and tx.cve_alumno = ta.cve_alumno))
					select ta.matricula, ta.nombre, ta.paterno, ta.materno, ta.email, ta.telefono,
							tb.ingreso_cve, tb.ingreso_desc,
							tc.actual_cve, tc.actual_desc, tc.actual_semestre, tc.actual_estatus, tc.actual_destatus,
							td.egreso_cve, td.egreso_desc,
							te.ultimo_cve, te.ultimo_desc, te.ultimo_semestre, te.ultimo_estatus, te.ultimo_destatus
					from datos_alumno ta, semestre_ingreso tb, semestre_actual tc, semestre_egreso td, semestre_ultimo te
					where ta.matricula = tb.matricula(+)
						and ta.matricula = tc.matricula(+)
						and ta.matricula = td.matricula(+)
						and ta.matricula = te.matricula(+)
				""",
				[matricula, escuela, matricula, escuela, matricula, escuela, matricula, escuela, matricula]
			)
			return queryset



class getCiclosEgreso(generics.ListAPIView):
	permission_classes=[AllowAny]
	"""
	API que obtiene un listado de ciclos de egreso de una escuela o facultad específica.
	"""

	serializer_class = DBCicloSerializer
	
	def get_queryset(self):
		p_escuela		= self.kwargs.get('escuela', None)
		if p_escuela is not None:
			# Consultamos la tabla de mov_alumno de la escuela con estatus de EGRESO
			movAlumEgre = DBMovAlumnos.objects.using('escolares')\
								.filter(escuela=p_escuela)\
								.filter(estatus=7)
			# Consultamos los ciclos que estén en la consulta de arriba
			queryset = DBCiclo.objects.using('escolares')\
								.filter(ciclo__in=Subquery(movAlumEgre.values('ciclo')))\
								.order_by('ciclo')
			return queryset



class searchAlumnos(generics.ListAPIView):
	permission_classes=[AllowAny]
	"""
	API que obtiene un listado de alumnos insccritos en una escuela específica. 
	Puede recibir como parámetros opcionales la matrícula, nombre, apellidos o semestre.
	"""

	serializer_class = AlumnosSerializer
	
	def get_queryset(self):
		escuela		= self.kwargs.get('escuela', None)
		matricula	= self.request.query_params.get('matricula', '''%%''')
		nombre		= self.request.query_params.get('nombre', '''%%''')
		apellido	= self.request.query_params.get('apellido', '''%%''')
		semestre	= self.request.query_params.get('semestre', None)

		if escuela is not None:
			consulta = ""
			if semestre is not None:
				if len(str(semestre)) == 1:
					consulta = """ and ta.semestre = """ + str(semestre) + """ and ta.cve_ciclo in (select cve_ciclo from desarrollo.ciclo where sysdate between f_inicial and f_final and cve_tipo_ciclo = 2) """
				else:
					consulta = """ and ta.cve_estatus = 7 and ta.cve_ciclo = '""" + semestre + """' """

			queryset = DatosAlumnos.objects.using('escolares').raw(
				"""
					select trim(ta.cve_alumno) as matricula, tb.nombre, tb.paterno, tb.materno
					from desarrollo.mov_alumno ta, desarrollo.alumno tb, desarrollo.ciclo tc
					where trim(ta.cve_alumno) = trim(tb.cve_alumno) and ta.cve_ciclo = tc.cve_ciclo
					and ta.cve_escuela = %s 
					and trim(tb.cve_alumno) like '%%""" + matricula + """%%'
					and tb.nombre like '%%""" + nombre + """%%'
					and tb.paterno||' '||tb.materno like '%%""" + apellido + """%%'
				"""
				+ consulta +
				""" 
					group by ta.cve_alumno, tb.nombre, tb.paterno, tb.materno
					order by tb.paterno
				""",
				[escuela]
			)
			return queryset



class countAlumnos(generics.ListAPIView):
	permission_classes=[AllowAny]
	"""
	API que obtiene un conteo de alumnos activos e inactivos de una escuela o facultad en el ciclo actual.
	"""
	serializer_class = ContarSerializer
	def get_queryset(self):
		p_escuela		= self.kwargs.get('escuela', None)
		if p_escuela is not None:
			queryset = ContarAlumnos.objects.using('escolares').raw(
			 	"""
			 		with
			 			total as
			 				(select ta.cve_escuela as escuela, count(*) as total
			 					from desarrollo.mov_alumno ta
			 					where ta.cve_escuela = %s
			 					and ta.fecha_mov = (select max(fecha_mov) from desarrollo.mov_alumno tx where tx.cve_escuela = ta.cve_escuela and tx.cve_alumno = ta.cve_alumno)
			 					group by ta.cve_escuela),
			 			activos as
			 				(select ta.cve_escuela as escuela, count(*) as activos
			 					from desarrollo.mov_alumno ta
			 					where ta.cve_escuela = %s
			 					and ta.cve_estatus in (1,2,5,7)
			 					and ta.fecha_mov = (select max(fecha_mov) from desarrollo.mov_alumno tx where tx.cve_escuela = ta.cve_escuela and tx.cve_alumno = ta.cve_alumno)
			 					group by ta.cve_escuela)
			 		select ta.escuela, ta.total, nvl(tb.activos,0) as activos, (ta.total-nvl(tb.activos,0)) as bajas 
			 		from total ta, activos tb
			 		where ta.escuela = tb.escuela(+)
			 	""",
			 	[p_escuela, p_escuela]
			)
			return queryset



class getEstadistica(generics.ListAPIView):
	permission_classes=[AllowAny]c
	"""
	API que obtiene listado de alumnos activos e inactivos de una escuela o facultad. 
 	Se recibe como parámetro la clave del ciclo a consultar o el número de semestre en el ciclo actual.
	"""
	serializer_class = EstadisticaSerializer
	
	def get_queryset(self):
		p_escuela = self.kwargs.get('escuela', None)
		p_ciclo = self.request.query_params.getlist('semestre', None)
		
		bandera_semestres=False
		# Si viene 1, 2, 3..., se trabaja sobre el ciclo actual, de lo contrario por los ciclos recibidos
		if len(p_ciclo[0]) == 1:
			bandera_semestres=True
			today = date.today()
			lCiclos = [obj for obj in DBCiclo.objects.using('escolares').filter(cve_tipo_ciclo=2)\
									.filter(f_inicial__lte=today).filter(f_final__gte=today) 
						if obj.ciclo_desc[2:3] != '-']
		else:
			bandera_semestres=False
			lCiclos = DBCiclo.objects.using('escolares').filter(cve_tipo_ciclo=2).filter(ciclo__in=p_ciclo).order_by('ciclo')
		
		for v_ciclo in lCiclos:
			if bandera_semestres:
				# Se obtienen los alumnos inscrito, reinscritos, titulados, egresados y de movilidad en el semestre
				lAct = DBMovAlumnos.objects.using('escolares').filter(escuela=p_escuela).filter(ciclo=v_ciclo.ciclo)\
									.filter(estatus__in=(1,2,5,7,8,9)).filter(semestre__in=p_ciclo)
				# Se obtienen las bajas del ciclo y semestre
				lINAct = DBMovAlumnos.objects.using('escolares').filter(escuela=p_escuela).filter(ciclo=v_ciclo.ciclo)\
									.filter(estatus__in=(3,4)).filter(semestre__in=p_ciclo)
			else:
				# Se obtienen los egresados del ciclo
				lAct = DBMovAlumnos.objects.using('escolares').filter(escuela=p_escuela).filter(ciclo=v_ciclo.ciclo)\
									.filter(estatus=7)
				# Se obtienen las bajas del ciclo
				lINAct = DBMovAlumnos.objects.using('escolares').filter(escuela=p_escuela).filter(ciclo=v_ciclo.ciclo)\
									.filter(estatus__in=(3,4))

			v_ciclo.activos = lAct
			v_ciclo.inactivos = lINAct
		return lCiclos



class getAlumno(generics.ListAPIView):
	permission_classes=[AllowAny]
	def get_queryset(self):
		if request.method == 'POST':
			buscado=request.POST
			print(buscado['nombe'])
