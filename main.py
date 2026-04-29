from flask import Flask, render_template, redirect, request, abort, flash, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from data.film import Film
from data.review import Review
from data.comment import Comment
from data.forum_post import ForumPost
from data.favorite import Favorite
from data.rating import Rating
from data.contact import ContactMessage
from forms.user import RegisterForm, LoginForm
from forms.film import FilmForm
from forms.review import ReviewForm
from forms.comment import CommentForm
from forms.forum import ForumPostForm
from forms.profile import ProfileForm
from forms.search import SearchForm
from forms.contact import ContactForm
from config import YANDEX_COLORS, GENRES, COUNTRIES, YEARS

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'kino_forum_super_secret_key_2026'

STYLE = '''
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',Arial,sans-serif;background:#f0f0f0;color:#000}
.ya-header{background:#fc0;height:60px;display:flex;align-items:center;justify-content:space-between;padding:0 30px;position:sticky;top:0;z-index:100;box-shadow:0 2px 4px rgba(0,0,0,0.1)}
.ya-logo{font-size:26px;font-weight:800;color:#000;text-decoration:none}
.ya-logo span{color:#f00}
.ya-nav{display:flex;gap:5px}
.ya-nav a{text-decoration:none;color:#000;padding:8px 16px;border-radius:20px;font-size:14px;font-weight:500}
.ya-nav a:hover{background:rgba(0,0,0,0.08)}
.ya-header-right{display:flex;align-items:center;gap:12px}
.ya-btn{display:inline-block;padding:10px 22px;border-radius:24px;text-decoration:none;font-size:14px;font-weight:600;border:none;cursor:pointer;transition:all 0.2s}
.ya-btn:hover{transform:translateY(-1px);box-shadow:0 4px 8px rgba(0,0,0,0.15)}
.ya-btn-yellow{background:#fc0;color:#000}
.ya-btn-black{background:#000;color:#fff}
.ya-btn-red{background:#f33;color:#fff}
.ya-btn-gray{background:#e0e0e0;color:#000}
.ya-btn-outline{background:transparent;border:2px solid #fc0;color:#000}
.ya-btn-sm{padding:6px 14px;font-size:12px}
.ya-container{max-width:1100px;margin:0 auto;padding:30px 20px}
.ya-card{background:#fff;border-radius:16px;padding:24px;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,0.06)}
.ya-input{width:100%;padding:14px 16px;border:2px solid #e8e8e8;border-radius:12px;font-size:15px;background:#fafafa}
.ya-input:focus{border-color:#fc0;outline:none;background:#fff}
.ya-input-group{margin-bottom:18px}
.ya-input-group label{display:block;margin-bottom:6px;font-weight:600;font-size:14px;color:#333}
.ya-alert{padding:14px 18px;border-radius:12px;margin-bottom:18px;font-size:14px}
.ya-alert-error{background:#fff0f0;color:#c00;border-left:4px solid #f33}
.ya-alert-success{background:#f0fff0;color:#0a0;border-left:4px solid #0a0}
.ya-alert-info{background:#f0f0ff;color:#06f;border-left:4px solid #06f}
.ya-avatar{width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:700;color:#000;flex-shrink:0}
.ya-avatar-sm{width:32px;height:32px;font-size:14px}
.ya-avatar-lg{width:100px;height:100px;font-size:44px}
.ya-dropdown{position:relative;display:inline-block}
.ya-dropdown-btn{background:none;border:none;cursor:pointer;display:flex;align-items:center;gap:8px;font-size:14px;font-weight:500;padding:6px 12px;border-radius:20px}
.ya-dropdown-btn:hover{background:rgba(0,0,0,0.05)}
.ya-dropdown-menu{display:none;position:absolute;right:0;top:100%;background:#fff;min-width:200px;box-shadow:0 8px 24px rgba(0,0,0,0.15);border-radius:12px;z-index:10}
.ya-dropdown:hover .ya-dropdown-menu{display:block}
.ya-dropdown-menu a{display:block;padding:12px 18px;text-decoration:none;color:#000;font-size:14px}
.ya-dropdown-menu a:hover{background:#f5f5f5}
.ya-grid{display:grid;gap:20px}
.ya-grid-2{grid-template-columns:1fr 1fr}
.ya-grid-3{grid-template-columns:1fr 1fr 1fr}
.ya-grid-4{grid-template-columns:1fr 1fr 1fr 1fr}
.ya-flex{display:flex;gap:10px;align-items:center}
.ya-flex-between{display:flex;justify-content:space-between;align-items:center}
.ya-tag{display:inline-block;padding:4px 10px;border-radius:12px;font-size:12px;background:#f0f0f0;margin:2px}
.ya-rating{color:#fc0;font-size:20px}
.ya-text-muted{color:#999}
.ya-text-sm{font-size:13px}
.ya-mb{margin-bottom:10px}
.ya-mt{margin-top:10px}
.ya-film-poster{width:100%;height:350px;object-fit:cover;border-radius:12px;background:#e0e0e0;display:flex;align-items:center;justify-content:center;font-size:60px;color:#999}
.ya-section-title{font-size:22px;font-weight:700;margin-bottom:20px;padding-bottom:10px;border-bottom:3px solid #fc0}
.ya-footer{text-align:center;padding:30px;color:#999;font-size:13px;margin-top:40px;border-top:1px solid #e0e0e0}
@media(max-width:768px){.ya-grid-2,.ya-grid-3,.ya-grid-4{grid-template-columns:1fr}.ya-header{padding:0 15px}}
</style>
'''

def get_header():
    if current_user.is_authenticated:
        user_btn = f'''
        <div class="ya-dropdown">
            <button class="ya-dropdown-btn">
                <div class="ya-avatar ya-avatar-sm" style="background:{YANDEX_COLORS[current_user.id % 12]}">{current_user.name[0].upper()}</div>
                {current_user.name}
            </button>
            <div class="ya-dropdown-menu">
                <a href="/profile/{current_user.id}">📋 Профиль</a>
                <a href="/my_favorites">⭐ Избранное</a>
                <a href="/profile/edit">⚙️ Настройки</a>
                <a href="/logout">🚪 Выйти</a>
            </div>
        </div>'''
    else:
        user_btn = '''
        <a href="/login" class="ya-btn ya-btn-outline">Войти</a>
        <a href="/register" class="ya-btn ya-btn-yellow">Регистрация</a>'''
    return f'''
    <header class="ya-header">
        <a href="/" class="ya-logo">Кино<span>.</span>Форум</a>
        <nav class="ya-nav">
            <a href="/">Главная</a>
            <a href="/films">Фильмы</a>
            <a href="/forum">Форум</a>
            <a href="/top">Топ</a>
            <a href="/search">🔍 Поиск</a>
            <a href="/contacts">📞 Контакты</a>
        </nav>
        <div class="ya-header-right">{user_btn}</div>
    </header>'''

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)

@app.route('/')
def index():
    db_sess = db_session.create_session()
    latest_films = db_sess.query(Film).order_by(Film.created_date.desc()).limit(6).all()
    top_films = db_sess.query(Film).order_by(Film.rating.desc()).limit(5).all()
    latest_reviews = db_sess.query(Review).order_by(Review.created_date.desc()).limit(5).all()
    latest_forum = db_sess.query(ForumPost).order_by(ForumPost.created_date.desc()).limit(5).all()
    return render_template('index.html', latest_films=latest_films, top_films=top_films, latest_reviews=latest_reviews, latest_forum=latest_forum, YANDEX_COLORS=YANDEX_COLORS, STYLE=STYLE, get_header=get_header)

@app.route('/films')
def films():
    db_sess = db_session.create_session()
    genre_filter = request.args.get('genre', '')
    country_filter = request.args.get('country', '')
    year_filter = request.args.get('year', '')
    sort_by = request.args.get('sort', 'newest')
    query = db_sess.query(Film)
    if genre_filter:
        query = query.filter(Film.genre.contains(genre_filter))
    if country_filter:
        query = query.filter(Film.country.contains(country_filter))
    if year_filter:
        query = query.filter(Film.year == int(year_filter))
    if sort_by == 'rating':
        query = query.order_by(Film.rating.desc())
    elif sort_by == 'title':
        query = query.order_by(Film.title)
    else:
        query = query.order_by(Film.created_date.desc())
    films = query.all()
    return render_template('films.html', films=films, GENRES=GENRES, COUNTRIES=COUNTRIES, YEARS=YEARS, current_genre=genre_filter, current_country=country_filter, current_year=year_filter, current_sort=sort_by, STYLE=STYLE, get_header=get_header)

@app.route('/film/<int:id>')
def view_film(id):
    db_sess = db_session.create_session()
    film = db_sess.get(Film, id)
    if not film:
        abort(404)
    reviews = db_sess.query(Review).filter(Review.film_id == id).order_by(Review.created_date.desc()).all()
    ratings = db_sess.query(Rating).filter(Rating.film_id == id).all()
    avg_rating = sum([r.rating for r in ratings]) / len(ratings) if ratings else 0
    user_rating = None
    is_favorite = False
    if current_user.is_authenticated:
        ur = db_sess.query(Rating).filter(Rating.user_id == current_user.id, Rating.film_id == id).first()
        if ur:
            user_rating = ur.rating
        fav = db_sess.query(Favorite).filter(Favorite.user_id == current_user.id, Favorite.film_id == id).first()
        if fav:
            is_favorite = True
    similar_films = db_sess.query(Film).filter(Film.id != id).limit(4).all()
    return render_template('view_film.html', film=film, reviews=reviews, avg_rating=round(avg_rating, 1), user_rating=user_rating, is_favorite=is_favorite, similar_films=similar_films, YANDEX_COLORS=YANDEX_COLORS, STYLE=STYLE, get_header=get_header)

@app.route('/add_film', methods=['GET', 'POST'])
@login_required
def add_film():
    form = FilmForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        film = Film()
        film.title = form.title.data
        film.director = form.director.data
        film.year = form.year.data
        film.genre = form.genre.data
        film.country = form.country.data
        film.duration = form.duration.data
        film.description = form.description.data
        film.user_id = current_user.id
        db_sess.add(film)
        db_sess.commit()
        flash('Фильм добавлен!', 'success')
        return redirect(f'/film/{film.id}')
    return render_template('add_film.html', form=form, STYLE=STYLE, get_header=get_header)

@app.route('/film/<int:id>/review', methods=['GET', 'POST'])
@login_required
def add_review(id):
    form = ReviewForm()
    db_sess = db_session.create_session()
    film = db_sess.get(Film, id)
    if not film:
        abort(404)
    if form.validate_on_submit():
        review = Review(title=form.title.data, content=form.content.data, user_id=current_user.id, film_id=id)
        db_sess.add(review)
        existing_rating = db_sess.query(Rating).filter(Rating.user_id == current_user.id, Rating.film_id == id).first()
        if existing_rating:
            existing_rating.rating = form.rating.data
        else:
            db_sess.add(Rating(rating=form.rating.data, user_id=current_user.id, film_id=id))
        ratings = db_sess.query(Rating).filter(Rating.film_id == id).all()
        film.rating = sum([r.rating for r in ratings]) / len(ratings)
        film.review_count = len(db_sess.query(Review).filter(Review.film_id == id).all())
        db_sess.commit()
        flash('Рецензия опубликована!', 'success')
        return redirect(f'/film/{id}')
    return render_template('add_review.html', form=form, film=film, STYLE=STYLE, get_header=get_header)

@app.route('/rate_film/<int:id>', methods=['POST'])
@login_required
def rate_film(id):
    rating_value = int(request.form.get('rating', 0))
    if rating_value < 1 or rating_value > 10:
        return redirect(f'/film/{id}')
    db_sess = db_session.create_session()
    film = db_sess.get(Film, id)
    existing = db_sess.query(Rating).filter(Rating.user_id == current_user.id, Rating.film_id == id).first()
    if existing:
        existing.rating = rating_value
    else:
        db_sess.add(Rating(rating=rating_value, user_id=current_user.id, film_id=id))
    ratings = db_sess.query(Rating).filter(Rating.film_id == id).all()
    film.rating = sum([r.rating for r in ratings]) / len(ratings)
    db_sess.commit()
    return redirect(f'/film/{id}')

@app.route('/favorite/<int:id>')
@login_required
def toggle_favorite(id):
    db_sess = db_session.create_session()
    fav = db_sess.query(Favorite).filter(Favorite.user_id == current_user.id, Favorite.film_id == id).first()
    if fav:
        db_sess.delete(fav)
    else:
        db_sess.add(Favorite(user_id=current_user.id, film_id=id))
    db_sess.commit()
    return redirect(f'/film/{id}')

@app.route('/my_favorites')
@login_required
def my_favorites():
    db_sess = db_session.create_session()
    favs = db_sess.query(Favorite).filter(Favorite.user_id == current_user.id).all()
    films = [db_sess.get(Film, f.film_id) for f in favs]
    return render_template('favorites.html', films=films, YANDEX_COLORS=YANDEX_COLORS, STYLE=STYLE, get_header=get_header)

@app.route('/forum')
def forum():
    db_sess = db_session.create_session()
    posts = db_sess.query(ForumPost).order_by(ForumPost.created_date.desc()).all()
    return render_template('forum.html', posts=posts, YANDEX_COLORS=YANDEX_COLORS, STYLE=STYLE, get_header=get_header)

@app.route('/forum/add', methods=['GET', 'POST'])
@login_required
def add_forum_post():
    form = ForumPostForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        post = ForumPost(title=form.title.data, content=form.content.data, category=form.category.data, user_id=current_user.id)
        db_sess.add(post)
        db_sess.commit()
        return redirect('/forum')
    return render_template('add_forum_post.html', form=form, STYLE=STYLE, get_header=get_header)

@app.route('/forum/<int:id>')
def view_forum_post(id):
    db_sess = db_session.create_session()
    post = db_sess.get(ForumPost, id)
    if not post:
        abort(404)
    post.views += 1
    db_sess.commit()
    comments = db_sess.query(Comment).filter(Comment.forum_post_id == id).order_by(Comment.created_date).all()
    form = CommentForm()
    return render_template('view_forum_post.html', post=post, comments=comments, form=form, YANDEX_COLORS=YANDEX_COLORS, STYLE=STYLE, get_header=get_header)

@app.route('/forum/<int:id>/comment', methods=['POST'])
@login_required
def add_forum_comment(id):
    form = CommentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        db_sess.add(Comment(content=form.content.data, user_id=current_user.id, forum_post_id=id))
        post = db_sess.get(ForumPost, id)
        post.comment_count += 1
        db_sess.commit()
    return redirect(f'/forum/{id}')

@app.route('/top')
def top():
    db_sess = db_session.create_session()
    top_rated = db_sess.query(Film).order_by(Film.rating.desc()).limit(20).all()
    most_reviewed = db_sess.query(Film).order_by(Film.review_count.desc()).limit(20).all()
    return render_template('top.html', top_rated=top_rated, most_reviewed=most_reviewed, YANDEX_COLORS=YANDEX_COLORS, STYLE=STYLE, get_header=get_header)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    results = None
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        q = form.query.data
        films = db_sess.query(Film).filter(Film.title.contains(q)).all()
        reviews = db_sess.query(Review).filter(Review.content.contains(q)).all()
        posts = db_sess.query(ForumPost).filter(ForumPost.title.contains(q) | ForumPost.content.contains(q)).all()
        results = {'films': films, 'reviews': reviews, 'posts': posts}
    return render_template('search.html', form=form, results=results, YANDEX_COLORS=YANDEX_COLORS, STYLE=STYLE, get_header=get_header)

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        db_sess.add(ContactMessage(name=form.name.data, email=form.email.data, message=form.message.data))
        db_sess.commit()
        flash('Сообщение отправлено!', 'success')
    return render_template('contacts.html', form=form, STYLE=STYLE, get_header=get_header)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, message="Пароли не совпадают", STYLE=STYLE, get_header=get_header)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', form=form, message="Пользователь уже существует", STYLE=STYLE, get_header=get_header)
        user = User(name=form.name.data, email=form.email.data, about=form.about.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/')
    return render_template('register.html', form=form, STYLE=STYLE, get_header=get_header)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', form=form, message="Неверный логин или пароль", STYLE=STYLE, get_header=get_header)
    return render_template('login.html', form=form, STYLE=STYLE, get_header=get_header)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/profile/<int:user_id>')
def profile(user_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)
    if not user:
        abort(404)
    reviews = db_sess.query(Review).filter(Review.user_id == user_id).order_by(Review.created_date.desc()).limit(10).all()
    posts = db_sess.query(ForumPost).filter(ForumPost.user_id == user_id).order_by(ForumPost.created_date.desc()).limit(10).all()
    films = db_sess.query(Film).filter(Film.user_id == user_id).all()
    return render_template('profile.html', user=user, reviews=reviews, posts=posts, films=films, YANDEX_COLORS=YANDEX_COLORS, STYLE=STYLE, get_header=get_header)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    db_sess = db_session.create_session()
    user = db_sess.get(User, current_user.id)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.about = form.about.data
        db_sess.commit()
        return redirect(f'/profile/{current_user.id}')
    form.name.data = user.name
    form.email.data = user.email
    form.about.data = user.about
    return render_template('edit_profile.html', form=form, STYLE=STYLE, get_header=get_header)

@app.route('/admin/messages')
@login_required
def view_messages():
    db_sess = db_session.create_session()
    messages = db_sess.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()
    result = ""
    for msg in messages:
        result += f"<div class='ya-card'><strong>{msg.name}</strong> ({msg.email})<br>{msg.message}<br><small>{msg.created_at}</small></div>"
    return f"{STYLE}{get_header()}<div class='ya-container'><h1>Сообщения</h1>{result}</div>"

@app.errorhandler(404)
def not_found(e):
    return f"{STYLE}{get_header()}<div class='ya-container'><div class='ya-card' style='text-align:center'><h1>404</h1><p>Страница не найдена</p><a href='/' class='ya-btn ya-btn-yellow'>На главную</a></div></div>", 404

@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html', STYLE=STYLE, get_header=get_header), 401

def main():
    db_session.global_init("db/kino_forum.db")
    app.run()

if __name__ == '__main__':
    main()