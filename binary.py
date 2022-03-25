from flask import Flask, render_template, request, flash, redirect
from flask import *
import os
import shutil
from flask_mysqldb import MySQL, MySQLdb
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
import mysql
import json
import subprocess
import urllib.request
import MySQLdb.cursors
import sys
from flask_mysqldb import MySQL
import mysql.connector
from werkzeug.utils import secure_filename
import os
from fileconversion import*
# import magic
import urllib.request
import zipfile


def convertToBinary(filename):
    with open(filename, 'rb') as file:
        binarydata = file.read()
    return binarydata


def convertBinaryToFile(binarydata, filename):
    with open(filename, 'wb') as file:
        file.write(binarydata)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'cairocoders-ednalan'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Yashw@123@localhost:3306/deepblue'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Yashw@123'
app.config['MYSQL_DB'] = 'deepbluecomp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
# db = SQLAlchemy(app)

UPLOAD_FOLDER = "C:\\Users\\Yash\\PycharmProjects\\flask\\static\\files"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg',
                         'jpeg', 'docx', 'doc', 'rtf', 'odt', 'html', 'txt'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["POST", "GET"])
def hello():
    return render_template('Homepage.html')


@app.route('/upload2', methods=["POST", "GET"])
def upload2():
    return render_template('upload2.html')


@app.route("/upload", methods=['POST', 'GET'])
def upload():
    cur = mysql.connection.cursor()
    #cursor = mysql.connection.cursor()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
       # name = request.form.get('first name')
        #last = request.form.get('Last name')
        #mail = request.form.get('email')
        #addno = request.form.get('Admissionno')
        if 'fileInput' not in request.files:
            flash("No file part")
            return redirect(request.url)
        files = request.files.getlist('fileInput')
        val = 1

        # print(files)
       # enumerate(list)

        for file in files:

            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):

                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                binary = "C:\\Users\\Yash\\PycharmProjects\\flask\\static\\files\\" + filename
                #file1 = "C:\\Users\\Yash\\PycharmProjects\\flask\\static\\files\\2021-12-08.png"
                x = binary.rindex("\\")
                y = binary.index(".")

                num = str(val)
                val = val+1

                path = binary[:x + 1] + "resume" + num + binary[y:]
                filerename = "resume" + num + binary[y:]
                os.rename(binary, path)
                #binary = "C:\\Users\\Yash\\PycharmProjects\\flask\\static\\files\\"+filename
                binartfile = convertToBinary(path)

                cur.execute(
                    "INSERT INTO deepbluecomp_table(files_path,binaryfiles_path) VALUES (%s, %s)", (filerename, binartfile))
                print("hello")
                text1, link, mailid, phone_number, date, human_name, add, pincode, ftext = fileconversion(
                    path, num)
                cur.execute("INSERT INTO datastore( data, link, emailid, phoneno,date,humaname,address,code,data_two) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s )",
                            (text1, link, mailid, phone_number, date, human_name, add, pincode, ftext))

                #proc = subprocess.Popen('python author_script.py {}{} -p n -s n -m num'.format(UPLOAD_FOLDER, file.filename), shell=True,stdout=subprocess.PIPE)

    mysql.connection.commit()
    # print(file)
    cur.close()
    flash('File(s) successfully uploaded')
    # return redirect('/upload')
    return render_template('upload2.html')


@app.route("/delete")
def delete():

    folder = 'C:\\Users\\Yash\\PycharmProjects\\flask\\static\\files'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    return render_template('upload2.html')


if __name__ == "__main__":
    app.run(debug=True)

# app.run(debug=True)
