
from flask import flash, render_template, request, redirect, url_for, session, Blueprint
import os
from datetime import date, datetime, timedelta
from decimal import Decimal
from flask import jsonify
from globalController import lincolnCinema


bp = Blueprint('adminDashboard1', __name__, )

def is_authenticated():
    return lincolnCinema.loggedin


@bp.route('/hqAdmin/home')
def adminDashboard1():
    if not 'loggedin' in session or session['role'] != 'HQ_Admin':
        return redirect(url_for('login.login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Fetch branches from the database
    cursor.execute('SELECT * FROM branches WHERE branchActive = TRUE;')
    branches = cursor.fetchall()


    # Fetch additional information for each branch. 
    for branch in branches:
        cursor.execute('SELECT * FROM pizzas WHERE branchID = %s AND pizzaActive = TRUE', (branch['branchID'],))
        branch['specialty_pizzas'] = cursor.fetchall()
        
        cursor.execute('SELECT * FROM sideOfferings WHERE branchID = %s AND sideOfferingActive = TRUE', (branch['branchID'],))
        branch['specialty_sides'] = cursor.fetchall()
        
        cursor.execute('SELECT * FROM drinks WHERE branchID = %s AND drinkActive = TRUE', (branch['branchID'],))
        branch['specialty_drinks'] = cursor.fetchall()

        cursor.execute('SELECT * FROM AdminInfo WHERE userID = %s;', (branch['branchAdminID'],))
        branch['branchAdminInfo'] = cursor.fetchone()

        cursor.execute('SELECT * FROM simplePromotions WHERE branchID = %s AND sPromoActive = TRUE', (branch['branchID'],))
        branch['simplePromo'] = cursor.fetchall()

        cursor.execute('SELECT * FROM comboPromotions WHERE branchID = %s AND cPromoActive = TRUE', (branch['branchID'],))
        branch['comboPromo'] = cursor.fetchall()

        cursor.execute('SELECT * FROM orders WHERE branchID = %s AND orderActive = TRUE', (branch['branchID'],))
        totalAmountOrders = cursor.fetchall()

        cursor.execute('SELECT orderDate, totalAmount FROM orders WHERE branchID = %s AND orderDate BETWEEN NOW() - INTERVAL 30 DAY AND NOW() ORDER BY orderDate DESC;', (branch['branchID'],))
        orders30Days = cursor.fetchall()

        totalAmount = 0
        totalCustomer = 0
        customerIDTemp = 0
        for i in totalAmountOrders:
            totalAmount += i['totalAmount']
            if i['customerID'] != customerIDTemp:
                totalCustomer += 1
                customerIDTemp = i['customerID']

        cursor.execute('SELECT od.productID, COUNT(od.productID) as count FROM orderDetails od\
        JOIN orders o ON od.orderID = o.orderID\
        WHERE o.branchID = %s AND o.orderDate BETWEEN NOW() - INTERVAL 30 DAY AND NOW()\
        GROUP BY od.productID ORDER BY count DESC', (branch['branchID'],))
        topProducts = cursor.fetchall()

        for i in topProducts:
            if i['productID'] < 200:
                cursor.execute("SELECT * FROM pizzas WHERE pizzaID = %s;", (i['productID'],))
                productName = cursor.fetchone()
                i['productID'] = productName['pizzaName']

            elif i['productID'] < 300:
                cursor.execute("SELECT * FROM sideOfferings WHERE sideOfferingID = %s;", (i['productID'],))
                productName = cursor.fetchone()
                i['productID'] = productName['offeringName']

            else:
                cursor.execute("SELECT * FROM drinks WHERE drinkID = %s;", (i['productID'],))
                productName = cursor.fetchone()
                i['productID'] = productName['drinkName']
        
        branch['totalAmounts'] = totalAmount
        branch['orderAmounts'] = len(totalAmountOrders)
        branch['totalCustomer'] = customerIDTemp
        branch['orders30Days'] = orders30Days
        branch['topProducts'] = topProducts

    return render_template('adminDashboard1.html', branches=branches)

@bp.route('/hqadmin/profile')
def hqadminProfile():    
    if is_authenticated():
        if session['role'] == 'HQ_Admin':    
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    
            # Fetch admininfo from the database
            cursor.execute('SELECT users.userID, users.userName, users.userPassword, admininfo.title, admininfo.firstName, admininfo.lastName, admininfo.phoneNumber FROM admininfo JOIN users ON admininfo.userID = users.userID WHERE admininfo.userID = %s',(session['id'],))
            hqadminInfo = cursor.fetchone()           
            return render_template('hqadminProfile.html', hqadminInfo=hqadminInfo)
        else:
            return "unauthorized"
    else:
        return redirect(url_for('login.login'))    
    

    if is_authenticated():
        userID = request.form.get('userID')        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    
        # Fetch admininfo from the database
        cursor.execute('''SELECT users.userID, users.userName, users.userPassword, admininfo.title, admininfo.firstName, admininfo.lastName, admininfo.phoneNumber 
                       FROM admininfo JOIN users 
                       ON admininfo.userID = users.userID 
                       WHERE admininfo.adminActive=True AND admininfo.userID = %s''',(userID,))
        account = cursor.fetchone()        
             
        if account:
            userName = request.form.get('userName')
            title = request.form.get('title')
            firstName = request.form.get('firstName')
            lastName = request.form.get('lastName')
            phoneNumber = request.form.get('phoneNumber')           
            userPassword = request.form.get('userPassword')
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)            
            #if username is changed:
            if userName != account['userName']:
                #check if username already exists in database                
                if userNameCrash(userName):
                    flash('Failed. Username already exists. Please choose a different username.','error')
                    return redirect(url_for('adminDashboard1.hqadminProfile'))
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

            if firstName != account['firstName'] or lastName != account['lastName'] or phoneNumber != account['phoneNumber'] or title != account['title']:
                    cursor.execute('UPDATE admininfo SET firstName=%s,lastName=%s,phoneNumber=%s,title=%s WHERE admininfo.userID = %s', (firstName,lastName,phoneNumber,title,userID,))
                    mysql.connection.commit()
                    flash('Profile information updated successfully!','success')
                    return redirect(url_for('adminDashboard1.hqadminProfile'))           
            else:                
                return redirect(url_for('adminDashboard1.hqadminProfile'))
        else:
            return "unauthorized"
    else:
        return redirect(url_for('login.login'))


@bp.route('/nationalProducts', methods=['GET'])
def nationalProducts():
    if 'loggedin' in session and session['role'] == 'HQ_Admin':
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Fetch the pizzas, side offerings, and drinks that are national (branchID is NULL) and active
        cursor.execute('SELECT * FROM pizzas WHERE branchID IS NULL AND pizzaActive = TRUE ORDER BY pizzaName')
        pizzas = cursor.fetchall()

        # Group the pizzas by their name
        pizzas = [list(g) for k, g in groupby(pizzas, key=itemgetter('pizzaName'))]

        cursor.execute('SELECT * FROM sideOfferings WHERE branchID IS NULL AND sideOfferingActive = TRUE')
        side_offerings = cursor.fetchall()

        cursor.execute('SELECT * FROM drinks WHERE branchID IS NULL AND drinkActive = TRUE')
        drinks = cursor.fetchall()

        cursor.execute('SELECT * FROM toppings WHERE toppingActive = TRUE')
        toppings = cursor.fetchall()

        cursor.close()

        return render_template('nationalProducts.html', pizzas=pizzas, side_offerings=side_offerings, drinks=drinks, toppings=toppings)

    return redirect(url_for('login.login'))


@bp.route('/addPizza', methods=['POST'])
def addPizza():
    if 'loggedin' in session and session['role'] == 'HQ_Admin':
        pizzaName = request.form['pizzaName']
        description = request.form['description']
        
        sizes = ['Small', 'Medium', 'Large']
        prices = [request.form['smallPrice'], request.form['mediumPrice'], request.form['largePrice']]
        preparetimes = [request.form['smallPrepareTime'], request.form['mediumPrepareTime'], request.form['largePrepareTime']]
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        for size, price, preparetime in zip(sizes, prices, preparetimes):
            cursor.execute("""
                INSERT INTO pizzas (pizzaName, description, size, price, preparetime)
                VALUES (%s, %s, %s, %s, %s)
            """, (pizzaName, description, size, price, preparetime))
        
        if 'pizzaImage' in request.files and request.files['pizzaImage'].filename != '':
            image = request.files.get('pizzaImage')
            # fetch the id of the pizza that was just inserted
            first_pizzaId = cursor.lastrowid
            
            for offset in range(3):
                pizzaId = first_pizzaId - offset
                imageName = f"{pizzaId}.jpg"
                filePath = os.path.join('app', 'static', 'image', imageName)
                # save the image to the file system
                with open(filePath, 'wb') as f:
                    f.write(image.read())
                    # reset the file pointer to the beginning of the file
                    image.seek(0)

        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('adminDashboard1.nationalProducts'))
    return redirect(url_for('login.login'))






@bp.route('/deletePizzas', methods=['POST'])
def deletePizzas():
    if 'loggedin' in session and session['role'] == 'HQ_Admin':
        pizzaNames = request.json.get('pizzaNames', [])
        pizzaIds = request.json.get('pizzaIds', [])

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        if pizzaNames:  # Check if pizzaNames is not empty
            query_names = "UPDATE pizzas SET pizzaActive = FALSE WHERE pizzaName IN (%s)" % ', '.join(['%s'] * len(pizzaNames))
            cursor.execute(query_names, tuple(pizzaNames))
        
        if pizzaIds:  # Check if pizzaIds is not empty
            query_ids = "UPDATE pizzas SET pizzaActive = FALSE WHERE pizzaID IN (%s)" % ', '.join(['%s'] * len(pizzaIds))
            cursor.execute(query_ids, tuple(pizzaIds))
        
        mysql.connection.commit()
        cursor.close()

        return jsonify(success=True)

    return jsonify(success=False, error="Unauthorized access")
