from fpdf import FPDF


class SubjectPDF(FPDF):
	"""
		This class specifies the pdf output format of subject study sheets. Several information like study name, the QR-Code
		to enroll and subject name are stored.
	"""
	subject_name = 'Subject'

	def __init__(self, subj_name):
		super(SubjectPDF, self).__init__()
		self.subject_name = subj_name

	def header(self):
		"""prints a header of a new page (executed if pdf.add_page())

		"""

		# Arial bold 15
		self.set_font('Arial', size=18)
		# Title
		self.cell(180, 10, self.subject_name, ln=1, align='C')
		# Line break
		self.line(self.get_x(), self.get_y(), self.get_x()+190, self.get_y())
		self.ln(10)
		self.set_font("Arial", size=12)

	def draw_input_line(self, input_name):
		"""Draws a line which serves as a input field where you can write several information

			Parameters
			----------
				input_name
					Corresponding name of the input.
		"""

		self.cell(40, 10, txt=input_name, ln=0, align='L')
		self.cell(1, 10, txt=':', ln=0)
		self.line(self.get_x() + 3, self.get_y() + 7, self.get_x() + 60, self.get_y() + 7)
		self.ln(10)

	def draw_input_line_filled(self, input_name, write_on_line_text):
		"""Draws a line which serves as a input field where you can write several information. Input field will be written already.

			Parameters
			----------
				input_name
					Corresponding name of the input.
				write_on_line_text
					Text which should be written on the line.
		"""

		self.cell(40, 10, txt=input_name, ln=0, align='L')
		self.cell(1, 10, txt=':', ln=0)
		self.line(self.get_x() + 3, self.get_y() + 7, self.get_x() + 60, self.get_y() + 7)
		self.cell(63, 10, txt=write_on_line_text, ln=0, align='C')
		self.ln(10)

	def text_field(self, text):
		"""Draws text field.

			Parameters
			----------
				text
					Text to display
		"""

		self.cell(40, 10, txt=text, ln=0, align='L')
		self.ln(10)
