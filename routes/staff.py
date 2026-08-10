from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from models import *

staff_Bp = Blueprint('staff', __name__)

@staff_Bp.route('/staffdashboard')
@login_required
def staffdashboard():
    assigned_treks = Trek.query.filter_by(staff_id=current_user.id).all()
    alen = len(assigned_treks)
    total_users = User.query.filter_by(role=Role.trekker).count()
    open_treks = Trek.query.filter_by(status=TrekStatus.open).count()
    participants = Booking.query.filter_by(trek_id=current_user.id).count()
    return render_template('staff_dashboard.html', name=current_user.username, assigned_treks=assigned_treks, total_users=total_users, 
                           open_treks=open_treks, participants=participants, alen=alen)
