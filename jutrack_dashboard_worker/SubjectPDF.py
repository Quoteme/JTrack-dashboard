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
        """
        prints a header of a new page (executed if pdf.add_page())

        :return:
        """

        # Arial bold 15
        self.set_font('Arial', size=18)
        # Title
        self.cell(180, 10, self.subject_name, ln=1, align='C')
        # Line break
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(10)
        self.set_font("Arial", size=12)

    def draw_input_line(self, input_name):
        """
        Draws a line which serves as a input field where you can write several information

        :param input_name: Corresponding name of the input
        :return:
        """

        self.cell(40, 10, txt=input_name, ln=0, align='L')
        self.cell(1, 10, txt=':', ln=0)
        self.line(self.get_x() + 3, self.get_y() + 7, self.get_x() + 60, self.get_y() + 7)
        self.ln(10)

    def draw_input_line_filled(self, input_name, write_on_line_text):
        """
        Draws a line which serves as a input field where you can write several information. Input field will be written already

        :param input_name: Corresponding name of the input
        :param write_on_line_text: Text which should be written on the line
        :return:
        """

        self.cell(40, 10, txt=input_name, ln=0, align='L')
        self.cell(1, 10, txt=':', ln=0)
        self.line(self.get_x() + 3, self.get_y() + 7, self.get_x() + 60, self.get_y() + 7)
        self.cell(63, 10, txt=write_on_line_text, ln=0, align='C')
        self.ln(10)

    def text_field(self, text):
        """
        Draws text field

        :param text: text to display
        :return:
        """

        self.cell(40, 10, txt=text, ln=0, align='L')
        self.ln(10)

    def qr_code(self, qr_code_path, number_codes):
        """
        Draws all 4 qr codes for different activations

        :param qr_code_path: path to qr_code to img file. Only needs the activation number to be completed
        :param number_codes: number of activation codes (4)
        :return:
        """
        for i in range(1, number_codes):
            self.text_field('Activation ' + str(i))
            self.draw_input_line('Date of activation')
            self.image(qr_code_path + '_' + str(i) + '.png', x=140, y=75 + (i - 1) * 40, w=40)
            self.ln(20)
