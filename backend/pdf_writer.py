import os
import textwrap
from fpdf import FPDF

WRITE_FILE_PATH = 'resume.pdf'

resume = """
Write me Outstanding Resume for [JOB] based on my [RESUME] 

[RESUME]
Here is my resume: 

Education 
Bobir Akilkhanov Academy Ai/ML 
GPA: 9/10 

New Uzbekistan University 
Software Engineering
GPA: 4.6/5 

Academic test results IELTS IDP

Research 
New Uzbekistan University AyoobkhanMohamedUvazeAhamed m.u.ahamed@wiut.uz

[JOB]
Here is Job: 

Snap Inc. is a technology company. We believe the camera presents the greatest opportunity to improve the way people live and communicate. We contribute to human progress by empowering people to express themselves, live in the moment, learn about the world, and have fun together. We are looking for Apprentices to join an Engineering program at Snap Inc. called Snap Up. Snap Up is a full time 11 month engineering rotational program created by Snap to provide career development opportunities to new graduates with limited or no technical software engineering work experience. Snap Up is designed to provide Apprentices with on-the-job training and close mentorship opportunities that maximize opportunity to level up into engineering professional roles. This program requires you to be in office at least four days a week at any one of our major engineering office locations: Santa Monica, New York City, Palo Alto, or Seattle.
"""

def clear_text(text):
    text = text.replace('•', '')
    text = text.replace('_', '')
    text = text.replace('-', '')
    text = text.replace('—', '')
    text = text.replace('Proof:ZView', '')
    text = text.replace('Proof: ZView', '')
    text = text.replace('Proof:Z View', '')
    text = text.replace('Proof: Z View', '')

    return text


def get_pdf(prompt):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Courier', size=fontsize_pt)

    prompt = clear_text(prompt)
    splitted = prompt.split('\n')

    for line in splitted:
        lines = textwrap.wrap(line, int(width_text))

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)

    pdf.output(WRITE_FILE_PATH, 'F') # type: ignore
    
    return WRITE_FILE_PATH


# get_pdf(resume)