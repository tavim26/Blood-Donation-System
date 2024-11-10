from flask import render_template, request, redirect, url_for
from database import db
from models.donor import Donor
from models.eligibility_form import EligibilityForm


def create_formular_controller(app):
    @app.route('/form/details/<int:FormID>', methods=['GET'])
    def form_details(FormID):
        # Caută formularul în baza de date
        form = EligibilityForm.query.get(FormID)

        # Renderizează un template pentru a afișa detaliile formularului
        return render_template('assistant/form_details.html', form=form)


    @app.route('/create/form/<int:id>', methods=['GET', 'POST'])
    def create_form(id: int):
        donor = Donor.query.get(id)

        if request.method == 'POST':
            try:
                form_name = request.form['name']
                blood_group = request.form['blood_group']
                age = int(request.form['age'])
                gender = request.form['gender']
                weight = int(request.form['weight'])
                notes = request.form.get('notes', '')

                new_form = EligibilityForm(
                    DonorID=id,
                    FormName=form_name,
                    BloodGroup=blood_group,
                    Age=age,
                    Gender=gender,
                    Weight=weight,
                    Notes=notes,
                    IsEligible=True
                )

                db.session.add(new_form)
                db.session.commit()

                return redirect(url_for('donor_dashboard'))  # Poți redirecționa către donor_dashboard

            except Exception as e:
                str(e)

        forms = EligibilityForm.query.filter_by(DonorID=id).all()  # Adaugă lista de formulare
        return render_template('donor/form_create.html', donor_id=id, forms=forms)
