import os
import random
from fdfgen import forge_fdf

fields = [('SameFamilyCB', '/Yes')]

fdf = forge_fdf(
    pdf_form_url='',
    fdf_data_strings=[('SameChildCB', 'Yes')],
)
with open('fdf/po_appdata.fdf', 'wb') as f:
    f.write(fdf)

status = os.system(
    'pdftk fdf/po_application_form.pdf fill_form fdf/po_appdata.fdf output po_application_complete' + str(random.randint(0, 100)) + '.pdf'
)
