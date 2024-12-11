# donations.py
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .db import get_db  # 确保从项目的根目录导入 db

donations_bp = Blueprint('donations', __name__)

@donations_bp.route('/accept_donation', methods=['GET', 'POST'])
@login_required
def accept_donation():
    if current_user.role != 'volunteer':
        flash('Only volunteers can accept donations.', 'danger')
        return redirect(url_for('auth.index'))

    if request.method == 'POST':
        description = request.form.get('description')
        price = request.form.get('price')
        quantity = request.form.get('quantity')

        if not description or not price or not quantity:
            flash('All fields are required.')
            return redirect(url_for('donations.accept_donation'))

        try:
            price = float(price)
            quantity = int(quantity)

            db = get_db()
            cursor = db.cursor()

            cursor.execute(
                'INSERT INTO Items (description, price, stockQuantity, donator) VALUES (%s, %s, %s, %s)',
                (description, price, quantity, current_user.username)
            )
            db.commit()
            flash('Donation successfully accepted.', 'success')
            return redirect(url_for('auth.index'))
        except ValueError:
            flash('Invalid input for price or quantity.', 'danger')
            return redirect(url_for('donations.accept_donation'))
        except Exception as e:
            db.rollback()
            flash(f'Error accepting donation: {str(e)}', 'danger')
            return redirect(url_for('donations.accept_donation'))

    return render_template('donations/accept_donation_form.html')


@donations_bp.route('/view_donations')
@login_required
def view_donations():
    if current_user.role != 'staff':
        flash('Only staff members can view donations.', 'danger')
        return redirect(url_for('auth.index'))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # 查询 Items 表并包含捐赠人信息
    cursor.execute(
        'SELECT i.itemId, i.description, i.price, i.stockQuantity, i.donator '
        'FROM Items i'
    )
    donations = cursor.fetchall()

    return render_template('donations/view_donations.html', donations=donations)