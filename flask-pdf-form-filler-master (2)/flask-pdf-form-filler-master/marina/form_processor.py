import os
import random
from fdfgen import forge_fdf
import time
from helpers import send_email

def process_application_form(form, fdf_file, form_type):
    fdf = forge_fdf(
        pdf_form_url='',
        fdf_data_strings=process_form(form),
        checkbox_checked_name='Yes'
    )
    with open(fdf_file, 'wb') as f:
        f.write(fdf)
    status = os.system(
        'pdftk ' + form_type + '.pdf fill_form ' + fdf_file + ' output ' + form_type + '_complete.pdf'
    )
    if status == 0:
        send_email(
            email=form['email'],
            message_type=form_type,
            file=form_type + '_complete.pdf'
        )

def process_form(form):
    items = [
        (item[0], ''.join(item[1])) for item in dict(form).items()
    ]
    buttons = process_buttons(items)
    text_boxes = list(filter(lambda item: 'CB' not in item[0], items))
    return text_boxes + buttons

def process_buttons(items):
    checkboxes = list(filter(lambda item: 'CB' in item[0], items))
    checkboxes = [(item[0], 'Yes') for item in checkboxes]
    radio_buttons = list(filter(lambda item: 'CBR' in item[0], items))
    return checkboxes + [
        process_item(item) for item in radio_buttons
    ]


def process_item(item):
    if item[1] == 'yes':
        return (item[0][:-3] + 'YesCB', 'Yes')
    return item[0]
    
