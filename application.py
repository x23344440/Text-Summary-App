from flask import Flask,redirect, request, render_template, jsonify, url_for
from database import create_connection
import requests
import os


application = Flask(__name__)

@application.route("/",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if name and email and password:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("insert into mstr_user (name, email, password) values (%s,%s,%s)",(name, email, password))
            conn.commit()
            cur.close()
        else:
            return "Data not found"
        return render_template("signup.html")
    else:
        return render_template("signup.html")


@application.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email and password:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("select * from mstr_user where email=%s and password=%s",(email, password))
            res = cur.fetchone()
            if res is None:
                return "Wrong email id password"
            else:
                return render_template("all.html")
        else:
            return "Data not found"
    else:
        return render_template("login.html")


@application.route("/all",methods=["GET","POST"])
def all():
    if request.method == "POST":
        return render_template("all.html")
    return render_template("all.html")
    
""" 
@application.route("/news",methods=["GET","POST"])
def news():
    news_data = None
    if request.method == "POST":
        keyword = request.form['keyword']
        country = request.form['country']

        API_URL = "http://127.0.0.1:3030/news"

        try:
            json_data = {"keyword": keyword, "country": country}
            response = requests.get(API_URL, json=json_data, stream=True)
            if response.status_code == 200:
                data = response.json()
                news_data = data.get("description", "No News Found")
                print("NEWZZZ ---------->> ",news_data)
            else:
                news_data = "Failed to get newz. Error from API."
        except Exception as e:
            news_data = f"An error occurred: {str(e)}"
    return render_template("all.html",news_data=news_data)  """


@application.route("/news", methods=["GET", "POST"])
def news():
    news_list = None
    descriptions = None  # Initialize descriptions to avoid errors

    if request.method == "POST":
        keyword = request.form['keyword']
        country = request.form['country']

        #API_URL = "http://127.0.0.1:3030/news"
        API_URL = "http://x23344440-scalable-api.eba-vj4crcif.ap-southeast-2.elasticbeanstalk.com/news"

        try:
            json_data = {"keyword": keyword, "country": country}
            response = requests.get(API_URL, json=json_data, stream=True)
            if response.status_code == 200:
                data = response.json()
                news_list = []

                # Extract title and description
                for article in data.get("results", []):
                    news_list.append({
                        "title": article.get("title"),
                        "description": article.get("description")
                    })

                # Extract only description values
                descriptions = [article.get("description") for article in data.get("results", [])]

                print("NEWZZZ ---------->> ", news_list)
                print("DESCRIPTIONS ----->> ", descriptions)

            else:
                news_list = "Failed to get newz. Error from API."

        except Exception as e:
            news_list = f"An error occurred: {str(e)}"

    return render_template("all.html", news_list=news_list, descriptions=descriptions)





@application.route("/summarization",methods=["GET","POST"])
def summarization():
    summary_text = None
    if request.method == "POST":
        text_input = request.form['text']
        #API_URL = "http://127.0.0.1:3030/summarize"
        API_URL = "http://x23344440-scalable-api.eba-vj4crcif.ap-southeast-2.elasticbeanstalk.com/summarize"

        try:
            json_data = {"text": text_input}
            response = requests.get(API_URL, json=json_data, stream=True)
            if response.status_code == 200:
                data = response.json()
                summary_text = data.get("Summarized Text", "No text translated")
                print("SUMMARIZED TEXT ---------->> ",summary_text)
            else:
                summary_text = "Failed to translate text. Error from API."
        except Exception as e:
            summary_text = f"An error occurred: {str(e)}"
    return render_template("all.html",summary_text=summary_text)



application.config['UPLOAD_FOLDER'] = './static'

@application.route("/text_to_speech", methods=["GET", "POST"])
def text_to_speech():
    download_url = None
    API_URL = "http://scalable-api-x23301295.eba-2tmezkmp.ap-southeast-2.elasticbeanstalk.com/text-to-speech"

    if request.method == "POST":

        text_input = request.form['text']
        
        if text_input:
           
            json_data = {"text": text_input}
            try:
                response = requests.get(API_URL, json=json_data, stream=True)
            
                if response.status_code == 200:
                    
                    file_path = os.path.join(application.config['UPLOAD_FOLDER'], 'api_audio.mp3')
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                    
                    download_url = url_for('static', filename='api_audio.mp3')
                else:
                    download_url = "Error generating audio. Try again."
            except Exception as e:
                download_url = f"An error occurred: {str(e)}"
    
    return render_template("all.html", download_url=download_url)




if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)