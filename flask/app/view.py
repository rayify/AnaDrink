from flask import render_template, request, jsonify
from app import app
from cassandra.cluster import Cluster


cluster = Cluster(['ec2-13-57-46-231.us-west-1.compute.amazonaws.com'])
session = cluster.connect('playground')


@app.route('/')
#def index():
    #return render_template("webUI.html")


@app.route('/index')
def index():
    user = {'nickname': 'Hanlei'} #fake user
    return render_template("index.html", title = 'Home', user = user)

@app.route('/drink')
def drink():
    return render_template("drink.html")

@app.route("/drink", methods=['GET','POST'])
def drink_post():
    
    #drink_name = request.form["drink_name"]
    print ('YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY')
    stmt_coffee = "SELECT drink,COUNT(*) FROM insight WHERE drink='coffee' ALLOW FILTERING"
    stmt_tea = "SELECT drink,COUNT(*) FROM insight WHERE drink='tea' ALLOW FILTERING"
    stmt_milk = "SELECT drink,COUNT(*) FROM insight WHERE drink='milk' ALLOW FILTERING"
    stmt_soda = "SELECT drink,COUNT(*) FROM insight WHERE drink='soda' ALLOW FILTERING"
    stmt_juice = "SELECT drink,COUNT(*) FROM insight WHERE drink='juice' ALLOW FILTERING"
    stmt_wine = "SELECT drink,COUNT(*) FROM insight WHERE drink='wine' ALLOW FILTERING"
    stmt_beer = "SELECT drink,COUNT(*) FROM insight WHERE drink='beer' ALLOW FILTERING"
    stmt_liquor = "SELECT drink,COUNT(*) FROM insight WHERE drink='liquor' ALLOW FILTERING"
    
    response_coffee = session.execute(stmt_coffee)
    response_tea = session.execute(stmt_tea)
    response_milk = session.execute(stmt_milk)
    response_soda = session.execute(stmt_soda)
    response_juice = session.execute(stmt_juice)
    response_wine = session.execute(stmt_wine)
    response_beer = session.execute(stmt_beer)
    response_liquor = session.execute(stmt_liquor)
    
    response_list = []
    for val in response_coffee:
        response_list.append(val)
    for val in response_tea:
        response_list.append(val)
    for val in response_milk:
        response_list.append(val)
    for val in response_soda:
        response_list.append(val)
    for val in response_juice:
        response_list.append(val)
    for val in response_wine:
        response_list.append(val)
    for val in response_beer:
        response_list.append(val)
    for val in response_liquor:
        response_list.append(val)
    
    jsonresponse_drink = [{"drink_name": x.drink, "count": x.count} for x in response_list]
    return render_template("drink.html", output=jsonresponse_drink)

'''
    
    
    
    response_list = []
    for val in response:
        response_list.append(val)
    jsonresponse=[{"fname": x.fname, "lname": x.lname, "id": x.id, "message": x.message, "time": x.time} for x in response_list]
    return render_template("emailop.html", output=jsonresponse)
'''
@app.route('/realtime')
def realtime():
    return render_template("realtime.html")

