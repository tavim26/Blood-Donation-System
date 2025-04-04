
from controllers import create_controllers
from controllers.admin_controller import create_admin_controllers
from controllers.assistant_controller import create_assistant_controllers
from controllers.donation_controller import create_donation_controller
from controllers.donor_controller import create_donor_controllers
from controllers.formular_controller import create_formular_controller
from controllers.notification_controller import create_notification_controller
from controllers.report_controller import create_report_controller
from controllers.schedule_controller import create_schedule_controller
from controllers.user_controller import create_user_controllers
from views import create_views


def register_controllers(app):
    try:
        create_views(app)
        create_controllers(app)
        create_user_controllers(app)
        create_admin_controllers(app)
        create_assistant_controllers(app)
        create_donor_controllers(app)
        create_schedule_controller(app)
        create_formular_controller(app)
        create_report_controller(app)
        create_donation_controller(app)
        create_notification_controller(app)

    except Exception as e:
        print(f"Error registering controllers: {e}")




