from flask import request, render_template, redirect, url_for, session, flash, jsonify


from models.notification import Notification

from extensions import db



def create_notification_controller(app):

    @app.route("/delete/notification/<int:notification_id>", methods=["GET"])
    def delete_notification(notification_id: int):
        notification = Notification.query.get_or_404(notification_id)

        try:
            db.session.delete(notification)
            db.session.commit()
            flash('Notification deleted successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while deleting the notification: {str(e)}', 'error')

        return redirect(url_for('donor_dashboard', id=session.get('user_id')))




