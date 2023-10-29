
from flask import flash, render_template, request, redirect, url_for, session, Blueprint, jsonify
import json
import os
from decimal import Decimal
from datetime import datetime, timezone
from globalController import lincolnCinema

bp = Blueprint('customerDashboard', __name__, )

def is_authenticated():
    return lincolnCinema.loggedin


def getAccountInfo():
    return {
                'name': lincolnCinema.loggedUser.name,
                'auth': lincolnCinema.loggedin,
                'username': lincolnCinema.loggedUser.username
            }

@bp.route('/payment')
def payment():
    if not is_authenticated():
        flash('You did not login!', 'success')
        return redirect(url_for('login.login'))
    elif 'cart' not in session:
        return redirect(url_for('customerDashboard.menu'))
    else:
        cart = session['cart']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    
        cursor.execute('SELECT users.userName, customers.firstName, customers.lastName, customers.email, customers.phoneNumber, customers.Address FROM customers JOIN users ON customers.userID = users.userID WHERE customers.userID = %s',(session['id'],))
        customerInfo = cursor.fetchone()     
        return render_template('payment.html', cartJs = json.dumps(cart), cart = cart, customerInfo = customerInfo)
    


@bp.route('/customer/myOrder')
def myOrder():
    if is_authenticated():
        role = session['role']
        customerID = getCustomerID(session['id'])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    
        # Fetch customerinfo from the database

        # Since I cannot jsonserialise the date object in Js, I can only write this longggggg SQL.
        cursor.execute('SELECT orders.orderID, orders.orderDate, orders.estimatedTime, orders.deliveryOption, orders.orderJSON,  \
                       orders.orderStatus, orders.totalAmount, orders.specialRequests, branches.branchName, branches.branchID\
                       ,payment.paymentMethod\
                       FROM orders JOIN branches ON branches.branchID = orders.branchID \
                       JOIN payment ON orders.orderID = payment.orderID\
                       WHERE orders.customerID = %s',(customerID,))
        allOrders = cursor.fetchall()

        cursor.execute('SELECT branchName from branches;')
        allBranch = cursor.fetchall()
        
        return render_template('myOrder.html', allOrders = allOrders, allBranch = allBranch)
    else:
        return redirect(url_for('login.login'))  


@bp.route('/customer/msg', methods=['GET'])
def msg():
    allMsg = []
    notiList = lincolnCinema.loggedUser.notiList
    for i in notiList:
        noti = {
            'content': i.content,
            'time':i.date
        }
    return render_template('displayMsg.html', allMsg = reversed(allMsg),accountInfo = getAccountInfo())

@bp.route('/profile')
def customerProfile():    
    if is_authenticated():
        user = lincolnCinema.loggedUser
       
        customerInfo = {
            'userName': user.username,
            'userPassword': user.userPassword,
            'firstName': user.name,
            'email': user.email,
            'phoneNumber': user.phone,
            'Address': user.address
        } 
        return render_template('customerProfile.html', customerInfo=customerInfo, accountInfo=getAccountInfo())

    else:
        return redirect(url_for('login.login'))    
    
