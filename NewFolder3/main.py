import html
import re
from flask import Flask, jsonify, make_response, render_template, request, redirect, send_file
from flask_login import current_user
from CountriesStatesCities import CountriesStatesCities
from backend import BackEnd
from flask_login import LoginManager, login_user, current_user, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from forgotpassword import ResetPassword
from contact import Contactemail
from SearchApi import SearchApi
# from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder = 'static')
be = BackEnd()
csc = CountriesStatesCities()
fp = ResetPassword()
cont = Contactemail()
se = SearchApi()
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
    return redirect('/news/read')

@app.route('/signup', methods=['POST', 'GET'])
def register():
    title = 'Signup | lastevents.space'
    metadata = "Signup and enter into this space to read, write and earn simply. See the last events' updates"
    if request.method == 'POST':
        if current_user.is_authenticated:
         return redirect("/")
        email = request.form["email"]
        password = request.form["password"]
        confirmpassword = request.form["confirm_password"]
        username = request.form["username"]
        country = request.form["country"]
        state = request.form["state"]
        city = request.form["city"]
        if city != None:
         city = city.title()
        count = 0
        emailalert = None
        passwordalert = None
        confirmpasswordalert = None
        countalert = None
        statealert = None
        catalert = None
        cityalert = None
        usernamealert = None
        alert = None
        if country.isspace() or len(country) < 1:
            countalert = "border : 1px solid red; box-shadow: none"
            count += 1
        if state.isspace() or len(state) < 1:
            statealert = "border : 1px solid red; box-shadow: none"
            count += 1
        if username.isspace() or len(username) < 1:
            usernamealert = "border : 1px solid red; box-shadow: none"
            count += 1
        if city.isspace() or len(city) < 1:
            cityalert = "border : 1px solid red; box-shadow: none"
            count += 1
        if email.isspace() or len(email) < 1:
            emailalert = "border : 1px solid red; box-shadow: none"
            count += 1
        if len(password) < 1:#isspace()
            passwordalert = "border : 1px solid red; box-shadow: none"
            count += 1
        if len(confirmpassword) < 1:#isspace()
            confirmpasswordalert = "border : 1px solid red; box-shadow: none"
            count += 1
        if len(password) < 8:
            alert = "Password should have minimum of '8' characters"
            return render_template('signup.html',
                                   countalert=countalert,
                                   statealert=statealert,
                                   catalert=catalert,
                                   cityalert=cityalert,
                                   emailalert=emailalert,
                                   passwordalert=passwordalert,
                                   confirmpasswordalert=confirmpasswordalert,
                                   usernamealert=usernamealert,
                                   countryval=country,
                                   stateval=state,
                                   cityval=city,
                                   emailval=email,
                                   passwordval=password,
                                    confirmpasswordval=confirmpassword,
                                   usernameval=username,
                                   alert=alert,
                                   logged_in = current_user.is_authenticated,
                                   title="Sign Up | lastevents.space",
                                   signup_login_="#8479794f",
                                   redi=False,
                                   is_signinpage=True
                                   )
        # if catalert.isspace() or len(catalert) < 1:
        #     catalert = "border : 1px solid red; box-shadow: none"
        #     count += 1
        if count > 0:
            return render_template('signup.html',
                                   countalert=countalert,
                                   statealert=statealert,
                                   catalert=catalert,
                                   cityalert=cityalert,
                                   emailalert=emailalert,
                                   passwordalert=passwordalert,
                                   confirmpasswordalert=confirmpasswordalert,
                                   usernamealert=usernamealert,
                                   countryval=country,
                                   stateval=state,
                                   cityval=city,
                                   emailval=email,
                                   passwordval=password,
                                   confirmpasswordval=confirmpassword,
                                   usernameval=username,
                                   logged_in = current_user.is_authenticated,
                                   title='Sign Up | lastevents.space',
                                   signup_login_="#8479794f",
                                   redi=True,
                                   is_signinpage=True
                                   )

        if not be.validemail(email=email):
            alert = "Email already exists"
            return render_template('signup.html',
                                   countalert=countalert,
                                   statealert=statealert,
                                   catalert=catalert,
                                   cityalert=cityalert,
                                   emailalert=emailalert,
                                   passwordalert=passwordalert,
                                   confirmpasswordalert=confirmpasswordalert,
                                   usernamealert=usernamealert,
                                   countryval=country,
                                   stateval=state,
                                   cityval=city,
                                   emailval=email,
                                   passwordval=password,
                                   confirmpasswordval=confirmpassword,
                                   usernameval=username,
                                   alert=alert,
                                   logged_in = current_user.is_authenticated,
                                   title="Sign Up | lastevents.space",
                                   signup_login_="#8479794f",
                                   redi = True,
                                   is_signinpage=True
                                   )

        if not be.validusername(username=username):
            alert = "username not available"
            return render_template('signup.html',
                                   countalert=countalert,
                                   statealert=statealert,
                                   catalert=catalert,
                                   cityalert=cityalert,
                                   emailalert=emailalert,
                                   passwordalert=passwordalert,
                                   confirmpasswordalert=confirmpasswordalert,
                                   usernamealert=usernamealert,
                                   countryval=country,
                                   stateval=state,
                                   cityval=city,
                                   emailval=email,
                                   passwordval=password,
                                   confirmpasswordval=confirmpassword,
                                   usernameval=username,
                                   alert=alert,
                                   logged_in = current_user.is_authenticated,
                                   title="Sign Up | lastevents.space",
                                   signup_login_="#8479794f",
                                   redi = True,
                                   is_signinpage=True
                                   )

        if password != confirmpassword:
            alert = "Password and confirm password should be same"
            return render_template('signup.html',
                                   countalert=countalert,
                                   statealert=statealert,
                                   catalert=catalert,
                                   cityalert=cityalert,
                                   emailalert=emailalert,
                                   passwordalert=passwordalert,
                                   confirmpasswordalert=confirmpasswordalert,
                                   usernamealert=usernamealert,
                                   countryval=country,
                                   stateval=state,
                                   cityval=city,
                                   emailval=email,
                                   passwordval=password,
                                   confirmpasswordval=confirmpassword,
                                   usernameval=username,
                                   alert=alert,
                                   logged_in = current_user.is_authenticated,
                                   title="Sign Up | lastevents.space",
                                   signup_login_="#8479794f",
                                   redi = True,
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
        return redirect('/login')
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
            emailalert = "border : 1px solid red; box-shadow: none"
            count += 1
        if password.isspace() or len(password) < 1:
            passwordalert = "border : 1px solid red; box-shadow: none"
            count += 1
        if  count > 0:
            return render_template("signin.html", emailalert=emailalert, passwordalert=passwordalert, logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f", is_signinpage=True)
        if not be.validemail(email):
            if be.validemail_and_password_for_login(email, password):
                user = User.query.filter_by(email=email).first()
                login_user(user)
                be.setNotification(user_id=current_user.user_id, notify_msg="Logged in")
                if to == None:
                  if not be.is_verified(user_id=current_user.user_id):
                    return redirect("/verify")
                  else:
                    return redirect("/home")
                elif to == 'write':
                    return redirect("/news/write")
                elif to == 'bwrite':
                    return redirect("/blog/write")
                elif to == 'wwrite':
                    return redirect("/wofday/write")
                elif to == 'earninfo':
                    return redirect("/earninfo")
            else:
                if to == 'write':
                    return render_template("signin.html", is_signinpage=True, to=f"?to={to}", alert="Password incorrect", logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f")
                if to == 'bwrite':
                    return render_template("signin.html", is_signinpage=True, to=f"?to={to}", alert="Password incorrect", logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f")
                if to == 'wwrite':
                    return render_template("signin.html", is_signinpage=True, to=f"?to={to}", alert="Password incorrect", logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f")
                if to == 'earninfo':
                    return render_template("signin.html", is_signinpage=True, to=f"?to={to}", alert="Password incorrect", logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f")
                else:
                    return render_template("signin.html", is_signinpage=True, alert="Password incorrect", logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f")
        else:
            if to == 'write':
                    return render_template("signin.html", is_signinpage=True, to=f"?to={to}", alert="Email not found", logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f")
            if to == 'bwrite':
                    return render_template("signin.html", is_signinpage=True, to=f"?to={to}", alert="Email not found", logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f")
            if to == 'wwrite':
                    return render_template("signin.html", is_signinpage=True, to=f"?to={to}", alert="Email not found", logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f")
            if to == 'earninfo':
                    return render_template("signin.html", is_signinpage=True, to=f"?to={to}", alert="Email not found", logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f")
            return render_template("signin.html", is_signinpage=True, alert="Email not found", logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f")
    else:
        # if current_user.is_authenticated:
        #     return redirect("/")
        if current_user.is_authenticated:
            return redirect('/')
        if to != None:
           return render_template("signin.html", is_signinpage=True, to=f"?to={to}", alert="Writing requires login", logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f")
        return render_template("signin.html", is_signinpage=True, logged_in = current_user.is_authenticated, title="Login | lastevents.space", signup_login_="#8479794f")
        # return render_template("signin.html")

@app.route('/news/read')
def news_read():
    title = "News | Read | RecentUpdates - lastevents.space"
    metadata = """Space for reading recently updated news articles in real-time, we are trying to provide you with high-quality news about the last events, write news in your own style and get paid."""
    if request.method == 'GET':
       todays_word = be.get_todays_word()
       if current_user.is_authenticated and request.args.get('tpe') != "ww":
            user = be.get_user_instance(user_id=current_user.user_id)
            return redirect(f"/news/read/{user['country']}/{user['state']}/general/{user['city']}")
       else:
            articles_news = be.get_all_news_content()
            blogs = be.blog_get()[0:10]
            return render_template("read.html",
                              todays_word=todays_word,
                              logged_in = current_user.is_authenticated,
                              title=title,
                              metadata=metadata,
                              read__="#8479794f",
                              response = articles_news,
                              recent_blogs = blogs,
                              __me__=True
                              )
    else:
        return "Method not allowed"

@app.route('/blog/read')
def blog_read():
    title = "Blog | Read | RecentArticles - lastevents.space"
    metadata = 'Space for reading and writing blog articles, write and monetize your content here.'
    if request.method == 'GET':
        response = be.blog_get()
        if current_user.is_authenticated:
            notifications = be.getNotifcations(user_id=current_user.user_id)
            drafts = be.getdraftsofUser(user_id=current_user.user_id)
            return render_template("blog.html", response=response, logged_in = current_user.is_authenticated, title=title, metadata=metadata, blog__="#8479794f", notifications=notifications, drafts=drafts)
        return render_template("blog.html", response=response, logged_in = current_user.is_authenticated, title=title, metadata=metadata, blog__="#8479794f")

@app.route('/news/read/filter', methods = ['POST', 'GET'])
def news_get_filter():
    if request.method == 'POST':
        req = request.form
        country = req["country"].title()
        state = req["state"].title()
        category = req["category"].title()
        city = req["city"].title()
        if city != None:
         city = city.title()
        count = 0
        countalert = None
        statealert = None
        catalert = None
        cityalert = None
        if len(city) < 1:
            city = None
        if country.isspace() or len(country) < 1:
            countalert = "border : 1px solid red; box-shadow: none"
            count += 1
        if state.isspace() or len(state) < 1:
            statealert = "border : 1px solid red; box-shadow: none"
            count += 1
        if category.isspace() or len(category) < 1:
            catalert = "border : 1px solid red; box-shadow: none"
            count += 1
        # if city.isspace() or len(city) < 1:
        #     cityalert = "border : 1px solid red; box-shadow: none"
        #     count += 1
        if count > 0:
         notifications = be.getNotifcations(user_id=current_user.user_id)
         drafts = be.getdraftsofUser(user_id=current_user.user_id)
         return render_template("read.html",
                               countalert=countalert,
                               statealert=statealert,
                               catalert=catalert,
                               cityalert=cityalert,
                               todays_word = be.get_todays_word(),
                               alert=True,
                               logged_in = current_user.is_authenticated,
                               title=f"News | {country} | {category} | lastevents.space",
                               read__="#8479794f",
                               __me__ = True,
                               notifications=notifications,
                               drafts=drafts)

        return redirect(f"/news/read/{country}/{state}/{category}/{city}")

@app.route("/news/read/view/<news_id_or_news_heading>")
def view_news_article(news_id_or_news_heading):
    # formatted_url = news_id_or_news_heading.replace('-', ' ')
    news = be.view_news_article(news_id_or_news_heading)
    # return jsonify({"news":news})\
    # news["news"] = html.unescape(news["news"])
    # related_news = be.news_get()

    if news == 'blog':
        return redirect(f'/blog/read/view/{news_id_or_news_heading}')
    title = f"{news['heading']} - lastevents.space"
    data = be.all_news_articles_than_one(news_id_or_news_heading)[0:10]
    if current_user.is_authenticated:
     notifications = be.getNotifcations(user_id=current_user.user_id)
     drafts = be.getdraftsofUser(user_id=current_user.user_id)
     return render_template("view.html", response=news, news=True, logged_in = current_user.is_authenticated, data=data, title=title, notifications=notifications, drafts=drafts)
    return render_template("view.html", response=news, news=True, logged_in = current_user.is_authenticated, data=data, title=title)

@app.route("/blog/read/view/<blog_id_or_blogs_heading>")
def view_blogs_article(blog_id_or_blogs_heading):
    # formatted_url = blog_id_or_blogs_heading.replace('-', ' ')
    blog = be.view_blogs_article(blog_id_or_blogs_heading)
    # for_you_blogs = be.blog_get()
    title = f"{blog['heading']} - lastevents.space"
    # metadata = blog["description"]
    metadata = ''
    data = be.all_blog_aritcles_than_one(heading_url=blog_id_or_blogs_heading)[0:10]
    comments = be.getCommentsofArticle(article_id=blog_id_or_blogs_heading)
    if current_user.is_authenticated:
     notifications = be.getNotifcations(user_id=current_user.user_id)
     drafts = be.getdraftsofUser(user_id=current_user.user_id)
     return render_template("view.html", response=blog, blog=True, logged_in = current_user.is_authenticated, data=data[0:10], title=title, metadata=metadata, read__="#8479794f", notifications=notifications, drafts=drafts, comments=comments)
    return render_template("view.html", response=blog, blog=True, logged_in = current_user.is_authenticated, data=data[0:10], title=title, metadata=metadata, read__="#8479794f", comments=comments)
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
    todays_word = be.get_todays_word()
    blogs = be.blog_get()[0:10]
    if current_user.is_authenticated:
     notifications = be.getNotifcations(user_id=current_user.user_id)
     drafts = be.getdraftsofUser(user_id=current_user.user_id)
     return render_template("read.html",
                           response = response,
                           country=country,
                           state=state,
                           category=category,
                           city=city,
                           todays_word=todays_word,
                           logged_in = current_user.is_authenticated,
                           recent_blogs=blogs,
                           title=f"News | Read | {country} | {category}",
                           read__="#8479794f",
                           __me__=True,
                           notifications=notifications,
                           drafts=drafts,
                           code_342 = True
                           )

    return render_template("read.html",
                           response = response,
                           country=country,
                           state=state,
                           category=category,
                           city=city,
                           todays_word=todays_word,
                           logged_in = current_user.is_authenticated,
                           recent_blogs=blogs,
                           title=f"News | Read | {country} | {category}",
                           read__="#8479794f",
                           __me__=True,
                           code_342 = True
                           )

@app.route('/earninfo')
def earninfo():
    title = "Earn | Info - lastevents.space "
    metadata = "Space for earning by writing lastevents(news) or blog articles, make money as simple as possible"
    if current_user.is_authenticated:
        notifications = be.getNotifcations(user_id=current_user.user_id)
        drafts = be.getdraftsofUser(user_id=current_user.user_id)
        return render_template('earninfo.html', logged_in = current_user.is_authenticated, title=title, metadata = metadata, earninfo__="#8479794f", notifications=notifications, drafts=drafts)
    return render_template('earninfo.html', logged_in = current_user.is_authenticated, title=title, metadata = metadata, earninfo__="#8479794f")

@app.route('/api/create/draft', methods=["POST"])
def create_draft():
    if request.method == 'POST':
        if current_user.is_authenticated:
            data = request.get_json()
            draftvalue = be.createDraft(user_id=current_user.user_id, type_=data["type"])
            return jsonify({"response":draftvalue})

@app.route('/news/write')
def newswrite():
    title = 'News | Write - lastevents.space'
    metadata = 'Here is the space for writing your news article, lastevents. Start your earning here.'
    if current_user.is_authenticated:
     data = be.get_user_instance(user_id=current_user.user_id)
     notifications = be.getNotifcations(user_id=current_user.user_id)
     drafts = be.getdraftsofUser(user_id=current_user.user_id)
    #  draftvalue = be.createDraft(user_id=current_user.user_id, type_="news")
     draftvalue = ''
     return render_template('newswrite.html',
                            user_country = data["country"],
                            user_state = data["state"],
                            editing__ = None,
                            user_city=data["city"],
                            logged_in = current_user.is_authenticated,
                            title=title, metadata=metadata,
                            write__="#8479794f",
                            notifications=notifications,
                            drafts=drafts,
                            draftvalue=draftvalue,
                            _ = True
                            )
    else:
     return redirect("/login?to=write")

@app.route('/news/edit/<heading_url>')
def newswrite_edit(heading_url):
    if current_user.is_authenticated:
       if request.args.get('v') != 'dt':
        news = be.view_news_article(url_heading=heading_url)
        if current_user.user_id != news["author_id"]:
            return "Unauthorized"
        notifications = be.getNotifcations(user_id=current_user.user_id)
        drafts = be.getdraftsofUser(user_id=current_user.user_id)
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
                            notifications=notifications,
                            drafts=drafts,
                            _ = True)
       elif request.args.get('v') == 'dt':
        draft = be.getdraft(draft_id=request.args.get('viawe'))
        if current_user.user_id != draft["user_id"]:
            return "Unauthorized"
        notifications = be.getNotifcations(user_id=current_user.user_id)
        drafts = be.getdraftsofUser(user_id=current_user.user_id)
        return render_template('newswrite.html',
                            news_heading=news["heading"],
                            news_news=draft["article_data"],
                            editing_ = True,
                            logged_in = current_user.is_authenticated,
                            title="News | Edit | Draft | lastevents.space",
                            notifications=notifications,
                            drafts=drafts,
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
        notifications = be.getNotifcations(user_id=current_user.user_id)
        drafts = be.getdraftsofUser(user_id=current_user.user_id)
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
                            notifications=notifications,
                            drafts=drafts,
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
        notifications = be.getNotifcations(user_id=current_user.user_id)
        drafts = be.getdraftsofUser(user_id=current_user.user_id)
        return render_template('blogwrite.html',
                            blog_heading=draft["heading"],
                            blog_blog=draft["article_data"],
                            editing__ = True,
                            draftvalue = request.args.get('viawe'),
                            getvalue = f"?v=dt&viawe={request.args.get('viawe')}",
                            logged_in = current_user.is_authenticated,
                            title="Blog | Edit | Draft | lastevents.space",
                            notifications=notifications,
                            drafts=drafts,
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
        notifications = be.getNotifcations(user_id=current_user.user_id)
        drafts = be.getdraftsofUser(user_id=current_user.user_id)
        return render_template('blogwrite.html',
                            blog_heading=blog["heading"],
                            blog_blog=blog["blog"],
                            getvalue=f"?edit=True&p={heading_url}",
                            editing__ = True,
                            logged_in = current_user.is_authenticated,
                            title="Blog | Edit | lastevents.space",
                            notifications=notifications,
                            drafts=drafts,
                            _ = True)

@app.route('/blog/write')
def blogwrite():
    title = 'Blog | Write - lastevents.space'
    metadata = 'Here is the space for writing blog articles, interesting topics, and coding snippets. Start your earnings here.'
    if current_user.is_authenticated:
     notifications = be.getNotifcations(user_id=current_user.user_id)
     drafts = be.getdraftsofUser(user_id=current_user.user_id)
    #  draftvalue = be.createDraft(user_id=current_user.user_id, type_="blog")
     draftvalue = ""
     return render_template('blogwrite.html',
                            editing__=None,
                            logged_in = current_user.is_authenticated,
                            title=title, metadata=metadata,
                            write="#8479794f",
                            notifications=notifications,
                            drafts=drafts,
                            draftvalue=draftvalue,
                            _ = True)
    else:
     return redirect("/login?to=bwrite")

@app.route('/wofday/write')
def wordofthedaywrite():
    if current_user.is_authenticated:
     if be.is_woftheday_stack_available():
      notifications = be.getNotifcations(user_id=current_user.user_id)
      drafts = be.getdraftsofUser(user_id=current_user.user_id)
      return render_template('wordofthedaywrite.html',
                             logged_in = current_user.is_authenticated,
                             title="Word Of The Day | Write | lastevents.space",
                             value=True,
                             notifications=notifications,
                             drafts=drafts)
     else:
       notifications = be.getNotifcations(user_id=current_user.user_id)
       drafts = be.getdraftsofUser(user_id=current_user.user_id)
       return render_template('wordofthedaywrite.html',
                              logged_in = current_user.is_authenticated,
                              title="Word Of The Day | Write | lastevents.space",
                              value=False,
                              notifications=notifications,
                              drafts=drafts)
    else:
     return redirect("/login?to=wwrite")

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

@app.route('/wordmean')
def wordmean():
    response = be.get_todays_word()
    notifications = None
    drafts = None
    if current_user.is_authenticated:
        notifications = be.getNotifcations(user_id=current_user.user_id)
        drafts = be.getdraftsofUser(user_id=current_user.user_id)
    return render_template("wordmean.html",
                           response=response,
                           logged_in = current_user.is_authenticated,
                           title="Word | Meaning | lastevents.space",
                           notifications=notifications,
                           drafts=drafts)

@app.route('/home')
def home():
    home_meta = '''Space for reading, writing news, and earning money from your news and blog articles. We are providing you with news updates and the last events in our space'''
    title = "Space for sharing the latest events and keep yourself updated."
    notifications = None
    drafts = None
    print(current_user.is_authenticated)
    if current_user.is_authenticated == True:
     print("yes")
     drafts = be.getdraftsofUser(user_id=current_user.user_id)
     notifications = be.getNotifcations(user_id=current_user.user_id)
    print(notifications)
    return render_template("welcome.html", logged_in = current_user.is_authenticated, welcome=True, title=title, metadata=home_meta, notifications=notifications, drafts=drafts)

@app.route('/verify', methods=['POST', 'GET'])
def verify():
    if request.method == 'GET':
      if current_user.is_authenticated:
        if be.is_verified(user_id=current_user.user_id):
            return redirect('/home')
        else:
            val = be.send_verification_code(email=current_user.email, user_id=current_user.user_id, username=current_user.username)
            notifications = be.getNotifcations(user_id=current_user.user_id)
            drafts = be.getdraftsofUser(user_id=current_user.user_id)
            return render_template('verify.html', logged_in = current_user.is_authenticated, title="Verify", email=current_user.email, notifications=notifications, drafts=drafts)
      else:
            notifications = be.getNotifcations(user_id=current_user.user_id)
            drafts = be.getdraftsofUser(user_id=current_user.user_id)
            return render_template('verify.html', logged_in = current_user.is_authenticated, title="Verify", email=current_user.email, notifications=notifications, drafts=drafts)
    if request.method == 'POST':
        if current_user.is_authenticated:
            code = request.form['code']
            val = be.check_verification_code(email=current_user.email, user_id=current_user.user_id, code=code)
            if val == True:
             return redirect('/')
            else:
             notifications = be.getNotifcations(user_id=current_user.user_id)
             drafts = be.getdraftsofUser(user_id=current_user.user_id)
             return render_template('verify.html', logged_in = current_user.is_authenticated, title="Verify", email=current_user.email, alert="Incorrect Code", notifications=notifications, drafts=drafts)

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
        if href == "me":
            me = True
            bac_val_me = "#8479794f"
        elif href == "yourarticles":
            yourarticles = True
            bac_val_art = "#8479794f"
            if request.args.get("t") == "news":
                user_articles = be.get_users_articles(user_id=current_user.user_id)
                data["today"] = user_articles["today"]
                data["previous"] = user_articles["previous"]
                news_2324 = True
            if request.args.get("t") == "blog":
                user_blog_articles = be.get_users_blog_article(user_id=current_user.user_id)
                data["today"] = user_blog_articles["today"]
                data["previous"] = user_blog_articles["previous"]
                blog_2324 = True
            if request.args.get("t") == "comments":
                print(comments_2324 )
                user_comments = be.getCommentsofUser(user_id=current_user.user_id)
                data["today"] = user_comments["today"]
                data["previous"] = user_comments["previous"]
                print(data)
                comments_2324 = True
        elif href == "yourincome":
            yourincome = True
            bac_val_yi = "#8479794f"
        else:
            return redirect("/data/me")
        notifications = be.getNotifcations(user_id=current_user.user_id)
        drafts = be.getdraftsofUser(user_id=current_user.user_id)
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
                            notifications=notifications,
                            drafts=drafts,
                            __me__ = True
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
            countalert = ''
            statealert = ''
            catalert = ''
            newsalert = ''
            headalert = ''
            head_url_alert = ''
            body_alert = ''
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
                countalert = "border : 1px solid red; box-shadow: none"
                count += 1
            if state.isspace() or len(state) < 1:
                statealert = "border : 1px solid red; box-shadow: none"
                count += 1
            if category.isspace() or len(category) < 1:
                catalert = "border : 1px solid red; box-shadow: none"
                count += 1
            # if city.isspace() or len(city) < 1:
            #     cityalert = "border : 1px solid red; box-shadow: none"
            #     count += 1
            if heading.isspace() or len(heading) < 1:
                headalert = "border : 1px solid red; box-shadow: none"
                head_url_alert = "This field should not be empty"
                count += 1
            if news.isspace() or len(news) < 1:
                newsalert = "border : 1px solid red; box-shadow: none"
                count += 1
            if request.args.get('v') == 'dt':
                editing__ = True
            if count > 0:
                data =  be.get_user_instance(user_id=current_user.user_id)
                notifications = be.getNotifcations(user_id=current_user.user_id)
                drafts = be.getdraftsofUser(user_id=current_user.user_id)
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
                            notifications=notifications,
                            drafts=drafts,
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
            print(request.args.get('v'))
            if request.args.get('v') == 'dt':
                    be.deletedraft(draft_id=request.args.get('viawe'), user_id=current_user.user_id)
            # return jsonify({"message":response})
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
            headalert = ''
            blogalert = ''
            head_url_alert = ''
            body_alert = ''
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
                headalert = "border : 1px solid red; box-shadow: none"
                count += 1
            if blog.isspace() or len(blog) < 1:
                blogalert = "border : 1px solid red; box-shadow: none"
                count += 1
            if request.args.get('v') == 'dt':
                editing__ = True
            if count > 0:
                notifications = be.getNotifcations(user_id=current_user.user_id)
                drafts = be.getdraftsofUser(user_id=current_user.user_id)
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
                                       notifications=notifications,
                                       drafts=drafts,
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



@app.route("/api/news/article/user/news/delete", methods=['POST'])
def delete_user_article():
    if request.method == 'POST':
        # if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
        if current_user.is_authenticated:
            req = request.get_json()
            url_heading = req["heading_url"]
            response = be.delete_user_article(url_heading, user_id=current_user.user_id)
            # response = None
            # time.sleep(5)
            return jsonify(response)
        else:
            return "Unauthorized"
    else:
        return "Invalid Request"

@app.route("/api/blog/article/user/blog/delete", methods=['POST'])
def delete_user_blog_article():
    if request.method == 'POST':
        # if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
        if current_user.is_authenticated:
            req = request.get_json()
            user_id = current_user.user_id
            url_heading = req["heading_url"]
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

@app.route("/new/word/today/write", methods=['POST'])
def insert_todays_word():
    if request.method == 'POST':
        # if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
        if current_user.is_authenticated:
           if be.is_woftheday_stack_available():
            req = request.form
            word = req["word"]
            meaning = req["meaning"]
            wordalert = None
            meaningalert = None
            count = 0
            if word.isspace():
                wordalert = "border : 1px solid red; box-shadow:none"
                count += 1
            if meaning.isspace():
                meaningalert = "border : 1px solid red; box-shadow:none"
                count += 1
            if count > 1:
                notifications = be.getNotifcations(user_id=current_user.user_id)
                drafts = be.getdraftsofUser(user_id=current_user.user_id)
                return render_template("wordofthedaywrite.html",
                                       wordalert=wordalert,
                                       meaningalert=meaningalert,
                                       notifications=notifications,
                                       logged_in = current_user.is_authenticated,
                                       drafts=drafts)
            # user_id = req["user_id"]
            user_id = current_user.user_id
            # user_id = "ZOmRx01085587870"
            response = be.insert_todays_word(word=word, meaning=meaning, user_id=user_id)
            # return jsonify(response)
            return redirect('/news/read')
           else:
             notifications = be.getNotifcations(user_id=current_user.user_id)
             drafts = be.getdraftsofUser(user_id=current_user.user_id)
             return render_template('wordofthedaywrite.html', logged_in = current_user.is_authenticated, title="Word Of The Day | Write | lastevents.space", value=False, notifications=notifications, drafts=drafts)
        else:
            return "Unauthorized"
    else:
        return "Invalid Request"


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

@app.route('/api/<heading_url>/<val>/12087', methods=['GET', 'POST'])
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
            notifications = be.getNotifcations(user_id=current_user.user_id)
            drafts = be.getdraftsofUser(user_id=current_user.user_id)
            return render_template('contact.html', logged_in = current_user.is_authenticated, alert="Fields should not be empty", welcome=True, title="Contact | lastevents.space", notifications=notifications, drafts=drafts)
           return render_template('contact.html', logged_in = current_user.is_authenticated, alert="Fields should not be empty", welcome=True, title="Contact | lastevents.space")
        val = cont.email(email=email, message=message)
        if current_user.is_authenticated:
         notifications = be.getNotifcations(user_id=current_user.user_id)
         drafts = be.getdraftsofUser(user_id=current_user.user_id)
         return render_template('contact.html', logged_in = current_user.is_authenticated, alert="Message sent successfully", welcome=True, title="Contact | lastevents.space", notifications=notifications, drafts=drafts)
        return render_template('contact.html', logged_in = current_user.is_authenticated, alert="Message sent successfully", welcome=True, title="Contact | lastevents.space")
    if current_user.is_authenticated:
     notifications = be.getNotifcations(user_id=current_user.user_id)
     drafts = be.getdraftsofUser(user_id=current_user.user_id)
     return render_template('contact.html', logged_in = current_user.is_authenticated, contact__="#8479794f", welcome=True, title="Contact | lastevents.space", notifications=notifications, drafts=drafts)
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

@app.route('/search')
def search():
    notifications = []
    if current_user.is_authenticated:
        notifications = be.getNotifcations(user_id=current_user.user_id)
        drafts = be.getdraftsofUser(user_id=current_user.user_id)
        return render_template("search.html", title="Search | lastevents.space", search__="#8479794f", logged_in = current_user.is_authenticated, notifications=notifications, drafts=drafts)
    return render_template("search.html", title="Search | lastevents.space", search__="#8479794f", logged_in = current_user.is_authenticated)

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

@app.route('/api/create/user/comment/<article_id>', methods=['POST', 'GET'])
def createComment(article_id):
    if request.method == 'POST':
      if current_user.is_authenticated:
          comment = request.get_json()["comment"]
          author = current_user.username
          val = be.setComment(user_id=current_user.user_id, comment_=comment, article_id=article_id, author=author)
          print(val)
          return jsonify(val)

@app.route('/delete/user/comment/<comment_id>', methods=['POST', 'GET'])
def deleteUserComment(comment_id):
    if request.method == 'POST':
      if current_user.is_authenticated:
          be.deleteComment(user_id=current_user.user_id, comment_id=comment_id)
          return jsonify({'response':True})

@app.route('/api/draft/article/<draft_id>', methods=['POST', 'GET'])
def draftsave(draft_id):
    if request.method == "POST":
        if current_user.is_authenticated:
            user_id = current_user.user_id
            data = request.get_json()
            heading = data["heading"]
            article_data = data["article_data"]
            print(heading)
            print(article_data)
            response = be.editDraft(user_id=user_id, draft_id=draft_id, heading=heading, article_data=article_data)
            return jsonify({"response":response})

@app.route('/api/delete/user/draft/<draft_id>', methods=['POST'])
def deleteuserdraft(draft_id):
    if request.method == 'POST':
      if current_user.is_authenticated:
          be.deletedraft(user_id=current_user.user_id, draft_id=draft_id)
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

# CHATSPACE

@app.route('/chat/<chat_room_id>')
def chatspace(chat_room_id):
    chats = be.getChatsByRoomId(chat_room_id=chat_room_id)
    print(current_user.user_id)
    return render_template("chatspace.html", logged_in=current_user.is_authenticated, chats=chats, user_id=current_user.user_id)

# GROUPS

@app.route('/groups/root/space')
def rootspace():
    groups = be.get_available_countries()
    print(groups)
    return render_template('groups.html', logged_in=current_user.is_authenticated, groups=groups, val="Main")

@app.route('/api/groups/root/space', methods=['POST'])
def apirootspace():
    groups = be.get_available_countries()
    print(groups)
    # return render_template('groups.html', logged_in=current_user.is_authenticated, groups=groups, val="Main")
    return jsonify({'response':groups})

@app.route('/groups/root/space/<group>')
def rootspacesubgroup(group):
    newsubgroups = []
    groups = csc.getStatesByCountry(group)
    subgroups = be.get_available_states(country=group)
    high_contributor = be.get_high_contributor_by_country(group)
    for i in subgroups:
        if i["username"] in groups and i["username"] not in newsubgroups:
            newsubgroups.append(i)
    print(newsubgroups)
    return render_template('groups.html', logged_in=current_user.is_authenticated, groups=newsubgroups, val="Subgroup", high_contributor=high_contributor, group_=group)

@app.route('/api/groups/root/space/<group>', methods=['POST'])
def apirootspacesubgroup(group):
    newsubgroups = []
    groups = csc.getStatesByCountry(group)
    subgroups = be.get_available_states(country=group)
    high_contributor = be.get_high_contributor_by_country(group)
    for i in subgroups:
        if i["username"] in groups and i["username"] not in newsubgroups:
            newsubgroups.append(i)
    print(newsubgroups)
    # return render_template('groups.html', logged_in=current_user.is_authenticated, groups=newsubgroups, val="Subgroup", high_contributor=high_contributor, group_=group)
    return jsonify({"response":newsubgroups})

@app.route('/groups/root/space/<group>/<subgroup>')
def rootspacesubgroupmembers(group, subgroup):
    groups = be.get_all_users_by_state(subgroup)
    high_contributor = be.get_high_contributor_by_state(group, subgroup)
    print(high_contributor)
    return render_template('groups.html', logged_in=current_user.is_authenticated, groups=groups, val="Member", high_contributor=high_contributor)

@app.route('/api/groups/root/space/<group>/<subgroup>', methods=['POST'])
def apirootspacesubgroupmembers(group, subgroup):
    groups = be.get_all_users_by_state(subgroup)
    high_contributor = be.get_high_contributor_by_state(group, subgroup)
    # print(high_contributor)
    # return render_template('groups.html', logged_in=current_user.is_authenticated, groups=groups, val="Member", high_contributor=high_contributor)
    return jsonify({"response":groups})

# SOCKET IO

# @socketio.on('connect')
# def connect():
#     socketio.send("Connected")

# @socketio.on('message')
# def message(msg):
#     print(msg)
#     response = be.insertChat(username=current_user.username,
#                   user_id=current_user.user_id,
#                   text=msg["text"],
#                   chat_room_id=msg["chat_room_id"],
#                   )
#     socketio.send({"text":msg, "chat_id":response})
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

if __name__ == "__main__":
    # socketio.run(app, debug=True, port=8000)
    app.run(debug=True, port=8000)
