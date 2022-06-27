from contextlib import redirect_stderr
import html
from os import abort
from click import password_option
from flask import Flask, jsonify, render_template, request, redirect
from flask_login import current_user
from sqlalchemy import false, true
from CountriesStatesCities import CountriesStatesCities
from backend import BackEnd
from flask_login import LoginManager, login_user, current_user, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from forgotpassword import ResetPassword
from contact import Contactemail
from SearchApi import SearchApi

app = Flask(__name__)
be = BackEnd()
csc = CountriesStatesCities()
fp = ResetPassword()
cont = Contactemail()
se = SearchApi()

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
                                   title="Sign Up",
                                   signup_login_="#8479794f"
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
                                   title='Sign Up',
                                   signup_login_="#8479794f"
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
                                   title="Sign Up",
                                   signup_login_="#8479794f"
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
                                   title="Sign Up",
                                   signup_login_="#8479794f"
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
                                   title="Sign Up",
                                   signup_login_="#8479794f"
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
        return render_template("signup.html", logged_in = current_user.is_authenticated, title="Sign Up", signup_login_="#8479794f")

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
            return render_template("signin.html", emailalert=emailalert, passwordalert=passwordalert, logged_in = current_user.is_authenticated, title="Login", signup_login_="#8479794f")
        if not be.validemail(email):
            if be.validemail_and_password_for_login(email, password):
                user = User.query.filter_by(email=email).first()
                login_user(user)
                if to == None:
                    return redirect("/home")
                elif to == 'write':
                    return redirect("/news/write")
                elif to == 'bwrite':
                    return redirect("/blog/write")
                elif to == 'wwrite':
                    return redirect("/wofday/write")
            else:
                if to == 'write':
                    return render_template("signin.html", to=f"?to={to}", alert="Password incorrect", logged_in = current_user.is_authenticated, title="Login", signup_login_="#8479794f")
                if to == 'bwrite':
                    return render_template("signin.html", to=f"?to={to}", alert="Password incorrect", logged_in = current_user.is_authenticated, title="Login", signup_login_="#8479794f")
                if to == 'wwrite':
                    return render_template("signin.html", to=f"?to={to}", alert="Password incorrect", logged_in = current_user.is_authenticated, title="Login", signup_login_="#8479794f")
                else:       
                    return render_template("signin.html", alert="Password incorrect", logged_in = current_user.is_authenticated, title="Login", signup_login_="#8479794f")
        else:
            if to == 'write':
                    return render_template("signin.html", to=f"?to={to}", alert="Email not found", logged_in = current_user.is_authenticated, title="Login", signup_login_="#8479794f")
            if to == 'bwrite':
                    return render_template("signin.html", to=f"?to={to}", alert="Email not found", logged_in = current_user.is_authenticated, title="Login", signup_login_="#8479794f")
            if to == 'wwrite':
                    return render_template("signin.html", to=f"?to={to}", alert="Email not found", logged_in = current_user.is_authenticated, title="Login", signup_login_="#8479794f")
            return render_template("signin.html", alert="Email not found", logged_in = current_user.is_authenticated, title="Login", signup_login_="#8479794f")
    else:
        # if current_user.is_authenticated:
        #     return redirect("/")
        if to != None:
           return render_template("signin.html", to=f"?to={to}", alert="Writing requires login", logged_in = current_user.is_authenticated, title="Login", signup_login_="#8479794f")
        return render_template("signin.html", logged_in = current_user.is_authenticated, title="Login", signup_login_="#8479794f")
        # return render_template("signin.html")
        
@app.route('/news/read')
def news_read():
    if request.method == 'GET':
       todays_word = be.get_todays_word() 
       if current_user.is_authenticated:
           user = be.get_user_instance(user_id=current_user.user_id)
        #    print(user['city'])
           return redirect(f"/news/read/{user['country']}/{user['state']}/general/{user['city']}")
       else:
            articles_news = be.get_all_news_content()
            blogs = be.blog_get()[0:10]
            return render_template("read.html",
                              todays_word=todays_word,
                              logged_in = current_user.is_authenticated,
                              title="News | Read",
                              read__="#8479794f",
                              response = articles_news,
                              recent_blogs = blogs,
                              __me__=True
                                        )
    else:
        return "Method not allowed"        
        
@app.route('/blog/read')
def blog_read():
    if request.method == 'GET':
        response = be.blog_get()
        return render_template("blog.html", response=response, logged_in = current_user.is_authenticated, title="Blog | Read", blog__="#8479794f")
        
@app.route('/news/read/filter', methods = ['POST', 'GET'])
def news_get_filter():
    if request.method == 'POST':
        req = request.form
        country = req["country"].title()
        state = req["state"].title()
        category = req["category"].title()
        city = req["city"].title()
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
         return render_template("read.html",
                               countalert=countalert,
                               statealert=statealert,
                               catalert=catalert,
                               cityalert=cityalert,
                               todays_word = be.get_todays_word(),
                               alert=True,
                               logged_in = current_user.is_authenticated,
                               title=f"News | {country} | {category}",
                               read__="#8479794f",
                               __me__ = True)
        
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
    data = be.all_news_articles_than_one(news_id_or_news_heading)
    return render_template("view.html", response=news, news=True, logged_in = current_user.is_authenticated, data=data, title=f"{news['heading']} | news.org")

@app.route("/blog/read/view/<blog_id_or_blogs_heading>")
def view_blogs_article(blog_id_or_blogs_heading):
    # formatted_url = blog_id_or_blogs_heading.replace('-', ' ')
    blog = be.view_blogs_article(blog_id_or_blogs_heading)
    # for_you_blogs = be.blog_get()
    data = be.all_blog_aritcles_than_one(heading_url=blog_id_or_blogs_heading)
    return render_template("view.html", response=blog, blog=True, logged_in = current_user.is_authenticated, data=data[0:10], title=f"{blog['heading']} | news.org", read__="#8479794f")
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
                           __me__=True
                           )      
        
@app.route('/earninfo')
def earninfo():
    return render_template('earninfo.html', logged_in = current_user.is_authenticated, title="Earn | Info", earninfo__="#8479794f")        
        
@app.route('/news/write')
def newswrite():
    if current_user.is_authenticated:
     data = be.get_user_instance(user_id=current_user.user_id)
     return render_template('newswrite.html', 
                            user_country = data["country"],
                            user_state = data["state"],
                            user_city=data["city"],logged_in = current_user.is_authenticated, title="News | Write", write__="#8479794f")                
    else:
     return redirect("/login?to=write") 

@app.route('/news/edit/<heading_url>')
def newswrite_edit(heading_url):
    if current_user.is_authenticated:
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
                            getvalue=f"?edit=True&p={heading_url}", logged_in = current_user.is_authenticated, title="News | Edit") 

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
                            getvalue=f"?edit=True&p={heading_url}", logged_in = current_user.is_authenticated, title="Blog | Edit")      
         
@app.route('/blog/write')
def blogwrite():
    if current_user.is_authenticated:
     return render_template('blogwrite.html', logged_in = current_user.is_authenticated, title="Blog | Write", write="#8479794f")                
    else:
     return redirect("/login?to=bwrite") 
             
@app.route('/wofday/write')
def wordofthedaywrite():
    if current_user.is_authenticated:
     if be.is_woftheday_stack_available():   
      return render_template('wordofthedaywrite.html', logged_in = current_user.is_authenticated, title="Word Of The Day | Write", value=True)                
     else:
      return render_template('wordofthedaywrite.html', logged_in = current_user.is_authenticated, title="Word Of The Day | Write", value=False)
    else:
     return redirect("/login?to=wwrite") 
         
@app.route('/forgotpassword', methods=['POST', 'GET'])
def forgotpassword():
    if request.method == 'POST':
         email = request.form["email"]
         if not be.validemail(email=email):
           fp.sendresetpasswordmail(email=email)
           return render_template("forgotpassword.html", logged_in = current_user.is_authenticated, title="ForgotPassword", alert="Check your mail for further details")               
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
    return render_template("wordmean.html", response=response, logged_in = current_user.is_authenticated, title="Word | Meaning")
@app.route('/home')
def home():
    return render_template("welcome.html", logged_in = current_user.is_authenticated, welcome=True, title="Home")
    
@app.route('/verify', methods=['POST', 'GET'])
def verify():
    if request.method == 'GET': 
      if current_user.is_authenticated:
        if be.is_verified(user_id=current_user.user_id):
            return redirect('/home')
        else:    
            val = be.send_verification_code(email=current_user.email, user_id=current_user.user_id)
            return render_template('verify.html', logged_in = current_user.is_authenticated, title="Verify", email=current_user.email)   
      else:
            return render_template('verify.html', logged_in = current_user.is_authenticated, title="Verify", email=current_user.email)   
    if request.method == 'POST':
        if current_user.is_authenticated:
            code = request.form['code']
            val = be.check_verification_code(email=current_user.email, user_id=current_user.user_id, code=code)
            if val == True:
             return redirect('/')
            else:
             return render_template('verify.html', logged_in = current_user.is_authenticated, title="Verify", email=current_user.email, alert="Incorrect Code")

@app.route('/data/<href>')
def userdata(href):
    if current_user.is_authenticated:
        data = be.get_user_instance(user_id=current_user.user_id)
        me = False
        yourarticles = False
        yourincome = False
        news_2324 = False
        blog_2324 = False
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
        elif href == "yourincome":
            yourincome = True
            bac_val_yi = "#8479794f"
        else:
            return redirect("/data/me")
        return render_template("data.html", 
                            response=data,
                            me = me,
                            yourarticles = yourarticles,
                            yourincome = yourincome,
                            news_2342 = news_2324,
                            blog_2342 = blog_2324,
                            logged_in = current_user.is_authenticated,
                            me_=bac_val_me,
                            articles_=bac_val_art,
                            yourincome_ = bac_val_yi,
                            title="News | Articles | Data",
                            me__="#8479794f",
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
            keywords = req["keywords"].split(',')
            count = 0
            countalert = None
            statealert = None
            catalert = None
            newsalert = None
            headalert = None
            head_url_alert = None
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
                count += 1            
            if news.isspace() or len(news) < 1:
                newsalert = "border : 1px solid red; box-shadow: none"
                count += 1            
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
                            alert = head_url_alert,
                            news_news = news,
                            news_heading = heading,
                            news_category = category,
                            logged_in = current_user.is_authenticated,
                            title="News | Write"
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
                    keywords=keywords
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
                )
                if response == "Update not accepted":
                    return "Unauthorized"
                if response == "Invalid heading":
                    return 
            # return jsonify({"message":response})
            return redirect(f'/news/read/{country}/{state}/{category}/{city}')
        else:
            return "Unauthorized"
    else:
        return "Invalid Request"

@app.route('/sample/newstemplates')
def news_templates():
    return render_template('newstemplates.html')

# @app.route('/api/blog/article/write', methods=['POST', 'GET'])
# def api_blog_article_write():
#     if request.method == 'POST':
#         if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
#             req = request.get_json()
#             heading = req["heading"]
#             blog = req["blog"]
#             keywords = req["keywords"]
#             if heading.isspace():
#                 return "Heading should not be empty"
#             else:
#                 pass
#             if len(heading) < 1:
#                 return "Heading should not be empty"
#             else:
#                 pass
#             if blog.isspace():
#                return "Text Field should not be empty"
#             else:
#                 pass
#             if len(blog) < 1:
#                return "Text Field should not be empty"
#             else:
#                 pass
#             # author_id = current_user.user_id
#             author_id = current_user.user_id
#             author_name = current_user.author_name
#             response = be.blogs_article_write(
#                 heading=heading,
#                 author_id=author_id,
#                 author_name=author_name,
#                 blog=blog,
#                 keywords=keywords
#             )
#             return jsonify({"message":response})
#         else:
#             return "Unauthorized"
#     else:
#         return "Invalid Request"

@app.route('/blog/article/write', methods=['POST', 'GET'])
def api_blog_article_write():
    if request.method == 'POST':
        # if request.headers.get("api-id") == "api-2342-unafeaeAdf34-234234.2342-234":
        if current_user.is_authenticated:  
            req = request.form
            heading = req["heading"]
            blog = req["blog"]
            keywords = req["keywords"].split(',')
            count = 0
            headalert = None
            blogalert = None
            head_url_alert = None
            if not be.validheadingurls(heading_url=heading.replace(" ", "-").replace("?", "")):
               head_url_alert = "You cannot use this heading, this already exists"
               count += 1          
            if heading.isspace() or len(heading) < 1:
                headalert = "border : 1px solid red; box-shadow: none"
                count += 1            
            if blog.isspace() or len(blog) < 1:
                blogalert = "border : 1px solid red; box-shadow: none"
                count += 1        
            if count > 0:
                return render_template("blogwrite.html",
                                       blogalert=blogalert,
                                       headalert=headalert,
                                       logged_in = current_user.is_authenticated,
                                       blog_heading=heading,
                                       blog_blog=blog,
                                       alert=head_url_alert)    
            # author_id = current_user.user_id
            author_id = current_user.user_id
            author_name = current_user.username
            if request.args.get('edit') != "True":
                response = be.blogs_article_write(
                    heading=heading,
                    author_id=author_id,
                    author_name=author_name,
                    blog=blog,
                    keywords=keywords
                )
            elif request.args.get('edit') == "True":
                response = be.edit_blog(
                    heading=heading,
                    author_id=author_id,
                    prev_heading_url=request.args.get("p"),
                    blog=blog,
                    keywords=keywords,
                    blog__="#8479794f"
                )
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
                return render_template("wordofthedaywrite.html",
                                       wordalert=wordalert,
                                       meaningalert=meaningalert,
                                       logged_in = current_user.is_authenticated)
            # user_id = req["user_id"]
            user_id = current_user.user_id
            # user_id = "ZOmRx01085587870"
            response = be.insert_todays_word(word=word, meaning=meaning, user_id=user_id)
            # return jsonify(response)
            return redirect('/news/read')
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
        # print(val)
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
            return render_template('contact.html', logged_in = current_user.is_authenticated, alert="Fields should not be empty", welcome=True, title="Contact |")
        val = cont.email(email=email, message=message)
        return render_template('contact.html', logged_in = current_user.is_authenticated, alert="Message sent successfully", welcome=True, title="Contact |")
    return render_template('contact.html', logged_in = current_user.is_authenticated, contact__="#8479794f", welcome=True, title="Contact | ")
      
@app.route('/api/search', methods=['POST'])
def apisearch():
    data = request.get_json()["text"]
    resp = se.Search(text = data)
    # print(resp)
    # resp_ = be.get_articles_by_heading_url(heading_urls=resp)
    return jsonify({"response":resp})
      
@app.route('/privacy')
def privacy(): 
    return render_template("privacy.html", welcome=True, title="Privacy | ")     
      
@app.route('/terms')
def terms(): 
    return render_template("terms.html", welcome=True, title="Terms | ") 
      
@app.route('/about')
def about(): 
    return render_template("about.html", welcome=True, title="About | ")       
      
@app.route('/search')
def search():
    return render_template("search.html", title="Search |", search__="#8479794f", logged_in = current_user.is_authenticated)      
      
@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect('/login')
    else:
        return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)
