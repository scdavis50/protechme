from flask import Flask, render_template, request, redirect
from form_processor import process_application_form

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/po_application_form', methods=("GET", "POST"))
def po_application_form():
    if request.method == 'POST':
        process_application_form(
            form=request.form,
            fdf_file='fdf/po_appdata.fdf',
            form_type='po_application_form'
        )
        return redirect("success")
    return render_template('po_application_form.html')

@app.route('/protective_order_form', methods=("GET", "POST"))
def protective_order_form():
    if request.method == 'POST':
        process_application_form(
            form=request.form,
            fdf_file='fdf/po_data.fdf',
            form_type='protective_order_form'
        )
        return redirect("success")
    return render_template('protective_order_form.html')

@app.route('/temporary_exparteorder', methods=("GET", "POST"))
def temporary_exparteorder():
    if request.method == 'POST':
        process_application_form(
            form=request.form,
            fdf_file='fdf/exparte_data.fdf',
            form_type='temporary_exparteorder'
        )
        return redirect("success")
    return render_template('temporary_exparte_form.html')

@app.route('/success')
def success():
    return render_template('success.html')
