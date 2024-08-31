from pathlib import Path as path

from gpddatabase.Exceptions import ExceptionNoDirectory
from gpddatabase.Exceptions import ExceptionNotWritable

#since object members in this class are created dynamically, disable pylint error with:
#pylint: disable=no-member
class MarkdownExclusiveDatabase:

	''' Markdown functionalities of ExclusiveDatabase class.'''

	def convert_to_markdown(self, directory):

		''' Get markdown representation.'''

		#result
		output = ''

		output += '# Available datasets' + '\n'
		output += '\n'

		#check if directory exist
		if not path(directory).is_dir():
			raise ExceptionNoDirectory(directory)

		#loop over all files
		for uuid in self.get_uuids():

			#get object
			dataObject = self.get_data_object(uuid)

			#print
			output += '[' + uuid + '](' + 'file_' + uuid + '.markdown' + ')' + '\n'

			#write
			try:

				with open(directory + '/file_' + uuid + '.markdown', 'w', encoding="utf-8") as file:
					print(dataObject.convert_to_markdown(), file=file)

			except FileNotFoundError as err:
				raise ExceptionNotWritable(directory) from err

		#write
		try:

			with open(directory + '/data_sets.markdown', 'w', encoding="utf-8") as file:
				print(output, file=file)

		except FileNotFoundError as err:
			raise ExceptionNotWritable(directory) from err
