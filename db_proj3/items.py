# items.py
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from .db import get_db
from db_proj3 import db  # 确保从项目的根目录导入 db

items_bp = Blueprint('items', __name__)

@items_bp.route('/find_single_item', methods=['GET', 'POST'])
@login_required
def find_single_item():
    if request.method == 'POST':
        item_id = request.form.get('item_id')  # 使用 get 方法来避免 KeyError

        if not item_id:
            flash('Item ID is required.')
            return redirect(url_for('items.find_single_item'))

        try:
            item_id = int(item_id)  # 尝试将 item_id 转换为整数
        except ValueError:
            flash('Invalid Item ID format.')
            return redirect(url_for('items.find_single_item'))

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            'SELECT itemId, description, price, stockQuantity, donator '
            'FROM Items '
            'WHERE itemId = %s', (item_id,)
        )
        item = cursor.fetchone()

        if item:
            return render_template('items/find_single_item_result.html', item=item)
        else:
            flash('Item not found.')

    return render_template('items/find_single_item_form.html')


@items_bp.route('/find_order_items', methods=['GET', 'POST'])
@login_required
def find_order_items():
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        if not order_id:
            flash('Order ID is required.')
            return redirect(url_for('items.find_order_items'))

        try:
            db = get_db()
            cursor = db.cursor(dictionary=True)

            # 查询订单中的物品及其位置
            cursor.execute(
                '''
                SELECT i.itemId, i.description, i.price, oi.quantity, i.location
                FROM OrderItems oi 
                JOIN Items i ON oi.itemId = i.itemId 
                WHERE oi.orderId = %s
                ''',
                (order_id,)
            )
            items = cursor.fetchall()

            if items:
                return render_template('items/find_order_items_result.html', items=items)
            else:
                flash('No items found for the given Order ID.')
                return redirect(url_for('items.find_order_items'))
        except Exception as e:
            flash(f'An error occurred while processing your request: {str(e)}')
            return redirect(url_for('items.find_order_items'))

    return render_template('items/find_order_items_form.html')