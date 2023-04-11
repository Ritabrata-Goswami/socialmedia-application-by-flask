from flask import *
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy  
import pyodbc
import os
import random
from werkzeug.utils import secure_filename
from markupsafe import Markup, escape
from hashlib import sha512
import time
from datetime import datetime
from flask_mail import Mail, Message
import json
import collections
from sqlalchemy import *


app = Flask(__name__, template_folder='./Matrimonial', static_folder='Matrimonial')
mail = Mail(app)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://ABC\SQLEXPRESS/matrimonial?tursted_connection=yes&driver=ODBC Driver 17 for SQL Server' 
app.config['SECRET_KEY'] = "ritabrata@matrimonial#2023" 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app) 

class registration(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(500))
    country = db.Column(db.String(500))
    email = db.Column(db.String(500))
    password = db.Column(db.String(500))
    phone = db.Column(db.Integer) 
    address = db.Column(db.String(2000))
    gender = db.Column(db.String(100))
    photo = db.Column(db.String(1000))
    dob = db.Column(db.String(100))
    profile_url = db.Column(db.String(500)) 

    def __init__(self, name, country, email, password, phone, address, gender, photo, dob, profile_url):
        self.name  = name 
        self.country = country
        self.email = email
        self.password = password
        self.phone = phone
        self.address = address
        self.gender = gender
        self.photo = photo
        self.dob = dob
        self.profile_url = profile_url


class otpsave(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(500))
    user_email = db.Column(db.String(500))
    otp = db.Column(db.String(500))
    time_send = db.Column(db.String(500))

    def __init__(self, user_id, user_name, user_email, otp, time_send):
        self.user_id  = user_id
        self.user_name = user_name
        self.user_email = user_email
        self.otp = otp
        self.time_send = time_send


class uploads(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(500))
    user_email = db.Column(db.String(500))
    user_ph = db.Column(db.String(100))
    user_account_url = db.Column(db.String(500))
    file_name = db.Column(db.String(800))
    file_description = db.Column(db.String(4000))
    uploading_time = db.Column(db.String(100))

    def __init__(self, user_id, user_name, user_email, user_ph, user_account_url, file_name, file_description, uploading_time):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        self.user_ph = user_ph
        self.user_account_url = user_account_url
        self.file_name = file_name
        self.file_description = file_description
        self.uploading_time = uploading_time


class users_react(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    file_id = db.Column(db.Integer)
    user_name = db.Column(db.String(500))
    user_email = db.Column(db.String(500))
    user_ph = db.Column(db.String(100))
    user_account_url = db.Column(db.String(500))
    reaction = db.Column(db.Integer)
    reaction_time = db.Column(db.String(100))
    react_by_id = db.Column(db.Integer)
    react_by_name = db.Column(db.String(500))
    react_by_ph = db.Column(db.String(200))

    def __init__(self, user_id, file_id, user_name, user_email, user_ph, user_account_url, reaction, reaction_time, react_by_id, react_by_name, react_by_ph):
        self.user_id = user_id
        self.file_id = file_id
        self.user_name = user_name
        self.user_email = user_email
        self.user_ph = user_ph
        self.user_account_url = user_account_url
        self.reaction = reaction
        self.reaction_time = reaction_time
        self.react_by_id = react_by_id
        self.react_by_name = react_by_name
        self.react_by_ph = react_by_ph




@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/user', methods=['GET'])
def reg_page():
    return render_template('user_page.html')

@app.route('/registration', methods=['GET','POST'])
def user_registration():
    if request.method == 'POST':

        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789%^&*$#ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pw_length = 8
        mypssw = ""

        for i in range(pw_length):
            next_index = random.randrange(len(alphabet))
            mypssw = mypssw + alphabet[next_index]
        mypssw_hash = bcrypt.generate_password_hash(mypssw)  #converting the actual password into hashed password

        name = escape(request.form['enter_name']) 
        country = request.form['country'] 
        email = escape(request.form['enter_email'])
        password = mypssw_hash  
        phone = escape(request.form['enter_ph']) 
        address = escape(request.form['enter_addr']) 
        gender = request.form['enter_gender'] 
        f = request.files['enter_photo']
        file_name = request.files['enter_photo'].filename
        
        f_alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        f_length = 15
        f_name = ""

        for i in range(f_length):
            f_index = random.randrange(len(f_alphabet))
            f_name = f_name + f_alphabet[f_index]

        list_file_name = file_name.split('.')
        list_file_name_new = list_file_name[0] + '_' + str(time.time()) + '_' + f_name + '.' + list_file_name[1]
        print(list_file_name_new)

        photo = secure_filename(list_file_name_new)
        dob = request.form['enter_dob']

        url_alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        url_length = 10
        url_name = ""

        for i in range(url_length):
            url_index = random.randrange(len(url_alphabet))
            url_name = url_name + url_alphabet[url_index]
        
        profile_url = url_name

        registration_values = registration(name,country,email,password,phone,address,gender,photo,dob,profile_url)
        print('----------------------------------------------------------')
        print(mypssw_hash)
        print('Actual password:- ', mypssw)
        
        email_check = registration.query.filter_by(email = email).first()
        ph_check = registration.query.filter_by(phone = phone).first()

        if not email_check and not ph_check:       #To check whether the newly entered email has match with any of the existed row or not. 
            app.config['UPLOAD_FOLDER'] = r'C:\Users\abc123\Desktop\python\Flask code\Matrimonial\photo\matrimonial_profile_photo'
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], photo))
            db.session.add(registration_values)
            db.session.commit()  #add the data to db table.

            return jsonify({'message':'Thank you ' + name + ' for successful registration.'})
        else:
            return jsonify({'message':'Either email or phone number is already registered! Please try with a new email or phone number.'})
      

@app.route('/authentication', methods=['GET','POST'])
def login_users():
    if request.method == 'POST':

        enter_email = escape(request.form['enter_id'])
        enter_pass = escape(request.form['enter_password'])

        login_auth = registration.query.filter_by(email = enter_email).first()
        authenticated_user = bcrypt.check_password_hash(login_auth.password, enter_pass)

        if login_auth and authenticated_user: 
            session['status'] = True
            session['user_email'] = enter_email
            fetch_url = registration.query.filter_by(email = enter_email).first()
            session['session_url'] = fetch_url.profile_url
            session['session_id'] = fetch_url.id
            # return redirect(url_for('profile'))
            return redirect('/'+fetch_url.profile_url)
        else:
            return jsonify({'message':'Sorry Login Failed!'})


@app.route('/logout', methods=['GET'])
def user_logout():
    session.pop('user_email')
    return redirect('/')


@app.route('/<url>', methods=['GET'])
def profile(url):
    if 'user_email' in session and session['status'] == True:
        email = session['user_email']
        get_edit_details = registration.query.filter_by(email = email).first()

        get_session_url = session['session_url']
        get_row = registration.query.filter_by(profile_url = url).first()

        get_all_photos = uploads.query.filter(uploads.file_name!='NULL').filter_by(user_account_url=url).all()
        new_photos_list = []

        for index, item in zip(range(2), get_all_photos):
            new_photos_list.append(item)

        get_all_files = uploads.query.filter_by(user_account_url=url).order_by(uploads.id.desc()).all()
        
        total_like = users_react.query.with_entities(users_react.file_id, func.sum(users_react.reaction)).filter_by(user_id = get_row.id).group_by(users_react.file_id).all()

        account_id = session['session_id']
        get_react_by_info = users_react.query.filter_by(user_id = get_row.id).all()

        return render_template('profile.html', row_val = get_row, send_session_url = get_session_url, get_all_edits = get_edit_details, display_profile_photos = new_photos_list, all_photos=get_all_files, total_like=total_like, get_react_by_info=get_react_by_info, session_user_id=account_id)
    else:
        return redirect('/')


@app.route('/<url>/search')
def search(url):
    get_session_url = session['session_url']
    get_row = registration.query.filter_by(profile_url = url).first()

    if(get_row.gender == 'male'):
        session['get_gender'] = 'female'
    else:
        session['get_gender'] = 'male'

    default_search_val = registration.query.filter_by(gender = session['get_gender']).all()
    fetch_all = registration.query.all()
    result_list = []
    for row in fetch_all:
        all_val_dict = {"name":row.name}
        result_list.append(all_val_dict)
        name_val_json = json.dumps(result_list, indent=4)

    return render_template('search.html', row_val = get_row, send_session_url = get_session_url, default_search = default_search_val, all_json_name = name_val_json)


@app.route('/get-search', methods=['POST'])
def search_res():
    if request.method == 'POST':
        json_data = request.get_json()

        search_val = json_data[0]['searchByCountry']

        get_session_url = session['session_url']
        get_row = registration.query.filter_by(profile_url = get_session_url).first()
        if(get_row.gender == 'male'):
            session['get_gender'] = 'female'
        else:
            session['get_gender'] = 'male'
                                                        #   If no records found ORM returns None
        if registration.query.filter_by(country = search_val, gender = session['get_gender']).first() is not None:   
            get_search_res = registration.query.filter_by(country = search_val, gender = session['get_gender']).all()
            get_search_list = []
            for row in get_search_res:
                val_dict = {
                    "name" : row.name,
                    "country" : row.country,
                    "gen" : row.gender,
                    "photo" : row.photo,
                    "url" : row.profile_url
                }  

                get_search_list.append(val_dict)
                produce_json = json.dumps(get_search_list, indent=4)
            print('---------------------------------------')
            print(produce_json)

            return produce_json
        else:
            print('No Search Result Found!')
            empty_row_res = {'response':'No Search Result Found!'}
            return jsonify(empty_row_res)


@app.route('/tab-search', methods=['POST'])
def tab_search():
    if request.method == 'POST':
        json_data = request.get_json()

        search_val = json_data[0]['searchByName']
                                        # ORM equivalent to LIKE operator
        search = "%{}%".format(search_val)
        get_names = registration.query.filter(registration.name.like(search)).all()
        
        if registration.query.filter(registration.name.like(search)).first() is not None:
            name_list = []
            for name_val in get_names:
                name_dict = {
                    "name" : name_val.name,
                    "country" : name_val.country,
                    "gen" : name_val.gender,
                    "photo" : name_val.photo,
                    "url" : name_val.profile_url
                }
                name_list.append(name_dict)
                produce_name_json = json.dumps(name_list, indent=4)
            print('-----------------------------------------')
            print(produce_name_json)

            return produce_name_json
        else:
            print('No Search Result Found!')
            empty_row_res = {'response':'No Search Result Found!'}
            return jsonify(empty_row_res)


@app.route('/update-profile', methods=['POST'])
def profile_details_update():
    if request.method == 'POST':
        email = session['user_email']
        user_id = session['session_id']
        profile_edit = registration.query.get_or_404(user_id)

        update_json_data = request.get_json()
        
        print('----------------------------------------')
        print(update_json_data)
        print('----------------------------------------')

        update_email = update_json_data[0]['sendEmail']
        update_phone = update_json_data[1]['sendPhone']
        update_address = update_json_data[2]['sendAddress']
        update_country = update_json_data[3]['sendCountry']

        profile_edit.email = update_email
        profile_edit.phone = update_phone
        profile_edit.address = update_address
        profile_edit.country = update_country

        db.session.add(profile_edit)
        db.session.commit()
        
        get_updated_profile = registration.query.filter_by(id=user_id).first()
        updated_profile_list = []
        updated_profile_dict = {
            "gender":get_updated_profile.gender,
            "dob":get_updated_profile.dob,
            "email":get_updated_profile.email,
            "ph":get_updated_profile.phone,
            "addr":get_updated_profile.address,
            "country":get_updated_profile.country,
            "response":"Details Updated Successfully!"
        }
        updated_profile_list.append(updated_profile_dict)
        result_response = json.dumps(updated_profile_list, indent=4)

        print('----------------------------------------')
        print(result_response)
        print('----------------------------------------')

        return result_response


@app.route('/profile-pic', methods=['POST'])
def profile_photo_update():
    if request.method == 'POST':
        user_id = session['session_id']
        profile_photo = request.files['upload-photo']
        profile_photo_name = request.files['upload-photo'].filename

        f_alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        f_length = 15
        f_name = ""

        for i in range(f_length):
            f_index = random.randrange(len(f_alphabet))
            f_name = f_name + f_alphabet[f_index]
        
        list_file_name = profile_photo_name.split('.')
        list_file_name_new = list_file_name[0] + '_' + str(time.time()) + '_' + f_name + '.' + list_file_name[1]
        print(list_file_name_new)
        
        photo = secure_filename(list_file_name_new)

        profile_edit = registration.query.get_or_404(user_id)

        profile_edit.photo = photo
        db.session.add(profile_edit)
        db.session.commit()

        app.config['UPLOAD_FOLDER'] = r'C:\Users\abc123\Desktop\python\Flask code\Matrimonial\photo\matrimonial_profile_photo'
        profile_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo))

        get_updated_profile_photo = registration.query.filter_by(id=user_id).first()
        update_photo_list = []
        update_photo_dict = {
            "profilePhoto":get_updated_profile_photo.photo,
            "response":"Profile Photo Updated Successfully!"
        }
        update_photo_list.append(update_photo_dict)
        update_photo_result = json.dumps(update_photo_list, indent=4)
        
        print('----------------------------------------')
        print(update_photo_result)
        print('----------------------------------------')

        return jsonify(update_photo_list)


@app.route('/<url>/photo')
def display_photo(url):
    user_id = session['session_id']
    email = session['user_email']
    session_url = session['session_url']

    get_name = registration.query.filter_by(profile_url=url).first()
    profile_name = get_name.name
    get_profile_url = get_name.profile_url
    
    if uploads.query.filter_by(user_account_url=url).first() is not None: 
        get_photos = uploads.query.filter_by(user_account_url=url).all()

        photos_list = []
        for photo_res in get_photos:
            photos_dict = {
            "name":photo_res.file_name,
            "obj_description":photo_res.file_description,
            "upload_time":photo_res.uploading_time
            }
            photos_list.append(photos_dict)

        print('---------------------------------------------')
        print(photos_list)
        print('---------------------------------------------')

        return render_template('photo.html', url=get_profile_url, send_name=profile_name, send_session_url=session_url, send_photo_jsonify = json.dumps(photos_list), all_photos=get_photos)
    else:
        no_photo_list = []
        response = {
            "response":"No Image or Video Uploaded Yet."
        }
        no_photo_list.append(response)

        return render_template('photo.html', url=get_profile_url, send_name=profile_name, send_session_url=session_url, no_photo_found=jsonify(no_photo_list))



@app.route('/upload',methods=['POST'])
def upload_files():
    if request.method == 'POST':
        user_id = session['session_id']
        upload_photo = request.files['file']
        upload_photo_name = request.files['file'].filename
        description = request.form['description']

        t = datetime.now()

        f_alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        f_length = 25
        f_name = ""

        for i in range(f_length):
            f_index = random.randrange(len(f_alphabet))
            f_name = f_name + f_alphabet[f_index]
        
        list_file_name = upload_photo_name.split('.')
        list_file_name_new = list_file_name[0] + '_' + str(time.time()) + '_' + f_name + '.' + list_file_name[1]
        print(list_file_name_new)

        get_user_details = registration.query.filter_by(id=user_id).first()

        upload_files_details = uploads(user_id, get_user_details.name, get_user_details.email, get_user_details.phone, get_user_details.profile_url, secure_filename(list_file_name_new), description, t)

        db.session.add(upload_files_details)
        db.session.commit()

        app.config['UPLOAD_FOLDER'] = r'C:\Users\abc123\Desktop\python\Flask code\Matrimonial\photo\serve_photos'
        upload_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(list_file_name_new)))

        get_upload_file_details = uploads.query.filter_by(user_id=session['session_id']).order_by(uploads.id.desc()).first()
        get_photos = uploads.query.filter_by(user_id=user_id).all()

        photos_list = []
        for photo_res in get_photos:
            photos_dict = {
            "name":photo_res.file_name,
            "obj_description":photo_res.file_description,
            "upload_time":photo_res.uploading_time
            }
            photos_list.append(photos_dict)

        upload_list=[]
        upload_dict = {
            "name":get_upload_file_details.user_name,
            "photo_or_video":get_upload_file_details.file_name,
            "description":get_upload_file_details.file_description,
            "upload_time":get_upload_file_details.uploading_time,
            "series":json.dumps(photos_list),
            "response":"Upload Successfull."
        }
        upload_list.append(upload_dict)
        result = json.dumps(upload_list, indent=4)

        print('---------------------------------------------')
        print(result)
        print('---------------------------------------------')
        
        return jsonify(upload_list)


@app.route('/update-status', methods=['POST'])
def status_update():
    if request.method == 'POST':
        update_status = request.get_json()
        
        description = update_status[0]['status']
        file_name = update_status[1]['id']
 
        get_file_id = uploads.query.filter_by(file_name=file_name).first()

        id = get_file_id.id

        file_edit = uploads.query.get_or_404(id)
        file_edit.file_description = description

        db.session.add(file_edit)
        db.session.commit()
        
        get_file_desc = uploads.query.filter_by(id=get_file_id.id).first()

        desc_list = []
        desc_dict = {
            "description":get_file_desc.file_description,
            "user_account":get_file_desc.user_account_url,
            "response":"Description Updated Successfully!"
        }
        desc_list.append(desc_dict)
        result = json.dumps(desc_list, indent=4)

        print('---------------------------------------')
        print(result)
        print('---------------------------------------')

        return result
    

@app.route('/delete-status',methods=['POST'])
def status_deleted():
    if request.method == 'POST':
        session_url = session['session_url']

        delete_status = request.get_json()

        get_delete_id = delete_status[0]['id']

        get_file_id = uploads.query.filter_by(file_name=get_delete_id).first()
        id = get_file_id.id

        file_delete = uploads.query.get_or_404(id)

        db.session.delete(file_delete)
        db.session.commit()

        delete_list = []
        delete_dict = {
            "user_account":session_url,
            "response":"Post Successfully Deleted!"
        }
        delete_list.append(delete_dict)
        result = json.dumps(delete_list, indent=4)

        print('---------------------------------------')
        print(result)
        print('---------------------------------------')

        return jsonify(delete_list) 


@app.route('/fetch-photo-info', methods=['POST'])
def fetch_photo_display_info():
    if request.method == 'POST':
        fetch_info_all = request.get_json()

        file_name = fetch_info_all[0]['sendId']

        get_file_id = uploads.query.filter_by(file_name=file_name).first()

        fetch_list = []
        fetch_dict = {
            "img_or_vid_name":get_file_id.file_name,
            "content":get_file_id.file_description,
            "upload_time":get_file_id.uploading_time,
        }
        fetch_list.append(fetch_dict)
        result = json.dumps(fetch_list, indent=4)

        print('---------------------------------------')
        print(result)
        print('---------------------------------------')

        return result
    

@app.route('/send-file-status', methods=['POST'])
def send_profile_status():
    if request.method == 'POST':
        user_id = session['session_id']
        profile_file = request.files['file']
        profile_file_name = request.files['file'].filename
        description = request.form['description']

        t = datetime.now()

        f_alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        f_length = 25
        f_name = ""

        for i in range(f_length):
            f_index = random.randrange(len(f_alphabet))
            f_name = f_name + f_alphabet[f_index]
        
        list_file_name = profile_file_name.split('.')
        list_file_name_new = list_file_name[0] + '_' + str(time.time()) + '_' + f_name + '.' + list_file_name[1]

        app.config['UPLOAD_FOLDER'] = r'C:\Users\abc123\Desktop\python\Flask code\Matrimonial\photo\serve_photos'
        profile_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(list_file_name_new)))

        get_user_details = registration.query.filter_by(id=user_id).first()

        upload_files_details = uploads(user_id, get_user_details.name, get_user_details.email, get_user_details.phone, get_user_details.profile_url, secure_filename(list_file_name_new), description, t)

        db.session.add(upload_files_details)
        db.session.commit()
        get_upload_file_details = uploads.query.filter_by(user_id=session['session_id']).order_by(uploads.id.desc()).first()

        send_status_list = []
        send_status_dict = {
            "file_id":get_upload_file_details.id,
            "name":get_user_details.name,
            "photo_or_video":get_upload_file_details.file_name,
            "description":get_upload_file_details.file_description,
            "upload_time":get_upload_file_details.uploading_time
        }
        send_status_list.append(send_status_dict)
        result = json.dumps(send_status_list, indent=4)

        print('---------------------------------------')
        print(result)
        print('---------------------------------------')

        return jsonify(send_status_list)



@app.route('/send-status', methods=['POST'])
def user_send_status():
    if request.method == 'POST':
        user_id = session['session_id']
        json_data = request.get_json()

        description = json_data[0]['desc']
        default_file = 'NULL'

        t = datetime.now()

        get_user_details = registration.query.filter_by(id=user_id).first()

        upload_files_details = uploads(user_id, get_user_details.name, get_user_details.email, get_user_details.phone, get_user_details.profile_url, default_file, description, t)

        db.session.add(upload_files_details)
        db.session.commit()

        get_upload_file_details = uploads.query.filter_by(user_id=session['session_id']).order_by(uploads.id.desc()).first()

        send_status_list = []
        send_status_dict = {
                "user_id":get_upload_file_details.id,
                "name":get_upload_file_details.user_name,
                "description":get_upload_file_details.file_description,
                "upload_time":get_upload_file_details.uploading_time
        }
        send_status_list.append(send_status_dict)
        result = json.dumps(send_status_list, indent=4)

        print('---------------------------------------')
        print(result)
        print('---------------------------------------')

        return result


@app.route('/delete-post', methods=['POST'])
def delete_post():
    if request.method == 'POST':
        session_url = session['session_url']
        json_data = request.get_json()
        delete_id = json_data[0]['sendDeleteId']

        file_delete = uploads.query.get_or_404(delete_id)

        db.session.delete(file_delete)
        db.session.commit()

        # reaction ids corresponding to file id also need to delete.
        
        delete_list = []
        delete_dict = {
            "user_account":session_url,
            "response":"Post Successfully Deleted!"
        }
        delete_list.append(delete_dict)
        result = json.dumps(delete_list, indent=4)

        print('---------------------------------------')
        print(result)
        print('---------------------------------------')

        return jsonify(delete_list)
    

@app.route('/sent-edit-request', methods=['POST'])
def edit_post():
    if request.method == 'POST':
        session_url = session['session_url']
        json_data = request.get_json()
        edit_id = json_data[0]['sendEditId']

        file_edit = uploads.query.filter_by(id=edit_id).first()

        send_request_list = []
        send_request_dict = {
            "file_id":file_edit.id,
            "file_name":file_edit.file_name,
            "file_descr":file_edit.file_description,
            "time":file_edit.uploading_time
        }
        send_request_list.append(send_request_dict)
        result = json.dumps(send_request_list, indent=4)

        print('---------------------------------------')
        print(result)
        print('---------------------------------------')

        return result


@app.route('/save-edit',methods=['POST'])
def save_edit():
    if request.method == 'POST':
        session_url = session['session_url']
        json_data = request.get_json()
        edit_id = json_data[0]['file_id']
        edit_val = json_data[1]['val']

        file_edit = uploads.query.get_or_404(edit_id)
        file_edit.file_description = edit_val

        db.session.add(file_edit)
        db.session.commit()

        edit_success_list = []
        edit_success_dict = {
            "user_url":session_url,
            "response":"Successfully Updated."
        }
        edit_success_list.append(edit_success_dict)
        result = json.dumps(edit_success_list, indent=4)

        print('---------------------------------------')
        print(result)
        print('---------------------------------------')

        return result


@app.route('/send-like',methods=['POST'])
def send_like():
    if request.method == 'POST':
        user_id = session['session_id']
        json_data = request.get_json()

        get_file_id = json_data[0]['reactionId']
        print('Insert Like id is:- ',get_file_id)
        file_details = uploads.query.filter_by(id=get_file_id).first()
        
        send_reaction = 1
        t = datetime.now()
        react_by_details = registration.query.filter_by(id = user_id).first()

        save_user_reaction = users_react(file_details.user_id, file_details.id, file_details.user_name, file_details.user_email, file_details.user_ph, file_details.user_account_url, send_reaction, t, user_id, react_by_details.name, react_by_details.phone)
        db.session.add(save_user_reaction)
        db.session.commit()

        # xyz = users_react.query.filter(user_id = session['session_id']).count()
        total_like = users_react.query.with_entities(func.sum(users_react.reaction)).filter_by(user_id = session['session_id'], file_id = get_file_id).all()

        like_success_list = []
        like_success_dict = {
            "like":total_like[0][0],
            "file_id":get_file_id,
            "response":"Like Counted."
        }
        like_success_list.append(like_success_dict)
        result = json.dumps(like_success_list, indent=4)

        print('---------------------------------------')
        print(result)
        print('---------------------------------------')

        return result 
    

@app.route('/send-update-dislike',methods=['POST'])
def update_dislike():
    if request.method == 'POST':
        user_id = session['session_id']
        json_data = request.get_json()

        get_file_id = json_data[0]['reactionId']
        print('Update Dislike Id Is:- ',get_file_id)
        file_details = uploads.query.filter_by(id=get_file_id).first()

        reaction_details = users_react.query.filter_by(file_id=get_file_id, react_by_id=user_id).first()

        reaction_edit = users_react.query.get_or_404(reaction_details.id)
        reaction_edit.reaction = 0

        db.session.add(reaction_edit)
        db.session.commit()

        total_like = users_react.query.with_entities(func.sum(users_react.reaction)).filter_by(user_id = session['session_id'], file_id = get_file_id).all()

        like_success_list = []
        like_success_dict = {
            "update_dislike":total_like[0][0],
            "file_id":get_file_id,
            "response":"Updated DisLike Counted."
        }
        like_success_list.append(like_success_dict)
        result = json.dumps(like_success_list, indent=4)

        print('---------------------------------------')
        print(result)
        print('---------------------------------------')

        return result 


@app.route('/send-update-like',methods=['POST'])
def update_like():
    if request.method == 'POST':
        user_id = session['session_id']
        json_data = request.get_json()

        get_file_id = json_data[0]['reactionId']
        print('Update Dislike Id Is:- ',get_file_id)
        file_details = uploads.query.filter_by(id=get_file_id).first()

        reaction_details = users_react.query.filter_by(file_id=get_file_id, react_by_id=user_id).first()

        reaction_edit = users_react.query.get_or_404(reaction_details.id)
        reaction_edit.reaction = 1

        db.session.add(reaction_edit)
        db.session.commit()

        total_like = users_react.query.with_entities(func.sum(users_react.reaction)).filter_by(user_id = session['session_id'], file_id = get_file_id).all()

        like_success_list = []
        like_success_dict = {
            "update_like":total_like[0][0],
            "file_id":get_file_id,
            "response":"Updated Like Counted."
        }
        like_success_list.append(like_success_dict)
        result = json.dumps(like_success_list, indent=4)

        print('---------------------------------------')
        print(result)
        print('---------------------------------------')

        return result 
    

@app.route('/<url>/settings', methods=['GET'])
def get_settings(url):
    get_session_url = session['session_url']
    user_account_id = session['session_id']
    user_session_email = session['user_email']

    # user_details = uploads.query.filter_by(user_id=).first()
    # user_details = uploads.query.get_or_404(edit_id)

    if uploads.query.filter_by(user_id=user_account_id).first() is not None:
        file = 'exists'
        return render_template('settings.html', send_session_url=get_session_url, user_id=user_account_id, send_file_status=file)
    else:
        file = 'NULL' 
        return render_template('settings.html', send_session_url=get_session_url, user_id=user_account_id, send_file_status=file)


@app.route('/delete-all-post', methods=['POST'])
def delete_all_post():
    if request.method == 'POST':
        json_data = request.get_json()

        delete_user_id = json_data[0]['passId']
        get_all = uploads.query.filter_by(user_id=delete_user_id).all()

        for get_file_id in get_all:
            file_delete = uploads.query.get_or_404(get_file_id.id) 
            db.session.delete(file_delete)
            db.session.commit()

        get_all_reactions = users_react.query.filter_by(user_id=delete_user_id).all()

        for get_react_id in get_all_reactions:
            reaction_delete = users_react.query.get_or_404(get_react_id.id) 
            db.session.delete(reaction_delete)
            db.session.commit()

        like_success_list = []
        like_success_dict = {
            "message":"All your files removed successfully!"
        }
        like_success_list.append(like_success_dict)
        result = json.dumps(like_success_list, indent=4)

        print('---------------------------------------')
        print(result)
        print('---------------------------------------')

        return result


# @app.route('/account-activity', methods=['GET'])
# def forget():
#     return render_template('account_activity_page.html')


# @app.route('/notification', methods=['GET'])
# def forget():
#     return render_template('notify.html')


# @app.route('/send-message', methods=['GET'])
# def forget():
#     return render_template('message.html')


@app.route('/forget-password', methods=['GET'])
def forget():
    return render_template('forget_pass.html')


@app.route("/send-otp", methods=['POST'])
def index():
   if request.method == 'POST':
        
        enter_email = escape(request.form['enter_id'])
        # enter_phone = escape(request.form['enter_ph_no'])

        email_check = registration.query.filter_by(email = enter_email).first()
        # ph_check = registration.query.filter_by(phone = enter_phone).first()

        t = datetime.now()

        otp_alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        otp_length = 6
        otp_name = ""

        for i in range(otp_length):
            otp_index = random.randrange(len(otp_alphabet))
            otp_name = otp_name + otp_alphabet[otp_index]

        if email_check:
            # msg = Message(
            #     'Matrimonial OTP',
            #     sender ='yourId@gmail.com',
            #     recipients = [enter_email]
            #    )
            # msg.body = 'Good day to ' + email_check.name + '. Your requested OTP is:- ' + str(otp_name) + '. Generated on ' + datetime.now() + '. Don\'t share this to anyone. Matrimonial will not be responsible for any kind of Loss of information.' 
            # mail.send(msg)
            
            message = 'Good day to ' + email_check.name + '. Your requested OTP is:- ' + str(otp_name) + '. Generated on ' + str(t) + '. Don\'t share this to anyone. Matrimonial will not be responsible for any kind of Loss of information.'     
            print(message)

            otp_values = otpsave(email_check.id, email_check.name, enter_email, otp_name, t)

            db.session.add(otp_values)
            db.session.commit()

            return 'OTP Sent to ' + enter_email
        else:
            return 'Please provide your registered email.'


if __name__ == '__main__':  
   app.run(port=4700, debug = True) 



# ----USERS CREDENTIALS----

# John@gmail.com
# hEPHJNb*

# Jani@gmail.com
# st^Bsgvs

# RG@gmail.com
# HtSr0h49

# pamela@gmail.com
# 3YUPmODT

# shamik@gmail.com
# G5O16%Ye

# william@gmail.com
# aaXqN2RV

# suz@gmail.com
# %j$fKVZ8


# ----SQL STATEMENT----

#   select distinct react_by_id from users_react where react_by_id NOT IN (select react_by_id from users_react where react_by_id = 5);