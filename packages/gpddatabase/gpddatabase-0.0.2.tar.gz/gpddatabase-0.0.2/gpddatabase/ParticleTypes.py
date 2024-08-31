from particle import Particle
from particle import ParticleNotFound

from gpddatabase.Exceptions import ExceptionUnknownType

class ParticleTypes:

	'''Class defining particle types. Uses python 'particle' library.'''

	def check_type(self, value):

		'''Check if type exist. If not, raise exception.'''

		try:
			Particle.findall(value)
		except ParticleNotFound as err:
			raise ExceptionUnknownType(value) from err

	def get_description(self, value):

		'''Get description of a given type.'''

		try:
			return Particle.findall(value).name
		except ParticleNotFound as err:
			raise ExceptionUnknownType(value) from err

	def get_particle(self, value):

		'''Get 'Particle' object (see 'particle' library) for a given type.'''

		try:
			return Particle.findall(value)
		except ParticleNotFound as err:
			raise ExceptionUnknownType(value) from err
