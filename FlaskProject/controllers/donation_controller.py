import random
from flask import url_for, redirect, flash, request
from database import db
from models.blood_stock import BloodStock
from models.donation import Donation
from models.donor import Donor
from models.eligibility_form import EligibilityForm
from models.schedule import Schedule


def create_donation_controller(app):
    @app.route("/create/donation/<int:schedule_id>", methods=['GET', 'POST'])
    def create_donation(schedule_id: int):
        print(f"Received request to create donation for schedule_id: {schedule_id}")

        if request.method == 'POST':
            # Obține schedule-ul pe baza schedule_id
            schedule = Schedule.query.filter_by(ScheduleID=schedule_id).first()
            if not schedule:
                flash('Schedule not found', 'error')
                print("Schedule not found")
                return redirect(url_for('donor_dashboard'))

            # Obține donor-ul pe baza schedule-ului
            donor = Donor.query.filter_by(DonorID=schedule.DonorID).first()
            if not donor:
                flash('Donor not found', 'error')
                print("Donor not found")
                return redirect(url_for('donor_dashboard'))

            # Obține formularul de eligibilitate
            eligibility_form = EligibilityForm.query.filter_by(FormID=schedule.FormID).first()
            if not eligibility_form:
                flash('Eligibility form not found', 'error')
                print("Eligibility form not found")
                return redirect(url_for('donor_dashboard'))

            print("All required data found, creating donation...")

            # Calculează cantitatea pe baza greutății (utilizând o valoare aleatorie în interval)
            weight = eligibility_form.Weight
            quantity = random.randint(350, 450) if weight > 50 else random.randint(250, 350)

            # Creează o nouă donație
            new_donation = Donation(
                ScheduleID=schedule.ScheduleID,
                BloodGroup=eligibility_form.BloodGroup,
                Quantity=quantity,
                DonationDate=schedule.AppointmentDate,
                Status='pending'
            )

            try:
                db.session.add(new_donation)
                schedule.Status = 'completed'
                db.session.commit()
                flash('Donation created successfully!', 'success')
                print("Donation created successfully")
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred creating the donation: {str(e)}', 'error')
                print(f'An error occurred: {str(e)}')

            return redirect(url_for('donor_dashboard'))
        else:
            # Manages the GET request here if needed
            flash('Please use the form to create a donation.', 'info')
            return redirect(url_for('donor_dashboard'))




    @app.route("/complete/donation/<int:id>", methods=['GET', 'POST'])
    def complete_donation(id: int):
        donation = Donation.query.filter_by(DonationID=id).first()
        if not donation:
            flash('Donation not found', 'error')
            return redirect(url_for('assistant_dashboard'))

        if request.method == 'POST':
            # Logica pentru cererea POST
            donation.Status = 'completed'
            blood_stock = BloodStock.query.filter_by(BloodGroup=donation.BloodGroup).first()
            if blood_stock:
                blood_stock.QuantityInStock += donation.Quantity
            else:
                blood_stock = BloodStock(BloodGroup=donation.BloodGroup, QuantityInStock=donation.Quantity)
                db.session.add(blood_stock)

            try:
                db.session.commit()
                flash('Donation status updated to completed and blood stock incremented.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred: {str(e)}', 'error')

            return redirect(url_for('assistant_dashboard'))
        else:
            flash('Please use the form to complete a donation.', 'info')
            return redirect(url_for('assistant_dashboard'))




    @app.route("/return/donation/<int:id>", methods=['GET', 'POST'])
    def return_donation(id: int):
        donation = Donation.query.filter_by(DonationID=id).first()
        if not donation:
            flash('Donation not found', 'error')
            return redirect(url_for('assistant_dashboard'))

        if request.method == 'POST':
            # Logica pentru cererea POST
            donation.Status = 'returned'
            try:
                db.session.commit()
                flash('Donation status updated to returned.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred: {str(e)}', 'error')

            return redirect(url_for('assistant_dashboard'))
        else:
            flash('Please use the form to return a donation.', 'info')
            return redirect(url_for('assistant_dashboard'))





    @app.route('/delete/donation/<int:donation_id>', methods=['GET'])
    def delete_donation(donation_id):
        # Găsirea donației
        donation = Donation.query.get_or_404(donation_id)

        # Obținerea informațiilor din donație
        blood_group = donation.BloodGroup
        quantity = donation.Quantity

        try:
            # Ștergerea donației
            db.session.delete(donation)

            # Actualizarea cantității din stocul total
            blood_stock = BloodStock.query.filter_by(BloodGroup=blood_group).first()
            if blood_stock:
                blood_stock.QuantityInStock = max(blood_stock.QuantityInStock - quantity,
                                                  0)  # Asigură-te că nu scade sub 0

            # Confirmarea modificărilor
            db.session.commit()
            flash('Donation deleted and stock updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting donation: {str(e)}', 'danger')

        # Redirecționare către pagina principală sau o altă pagină specifică
        return redirect(
            url_for('admin_dashboard'))