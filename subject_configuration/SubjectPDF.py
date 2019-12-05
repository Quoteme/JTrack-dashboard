from fpdf import FPDF


class SubjectPDF(FPDF):
	subject_name = 'Subject'

	def __init__(self, subj_name):
		super(SubjectPDF, self).__init__()
		self.subject_name = subj_name

	def header(self):
		# Arial bold 15
		self.set_font('Arial', size=18)
		# Title
		self.cell(180, 10, self.subject_name, ln=1, align='C')
		# Line break
		self.line(self.get_x(), self.get_y(), self.get_x()+190, self.get_y())
		self.ln(10)
		self.set_font("Arial", size=12)

	def draw_input_line(self, input_name):
		self.cell(40, 10, txt=input_name, ln=0, align='L')
		self.cell(1, 10, txt=':', ln=0)
		self.line(self.get_x() + 3, self.get_y() + 7, self.get_x() + 60, self.get_y() + 7)
		self.ln(10)

	def draw_input_line_filled(self, input_name, new_subj_name):
		self.cell(40, 10, txt=input_name, ln=0, align='L')
		self.cell(1, 10, txt=':', ln=0)
		self.line(self.get_x() + 3, self.get_y() + 7, self.get_x() + 60, self.get_y() + 7)
		self.cell(63, 10, txt=new_subj_name, ln=0, align='C')
		self.ln(10)

	def text_field(self, text):
		self.cell(40, 10, txt=text, ln=0, align='L')
		self.ln(10)
