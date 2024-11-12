from flask import request, render_template, redirect, url_for, session
from models.donor import Donor
from models.eligibility_form import EligibilityForm, db


def create_formular_controller(app):


    @app.route('/form/details', methods=['GET'])
    def form_details():
        form_id = session.get('form_id')
        form = EligibilityForm.query.get(form_id)

        return render_template('assistant/form_details.html', form=form)



    @app.route("/create/form/<int:id>", methods=['GET', 'POST'])
    def create_form(id: int):

        donor = Donor.query.get_or_404(id)  # Corectăm această linie

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
                print(str(e))  # Este bine să afișezi eroarea pentru debug

        else:
            return render_template('donor/form_create.html', donor=donor)
