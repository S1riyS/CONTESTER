from flask import Blueprint, render_template, request

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

# Admin
@admin.route('/')
def home_page():
    return render_template('admin/admin.html')

@admin.route('/create_task', methods=['GET', 'POST'])
def create_task_page():
    return render_template('admin/create_task.html')