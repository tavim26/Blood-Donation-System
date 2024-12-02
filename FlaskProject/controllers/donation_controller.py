import random
from flask import url_for, redirect, flash, request, session
from extensions import db
from models.blood_stock import BloodStock
from models.donation import Donation
from models.donor import Donor
from models.eligibility_form import EligibilityForm
from models.schedule import Schedule

def create_donation_controller(app):
    @app.route("/create/donation/<int:schedule_id>", methods=['GET', 'POST'])
    def create_donation(schedule_id: int):

        donor_id = session.get('user_id')

        try:
            # Obține schedule, donor și eligibility_form într-un singur bloc
            schedule = Schedule.query.filter_by(ScheduleID=schedule_id).first_or_404()
            donor = Donor.query.filter_by(DonorID=schedule.DonorID).first_or_404()
            eligibility_form = EligibilityForm.query.filter_by(FormID=schedule.FormID).first_or_404()

            # Calculăm cantitatea pe baza greutății
            weight = eligibility_form.Weight
            quantity = random.randint(350, 450) if weight > 50 else random.randint(250, 350)

            # Creăm o nouă donație
            new_donation = Donation(
                ScheduleID=schedule.ScheduleID,
                BloodGroup=eligibility_form.BloodGroup,
                Quantity=quantity,
                DonationDate=schedule.AppointmentDate,
                Status='pending'
            )

            db.session.add(new_donation)
            schedule.Status = 'completed'
            db.session.commit()
            flash('Donation created successfully!', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('donor_dashboard',id=donor_id))

        return redirect(url_for('donor_dashboard',id=donor_id))




    @app.route("/complete/donation/<int:id>", methods=['GET', 'POST'])
    def complete_donation(id: int):
        donation = Donation.query.filter_by(DonationID=id).first_or_404()

        assistant_id = session.get('user_id')

        if request.method == 'POST':
            # Actualizăm statusul donației și stocul de sânge
            donation.Status = 'completed'
            blood_stock = BloodStock.query.filter_by(BloodGroup=donation.BloodGroup).first()

            if blood_stock:
                blood_stock.QuantityInStock += donation.Quantity
            else:
                db.session.add(BloodStock(BloodGroup=donation.BloodGroup, QuantityInStock=donation.Quantity))

            try:
                db.session.commit()
                flash('Donation status updated to completed and blood stock incremented.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred: {str(e)}', 'error')

            return redirect(url_for('assistant_dashboard',id=assistant_id))

        flash('Please use the form to complete a donation.', 'info')
        return redirect(url_for('assistant_dashboard',id=assistant_id))




    @app.route("/return/donation/<int:id>", methods=['GET', 'POST'])
    def return_donation(id: int):
        donation = Donation.query.filter_by(DonationID=id).first_or_404()

        assistant_id = session.get('user_id')

        if request.method == 'POST':
            # Actualizăm statusul donației
            donation.Status = 'returned'
            try:
                db.session.commit()
                flash('Donation status updated to returned.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred: {str(e)}', 'error')

            return redirect(url_for('assistant_dashboard',id=assistant_id))

        flash('Please use the form to return a donation.', 'info')
        return redirect(url_for('assistant_dashboard',id=assistant_id))




    @app.route('/delete/donation/<int:donation_id>', methods=['GET'])
    def delete_donation(donation_id):
        donation = Donation.query.get_or_404(donation_id)
        blood_group = donation.BloodGroup
        quantity = donation.Quantity
        admin_id = session.get('user_id')

        try:
            db.session.delete(donation)
            blood_stock = BloodStock.query.filter_by(BloodGroup=blood_group).first()

            if blood_stock:
                blood_stock.QuantityInStock = max(blood_stock.QuantityInStock - quantity, 0)

            db.session.commit()
            flash('Donation deleted and stock updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting donation: {str(e)}', 'danger')

        return redirect(url_for('admin_dashboard',id=admin_id))
