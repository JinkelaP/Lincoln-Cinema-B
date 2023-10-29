
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


