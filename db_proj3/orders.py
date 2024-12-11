# orders.py
from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user
from .db import get_db
import mysql.connector

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/start_order', methods=['GET', 'POST'])
@login_required
def start_order():
    if current_user.role != 'staff':
        flash('Only staff members can start new orders.', 'danger')
        return redirect(url_for('auth.index'))

    if request.method == 'POST':
        client_username = request.form.get('client_username')

        if not client_username:
            flash('Client username cannot be empty.', 'warning')
            return render_template('orders/start_order_form.html')

        db = get_db()
        cursor = None
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                'INSERT INTO Orders (customerId, orderDate, status) VALUES (%s, NOW(), "start")',
                (client_username,)
            )
            db.commit()
            order_id = cursor.lastrowid
            session['order_id'] = order_id

            flash(f'Order successfully started for {client_username}.', 'success')
            return redirect(url_for('orders.add_to_current_order'))
        except Exception as e:
            db.rollback()
            flash(f'Error starting order: {str(e)}', 'danger')
            return render_template('orders/start_order_form.html')  # 返回当前表单页面
        finally:
            if cursor:
                cursor.close()

    return render_template('orders/start_order_form.html')

@orders_bp.route('/add_to_current_order', methods=['GET', 'POST'])
@login_required
def add_to_current_order():
    if current_user.role != 'staff':
        flash('Only staff members can add items to orders.', 'danger')
        return redirect(url_for('auth.index'))

    if 'order_id' not in session:
        flash('No active order found. Please start a new order first.', 'warning')
        return redirect(url_for('orders.start_order'))

    db = get_db()
    cursor = None
    selected_category = request.args.get('category') or request.form.get('category')

    try:
        cursor = db.cursor(dictionary=True)

        # Fetch categories for dropdown menu
        cursor.execute("SELECT id, name FROM Categories")
        categories = cursor.fetchall()

        if request.method == 'POST':
            item_id = request.form.get('item_id')
            quantity = int(request.form.get('quantity', 1))

            # 获取物品对应的类别名称
            cursor.execute(
                '''
                SELECT c.name AS categoryName 
                FROM Items i 
                JOIN Categories c ON i.categoryId = c.id 
                WHERE i.itemId = %s
                ''',
                (item_id,)
            )
            category_name_result = cursor.fetchone()
            
            if not category_name_result:
                flash('Item category not found.', 'danger')
                return redirect(url_for('orders.add_to_current_order', category=selected_category))
            
            category_name = category_name_result['categoryName']

            # Check if the item is already ordered
            cursor.execute(
                'SELECT COUNT(*) FROM OrderItems WHERE orderId = %s AND itemId = %s',
                (session['order_id'], item_id)
            )
            is_ordered = cursor.fetchone()['COUNT(*)']

            if is_ordered > 0:
                flash('Item has already been added to this order.', 'warning')
                return redirect(url_for('orders.add_to_current_order', category=selected_category))

            # Add the item to the order with its category
            cursor.execute(
                '''
                INSERT INTO OrderItems (orderId, itemId, quantity, category)
                VALUES (%s, %s, %s, %s)
                ''',
                (session['order_id'], item_id, quantity, category_name)
            )

            # Mark the item as ordered in the Items table
            cursor.execute(
                'UPDATE Items SET ordered = TRUE WHERE itemId = %s',
                (item_id,)
            )

            db.commit()
            flash('Item added to the order successfully.', 'success')
            return redirect(url_for('orders.add_to_current_order', category=selected_category))

        # Fetch available items that are not already ordered in this order and not marked as ordered
        items = []
        if selected_category:
            cursor.execute(
                '''
                SELECT i.itemId, i.description, c.name AS categoryName
                FROM Items i 
                JOIN Categories c ON i.categoryId = c.id
                LEFT JOIN OrderItems oi ON i.itemId = oi.itemId AND oi.orderId = %s 
                WHERE oi.itemId IS NULL AND i.ordered = FALSE AND c.name = %s
                ''',
                (session['order_id'], selected_category)
            )
            items = cursor.fetchall()

        return render_template('orders/add_to_current_order.html', items=items, categories=categories, selected_category=selected_category)

    except Exception as e:
        if db:
            db.rollback()
        flash(f'Error adding item to the order: {str(e)}', 'danger')
        return render_template('orders/add_to_current_order.html', categories=categories, selected_category=selected_category)
    finally:
        if cursor:
            cursor.close()

@orders_bp.route('/view_order/<int:order_id>')
@login_required
def view_order(order_id):
    if current_user.role != 'staff':
        flash('Only staff members can view orders.', 'danger')
        return redirect(url_for('auth.index'))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        '''
        SELECT o.orderId, o.orderDate, o.status, i.itemId, i.description, oi.quantity, oi.category
        FROM Orders o
        JOIN OrderItems oi ON o.orderId = oi.orderId
        JOIN Items i ON oi.itemId = i.itemId
        WHERE o.orderId = %s
        ''',
        (order_id,)
    )
    order_data = cursor.fetchall()

    return render_template('orders/view_order.html', order_id=order_id, items=order_data)

