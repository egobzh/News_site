from flask import render_template, redirect,url_for
from . import app,db
from .forms import NewNews,UserForm
from .models import News,Category,Feedback

def index():
    news_list = News.query.all()
    сategory = Category.query.all()
    return render_template("index.html",news_list=news_list,сategory=сategory )

def form():
    user_form = UserForm()
    сategory = Category.query.all()
    Feedback_comments = Feedback.query.all()
    if user_form.validate_on_submit():
        no=Feedback()
        no.name = user_form.name.data
        no.text = user_form.text.data
        no.email = user_form.email.data
        no.rating = user_form.rating.data
        db.session.add(no)
        db.session.commit()

        return redirect("/")

    return render_template("form.html", form=user_form,Feedback_comments=Feedback_comments,сategory=сategory)

def add_news():
    new = NewNews()
    new.category.choices = [cat.title for cat in Category.query.all()]
    сategory = Category.query.all()
    if new.validate_on_submit():
        no = News()
        no.title = new.title.data
        no.text = new.text.data
        no.category_id=int(Category.query.filter(Category.title == new.category.data).one().id)
        db.session.add(no)
        db.session.commit()

        return redirect("/")

    return render_template("add_news.html", form=new,сategory=сategory)

def news_detail(id):
    news_d = News.query.get(id)
    сategory = Category.query.all()
    return render_template("news_detail.html", news_d=news_d,сategory=сategory)

def category(id):
    сategory = Category.query.all()
    category_name = Category.query.filter(Category.id == id).one().title
    news = News.query.filter(News.category_id == id).all()
    return render_template("category.html",сategory=сategory,news=news,category_name=category_name)

app.add_url_rule('/', 'index', index)
app.add_url_rule('/feedbackform', 'form', form, methods=["GET", "POST"])
app.add_url_rule('/add_news', 'add_news', add_news, methods=["GET", "POST"])
app.add_url_rule('/news_detail/<int:id>', 'news_detail', news_detail)
app.add_url_rule('/category/<int:id>', 'category', category)
