import os
import datetime
from datetime import date
from flask import Flask, request, jsonify,render_template

from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras
import jwt
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}'

conn = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"), host=os.getenv("DB_HOST"))  


secret_key = os.environ.get('SECRET_KEY')

  

@app.route('/cars' ) 
def get_listing():
    id = request.args.get('id')
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM car_info WHERE id=%s", (id,))
    row = cursor.fetchone()
    if row:
     return jsonify(row), 200
    
    if row is None:
        return jsonify({'error': 'Car not found'}), 404






@app.route('/cars' ,methods=['POST'])
def post_listing():
    data = request.json
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO car_info (model,price,mileage,date_added, power_of_engine,number_of_previous_owners,transmission_type,fuel_type,fuel_consumption,co2_emissions) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s)", 
     (data['model'], data['price'],data['mileage'],data['date_added'],data['power_of_engine'],data['number_of_previous_owners'],
     data['transmission_type'],data['fuel_type'],data['fuel_consumption'],data['co2_emissions']))
    conn.commit()
    return jsonify({'message': 'Data inserted successfully'}), 201


@app.route('/user/delete/int:user_id', methods=['DELETE'])
def delete_user(user_id):
# Get the JWT token from the request headers
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split()[1]
    else:
        return jsonify({'error': 'Authorization header is missing'}), 401
# Decode the JWT token to get the user_id
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        user_id = payload['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    return jsonify({'message': 'User deleted successfully'}), 200



@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if request.json is None:
        return jsonify({'error': 'Invalid request, please provide a JSON payload'}), 400 
    fname = data['fname']
    lname = data['lname']
    email = data['email']
    phone_number = data['phonenumber']
    password = data['password']
    confirm_password = data['confirm_password']
 
    if password!= confirm_password :
        return jsonify({'error': "Passwords don't match"}), 400

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    row = cursor.fetchone()    
    if row:
        return jsonify({'error': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (fname,lname,email,phone_number, password_hash) VALUES (%s, %s,%s,%s,%s)",  (fname,lname,email,phone_number, hashed_password))
    conn.commit()
 
    return jsonify({'message': 'Data inserted successfully'}), 201








@app.route('/user')
def get_user():
    id = request.args.get('id')
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=%s", (id,))
    row = cursor.fetchone()
    if row:
     return jsonify(row), 200
    
    if row is None:
    
        return jsonify({'error': 'User not found'}), 404











@app.route('/users')
def get_users():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    row = cursor.fetchall()
    if row:
     return jsonify(row), 200
    
    if row is None:
        return jsonify({'error': 'User not found'}), 404




@app.route('/car/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    # Get the JWT token from the request headers
  auth_header = request.headers.get('Authorization')
  if auth_header:
        token = auth_header.split()[1]
  else:
        return jsonify({'error': 'Authorization header is missing'}), 401
  try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        user_id = payload['user_id']
  except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
  except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
  data = request.json
  color = data.get('color')
  mileage = data.get('mileage')
  price = data.get('price')
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM car_info WHERE id = %s", (car_id,))
  car = cursor.fetchone()
  if not car:
    return jsonify({'error': 'Car not found'}), 404
  cursor.execute("UPDATE car_info SET  color=%s, mileage=%s, price=%s WHERE id=%s", ( color, mileage, price,car_id))
  conn.commit()
    
  return jsonify({'message': 'Car details updated successfully'}), 200




@app.route('/vintage/show' ) 
def get_vintage():
    id = request.args.get('id')
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vintage_cars WHERE vintage_id=%s", (id,))
    row = cursor.fetchone()
    if row:
     return jsonify(row), 200
    
    if row is None:
        return jsonify({'error': 'Car not found'}), 404










@app.route('/car/buy', methods=['POST'])
def buy_car():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split()[1]
    else:
        return jsonify({'error': 'Authorization header is missing'}), 401
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        user_id = payload['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    data = request.json
    car_id = data['car_id']
    price = data['price']
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM car_info WHERE id = %s", (car_id,))
    car = cursor.fetchone()
    if car[11]==False:
              return jsonify({'error': 'Car is not available'}), 404
    if not car:
        return jsonify({'error': 'Car not found'}), 404
    cursor.execute("INSERT INTO sales (car_id, price, buyer_id) VALUES (%s, %s, %s)", (car_id, price, user_id))
    conn.commit()
    cursor.execute("UPDATE car_info SET availability=FALSE Where id= (%s)", (car_id,))
    conn.commit()
    cursor.execute("UPDATE car_info SET owner_id=%s Where id= (%s)", (car_id,user_id,))
    conn.commit()
    return jsonify({'message': 'Car bought successfully'}), 201







@app.route('/vintage/create', methods=['POST'])
def create_vintage():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split()[1]
    else:
        return jsonify({'error': 'Authorization header is missing'}), 401
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        user_id = payload['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    data = request.json
    make = data['make']
    model = data['model']
    year = data['year']
    color = data['color']
    power_of_engine = data['power_of_engine']
    mileage = data['mileage']
    price = data['price']
    image_url = data['image_url']
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vintage_cars (make, model, year, color, power_of_engine, mileage, price, availability, image_url, owner_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (make, model,year,color,power_of_engine,mileage,price,True,image_url, user_id))
    conn.commit()
    return jsonify({'message': 'Vintage car posted successfully'}), 201








@app.route('/auction/create', methods=['POST'])
def create_auction():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split()[1]
    else:
        return jsonify({'error': 'Authorization header is missing'}), 401
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        user_id = payload['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    data = request.json
    car_id = data['car_id']
    starting_price = data['starting_price']
    end_time = data['end_time']
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vintage_cars WHERE vintage_id = %s", (car_id,))
    car = cursor.fetchone()
    if car[8]==False:
      return jsonify({'error':'auction already exists'}),404  
    if not car:
        return jsonify({'error': 'Car not found'}), 404
    if car[3]==False:
              return jsonify({'error': 'Car is not available'}), 404              
    cursor.execute("INSERT INTO auction_info (vintage_id, starting_price, end_time, owner_id) VALUES (%s, %s, %s, %s)", (car_id, starting_price, end_time, user_id))
    conn.commit()
    cursor.execute("UPDATE vintage_cars SET availability=FALSE Where vintage_id= (%s)", (car_id,))
    conn.commit()
    return jsonify({'message': 'Auction created successfully'}), 201





@app.route('/auction/bid/show' ) 
def get_bids():
    id = request.args.get('id')
    
    cursor = conn.cursor()
    cursor.execute("SELECT bid_amount FROM bids WHERE auction_id=%s", (id,))
    row = cursor.fetchall()
    if row:
     return jsonify(row), 200
    
    if row is None:
        return jsonify({'error': 'auction does not exist '}), 404





@app.route('/auction/bid', methods=['POST'])
def placing_bid():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split()[1]
    else:
        return jsonify({'error': 'Authorization header is missing'}), 401
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        user_id = payload['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    data = request.json
    auction_id = data['auction_id']
    bid_amount = data['bid_amount']
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auction_info WHERE auction_id = %s", (auction_id,))
    auction = cursor.fetchone()
    if date.today()>auction[2]:
          cursor.execute("UPDATE auction_info SET is_open=FALSE Where auction_id= (%s)", (auction_id,))
          conn.commit      
    if auction[1] > float(bid_amount):
      return jsonify({'error': 'please enter a higher bid than the asking price'}),400
    if auction[4]==False:
      cursor.execute("UPDATE vintage_car SET owner_id=%s ", (auction[6],))
      conn.commit     
      return jsonify({'error': 'Auction is closed'}), 404
    if not auction:
        return jsonify({'error': 'Auction not found'}), 404
    cursor.execute("SELECT MAX(bid_amount) FROM bids WHERE auction_id = %s  ", (auction_id,))
    highest_bid = cursor.fetchone()[0]
    if highest_bid and float(bid_amount) <= highest_bid:
      return jsonify({'error': 'Bid amount must be greater than current highest bid'}), 400
    cursor.execute("INSERT INTO bids (auction_id, bid_amount, bidder_id) VALUES (%s, %s, %s)", (auction_id, bid_amount, user_id))
    conn.commit()
    cursor.execute("UPDATE auction_info SET highest_bid=%s ,highest_bidder_id=%s WHERE auction_id = %s", (bid_amount, user_id, auction_id))
    conn.commit()
    return jsonify({'message': 'Bid placed successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s LIMIT 1", (email,))
    row = cursor.fetchone()

    # user exists and password is correct
    if row and check_password_hash(row[5], password):
        # Generate JWT token and return it
        payload = {'user_id': row[0]}
        exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=240000)
        payload['exp'] = exp.timestamp()
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return jsonify({'message': 'User logged in', 'token': token}), 201

    # If the user is not found, return an error response
    if not row:
        return jsonify({'error': 'User not found'}), 404

    # If the user is found, but the password is incorrect, return an error response
    if not check_password_hash(row[5], password):
        return jsonify({'error': 'Incorrect password'}), 401




if __name__ == "__main__":
    app.run()