from io import BytesIO
from flask import request, render_template, redirect, url_for, session, flash, send_file, abort, jsonify
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from models.donor import Donor
from models.eligibility_form import EligibilityForm, db
from models.schedule import Schedule


def create_formular_controller(app):
    @app.route('/view/form/<int:id>', methods=['GET'])
    def form_details(id: int):
        form = EligibilityForm.query.get_or_404(id)
        return render_template('assistant/form_view.html', form=form)

    @app.route("/create/form/<int:id>", methods=['GET', 'POST'])
    def create_form(id: int):
        donor = Donor.query.get_or_404(id)

        if request.method == 'POST':
            try:
                # Obține datele din formular
                form_name = f"Form_{donor.user.FirstName}{donor.user.LastName}_{id}"  # Numele formularului automat
                blood_group = request.form['blood_group']
                age = int(request.form['age'])
                gender = request.form['gender']
                weight = int(request.form['weight'])
                notes = request.form.get('notes', '')

                # Creează formularul de eligibilitate
                new_form = EligibilityForm(
                    DonorID=id,
                    FormName=form_name,  # Setează numele formularului automat
                    BloodGroup=blood_group,
                    Age=age,
                    Gender=gender,
                    Weight=weight,
                    Notes=notes,
                    IsEligible=True
                )

                # Adaugă formularul în baza de date
                db.session.add(new_form)
                db.session.commit()

                return jsonify(
                    {'success': True, 'redirect_url': url_for('donor_dashboard', id=session.get('user_id'))}), 200

            except Exception as e:
                print(str(e))  # Tratează eroarea, dacă există
                return jsonify({'success': False, 'message': 'An error occurred while creating the form.'}), 500
        else:
            return render_template('donor/form_create.html', donor=donor)




    @app.route('/update/form/<int:form_id>', methods=['POST'])
    def update_form(form_id):
        form = EligibilityForm.query.get_or_404(form_id)

        try:
            form.IsEligible = request.form['eligibility'] == 'true'
            db.session.commit()
            flash('Form updated successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')

        return redirect(url_for('assistant_dashboard', id=session.get('user_id')))



    @app.route("/delete/form/<int:form_id>")
    def delete_form(form_id):
        form = EligibilityForm.query.get_or_404(form_id)
        attached_schedule = Schedule.query.filter_by(FormID=form_id).first()

        if attached_schedule:
            flash('Cannot delete this form as it is associated with a schedule.', 'danger')
            return redirect(url_for('donor_dashboard', id=session.get('user_id')))

        try:
            db.session.delete(form)
            db.session.commit()
            flash('Form deleted successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

        return redirect(url_for('donor_dashboard', id=session.get('user_id')))



    @app.route('/form/download/<int:form_id>', methods=['GET'])
    def download_eligibility_form(form_id):
        form = EligibilityForm.query.get_or_404(form_id)
        donor = Donor.query.get_or_404(form.DonorID)

        if not donor or not donor.user:
            abort(404, description="Donor or User not found")

        user = donor.user
        donor_full_name = f"{user.FirstName} {user.LastName}"

        buffer = BytesIO()

        pdf = canvas.Canvas(buffer, pagesize=letter)

        data = [
            ['Field', 'Value'],
            ['Form ID', form.FormID],
            ['Donor Name', donor_full_name],
            ['Form Name', form.FormName],
            ['Blood Group', form.BloodGroup],
            ['Age', form.Age],
            ['Gender', form.Gender],
            ['Weight', form.Weight],
            ['Is Eligible', 'Yes' if form.IsEligible else 'No'],
            ['Notes', form.Notes]
        ]

        table = Table(data, colWidths=[2 * inch, 4 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        table.wrapOn(pdf, 0, 0)
        table.drawOn(pdf, inch, 600)

        pdf.showPage()
        pdf.save()

        buffer.seek(0)

        return send_file(buffer, as_attachment=True, download_name='eligibility_form.pdf', mimetype='application/pdf')
