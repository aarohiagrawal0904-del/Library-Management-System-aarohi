from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Book, IssuedBook, User
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
def check_admin():
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash('Access Denied: Admins only.', 'danger')
        return redirect(url_for('main.home'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    total_books = Book.query.count()
    issued_books = IssuedBook.query.filter_by(status='issued').count()
    total_users = User.query.filter_by(role='student').count()
    
    recent_issues = IssuedBook.query.order_by(IssuedBook.issue_date.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                           total_books=total_books, 
                           issued_books=issued_books, 
                           total_users=total_users,
                           recent_issues=recent_issues)

@admin_bp.route('/books')
@login_required
def books():
    all_books = Book.query.all()
    return render_template('admin/books.html', books=all_books)

@admin_bp.route('/books/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        category = request.form.get('category')
        quantity = int(request.form.get('quantity'))
        
        book = Book(title=title, author=author, isbn=isbn, category=category, 
                    quantity=quantity, available_quantity=quantity)
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('admin.books'))
    return render_template('admin/add_book.html')

@admin_bp.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.isbn = request.form.get('isbn')
        book.category = request.form.get('category')
        quantity_diff = int(request.form.get('quantity')) - book.quantity
        book.quantity = int(request.form.get('quantity'))
        book.available_quantity += quantity_diff
        
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('admin.books'))
    return render_template('admin/edit_book.html', book=book)

@admin_bp.route('/books/delete/<int:book_id>')
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('admin.books'))

@admin_bp.route('/issue', methods=['GET', 'POST'])
@login_required
def issue_book():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        book_id = request.form.get('book_id')
        due_date_str = request.form.get('due_date')
        
        book = Book.query.get(book_id)
        user = User.query.get(user_id)
        
        if not book or not user:
            flash('Invalid Book or User ID', 'danger')
            return redirect(url_for('admin.issue_book'))
            
        if book.available_quantity < 1:
            flash('Book not available', 'warning')
            return redirect(url_for('admin.issue_book'))

        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        
        issue = IssuedBook(user_id=user.id, book_id=book.id, due_date=due_date)
        book.available_quantity -= 1
        
        db.session.add(issue)
        db.session.commit()
        flash('Book issued successfully', 'success')
        return redirect(url_for('admin.dashboard'))
        
    books = Book.query.filter(Book.available_quantity > 0).all()
    users = User.query.filter_by(role='student').all()
    return render_template('admin/issue_book.html', books=books, users=users)

@admin_bp.route('/return/<int:issue_id>')
@login_required
def return_book(issue_id):
    issue = IssuedBook.query.get_or_404(issue_id)
    if issue.status == 'returned':
        flash('Book already returned', 'info')
        return redirect(url_for('admin.dashboard'))
        
    issue.status = 'returned'
    issue.return_date = datetime.utcnow()
    
    # Calculate fine (simple logic: 10 units per day late)
    if issue.return_date.date() > issue.due_date:
        days_late = (issue.return_date.date() - issue.due_date).days
        issue.fine = days_late * 10.00
        
    issue.book.available_quantity += 1
    db.session.commit()
    flash(f'Book returned successfully. Fine: {issue.fine}', 'success')
    return redirect(url_for('admin.dashboard'))
