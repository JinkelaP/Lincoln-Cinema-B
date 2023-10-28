from app import mysql
from flask import flash, render_template, request, redirect, url_for, session, Blueprint, jsonify
import json
import os
from decimal import Decimal
from datetime import datetime, timezone
from globalController import lincolnCinema

bp = Blueprint('customerDashboard', __name__, )

def is_authenticated():
    return lincolnCinema.loggedin



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
    

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # preparing data for tracking order page

    # get cart item's preparation time from database

    cursor.execute('SELECT * from orders WHERE orderID = %s;', (orderID,))
    orderInfo = cursor.fetchone()

    branchID = orderInfo['branchID']

    cart = json.loads(orderInfo['orderJSON'])
    for item in cart:
        if item['id'] < 200:
            cursor.execute('SELECT preparetime from pizzas WHERE pizzaID = %s;', (item['id'],))
            result = cursor.fetchone()
            preparetime = result['preparetime']
            if item['size']['value'] == 'medium':
                preparetime += 5
            if item['size']['value'] == 'large':
                preparetime += 10
            item['preparetime'] = preparetime
        elif item['id'] < 300:
            cursor.execute('SELECT preparetime from sideOfferings WHERE sideOfferingID = %s;', (item['id'],))
            result = cursor.fetchone()
            item['preparetime'] = result['preparetime']
        else:
            item['preparetime'] = 0

    cursor.execute('SELECT * from branches WHERE branchID = %s and branchActive = 1;', (branchID,))
    branchInfo = cursor.fetchone()

    cursor.execute('SELECT * from customers WHERE customerID = %s and customerActive = 1;',(orderInfo['customerID'],))
    customerInfo = cursor.fetchone()

    startTimeDuration = branchInfo['startTime']
    totalSeconds = startTimeDuration.total_seconds()
    hours = int(totalSeconds // 3600)
    minutes = int((totalSeconds % 3600) // 60)
    seconds = int(totalSeconds % 60)
    formattedStartTime = f"{hours:02}:{minutes:02}:{seconds:02}"
    branchInfo['startTime'] = formattedStartTime

    endTimeDuration = branchInfo['endTime']
    totalSeconds = endTimeDuration.total_seconds()
    hours = int(totalSeconds // 3600)
    minutes = int((totalSeconds % 3600) // 60)
    seconds = int(totalSeconds % 60)
    formattedEndTime = f"{hours:02}:{minutes:02}:{seconds:02}"
    branchInfo['endTime'] = formattedEndTime

    if branchID == 1 or branchID == '1' :
        branchInfo['GPS'] = [-36.843326, 174.766817]
    elif branchID == 2 or branchID ==  '2':
        branchInfo['GPS'] = [50.735544, -1.778984]
    elif branchID == 3 or branchID == '3':
        branchInfo['GPS'] = [-41.286790, 174.776222]
    elif branchID == 4 or branchID == '4':
        branchInfo['GPS'] = [-45.033108, 168.656930]

    estimatedTime = utc_to_local(orderInfo['estimatedTime'])
    orderSubmitTime = utc_to_local(orderInfo['orderDate'])

    order = {
        'orderID': orderID,
        'cart': cart,
        'orderMethod': orderInfo['deliveryOption'],
        'orderStatus': 'order-placed',
        'specifiedPickupOrDeliveryTime': estimatedTime,
        'orderSubmitTime': orderSubmitTime,
        'branchInfo': branchInfo,
        'customerInfo': customerInfo,
        'specialRequests': orderInfo['specialRequests']
    }

    return render_template('trackOrder.html', order=order)
    

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
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    
    cursor.execute('SELECT * FROM notifications WHERE customerID = %s',(getCustomerID(session['id']),))
    allMsg = cursor.fetchall()
    return render_template('displayMsg.html', allMsg = reversed(allMsg))

@bp.route('/customer/profile')
def customerProfile():    
    if is_authenticated():
        if session['role'] == 'Customer':    
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    
            # Fetch customerinfo from the database
            cursor.execute('SELECT users.userID, users.userName, users.userPassword, customers.title, customers.firstName, customers.lastName, customers.email, customers.phoneNumber, customers.Address, customers.dateOfBirth, customers.Preferences FROM customers JOIN users ON customers.userID = users.userID WHERE customers.userID = %s',(session['id'],))
            customerInfo = cursor.fetchone()           
            return render_template('customerProfile.html', customerInfo=customerInfo)
        else:
            return "unauthorized"
    else:
        return redirect(url_for('login.login'))    
    

    if is_authenticated():
        userID = request.form.get('userID')        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    
        # Fetch customers from the database
        cursor.execute('''SELECT users.userID, users.userName, users.userPassword, customers.title, customers.firstName, customers.lastName, customers.email, customers.phoneNumber, customers.Address, customers.dateOfBirth, customers.Preferences
                       FROM customers JOIN users 
                       ON customers.userID = users.userID 
                       WHERE customers.customerActive=True AND customers.userID = %s''',(userID,))
        account = cursor.fetchone()        
             
        if account:

            userName = request.form.get('userName')
            title = request.form.get('title')
            firstName = request.form.get('firstName')
            lastName = request.form.get('lastName')

            email = request.form.get('email')
            phoneNumber = request.form.get('phoneNumber')
            Address = request.form.get('Address')
            dateOfBirth = request.form.get('dateOfBirth')
            Preferences = request.form.get('Preferences')
            userPassword = request.form.get('userPassword')
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)            
            #if username is changed:
            if userName != account['userName']:
                #check if username already exists in database                
                if userNameCrash(userName):
                    flash('Failed. Username already exists. Please choose a different username.','error')
                    return redirect(url_for('customerDashboard.customerProfile'))
                else:                    
                    cursor.execute('UPDATE users SET userName=%s WHERE userID=%s',(userName, userID))

                    mysql.connection.commit()
                    flash('Username changed successfully!','success')

            # check if the password is changed by comparing the input password with the password stored in database

            if userPassword.encode('utf-8') !=  account['userPassword'].encode('utf-8'):
                if userPassword != "********" and not bcrypt.checkpw(userPassword.encode('utf-8'), account['userPassword'].encode('utf-8')):                    
                    # if password is changed, then the new password needs to be encrypted before inserting into databse
                    hashed = passwordEncrypt(userPassword)
                    cursor.execute('UPDATE users SET userPassword=%s WHERE userID=%s',(hashed, userID))
                    mysql.connection.commit()
                    flash('Password changed successfully!','success')
            
            if 'avatar' in request.files and request.files['avatar'].filename != '':                
                avatar = request.files.get('avatar')                
                avatarName = f"{userID}.jpg"                
                filePath = os.path.join('app', 'static', 'avatar', avatarName)
                avatar.save(filePath)

            if firstName != account['firstName'] or lastName != account['lastName'] or phoneNumber != account['phoneNumber'] or title != account['title'] or email != account['email'] or Address != account['Address'] or dateOfBirth != account['dateOfBirth'] or Preferences != account['Preferences']:
                    cursor.execute('UPDATE customers SET title=%s,firstName=%s,lastName=%s,email=%s,phoneNumber=%s,Address=%s,dateOfBirth=%s,Preferences=%s WHERE customers.userID = %s', (title,firstName,lastName,email,phoneNumber,Address,dateOfBirth,Preferences,userID,))
                    mysql.connection.commit()
                    flash('Profile information updated successfully!','success')
                    return redirect(url_for('customerDashboard.customerProfile'))           
            else:                
                return redirect(url_for('customerDashboard.customerProfile'))
        else:
            return "unauthorized"
    else:
        return redirect(url_for('login.login'))
