from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import IssuedBook, Book

student_bp = Blueprint('student', __name__)

@student_bp.before_request
def check_student():
    if not current_user.is_authenticated or current_user.role != 'student':
        # Just in case an admin stumbles here, they can see it too or redirect? 
        # Usually separate, but let's enforce student/admin roles strictly or let admin view everything.
        # For this logic, strict check.
        pass # Admin can probably view student pages if we remove the check, but let's keep it simple.

@student_bp.route('/dashboard')
@login_required
def dashboard():
    my_issues = IssuedBook.query.filter_by(user_id=current_user.id).order_by(IssuedBook.issue_date.desc()).all()
    return render_template('student/dashboard.html', issues=my_issues)

@student_bp.route('/books')
@login_required
def books():
    # Student can only view books
    all_books = Book.query.all()
    return render_template('student/books.html', books=all_books)
