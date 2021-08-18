from rest_framework import generics

from .models import DatosAlumnoPorEgresar
from .serializers import DatosAlumnoPorEgresarSerializer


class getDatosAlumnoPorEgresar(generics.ListAPIView):
	"""
	
	Obtiene los datos del alumno que esta por egresar en un ciclo determinado
	
	"""
	serializer_class = DatosAlumnoPorEgresarSerializer
	
	def get_queryset(self):
		ciclo	= self.kwargs.get('ciclo', None)
		if ciclo is not None:
			matricula = self.kwargs.get('matricula', None)
			if matricula is not None:
				queryset = DatosAlumnoPorEgresar.objects.raw(
					"""
						select trim(ta.cve_alumno) as matricula, trim(tb.nombre) as nombre, trim(tb.paterno) as paterno, trim(tb.materno) as materno,
								trim(trim(tb.nombre||' '||tb.paterno)||' '||tb.materno) as nombre_completo,
								tb.sexo, to_char(tb.f_nacimiento, 'dd/mm/yyyy') as f_nacimiento,
								tb.cve_edo_nac as cve_estado, tc.desc_edo as estado,
								tb.cve_mun_nac as cve_municipio, td.desc_mun as municipio,
								trim(tb.calle) as calle, trim(tb.colonia) as colonia,
								trim(tb.telefono) as telefono, trim(tb.tel_cel) as celular,
								ta.cve_escuela, te.desc_escuela as escuela,
								ta.cve_carrera, tf.desc_carrera as carrera
						from desarrollo.mov_alumno ta, desarrollo.alumno tb, desarrollo.estado tc, desarrollo.municipio td,
								desarrollo.escuela te, desarrollo.carrera tf, desarrollo.plan_estudio tg
						where trim(ta.cve_alumno) = trim(tb.cve_alumno)
						and tb.cve_edo_nac = tc.cve_edo
						and tb.cve_edo_nac = td.cve_edo and tb.cve_mun_nac = td.cve_mun
						and ta.cve_escuela = te.cve_escuela
						and ta.cve_escuela = tf.cve_escuela and ta.cve_carrera = tf.cve_carrera
						and ta.cve_escuela = tg.cve_escuela and ta.cve_carrera = tg.cve_carrera and ta.cve_plan = tg.cve_plan
						and tf.cve_nivel = '1300'
						and ta.cve_estatus not in (3, 4, 5, 7)
						and ta.semestre = tg.num_ciclos
						and ta.cve_ciclo = %s
						and trim(ta.cve_alumno) = %s
					""", [ciclo, matricula]
				)
			return queryset
