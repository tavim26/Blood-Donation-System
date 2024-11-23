from flask import request, render_template, redirect, url_for, session, flash
from models.donor import Donor
from models.eligibility_form import EligibilityForm, db
from models.schedule import Schedule


def create_formular_controller(app):


    @app.route('/view/form/<int:id>', methods=['GET'])
    def form_details(id:int):

        form = EligibilityForm.query.get_or_404(id)

        return render_template('assistant/form_view.html', form=form)




    @app.route("/create/form/<int:id>", methods=['GET', 'POST'])
    def create_form(id: int):

        donor = Donor.query.get_or_404(id)

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

                return redirect(url_for('donor_dashboard'))

            except Exception as e:
                print(str(e))

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

        return redirect(url_for('assistant_dashboard'))





    @app.route("/delete/form/<int:form_id>")
    def delete_form(form_id):
        form = EligibilityForm.query.get_or_404(form_id)
        attached_schedule = Schedule.query.filter_by(FormID=form_id).first()

        if attached_schedule:
            flash('Cannot delete this form as it is associated with a schedule.', 'danger')
            return redirect(url_for('donor_dashboard'))

        try:
            db.session.delete(form)
            db.session.commit()
            flash('Form deleted successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

        return redirect(url_for('donor_dashboard'))