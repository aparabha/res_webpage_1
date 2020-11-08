from flask import Flask, render_template, url_for
import boto3
import json
import mysql.connector

ENDPOINT = "database-1.cljk2mlqcooe.eu-central-1.rds.amazonaws.com"
PORT = "3306"
USR = "admin"
PASSWD = "adminabc"
REGION = "eu-central-1"
DBNAME = "DATADOG"

app = Flask(__name__)


def getdata():
    # session = boto3.Session(profile_name='default')
    # client = boto3.client('rds')
    try:
        conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PASSWD, port=PORT, database=DBNAME)
        cur = conn.cursor()
        cur.execute("select * from OurMenu")
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json_data

    except Exception as e:
        print("Database connection failed due to {}".format(e))


@app.route('/')
def main():
    # data = []
    data = getdata()
    url='https://apara-bucket-1.s3.eu-central-1.amazonaws.com/catering/'
    return render_template("index.html", data=data, url=url)
    # return "Hello"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
