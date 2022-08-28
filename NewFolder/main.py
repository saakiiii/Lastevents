from ast import keyword
import html
import json
import re
from time import sleep, time
from unicodedata import category
from urllib import response
from flask import Flask, flash, jsonify, make_response, render_template, request, redirect, send_file
from flask_login import current_user
from CoStCi import CountriesStatesCities
from backend import BackEnd
from flask_login import LoginManager, login_user, current_user, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from codegenerator import codeId
from forgotpassword import ResetPassword
from contact import Contactemail
# from SearchApi import SearchApi
from codegenerator import codeId
# from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder = 'static')
be = BackEnd()
csc = CountriesStatesCities()
fp = ResetPassword()
cont = Contactemail()
# se = SearchApi()
# socketio = SocketIO(app)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user__.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "password"

login_manager = LoginManager()
login_manager.init_app(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def _():
    home_meta = '''lastevents(news) | Space for reading and composing news(lastevents) articles in real-time, we are trying to provide you with high-quality news about the latest events, compose news in your style, and get paid.'''
    # title = "Space for sharing the latest events and keep yourself updated."
    title = "Space for reading, writing news and earning. Share the latest events and keep yourself updated by news articles"
    metaimage = "https://images.lastevents.space/logo.jpg"

    if current_user.is_authenticated == True:
    #  drafts = be.getdraftsofUser(user_id=current_user.user_id)
    #  notifications = be.getNotifcations(user_id=current_user.user_id)
      pass
    return render_template("welcome.html", logged_in = current_user.is_authenticated, welcome=True, title=title, metadata=home_meta, metaimage=metaimage)

    # return redirect('/home')

@app.route('/signup', methods=['POST', 'GET'])
def register():
    title = 'Signup | lastevents.space'
    metadata = "Signup and enter into this space to read, write and earn simply. See the last events' updates"
    if request.method == 'POST':
        if current_user.is_authenticated:
         return redirect("/")
        email = request.form["email"]
        password = request.form["password"]
        username = request.form["username"]
        country = request.form["country"]
        state = request.form["state"]
        city = request.form["city"]
        count = 0
        emailalert = None
        passwordalert = None
        # confirmpasswordalert = None
        countalert = None
        statealert = None
        catalert = None
        cityalert = None
        usernamealert = None
        alert = None
        if country.isspace() or len(country) < 1:
            countalert = "Field should not be empty"
            count += 1
        if state.isspace() or len(state) < 1:
            statealert = "Field should not be empty"
            count += 1
        if username.isspace() or len(username) < 1:
            usernamealert = "Username should not be emtpy"
            count += 1
        if city.isspace() or len(city) < 1:
            cityalert = "Field should not be empty"
            count += 1
        if email.isspace() or len(email) < 1:
            emailalert = "Email should not be empty"
            count += 1
        if len(password) < 1:#isspace()
            passwordalert = "Password should not be empty"
            count += 1
        if not be.validemail(email=email):
            emailalert = "Email already exists"
            count += 1
        if len(password) < 8:
            passwordalert = "Password should have minimum of '8' characters"
            count += 1
        if not be.validusername(username=username):
            usernamealert = "username not available"
            count += 1
        # if len(confirmpassword) < 1:#isspace()
        #     confirmpasswordalert = "border : 1px solid red; box-shadow: none"
        #     count += 1

        if count > 0:
            return render_template('signup.html',
                                   countalert=countalert,
                                   statealert=statealert,
                                   catalert=catalert,
                                   cityalert=cityalert,
                                   emailalert=emailalert,
                                   passwordalert=passwordalert,
                                #    confirmpasswordalert=confirmpasswordalert,
                                   usernamealert=usernamealert,
                                   countryval=country,
                                   stateval=state,
                                   cityval=city,
                                   emailval=email,
                                   passwordval=password,
                                #    confirmpasswordval=confirmpassword,
                                   usernameval=username,
                                   logged_in = current_user.is_authenticated,
                                   title='Sign Up | lastevents.space',
                                   signup_login_="#8479794f",
                                   redi=True,
                                   is_signinpage=True
                                   )

        response = be.create_user(email=email,
                                 password=password,
                                 username=username,
                                 country = country,
                                 state = state,
                                 city = city
                                 )
        # return jsonify({"result":response})
        newuser = User(user_id = response["user_id"],
                       username=username,
                       email=email,
                       password=response["password"])
        db.session.add(newuser)
        db.session.commit()
        return redirect('/verify')
    else:
        if current_user.is_authenticated:
            return redirect("/")
        return render_template("signup.html", logged_in = current_user.is_authenticated, title=title, metadata=metadata, signup_login_="#8479794f")

@app.route('/login', methods=['POST', 'GET'])
def signin():
    to = request.args.get("to")
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect('/')
        req = request.form
        email = req["email"]
        password = req["password"]
        to = request.args.get("to")
        emailalert = None
        passwordalert = None
        count = 0
        if email.isspace() or len(email) < 1:
            emailalert = "Email should not be empty"
            count += 1
        if password.isspace() or len(password) < 1:
            passwordalert = "Password should not be empty"
            count += 1
        if  count > 0:
            return render_template("signin.html", emailalert=emailalert, passwordalert=passwordalert, logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f", is_signinpage=True)
        if not be.validemail(email):
            if be.validemail_and_password_for_login(email, password):
                user = User.query.filter_by(email=email).first()
                login_user(user)
                # be.setNotification(user_id=current_user.user_id, notify_msg="Logged in")
                if to == None:
                  if not be.is_verified(user_id=current_user.user_id):
                    return redirect("/home")
                  else:
                    return redirect("/home")
                else:
                    return redirect(to)
            else:
                if to != None:
                    return render_template("signin.html", is_signinpage=True, to=f"?to={to}", passwordalert="Password incorrect", logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f")
                else:
                    return render_template("signin.html", is_signinpage=True, passwordalert="Password incorrect", logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f")
        else:
            if to != None:
                    return render_template("signin.html", is_signinpage=True, to=f"?to={to}", emailalert="Email not found", logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f")
            return render_template("signin.html", is_signinpage=True, emailalert="Email not found", logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f")
    else:
        # if current_user.is_authenticated:
        #     return redirect("/")
        if current_user.is_authenticated:
            return redirect('/')
        if to != None:
           return render_template("signin.html", is_signinpage=True, to=f"?to={to}", alert="Writing requires login", logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f")
        return render_template("signin.html", is_signinpage=True, logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f")
        # return render_template("signin.html")

# @app.route('/news/read')
# def news_read():
#     title = "News | World News | Local News | Detailed News | Breifs | Write News | RecentUpdates - lastevents.space"
#     metadata = """lastevents.space - Space for reading, writing recently updated news articles in real-time, we are trying to provide you with high-quality news about the lastest events, write news in your own style and get paid."""
#     metaimage = "https://images.lastevents.space/logo.jpg"
#     if request.method == 'GET':
#     #   todays_word = be.get_todays_word()
#        if current_user.is_authenticated and request.args.get('tpe') != "ww":
#             user = be.get_user_instance(user_id=current_user.user_id)
#             return redirect(f"/news/read/{user['country']}/{user['state']}/general/{user['city']}")
#        else:
#             articles_news = be.get_all_news_content()
#             # blogs = be.blog_get()[0:10]
#             blogs = []
#             return render_template("read.html",
#                               logged_in = current_user.is_authenticated,
#                               title=title,
#                               metadata=metadata,
#                               read__="#8479794f",
#                               response = articles_news,
#                               recent_blogs = blogs,
#                               __me__=True,
#                               metaheadingurl="/news/read",
#                               metaimage=metaimage
#                               )
#     else:
#         return "Method not allowed"

@app.route('/news/read')
def newsread_():
    headline = be.get_all_news_content()[0]

    metaimage = "https://images.lastevents.space/logo.jpg"
    metadata = "lastevents.space - Space for reading, writing recently updated news articles in real-time, we are trying to provide you with high-quality news about the lastest events, write news in your own style and get paid."
    title = "News | World News | Local News | Detailed News | Briefs | Write News | RecentUpdates - lastevents.space"
    if current_user.is_authenticated:
        # user = be.get_user_instance(current_user.user_id)
        # exact = be.get_exact(country=user["country"], state=user["state"], city=user["city"], category="general")
        user_instance = be.get_user_instance(current_user.user_id)
        country = user_instance["country"]
        state = user_instance["state"]
        category = "General"
        city = user_instance["city"]
        fa08 = request.args.get("fi")
        if fa08 == "filter":
            country = request.args.get("co")
            state = request.args.get("st")
            city = request.args.get("ci")
            category = request.args.get("ca")

        return render_template("read1.html", title=title, metaimage=metaimage, metadata=metadata, headline = headline, fa08 = fa08, country=country, state=state, category=category, city=city, logged_in = current_user.user_id)
    else:
        return render_template("read1.html", title=title, metaimage=metaimage, metadata=metadata, headline = headline, country="United States", state="Washington", category="General", city="")

@app.route("/cav/<country>/<state>/<category>/<city>/4231", methods=["POST"])
def newsexact(country, state, category, city):
    return jsonify({"response":be.get_exact(country=country, state=state, category=category, city=city)})

@app.route("/cav/<country>/<state>/<city>/4232", methods=["POST"])
def newscity(country, state, city):
    return jsonify({"response":be.get_city(country=country, state=state, city=city)})

@app.route("/cav/<country>/<state>/4233", methods=["POST"])
def newsstate(country, state):
    val = be.get_state(country=country, state=state)
    return jsonify({"response":val})

@app.route("/cav/<country>/4234", methods=["POST"])
def newscountry(country):
    return jsonify({"response":be.get_country(country=country)})

@app.route("/cav/<country>/<category>/4235", methods=["POST"])
def newscategory(country, category):
    user_instance = be.get_user_instance(current_user.user_id)
    country = user_instance["country"]
    category = category
    return jsonify({"response":be.get_category(country=country, category=category)})

@app.route("/cav/wroo/4236", methods=["POST"])
def newsworldwide():
    return jsonify({"response":be.get_all_news_content()})

@app.route('/blog/read')
def blog_read():
    title = "Blog | Read | RecentArticles - lastevents.space"
    metadata = 'Space for reading and writing blog articles, write and monetize your content here.'
    metaimage = "https://images.lastevents.space/logo.jpg"
    if request.method == 'GET':
        # response = be.blog_get()
        response = []
        if current_user.is_authenticated:
            return render_template("blog.html", response=response, logged_in = current_user.is_authenticated, title=title, metadata=metadata, blog__="#8479794f", metaheadingurl="/blog/read")
        return render_template("blog.html", response=response, logged_in = current_user.is_authenticated, title=title, metadata=metadata, blog__="#8479794f", metaheadingurl="/blog/read", metaimage=metaimage)

@app.route('/blog/rec/ho', methods=["GET", "POST"])
def api_blog_read():
    if request.method == 'POST':
        response = be.blog_get()
        return jsonify({"response":response})

@app.route('/blog/rec/h', methods=["GET", "POST"])
def api_blog_read_():
    if request.method == 'POST':
        response = be.blog_get(for_="recent")
        return jsonify({"response":response})

# @app.route('/news/read/filter', methods = ['POST', 'GET'])
# def news_get_filter():
#     if request.method == 'POST':
#         req = request.form
#         country = req["country"].title()
#         state = req["state"].title()
#         category = req["category"].title()
#         city = req["city"].title()
#         if city != None:
#          city = city.title()
#         count = 0
#         countalert = None
#         statealert = None
#         catalert = None
#         cityalert = None
#         if len(city) < 1:
#             city = None
#         if country.isspace() or len(country) < 1:
#             countalert = "border : 1px solid red; box-shadow: none"
#             count += 1
#         if state.isspace() or len(state) < 1:
#             statealert = "border : 1px solid red; box-shadow: none"
#             count += 1
#         if category.isspace() or len(category) < 1:
#             catalert = "border : 1px solid red; box-shadow: none"
#             count += 1
#         # if city.isspace() or len(city) < 1:
#         #     cityalert = "border : 1px solid red; box-shadow: none"
#         #     count += 1
#         if count > 0:

#          return render_template("read.html",
#                                countalert=countalert,
#                                statealert=statealert,
#                                catalert=catalert,
#                                cityalert=cityalert,
#                                todays_word = be.get_todays_word(),
#                                alert=True,
#                                logged_in = current_user.is_authenticated,
#                                title=f"News | {country} | {category} | lastevents.space",
#                                read__="#8479794f",
#                                __me__ = True,)

#         return redirect(f"/news/read/{country}/{state}/{category}/{city}")

@app.route('/news/read/filter/<country>/<state>/<category>/<city>', methods = ['POST', 'GET'])
def news_get_filter(country, state, category, city):
    if request.method == 'POST':
        # country = req["country"].title()
        # state = req["state"].title()
        # category = req["category"].title()
        # city = req["city"].title()
        # return redirect(f"/news/read/{country}/{state}/{category}/{city}")
        return redirect(f"/cav/{country}/{state}/{category}/{city}/4231")


@app.route("/news/read/view/<news_id_or_news_heading>")
def view_news_article(news_id_or_news_heading):
    # formatted_url = news_id_or_news_heading.replace('-', ' ')
    news = be.view_news_article(news_id_or_news_heading)
    # return jsonify({"news":news})\
    # news["news"] = html.unescape(news["news"])
    # related_news = be.news_get()
    comments = be.getCommentsofArticle(article_id = news_id_or_news_heading)
    # comments = []
    if news == 'blog':
        return redirect(f'/blog/read/view/{news_id_or_news_heading}')
    title = f"{news['heading']} - lastevents.space"
    # data = be.all_news_articles_than_one(news_id_or_news_heading)[0:10]
    data = []
    # metaimage = news["image"]["bytes"]
    metaimage = f"http://127.0.0.1:8000/fi/im/osi/{news_id_or_news_heading}"
    if metaimage == None:
        metaimage = "https://images.lastevents.space/noload.jpg"
    if current_user.is_authenticated:
     return render_template("view.html", response=news, news=True, logged_in = current_user.is_authenticated, data=data, metaimage=metaimage, title=title, metaheadingurl="/news/read/view/"+news_id_or_news_heading, comments=comments, news_id=news_id_or_news_heading)
    return render_template("view.html", response=news, news=True, logged_in = current_user.is_authenticated, data=data, metaimage=metaimage, title=title, metaheadingurl="/news/read/view/"+news_id_or_news_heading, comments=comments, news_id=news_id_or_news_heading)

@app.route("/fi/im/osi/<news_id>")
def fiimosi(news_id):
    if request.method == "GET":
     article = be.view_news_article(news_id)
     image = be.get_first_image(article["news"])
     image_url = image["bytes"]
     if image_url != None:
      return redirect(image["bytes"])
     else:
      return redirect("https://images.lastevents.space/noload.jpg")

@app.route("/ana/a42/us4/<news_id>", methods=["POST", "GET"])
def getallnewsarticlesthanone(news_id):
    if request.method == 'POST':
        data = be.all_news_articles_than_one(news_id)[0:10]
        return jsonify({"response":data})

@app.route("/blog/read/view/<blog_id_or_blogs_heading>")
def view_blogs_article(blog_id_or_blogs_heading):
    # formatted_url = blog_id_or_blogs_heading.replace('-', ' ')
    blog = be.view_blogs_article(blog_id_or_blogs_heading)
    # for_you_blogs = be.blog_get()
    title = f"{blog['heading']} - lastevents.space"
    # metadata = blog["description"]
    metadata = ''
    metaimage = blog["image"]["bytes"]
    if metaimage == None:
        metaimage = "https://images.lastevents.space/noload.jpg"
    data = be.all_blog_aritcles_than_one(heading_url=blog_id_or_blogs_heading)[0:10]
    comments = be.getCommentsofArticle(article_id=blog_id_or_blogs_heading)
    if current_user.is_authenticated:
     return render_template("view.html", response=blog, blog=True, logged_in = current_user.is_authenticated, data=data[0:10], metaimage=metaimage, title=title, metadata=metadata, read__="#8479794f", comments=comments, metaheadingurl="/blog/read/view/"+blog_id_or_blogs_heading)
    return render_template("view.html", response=blog, blog=True, logged_in = current_user.is_authenticated, data=data[0:10], metaimage=metaimage, title=title, metadata=metadata, read__="#8479794f", comments=comments, metaheadingurl="/blog/read/view/"+blog_id_or_blogs_heading)
    # return jsonify({"blog":blog})

@app.route('/news/read/<country>/<state>/<category>/<city>')
def news_get_country_state_category(country, state, category, city):
    if city.isspace() or len(city) < 1:
        city = None
    response = be.news_get(
                       country=country.title(),
                       state=state.title(),
                       category=category.title(),
                       city=city.title()
                          )
    # return jsonify({"results":response})
    # todays_word = be.get_todays_word()
    # blogs = be.blog_get()[0:10]
    blogs = []
    metaimage = "https://images.lastevents.space/logo.jpg"
    if current_user.is_authenticated:
     return render_template("read.html",
                           response = response,
                           country=country,
                           state=state,
                           category=category,
                           city=city,
                           logged_in = current_user.is_authenticated,
                           recent_blogs=blogs,
                           title=f"News | Read | {country} | {category}",
                           read__="#8479794f",
                           __me__=True,
                           code_342 = True,
                           metaheadingurl=f"/news/read/{country}/{state}/{category}/{city}",
                           metaimage=metaimage
                           )

    return render_template("read.html",
                           response = response,
                           country=country,
                           state=state,
                           category=category,
                           city=city,
                           logged_in = current_user.is_authenticated,
                           recent_blogs=blogs,
                           title=f"News | Read | {country} | {category}",
                           read__="#8479794f",
                           __me__=True,
                           code_342 = True,
                           metaheadingurl=f"/news/read/{country}/{state}/{category}/{city}",
                           metaimage=metaimage
                           )

@app.route('/earninfo')
def earninfo():
    title = "Earn | Info - lastevents.space "
    metadata = "lastevents.space - Space for earning by writing lastestevents(news) or blog articles, make money as simple as possible by writing the news around you."
    if current_user.is_authenticated:
        return render_template('earninfo.html', logged_in = current_user.is_authenticated, title=title, metadata = metadata, earninfo__="#8479794f")
    return render_template('earninfo.html', logged_in = current_user.is_authenticated, title=title, metadata = metadata, earninfo__="#8479794f")

@app.route('/create/draft', methods=["POST"])
def create_draft():
    if request.method == 'POST':
        if current_user.is_authenticated:
            data = request.get_json()
            draftvalue = be.createDraft(user_id=current_user.user_id, type_=data["type"])
            return jsonify({"response":draftvalue})

@app.route('/news/write')
def newswrite():
    title = 'News | Write - lastevents.space'
    metadata = 'lastevents.space is the space for writing news article, lastest events. Start your earning here...'
    if current_user.is_authenticated:
     fa = request.args.get("fa")
     if fa == 'edit':
         i = request.args.get("i")
         news = be.get_news_by_id(news_id=i, user_id=current_user.user_id)
         return render_template('newswrite.html',
                            editing__ = True,
                            logged_in = current_user.is_authenticated,
                            title= 'News | Edit - lastevents.space', metadata=metadata,
                            write__="#8479794f",
                            news_id = i,
                            news = news,
                            _ = True)

     data = []
     news_id = codeId().generate_id()
     be.edit_news_draft(news_id=news_id)
     return render_template('newswrite.html',
                            editing__ = False,
                            logged_in = current_user.is_authenticated,
                            title=title, metadata=metadata,
                            write__="#8479794f",
                                news_id = news_id,
                            _ = True,
                            news = ""
                            )

    else:
     return redirect("/login?to=/news/write")

@app.route('/wri/a42/us4', methods=["POST", "GET"])
def userwritedetail():
    if request.method == "POST":
      if current_user.is_authenticated:
        return jsonify({"response":be.get_user_instance(current_user.user_id)})
      else:
          return jsonify({"response":"Unauthorized"})



@app.route('/opm/a42/us4', methods=["POST", "GET"])
def getopiallapi():
    if request.method == "POST":
        value = be.get_all_opis()
        value.reverse()
        return jsonify({"response":value})

@app.route('/news/edit/<heading_url>')
def newswrite_edit(heading_url):
    if current_user.is_authenticated:
       if request.args.get('v') != 'dt':
        news = be.view_news_article(url_heading=heading_url)
        if current_user.user_id != news["author_id"]:
            return "Unauthorized"
        return render_template('newswrite.html',
                            user_country = news["country"],
                            user_state = news["state"],
                            user_city= news["city"],
                            news_category=news["category"],
                            news_heading=news["heading"],
                            news_news=news["news"],
                            getvalue=f"?edit=True&p={heading_url}",
                            editing_ = True,
                            logged_in = current_user.is_authenticated,
                            title="News | Edit | lastevents.space",
                            _ = True)
       elif request.args.get('v') == 'dt':
        draft = be.getdraft(draft_id=request.args.get('viawe'))
        if current_user.user_id != draft["user_id"]:
            return "Unauthorized"
        return render_template('newswrite.html',
                            news_heading=news["heading"],
                            news_news=draft["article_data"],
                            editing_ = True,
                            logged_in = current_user.is_authenticated,
                            title="News | Edit | Draft | lastevents.space",
                            _ = True)
    else:
        return redirect('/login')

@app.route('/news/edit')
def newseditdraft():
    if current_user.is_authenticated:
       if request.args.get('v') == 'dt':
        user = be.get_user_instance(user_id=current_user.user_id)
        draft = be.getdraft(draft_id=request.args.get('viawe'))
        if current_user.user_id != draft["user_id"]:
            return "Unauthorized"
        return render_template('newswrite.html',
                            user_country = user["country"],
                            user_state = user["state"],
                            user_city = user["city"],
                            news_heading=draft["heading"],
                            news_news=draft["article_data"],
                            editing__ = True,
                            draftvalue = request.args.get('viawe'),
                            getvalue = f"?v=dt&viawe={request.args.get('viawe')}",
                            logged_in = current_user.is_authenticated,
                            title="News | Edit | Draft | lastevents.space",
                            _ = True)
       else:
           return "Page Not Found"
    else:
        return redirect('/login')

@app.route('/blog/edit')
def blogeditdraft():
    if current_user.is_authenticated:
       if request.args.get('v') == 'dt':
        user = be.get_user_instance(user_id=current_user.user_id)
        draft = be.getdraft(draft_id=request.args.get('viawe'))
        if current_user.user_id != draft["user_id"]:
            return "Unauthorized"
        return render_template('blogwrite.html',
                            blog_heading=draft["heading"],
                            blog_blog=draft["article_data"],
                            editing__ = True,
                            draftvalue = request.args.get('viawe'),
                            getvalue = f"?v=dt&viawe={request.args.get('viawe')}",
                            logged_in = current_user.is_authenticated,
                            title="Blog | Edit | Draft | lastevents.space",
                            _ = True)
       else:
           return "Page Not Found"
    else:
        return redirect('/login')


@app.route('/blog/edit/<heading_url>')
def blogeditwrite_edit(heading_url):
    if current_user.is_authenticated:
        blog= be.view_blogs_article(url_heading=heading_url)
        if current_user.user_id != blog["author_id"]:
            return "Unauthorized"
        return render_template('blogwrite.html',
                            blog_heading=blog["heading"],
                            blog_blog=blog["blog"],
                            getvalue=f"?edit=True&p={heading_url}",
                            editing__ = True,
                            logged_in = current_user.is_authenticated,
                            title="Blog | Edit | lastevents.space",
                            _ = True)

@app.route('/blog/write')
def blogwrite():
    title = 'Blog | Write - lastevents.space'
    metadata = 'lastevents.space is the space for writing news articles, blog articles, interesting topics, and coding snippets. Start your earnings here.'
    if current_user.is_authenticated:
    #  draftvalue = be.createDraft(user_id=current_user.user_id, type_="blog")
     fa = request.args.get("fa")
     if fa == 'edit':
         i = request.args.get("i")
         blog = be.get_blog_by_id(blog_id=i, user_id=current_user.user_id)
         return render_template('blogwrite.html',
                            editing__ = True,
                            logged_in = current_user.is_authenticated,
                            title= 'Blog | Edit - lastevents.space', metadata=metadata,
                            write__="#8479794f",
                            blog_id = i,
                            blog = blog,
                            _ = True)

     blog_id = codeId().generate_id()
     be.edit_blog_draft(blog_id=blog_id)
     return render_template('blogwrite.html',
                            editing__=None,
                            logged_in = current_user.is_authenticated,
                            title=title, metadata=metadata,
                            write="#8479794f",
                            _ = True,
                            blog_id=blog_id,
                            blog = '',
                            )
    else:
     return redirect("/login?to=/blog/write")

# @app.route('/wofday/write')
# def wordofthedaywrite():
#     if current_user.is_authenticated:
#      if be.is_woftheday_stack_available():
#       return render_template('wordofthedaywrite.html',
#                              logged_in = current_user.is_authenticated,
#                              title="Word Of The Day | Write | lastevents.space",
#                              value=True,
#                              )
#      else:
#       return render_template('wordofthedaywrite.html',
#                               logged_in = current_user.is_authenticated,
#                               title="Word Of The Day | Write | lastevents.space",
#                               value=False,
#                           )
#     else:
#      return redirect("/login?to=/wofday/write")

@app.route('/forgotpassword', methods=['POST', 'GET'])
def forgotpassword():
    if request.method == 'POST':
         email = request.form["email"]
         if not be.validemail(email=email):
           fp.sendresetpasswordmail(email=email)
           return render_template("forgotpassword.html", logged_in = current_user.is_authenticated, title="ForgotPassword", alert="Check your mail for further details")
         else:
           return render_template("forgotpassword.html", logged_in = current_user.is_authenticated, title="ForgotPassword", alert="This email account is not registered")
    return render_template("forgotpassword.html", logged_in = current_user.is_authenticated, title="ForgotPassword")

@app.route('/resetpassword', methods=['POST', 'GET'])
def resetpassword():
    key = request.args.get('key')
    if request.method == 'POST':
        password = request.form["password"]
        confirm_password = request.form["confirmpassword"]
        key = request.args.get('key')
        if len(password) > 7 :
         if password == confirm_password:
            val = fp.resetpassword(newpassword=password, key=key)
            if val == "Link Expired":
               return render_template("resetpassword.html", logged_in = current_user.is_authenticated, title="Resetpassword", key=key, alert=val)
            return render_template("resetpassword.html", logged_in = current_user.is_authenticated, title="Resetpassword", key=key, alert="Your password has been changed successfully")
         else:
            return render_template("resetpassword.html", logged_in = current_user.is_authenticated, title="Resetpassword", key=key, alert="Password and confirm password should be same")
        else:
            return render_template("resetpassword.html", logged_in = current_user.is_authenticated, title="Resetpassword", key=key, alert="Password field is required and have minimun of 8 characters")
    return render_template("resetpassword.html", logged_in = current_user.is_authenticated, title="Resetpassword", key=key)

@app.route("/data/ndr/<get_value>")
def notinddraft(get_value):
    title = None
    if get_value == 'dr':
        title = "Drafts"
        data = be.getdraftsofUser(user_id=current_user.user_id)
    elif get_value == 'not':
        title = "Notifications"
        data = be.getNotifcations(user_id=current_user.user_id)
    return render_template("notinddrafts.html", data=data, get_value = get_value, logged_in = current_user.is_authenticated, title=title)

# @app.route('/wordmean')
# def wordmean():
#     response = be.get_todays_word()
#     if current_user.is_authenticated:
#     return render_template("wordmean.html",
#                           response=response,
#                           logged_in = current_user.is_authenticated,
#                           title="Word | Meaning | lastevents.space",
#                           )

@app.route('/home')
def home():
    # home_meta = '''Space for reading, writing news, and earning money from your news and blog articles. We are providing you with news updates and the last events in our space'''
    # title = "Space for sharing the latest events and keep yourself updated."
    # if current_user.is_authenticated == True:
    # return render_template("welcome.html", logged_in = current_user.is_authenticated, welcome=True, title=title, metadata=home_meta)
    return redirect('/')

@app.route('/verify', methods=['POST', 'GET'])
def verify():
    if request.method == 'GET':
      if current_user.is_authenticated:
        if be.is_verified(user_id=current_user.user_id):
            return redirect('/home')
        else:
            val = be.send_verification_code(email=current_user.email, user_id=current_user.user_id, username=current_user.username)
            # notifications = be.getNotifcations(user_id=current_user.user_id)
            # drafts = be.getdraftsofUser(user_id=current_user.user_id)
            return render_template('verify.html', logged_in = current_user.is_authenticated, title="Verify", email=current_user.email)
      else:
            # notifications = be.getNotifcations(user_id=current_user.user_id)
            # drafts = be.getdraftsofUser(user_id=current_user.user_id)
            # notifications = None
            # drafts = None
            # return render_template('verify.html', logged_in = current_user.is_authenticated, title="Verify", email=current_user.email, notifications=notifications, drafts=drafts)
            return redirect("/login")
    if request.method == 'POST':
        if current_user.is_authenticated:
            code = request.form['code']
            val = be.check_verification_code(email=current_user.email, user_id=current_user.user_id, code=code)
            if val == True:
             return redirect('/')
            else:
             return render_template('verify.html', logged_in = current_user.is_authenticated, title="Verify", email=current_user.email, alert="Incorrect Code", metaheadingurl="/")

@app.route('/data/<href>')
def userdata(href):
    if current_user.is_authenticated:
        data = be.get_user_instance(user_id=current_user.user_id)
        me = False
        yourarticles = False
        yourincome = False
        news_2324 = False
        blog_2324 = False
        comments_2324 = False
        bac_val_me = None
        bac_val_art = None
        bac_val_yi = None
        pname = be.get_page_name_by_user_id(user_id=current_user.user_id)
        if href == "me":
            me = True
            data["contributions"] = be.calculate_user_contribution(user_id=current_user.user_id)
            bac_val_me = "#8479794f"
        elif href == "yourarticles":
            yourarticles = True
            bac_val_art = "#8479794f"
            if request.args.get("t") == "news":
                user_articles = be.get_users_articles(user_id=current_user.user_id)
                data["articles"] = user_articles
                data["total_articles"] - len(user_articles)
                news_2324 = True
            if request.args.get("t") == "blog":
                user_blog_articles = be.get_users_blog_article(user_id=current_user.user_id)
                data["articles"] = user_blog_articles
                data["total_blog_articles"] = len(user_blog_articles)
                blog_2324 = True
            if request.args.get("t") == "comments":
                user_comments = be.getCommentsofUser(user_id=current_user.user_id)
                data["total_comments"] = len(user_comments)
                data["comments"] = user_comments
                comments_2324 = True
        elif href == "yourincome":
            yourincome = True
            bac_val_yi = "#8479794f"
        else:
            return redirect("/op-me")
        return render_template("data.html",
                            response=data,
                            me = me,
                            yourarticles = yourarticles,
                            yourincome = yourincome,
                            news_2342 = news_2324,
                            blog_2342 = blog_2324,
                            comments_2324 = comments_2324,
                            logged_in = current_user.is_authenticated,
                            me_=bac_val_me,
                            articles_=bac_val_art,
                            yourincome_ = bac_val_yi,
                            title="News | Articles | Data | lastevents.space",
                            me__="#8479794f",
                            __me__ = True,
                            pname = pname
                            )
    else:
        return redirect('/login')
# @app.route('/api/news/article/write', methods=['POST', 'GET'])
# def api_news_article_write():
#     if request.method == 'POST':
#         if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
#             req = request.get_json()
#             heading = req["heading"]
#             news = req["news"]
#             if heading.isspace():
#                 return "Heading should not be empty"
#             else:
#                 pass
#             if len(heading) < 1:
#                 return "Heading should not be empty"
#             else:
#                 pass
#             if news.isspace():
#                return "Text Field should not be empty"
#             else:
#                 pass
#             if len(news) < 1:
#                return "Text Field should not be empty"
#             else:
#                 pass
#             country = req["country"]
#             category = req["category"]
#             state = req["state"]
#             city = req["city"]
#             keywords = req["keywords"]
#             # author_id = current_user.user_id
#             author_id = "ZOmRx01085587870"
#             response = be.news_article_write(
#                 heading=heading,
#                 author_id=author_id,
#                 news=news,
#                 country=country.title(),
#                 category=category.title(),
#                 state=state.title(),
#                 city=city.title(),
#                 keywords=keywords
#             )
#             return jsonify({"message":response})
#         else:
#             return "Unauthorized"
#     else:
#         return "Invalid Request"

@app.route('/me/<username>')
def profile(username):
    user = be.get_user_by_username(username = username)
    newsposts_ = []
    blogposts_ = []
    newsposts = be.get_users_articles(user["user_id"])
    blogposts = be.get_users_blog_article(user["user_id"])
    newsposts_.extend(newsposts["today"])
    newsposts_.extend(newsposts["previous"])
    blogposts_.extend(blogposts["today"])
    blogposts_.extend(blogposts["previous"])
    newsposts_.reverse()
    blogposts_.reverse()
    title = "Profile | "+user["username"]+" - lastevents.space"
    if current_user.is_authenticated:
        pass
    return render_template("profile.html", response=user, newsposts=newsposts_, blogposts=blogposts_, logged_in = current_user.is_authenticated, title=title)

@app.route('/news/article/write', methods=['POST', 'GET'])
def api_news_article_write():
    if request.method == 'POST':
        if current_user.is_authenticated:
        # if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
            req = request.form
            heading = req["heading"]
            news = req["news"]
            country = req["country"]
            category = req["category"]
            state = req["state"]
            city = req["city"]
            draftvalue = req["d_a8df0"]
            perm_ = None
            if request.args.get("edit") == "True":
                perm_ = None
            elif request.args.get('v') == 'dt':
                perm_ = None
            else:
               perm_ = req["perm_"]
            perm_une_ = req["perm_une_"]
            if city != None:
               city = city.title()
            keywords = req["keywords"].split(',')
            original_str = news
            replaced_str = re.sub('[/<\/?^>+(>|$)/g]', "", original_str)
            unescaped_str = html.unescape(replaced_str)
            count = 0
            countalert = False
            statealert = False
            catalert = False
            newsalert = False
            headalert = False
            head_url_alert = False
            body_alert = False
            editing__ = None
            # if unescaped_str.isspace() or len(unescaped_str) < 25:
            #     body_alert = ""
            #     count += 1
            if request.args.get('edit') == "True":
                editing__ = True
            if request.args.get('edit') != "True":
              if not be.validheadingurls(heading_url=heading.replace(" ", "-").replace("?", "")):
               head_url_alert = "You cannot use this heading, this already exists"
               count += 1
            if country.isspace() or len(country) < 1:
                countalert = "Country should not be empty"
                count += 1
            if state.isspace() or len(state) < 1:
                statealert = "State should not be empty"
                count += 1
            if category.isspace() or len(category) < 1:
                catalert = "Category should not be empty"
                count += 1
            # if city.isspace() or len(city) < 1:
            #     cityalert = "border : 1px solid red; box-shadow: none"
            #     count += 1
            if heading.isspace() or len(heading) < 1:
                headalert = "Field should not be empty"
                count += 1
            if news.isspace() or len(news) < 1:
                newsalert = "Field should not be empty"
                count += 1
            if request.args.get('v') == 'dt':
                editing__ = True
            if count > 0:
                data =  be.get_user_instance(user_id=current_user.user_id)
                return render_template('newswrite.html',
                            user_country = data["country"],
                            user_state = data["state"],
                            user_city=data["city"],
                            countalert = countalert,
                            statealert=statealert,
                            catalert=catalert,
                            headalert=headalert,
                            newsalert=newsalert,
                            news_news = news,
                            news_heading = heading,
                            news_category = category,
                            logged_in = current_user.is_authenticated,
                            body_alert = body_alert,
                            head_url_alert = head_url_alert,
                            getvalue=f"?v={request.args.get('v')}&viawe={request.args.get('viawe')}",
                            title="News | Write | lastevents.space",
                            editing__ = editing__,
                            _ = True
                            )

            # author_id = current_user.user_id
            author_id = current_user.user_id
            author_name = current_user.username
            if request.args.get('edit') != "True":
                response = be.news_article_write(
                    heading=heading,
                    author_id=author_id,
                    author_name=author_name,
                    news=news,
                    country=country.title(),
                    category=category.title(),
                    state=state.title(),
                    city=city.title(),
                    keywords=keywords,
                    perm_ = perm_,
                    perm_une_ = perm_une_
                )
                be.deletedraft(draft_id=draftvalue, user_id=current_user.user_id)
            elif request.args.get('edit') == 'True':
                response = be.edit_news(
                    heading=heading,
                    prev_heading_url=request.args.get("p"),
                    author_id=author_id,
                    news=news,
                    country=country.title(),
                    category=category.title(),
                    state=state.title(),
                    city=city.title(),
                    keywords=keywords,
                    perm_une_ = perm_une_
                )
                if response == "Update not accepted":
                    return "Unauthorized"
                if response == "Invalid heading":
                    return
            if request.args.get('v') == 'dt':
                    be.deletedraft(draft_id=request.args.get('viawe'), user_id=current_user.user_id)
            # return jsonify({"message":response})
            if len(city) < 1:
                city = 'None'
            return redirect(f'/news/read/{country}/{state}/{category}/{city}')
        else:
            return "Unauthorized"
    else:
        return "Invalid Request"

@app.route('/sample/newstemplates')
def news_templates():
    return render_template('newstemplates.html')

@app.route('/blog/article/write', methods=['POST', 'GET'])
def api_blog_article_write():
    if request.method == 'POST':
        # if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
        if current_user.is_authenticated:
            req = request.form
            heading = req["heading"]
            blog = req["blog"]
            keywords = req["keywords"].split(',')
            perm_ = None
            draftvalue = req['d_a8df0']
            if request.args.get("edit") == "True":
                perm_ = None
            elif request.args.get('v') == 'dt':
                perm_ = None
            else:
               perm_ = req["perm_"]
            count = 0
            original_str = blog
            replaced_str = re.sub('[/<\/?^>+(>|$)/g]', "", original_str)
            unescaped_str = html.unescape(replaced_str)
            headalert = False
            blogalert = False
            head_url_alert = False
            body_alert = False
            editing__ = None
            if unescaped_str.isspace() or len(unescaped_str) < 25:
                body_alert = "This field is required and it should have more than 25 characters"
                count += 1
            if request.args.get('edit') == "True":
                editing__ = True
            if request.args.get('edit') != "True":
             if not be.validheadingurls(heading_url=heading.replace(" ", "-").replace("?", "")):
               head_url_alert = "You cannot use this heading, this already exists"
               count += 1
            if heading.isspace() or len(heading) < 1:
                headalert = "Field should not be empty"
                count += 1
            if blog.isspace() or len(blog) < 1:
                blogalert = "Field should not be empty"
                count += 1
            if request.args.get('v') == 'dt':
                editing__ = True
            if count > 0:
                return render_template("blogwrite.html",
                                       blogalert=blogalert,
                                       headalert=headalert,
                                       logged_in = current_user.is_authenticated,
                                       blog_heading=heading,
                                       blog_blog=blog,
                                       body_alert=body_alert,
                                       head_url_alert=head_url_alert,
                                       editing__=editing__,
                                       getvalue=f"?v={request.args.get('v')}&viawe={request.args.get('viawe')}",
                                       _ = True)
            # author_id = current_user.user_id
            author_id = current_user.user_id
            author_name = current_user.username
            if request.args.get('edit') != "True":
                response = be.blogs_article_write(
                    heading=heading,
                    author_id=author_id,
                    author_name=author_name,
                    blog=blog,
                    keywords=keywords,
                    perm_ = perm_
                )
                be.deletedraft(draft_id=draftvalue, user_id=current_user.user_id)
            elif request.args.get('edit') == "True":
                response = be.edit_blog(
                    heading=heading,
                    author_id=author_id,
                    prev_heading_url=request.args.get("p"),
                    blog=blog,
                    keywords=keywords,
                )
            if request.args.get('v') == 'dt':
                    be.deletedraft(draft_id=request.args.get('viawe'), user_id=current_user.user_id)
            return redirect('/blog/read')
        else:
            return "Unauthorized"
    else:
        return "Invalid Request"

@app.route("/api/user/articles/data", methods=['POST'])
def get_user_articles_data():
    if request.method == 'POST':
        if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
            req = request.get_json()
            user_id = current_user.user_id
            # user_id = current_user.user_id
            response = be.user_articles_revenue_data(user_id=user_id)
            return jsonify(response)
        else:
            return "Unauthorized"
    else:
        return "Invalid Request"

@app.route("/api/user/articles", methods=['POST'])
def get_user_articles_for_dashboard():
    if request.method == 'POST':
        if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
            req = request.get_json()
            # user_id = "ZOmRx01085587870"
            user_id = current_user.user_id
            response = be.get_users_articles(user_id=user_id)
            return jsonify(response)
        else:
            return "Unauthorized"
    else:
        return "Invalid Request"



@app.route("/del/ava345/<heading_url>", methods=['POST'])
def delete_user_article(heading_url):
    if request.method == 'POST':
        # if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
        if current_user.is_authenticated:
            # req = request.get_json()
            # url_heading = req["heading_url"]
            url_heading = heading_url
            response = be.delete_user_article(url_heading, user_id=current_user.user_id)
            # response = None
            # time.sleep(5)
            return jsonify(response)
        else:
            return "Unauthorized"
    else:
        return "Invalid Request"

@app.route("/del/ava342/<heading_url>", methods=['POST'])
def delete_user_blog_article(heading_url):
    if request.method == 'POST':
        # if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
        if current_user.is_authenticated:
            # req = request.get_json()
            # user_id = current_user.user_id
            # url_heading = req["heading_url"]
            url_heading = heading_url
            response = be.delete_blog_user_article(url_heading, user_id=current_user.user_id)
            return jsonify(response)
        else:
            return "Unauthorized"
    else:
        return "Invalid Request"

@app.route("/api/user/update/username", methods=['POST'])
def update_user_name():
    if request.method == 'POST':
        # if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
        if current_user.is_authenticated:
            req = request.get_json()
            newusername = req["username"]
            user_id = current_user.user_id
            if newusername.isspace() or len(newusername) < 1:
                return jsonify({"response":"Username should not be empty"})
            if (not be.validusername(username=newusername)) and (newusername != current_user.username):
               return jsonify({"response":"Username already exists"})
            # user_id = "ZOmRx01085587870"
            response = be.update_user_name(user_id=user_id, newusername=newusername, prev_username=current_user.username)
            user = User.query.filter_by(user_id=current_user.user_id).first()
            user.username = newusername
            db.session.commit()

            return jsonify({"response":True})
        else:
            return "Unauthorized"
    else:
        return "Invalid Request"

@app.route("/api/user/update/country", methods=['POST'])
def update_user_country():
    if request.method == 'POST':
        # if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
        if current_user.is_authenticated:
            req = request.get_json()
            newcountry = req["country"]
            user_id = current_user.user_id
            # user_id = "ZOmRx01085587870"
            if newcountry.isspace() or len(newcountry) < 1:
                return jsonify({"response":"Country should not be empty"})
            # if (not be.validusername(username=newusername)) and (newusername != current_user.username):
            #    return jsonify({"response":"Username already exists"})
            response = be.update_user_country(user_id=user_id, country=newcountry)
            # return jsonify(response)
            return jsonify({"response":True})
        else:
            return "Unauthorized"
    else:
        return "Invalid Request"

@app.route("/api/user/update/state", methods=['POST'])
def update_user_state():
    if request.method == 'POST':
        # if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
        if current_user.is_authenticated:
            req = request.get_json()
            newstate = req["state"]
            user_id = current_user.user_id
            # user_id = "ZOmRx01085587870"
            if newstate.isspace() or len(newstate) < 1:
                return jsonify({"response":"State should not be empty"})
            response = be.update_user_state(user_id=user_id, state=newstate)
            return jsonify({"response":True})
        else:
            return "Unauthorized"
    else:
        return "Invalid Request"

@app.route("/api/user/update/city", methods=['POST'])
def update_user_city():
    if request.method == 'POST':
        # if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
        if current_user.is_authenticated:
            req = request.get_json()
            newcity = req["city"]
            if newcity != None:
                newcity = newcity.title()
            user_id = current_user.user_id
            # user_id = "ZOmRx01085587870"
            response = be.update_user_city(user_id=user_id, city=newcity)
            return jsonify(response)
        else:
            return "Unauthorized"
    else:
        return "Invalid Request"

@app.route("/update/pfad", methods=['POST'])
def update_profile():
    data = request.get_json()
    username = data["uca"]
    country = data["cxw"]
    state = data["sww"]
    response = be.update_profile(user_id=current_user.user_id, username = username, country = country, state = state)
    return jsonify({"response":True})

# @app.route("/api/word/today", methods=['POST'])
# def insert_todays_word():
#     if request.method == 'POST':
#         if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
#             req = request.get_json()
#             word = req["word"]
#             meaning = req["meaning"]
#             # user_id = req["user_id"]
#             user_id = current_user.user_id
#             # user_id = "ZOmRx01085587870"
#             response = be.insert_todays_word(word=word, meaning=meaning, user_id=user_id)
#             return jsonify(response)
#         else:
#             return "Unauthorized"
#     else:
#         return "Invalid Request"

# @app.route("/new/word/today/write", methods=['POST'])
# def insert_todays_word():
#     if request.method == 'POST':
#         # if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
#         if current_user.is_authenticated:
#         #    if be.is_woftheday_stack_available():
#             req = request.form
#             word = req["word"]
#             meaning = req["meaning"]
#             wordalert = None
#             meaningalert = None
#             count = 0
#             if word.isspace():
#                 wordalert = "border : 1px solid red; box-shadow:none"
#                 count += 1
#             if meaning.isspace():
#                 meaningalert = "border : 1px solid red; box-shadow:none"
#                 count += 1
#             if count > 0:
#                 notifications = be.getNotifcations(user_id=current_user.user_id)
#                 drafts = be.getdraftsofUser(user_id=current_user.user_id)
#                 return render_template("wordofthedaywrite.html",
#                                       wordalert=wordalert,
#                                       meaningalert=meaningalert,
#                                       notifications=notifications,
#                                       logged_in = current_user.is_authenticated,
#                                       drafts=drafts,
#                                       value=True)
#             # user_id = req["user_id"]
#             user_id = current_user.user_id
#             # user_id = "ZOmRx01085587870"
#             response = be.insert_todays_word(word=word, meaning=meaning, user_id=user_id)
#             # return jsonify(response)
#             # return redirect('/news/read')
#         #    else:
#             notifications = be.getNotifcations(user_id=current_user.user_id)
#             drafts = be.getdraftsofUser(user_id=current_user.user_id)
#             return redirect("/wordmean")
#         else:
#             return "Unauthorized"
#     else:
#         return "Invalid Request"


@app.route("/api/request/edit/news", methods=['POST'])
def api_request_edit_news():
    if request.method == 'POST':
        if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
            req = request.get_json()
            heading = req["heading"]
            news = req["news"]
            prev_heading_url = req["heading_url"]
            if heading.isspace():
                return "Heading should not be empty"
            else:
                pass
            if len(heading) < 1:
                return "Heading should not be empty"
            else:
                pass
            if news.isspace():
               return "Text Field should not be empty"
            else:
                pass
            if len(news) < 1:
               return "Text Field should not be empty"
            else:
                pass
            country = req["country"]
            category = req["category"]
            state = req["state"]
            city = req["city"]
            if city != None:
                city = city.title()
            keywords = req["keywords"].split(',')
            author_id = "ZOmRx01085587870"
            response = be.edit_news(heading=heading,
                                    prev_heading_url=prev_heading_url,
                                    news=news,
                                    country=country,
                                    category=category,
                                    state=state,
                                    city=city,
                                    keywords=keywords,
                                    author_id=author_id)
            return jsonify(response)
        else:
            return "Unauthorized"
    else:
        return "Invalid Request"

@app.route("/api/request/edit/blog", methods=['POST'])
def api_request_edit_blog():
    if request.method == 'POST':
        if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
            req = request.get_json()
            heading = req["heading"]
            blog = req["blog"]
            keywords = req["keywords"].split(',')
            prev_heading_url = req["heading_url"]
            if heading.isspace():
                return "Heading should not be empty"
            else:
                pass
            if len(heading) < 1:
                return "Heading should not be empty"
            else:
                pass
            if blog.isspace():
               return "Text Field should not be empty"
            else:
                pass
            if len(blog) < 1:
               return "Text Field should not be empty"
            else:
                pass
            author_id = current_user.user_id
            # author_id = "OWpNF12555498171"
            response = be.edit_blog(heading=heading,
                                    prev_heading_url=prev_heading_url,
                                    blog=blog,
                                    keywords=keywords,
                                    author_id=author_id)
            return jsonify(response)
        else:
            return "Unauthorized"
    else:
        return "Invalid Request"

@app.route('/api/email/valid', methods=['POST'])
def email_valid_check():
    if request.method == 'POST':
        val = be.validemail(request.get_json()["email"])
        return jsonify({"result":val})

@app.route('/api/username/valid', methods=['POST'])
def username_valid_check():
    if request.method == 'POST':
        val = be.validusername(request.get_json()["username"])
        return jsonify({"result":val})

@app.route('/api/get/states', methods=['POST', 'GET'])
def get_states_by_country():
    if request.method == 'POST':
        val = csc.getStatesByCountry(country=request.get_json()["country"])
        return jsonify({"result":val})

@app.route('/api/<heading_url>/<val>/424', methods=['GET', 'POST'])
def increment_view(heading_url, val):
    if request.method == 'POST':
    #    if current_user.is_authenticated:
          if val == "blog":
              val = "blogarticles"
          if val == "news":
              val = "newsarticles"
          response =  be.increment_page_views(heading_url, val=val)
          return jsonify({"response":response})

@app.route('/<heading_url>/<val>/12087', methods=['GET', 'POST'])
def reports_article(heading_url, val):
    if request.method == 'POST':
    #    if current_user.is_authenticated:
          response = None
          if val == "blog":
            response = be.report_blog(heading_url=heading_url, reporter_id=current_user.user_id)
          if val == "news":
            response = be.report_news(heading_url=heading_url, reporter_id=current_user.user_id)
          return jsonify({"response":response})

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form["email"]
        message = request.form["message"]
        if email.isspace() or message.isspace():
           if current_user.is_authenticated:
            return render_template('contact.html', logged_in = current_user.is_authenticated, alert="Fields should not be empty", welcome=True, title="Contact | lastevents.space")
           return render_template('contact.html', logged_in = current_user.is_authenticated, alert="Fields should not be empty", welcome=True, title="Contact | lastevents.space")
        val = cont.email(email=email, message=message)
        if current_user.is_authenticated:
         return render_template('contact.html', logged_in = current_user.is_authenticated, alert="Message sent successfully", welcome=True, title="Contact | lastevents.space")
        return render_template('contact.html', logged_in = current_user.is_authenticated, alert="Message sent successfully", welcome=True, title="Contact | lastevents.space")
    if current_user.is_authenticated:

     return render_template('contact.html', logged_in = current_user.is_authenticated, contact__="#8479794f", welcome=True, title="Contact | lastevents.space")
    return render_template('contact.html', logged_in = current_user.is_authenticated, welcome=True, title="Contact | lastevents.space")


@app.route('/api/search', methods=['POST'])
def apisearch():
    data = request.get_json()["text"]
    resp = se.Search(text = data)
    # resp_ = be.get_articles_by_heading_url(heading_urls=resp)
    return jsonify({"response":resp})

@app.route('/privacy')
def privacy():
    return render_template("privacy.html", welcome=True, title="Privacy | lastevents.space")

@app.route('/terms')
def terms():
    return render_template("terms.html", welcome=True, title="Terms | lastevents.space")

@app.route('/about')
def about():
    return render_template("about.html", welcome=True, title="About | lastevents.space")

# @app.route('/search')
# def search():
#     if current_user.is_authenticated:
#         return render_template("search.html", title="Search | lastevents.space", search__="#8479794f", logged_in = current_user.is_authenticated)
#     return render_template("search.html", title="Search | lastevents.space", search__="#8479794f", logged_in = current_user.is_authenticated)

@app.route('/api/delete/user/notification/<notify_id>', methods=['POST'])
def deleteusernotification(notify_id):
    if request.method == 'POST':
      if current_user.is_authenticated:
          be.deleteNotifications(user_id=current_user.user_id, notify_id=notify_id)
          return jsonify({'response':True})

@app.route('/api/deleteall/user/notification', methods=['POST'])
def deleteuserallnotification():
    if request.method == 'POST':
      if current_user.is_authenticated:
          be.deleteAllNotifications(user_id=current_user.user_id)
          return jsonify({'response':True})

@app.route('/create/user/comment/<article_id>', methods=['POST', 'GET'])
def createComment(article_id):
    if request.method == 'POST':
      if current_user.is_authenticated:
          comment = request.get_json()["comment"]
          author = current_user.username
          val = be.setComment(user_id=current_user.user_id, comment_=comment, article_id=article_id, author=author)
          return jsonify(val)

@app.route('/ava/vdfa/<comment_id>', methods=['POST', 'GET'])
def deleteUserComment(comment_id):
    if request.method == 'POST':
      if current_user.is_authenticated:
          be.deleteComment(user_id=current_user.user_id, comment_id=comment_id)
          return jsonify({'response':True})

@app.route('/draft/article/<draft_id>', methods=['POST', 'GET'])
def draftsave(draft_id):
    if request.method == "POST":
        if current_user.is_authenticated:
            user_id = current_user.user_id
            data = request.get_json()
            heading = data["heading"]
            article_data = data["article_data"]
            country = data["cjf_"]
            state = data["sts_"]
            category = data["cat_"]
            city = data["cia_"]
            keywords = data["kyw_"]
            sharepost = data["cxs_"]
            perm_une_ = data["cxo_"]
            publish = data["plia_"]
            response =  be.edit_news_draft(heading=heading, news=article_data, news_id=draft_id, country=country, state=state, city=city, category=category, author_id=current_user.user_id, author=current_user.username, keywords=keywords, perm_une_=perm_une_, can_share=sharepost, publish=publish)
            return jsonify({"response":response})

@app.route('/dafv/a23/<draft_id>', methods=['POST', 'GET'])
def draftsave_(draft_id):
    if request.method == "POST":
        if current_user.is_authenticated:
            user_id = current_user.user_id
            data = request.get_json()
            heading = data["heading"]
            article_data = data["article_data"]
            keywords = data["kyw_"]
            sharepost = data["cxs_"]
            publish = data["plia_"]
            response =  be.edit_blog_draft(heading=heading, blog=article_data, blog_id=draft_id, author_id=current_user.user_id, author=current_user.username, keywords=keywords, can_share=sharepost, publish=publish)
            return jsonify({"response":response})

@app.route('/afd/va32/<draft_id>', methods=['POST'])
def deleteuserdraft(draft_id):
    if request.method == 'POST':
      if current_user.is_authenticated:
          be.deletedraft(user_id=current_user.user_id, draft_id=draft_id)
          return jsonify({'response':True})

@app.route('/afd/va33/<draft_id>', methods=['POST'])
def deleteuserdraftBlog(draft_id):
    if request.method == 'POST':
      if current_user.is_authenticated:
          be.deletedraftblog(user_id=current_user.user_id, draft_id=draft_id)
          return jsonify({'response':True})

@app.route('/api/delete/c476/<chat_id>', methods=["POST"])
def deletechat(chat_id):
    if request.method == 'POST':
        if current_user.is_authenticated:
           response = be.delete_chat(chat_id=chat_id, user_id=current_user.user_id)
           return jsonify({"response":response})

@app.route('/sm/sitemap.txt')
def sitemap():
    return app.send_static_file('sitemap.txt')

@app.route('/pinterest-a4286.html')
def pinterest():
    return app.send_static_file("pinterest-a4286.html")

# @app.route('/im/logo')
# def images():
#     return app.send_static_file("logo.jpg")

@app.route('/ic/apple-touch-icon')
def icons():
    return app.send_static_file("apple-touch-icon.png")

@app.route('/robots.txt')
def robots():
    return app.send_static_file("robots.txt")


# CHATSPACE

# @app.route('/chat/<chat_room_id>')
# def chatspace(chat_room_id):
#     chats = be.getChatsByRoomId(chat_room_id=chat_room_id)
#     if be.get_user_instance(current_user.user_id)["country"] == csc.getCountries()[int(chat_room_id.split('-')[-1][2:])-1]:
#         try:
#             return render_template("chatspace.html", logged_in=current_user.is_authenticated, chats=chats, user_id=current_user.user_id,_m=True)
#         except AttributeError:
#             return "<a href='/login'>Login/Signup to continue</a>"
#     else:
#         return "Can't enter in this group"

# GROUPS

# @app.route('/groups/root/space')
# def rootspace():
#     groups = be.get_available_countries()
#     return render_template('groups.html', title="Groups | lastevents.space", logged_in=current_user.is_authenticated, groups=groups, val="Main", user_country=be.get_user_instance(current_user.user_id)["country"])

# @app.route('/api/groups/root/space', methods=['POST'])
# def apirootspace():
#     groups = be.get_available_countries()
#     # return render_template('groups.html', logged_in=current_user.is_authenticated, groups=groups, val="Main")
#     return jsonify({'response':groups})

# @app.route('/groups/root/space/<group>')
# def rootspacesubgroup(group):
#     newsubgroups = []
#     groups = csc.getStatesByCountry_(group)
#     subgroups = be.get_available_states(country=group)
#     high_contributor = be.get_high_contributor_by_country(group)
#     chat_room_id = f"GC-{group.split('-')[-1]}"

#     for i in subgroups:
#         if i["state"] in groups and i["state"] not in newsubgroups:
#             newsubgroups.append(i)
#     return render_template('groups.html',
#                           logged_in=current_user.is_authenticated,
#                           groups=newsubgroups,
#                           val="Subgroup",
#                           high_contributor=high_contributor,
#                           group_=group,
#                           user_state=be.get_user_instance(current_user.user_id)["state"],
#                           chat_room_id=chat_room_id,
#                           title="Groups | lastevents.space")

# @app.route('/api/groups/root/space/<group>', methods=['POST'])
# def apirootspacesubgroup(group):
#     newsubgroups = []
#     groups = csc.getStatesByCountry_(group)
#     subgroups = be.get_available_states(country=group)
#     for i in subgroups:
#         if i["state"] in groups and i["state"] not in newsubgroups:
#             newsubgroups.append(i)
#     # return render_template('groups.html', logged_in=current_user.is_authenticated, groups=newsubgroups, val="Subgroup", high_contributor=high_contributor, group_=group)
#     return jsonify({"response":newsubgroups})

# @app.route('/groups/root/space/<group>/<subgroup>')
# def rootspacesubgroupmembers(group, subgroup):
#     groups = be.get_all_users_by_state(group, subgroup)
#     high_contributor = be.get_high_contributor_by_state(group, subgroup)
#     chat_room_id = f"GC-{group.split('-')[-1]}"
#     return render_template('groups.html', title="Groups | lastevents.space", logged_in=current_user.is_authenticated, groups=groups, val="Member", high_contributor=high_contributor,chat_room_id=chat_room_id)

# @app.route('/api/groups/root/space/<group>/<subgroup>', methods=['POST'])
# def apirootspacesubgroupmembers(group, subgroup):
#     groups = be.get_all_users_by_state(group, subgroup)
#     return jsonify({"response":groups})

@app.route('/tst/<href>', methods=['POST', 'GET'])
def transact(href):
    if current_user.is_authenticated:
        title = "Transact | Yourincome - lastevents.space"
        if href == "paychc":
          user_instance = be.get_user_instance(user_id=current_user.user_id)
          if "accno" in user_instance.keys():
              if len(user_instance["accno"]) > 0:
                 return redirect("/tst/payam")
          return render_template("tst.html", href=href, logged_in=current_user.is_authenticated, username=current_user.username, title=title)
        # elif href == "paychc":
        #     return render_template("tst.html")
        elif href == "payde":
            hr = request.args.get("hr")
            return render_template("tst.html", href=href, hr=hr, logged_in=current_user.is_authenticated, title=title)
        elif href == "payam":
            balance = be.get_user_instance(user_id=current_user.user_id)["balance"]
            return render_template("tst.html", href=href, balance=balance, logged_in=current_user.is_authenticated, title=title)
        elif href == "payco":
            return render_template("tst.html", href=href, logged_in=current_user.is_authenticated, title=title)
    else:
        return redirect("/login?to=/tst/payde/pn")

@app.route("/tst/payde/pn", methods=["POST", "GET"])
def paydepn():
    if request.method == "POST":
      if current_user.is_authenticated:
        phoneno = request.form["phoneno"]
        cc = request.form["cc"]
        if phoneno.isspace() or cc.isspace():
            href = 'payde'
            return render_template("tst.html", href="payde", hr="pn", alert="Fields should not be empty")
        be.updatephonenumber(user_id=current_user.user_id, phoneno=phoneno, cc=cc)
        return redirect("/tst/payam")
      else:
        return redirect("/login?to=/tst/payde")
    else:
       return "Method Not Allowed"

@app.route("/tst/payde/ac", methods=["POST"])
def paydeac():
    if request.method == "POST":
        if current_user.is_authenticated:
           accno = request.form["accno"]
           ifsc = request.form["ifsc"]
           if accno.isspace() or ifsc.isspace():
               href = 'payde'
               return render_template("tst.html", href=href, hr="ac", alert="Fields should not be empty")
           be.updateaccountnumber(user_id=current_user.user_id, accno=accno, ifsc=ifsc)
           return redirect("/tst/payam")
        else:
            return redirect("/login?to=/tst/payde")
    else:
        return "Method Not Allowed"

@app.route("/tst/payam/su", methods=["POST", "GET"])
def payamsu():
    if request.method == "POST":
      if current_user.is_authenticated:
        balance = be.get_user_instance(user_id=current_user.user_id)["balance"]
        amount = request.form["amount"]
        href = None
        if amount.isspace():
            href = 'payam'
            return render_template("tst.html", href=href, alert="Should not be empty", balance=balance)
        try:
         if int(amount) > be.get_user_instance(user_id=current_user.user_id)["balance"]:
            href = 'payam'
            return render_template("tst.html", href=href, alert="Amount should less than or equal to balance", balance=balance)
        except:
            href = 'payam'
            return render_template("tst.html", href=href, alert="Enter valid amount", balance=balance)
        try:
         if int(amount) < 20:
            href = 'payam'
            return render_template("tst.html", href=href, alert="Amount should greater than 20", balance=balance)
        except:
            href = 'payam'
            return render_template("tst.html", href=href, alert="Enter valid amount", balance=balance)
        be.send_transact(user_id=current_user.user_id, amount=amount)
        be.save_transact(user_id=current_user.user_id, amount=amount, username=current_user.username)
        be.update_balance(user_id=current_user.user_id, newbalance=balance-int(amount))
        sleep(5)
        return redirect("/tst/payco")
      else:
        return redirect("/login?to=/tst/payam")
    return "Method Not Allowed"

# # # # # # # # # # # # OPINIONS # # # # # # # # # # # #
@app.route("/create/opi", methods=["POST", "GET"])
def create_opinion_post():
    title = "Create | Opinion | Meme | lastevents.space"
    metadata = "Create meme, image, quote and opinions. Share them in lastevents.space"
    metaimage = "https://images.lastevents.space/logo.jpg"
    if request.method == "POST":
        # keywords = request.form["keywords"]
        # if keywords != None:
        #     keywords = keywords.split(',')
        text = request.form["text"]
        img = request.files["image"]
        if len(img.filename) < 1:
            return render_template("opinioncreate.html", metaimage=metaimage, metadata=metadata, filealert="Select a valid image file", title=title, logged_in=current_user.is_authenticated)

        img_ = be.image_processing_and_uploading_fomr(img=img)
        post_id = be.create_opinion_post(user_id=current_user.user_id, username=current_user.username, keywords=[], text = text, image = img_)
        post_id = ""
        return redirect("/op-me")

    if request.method == "GET":
        if current_user.is_authenticated:
         if be.get_page_name_by_user_id(current_user.user_id) == False:
           return redirect("/create/page?to=/create/opi")
        #    return redirect("/op-me?c=aKIva", code=307)

         return render_template("opinioncreate.html", title=title, logged_in = current_user.is_authenticated)
        #  return redirect("/op-me", code=307)
        else:
            return redirect("/login")

@app.route("/delete/ge/post/<post_id>", methods=["POST", "GET"])
def delete_opinion_post(post_id)    :
    if request.method == "POST":
      if current_user.is_authenticated:
        response = be.delete_opinion_post(user_id=current_user.user_id, post_id=post_id)
        return jsonify({"result":response})

@app.route("/edit/opi/<post_id>", methods=["POST", "GET"])
def edit_opinion_post(post_id):
    if request.method == "POST":
        text = request.form["text"]
        response = be.edit_opinion_post(user_id="user_id", post_id=post_id, text=text)
        return jsonify({"result":response})
    if request.method == "GET":
        value = be.get_opinion_post(user_id="user_id", post_id=post_id)
        return jsonify({"result":value})

@app.route("/api/value/<post_id>", methods=["POST", "GET"])
def insert_opinion_post(post_id):
    if request.method == "POST":
       if current_user.is_authenticated:
        response = be.insert_opinion_value(user_id=current_user.user_id, post_id=post_id)
        return jsonify({"response":response})
       else:
        return jsonify({"result":"Unauthorized"})

@app.route("/api/comment/<post_id>", methods=["POST","GET"])
def insert_opinion_comment(post_id):
    if request.method == "POST":
        data = request.get_json()
        response = be.setComment(user_id="user_id", comment_=data["comment"], article_id=post_id, author="username")
        be.update_opinion_comment(post_id=post_id)
        return jsonify({"result":response})

@app.route("/api/delete/comment/<post_id>/<comment_id>", methods=["POST","GET"])
def delete_opinion_comment(post_id, comment_id):
    if request.method == "POST":
        response = be.deleteComment(user_id="user_id", comment_id=comment_id)
        be.update_opinion_comment(post_id=post_id)
        return jsonify({"result":response})

@app.route("/va/vapge", methods=["GET", "POST"])
def getpva():
    pagename = be.get_page_name_by_user_id(current_user.user_id)
    author = current_user.username
    return jsonify({"vaoue":pagename, "vaops":author})

@app.route("/create/page", methods=["POST","GET"])
def createpage():
    to = request.args.get("to")
    if to == None:
        to = "/date/me"
    title = "Create | Page - lastevents.space"
    metadata = "Create your page, upload memes, images, quotes and start earning - lastevents.space"
    metaimage = "https://images.lastevents.space/logo.jpg"
    if request.method == "POST":
        pagename = request.form["pagename"]
        pagedescription = request.form["pagedescription"]
        pagepurpose = request.form["pagepurpose"]
        pageinfo = False
        valid_page = False
        pagename_sp = False
        pagedesc_sp = False
        pagepur_sp = False
        pagedesc_len = False
        pagename_len = False
        count = 0
        if to != None:
                pageinfo = "Creating a opinion or meme requires page"
        if not be.is_valid_pagename(pagename=pagename):
            count += 1
            valid_page =  "Page name already exists"
        if pagename.isspace() or len(pagename) < 1:
            count += 1
            pagename_sp = "Page should not be empty"
        if len(pagename) > 20:
            count += 1
            pagename_len = "Page name should be less than 20 characters"
        if pagedescription.isspace() or len(pagedescription) < 1:
            count += 1
            pagedesc_sp = "Page description should not be empty"
        if len(pagedescription) > 150:
            count += 1
            pagedesc_len = "Description should be less than 150 characters"
        if pagepurpose.isspace() or len(pagepurpose) < 1:
            count += 1
            pagepur_sp = "Page purpose should not be empty"
        if count > 0:
            return render_template("pagecreate.html", logged_in = current_user.is_authenticated, title=title, pageinfo=pageinfo, pagealert=valid_page, pagenamealert = pagename_sp, pagenamealert1=pagename_len, pagedescalert = pagedesc_sp, pagedescalert1 = pagedesc_len, pagepuralert=pagepur_sp, get_value=to)
        response = be.createPage(pagename=pagename, pagedescription=pagedescription, pagepurpose=pagepurpose, username=current_user.username, user_id=current_user.user_id)
        return redirect(to)
    if request.method == "GET":
        pageinfo = None
        if to != None:
            pageinfo = "Creating a opinion or meme requires page"
        return render_template("pagecreate.html", logged_in=current_user.is_authenticated, metadata=metadata, metaimage = metaimage, get_value=to, pageinfo=pageinfo, title=title)

@app.route("/delete/page/<pagename>", methods=["POST","GET"])
def deletepage(pagename):
        response = be.deletePage(user_id=current_user.user_id, pagename=pagename)
        return jsonify({"response":"o-k-242"})

@app.route("/dava/422/<pagename>", methods=["POST", "GET"])
def updatedescription(pagename):
   resp = request.get_json()
   description = resp["de24"]
   return jsonify({"response":be.update_page_description(pagename=pagename, pagedescription=description, user_id=current_user.user_id)})

@app.route("/op-me", methods=['POST', 'GET'])
def opinions():
    title = "Opinions & Memes | lastevents.space"
    metadata = "Create a page upload memes, earn money for your memes. Share your opinions through images here | lastevents.space"
    metaimage = "https://images.lastevents.space/logo.jpg"
    # opis = be.get_all_opis()
    opis = []
    opis.reverse()
    if request.method == "POST":
        # c = request.args.get("c")
        return render_template("opinions.html", opis=opis, title=title, metadata=metadata, metaimage=metaimage, logged_in = current_user.is_authenticated, c=c)
    return render_template("opinions.html", opis=opis, title=title, metadata=metadata, metaimage=metaimage, logged_in = current_user.is_authenticated)




@app.route("/ge/<pagename>")
def pageview(pagename):
    page_details = be.get_pageview(pagename)
    if page_details == False:
        return "No page found"
    page_posts = be.get_pageposts(pagename)
    total_posts = len(page_posts)
    total_value = be.get_page_total_value_(page_details)
    title = f"{pagename} | lastevents.space"
    current_user_ = False
    if current_user.is_authenticated:
     if current_user.user_id == page_details["user_id"]:
        current_user_ = True
     else:
         pass
    else:
      pass
    return render_template("pageview.html", page_details=page_details, page_posts=page_posts, total_posts = total_posts, total_value = total_value, title=title, current_user_ = current_user_, logged_in = current_user.is_authenticated)


# @app.route("/ge/<pagename>")
# def pageview(pagename):
#   return f"{pagename} will soon appear here"
# # # # # # # # # # # # END OPINIONS # # # # # # # # # # # #

@app.route("/tst/delete/accno")
def deleteaccno():
   be.deleteaccno(user_id=current_user.user_id)
   return redirect("/data/yourincome")

@app.route("/google1e98e7e5f5d2465b.html")
def googleveri():
    return app.send_static_file("google1e98e7e5f5d2465b.html")

@app.route('/ads.txt')
def ads():
    return app.send_static_file("ads.txt")


# SOCKET IO

# @socketio.on('connect')
# def connect():
#     socketio.send("Connected")

# @socketio.on('message')
# def message(msg):
#     response = be.insertChat(username=current_user.username,
#                   user_id=current_user.user_id,
#                   text=msg["text"],
#                   chat_room_id=msg["chat_room_id"],
#                   )
#     socketio.send({"text":msg, "chat_id":response})


@app.route("/ne/cit/0v9")
def fromcity():
    resp = request.get_json()
    country = resp["country"]
    state = resp["state"]
    city = resp["city"]
    category = resp["category"]
    return jsonify({"response":be.get_news_from_exact(country, state, city, category)})

@app.route('/sm/sitemap.xml')
def sitemapxml():
    return app.send_static_file('sitemap.xml')



#LOGOUT

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect('/login')
    else:
        return redirect('/login')

@app.route('/dash')
def dash():
  if current_user.is_authenticated:
    a92f = request.args.get("t")
    user_instance = False
    notifications = False
    newsarticles = False
    blogarticles = False
    drafts = False
    pagename = False
    redi = False
    comments = False
    account = False
    title = "Dash | Me - lastevents.space"
    metaimage = "https://images.lastevents.space/logo.jpg"
    metadata = "See your articles, notifications, drafts and income data here..."
    ty = request.args.get("ty")
    if a92f == "profile":
     user_instance = be.get_user_instance(user_id=current_user.user_id)
     redi = True
    elif a92f == "notifications":
     notifications = be.getNotifcations(user_id=current_user.user_id)
    elif a92f == "drafts":
     if ty == "news":
      drafts = be.getdraftsofUser(user_id=current_user.user_id)
     elif ty == "blog":
      drafts = be.getdraftsofUserBlog(user_id=current_user.user_id)
    elif a92f == "income":
     user_instance = be.get_user_instance(user_id=current_user.user_id)
     user_instance["total_news_articles"] = be.get_users_articles(user_id=current_user.user_id)
     user_instance["total_blog_articles"] = be.get_users_blog_article(user_id=current_user.user_id)
     user_instance["total_memes_and_opinions_articles"] = len(be.get_opinions_of_user(user_id=current_user.user_id))
    elif a92f == "newsarticles":
      newsarticles = be.get_users_articles(user_id=current_user.user_id)
    elif a92f == "blogarticles":
      blogarticles = be.get_users_blog_article(user_id=current_user.user_id)
    elif a92f == "pages":
      pagename = be.get_page_name_by_user_id(user_id=current_user.user_id)
    elif a92f == "comments":
        comments = be.getCommentsofUser(user_id=current_user.user_id)
    elif a92f == "account":
        account = be.get_user_instance(user_id=current_user.user_id)
    return render_template("dash.html", a92f=a92f, title=title, metaimage = metaimage, metadata = metadata, data=user_instance, account=account, notifications=notifications, income=user_instance, drafts = drafts, logged_in=current_user.is_authenticated, newsarticles=newsarticles, blogarticles=blogarticles, pagename=pagename, redi=redi, ty=ty, comments=comments)
  else:
      return redirect('/login')

@app.route("/chooser")
def chooser():
    title = "Choose | What to do - lastevents.space"
    metaimage = "https://images.lastevents.space/logo.jpg"
    metadata = "What you want to write, select the option"
    return render_template("chooser.html",title=title, metaimage = metaimage, metadata = metadata)

@app.route("/del/account", methods=["POST", "GET"])
def deleteaccount():
    return jsonify({"reponse":True})

@app.route("/images/im342/<imagename>")
def imagesrender(imagename):
    return redirect(f"https://s3.ap-south-1.amazonaws.com/images.lastevents.space/{imagename}")

@app.errorhandler(404)
def pagenotfound(e):
    return render_template("pnf.html")

if __name__ == "__main__":
    # socketio.run(app, debug=True, port=8000)
    app.run(debug=True, port=8000)
