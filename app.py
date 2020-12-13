from flask import Flask, request, render_template, redirect, url_for, flash
import os
from flask_sqlalchemy import SQLAlchemy
from form import SingUpForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
import shutil
from sanitize_filename import sanitize

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = 'KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db_users = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'


class User(UserMixin, db_users.Model):
    id = db_users.Column(db_users.Integer, primary_key=True)
    fio = db_users.Column(db_users.String(150), index=True, unique=True)
    login = db_users.Column(db_users.String(64), index=True, unique=True)
    password_hash = db_users.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.login)


class Channels(db.Model):
    __tablename__ = 'channels'

    # Загальна інформація про ресурс

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)  # азвание канала
    general_information_about_the_resource = db.Column(db.Text)  # Загальна інформація про ресурс
    adres_img_for_general_information_about_the_resource = db.Column(db.Text)  # адрес картинки
    date_of_resourc_creation = db.Column(db.Text)  # Дата створення ресурсу
    other_social_platforms = db.Column(db.Text)  # Інші соціальні площадки

    # Вміст ресурсу

    resource_content_date = db.Column(db.Text)  # Вміст ресурсу станом на:
    publications_per_day = db.Column(db.Text)  # публікацій в день
    the_main_focus_of_the_channel = db.Column(db.Text)  # Основна спрямованість каналу
    related_areas = db.Column(db.Text)  # Суміжні напрямки
    channel_content = db.Column(db.Text)  # Вміст каналу
    adres_img_for_views = db.Column(db.Text)  # Ардес картинки для кол переглядів

    # Контактна інформація для зв'язку

    contact_information_for_communication = db.Column(db.Text)  # Контактна інформація для зв'язку
    adres_img_for_contact_information_for_communication = db.Column(
        db.Text)  # Ардес картинки для Контактна інформація для зв'язку

    # Платіжні засоби (належність), прайси на оплату реклами, умови

    price_for_advertising_news = db.Column(db.Text)  # Прайс на розміщення реклами, новин
    payment_is_made_by_card = db.Column(db.Text)  # Оплата здійснюється на карти

    # Причетні до ресурсу особи

    name_administrator = db.Column(db.Text)  # ФІО Адміністратора
    adres_img_for_photo_admin = db.Column(db.Text)  # Фото Адміністратора
    date_of_birth = db.Column(db.Text)  # Дата народження
    place_of_birth = db.Column(db.Text)  # Місце народження
    phone_number = db.Column(db.Text)  # телефон
    passport = db.Column(db.Text)  # паспорт
    drivers_license = db.Column(db.Text)  # Посвідчення водія
    other = db.Column(db.Text)  #

    # Результати відпрацювання SNIFER

    snifer = db.Column(db.Text)

    # Канали партнери / противники

    channel_partners = db.Column(db.Text)
    Channels_opponents = db.Column(db.Text)

    # Репости. Канали, які цитує

    channels_that_made_reposts = db.Column(db.Text)
    adres_img_for_channels_that_made_reposts = db.Column(db.Text)
    channels_quoted_by_the_telegram_channel = db.Column(db.Text)
    adres_img_for_channels_quoted_by_the_telegram_channel = db.Column(db.Text)

    def __repr__(self):
        return '<Poem (id=%s ' \
               'name=%s ' \
               'general_information_about_the_resource=%s ' \
               'adres_img_for_general_information_about_the_resource=%s ' \
               'date_of_resourc_creation=%s ' \
               'other_social_platforms=%s' \
               'resource_content_date=%s' \
               'publications_per_day=%s' \
               'the_main_focus_of_the_channel=%s' \
               'related_areas=%s' \
               'channel_content=%s' \
               'adres_img_for_views=%s' \
               'contact_information_for_communication=%s' \
               'adres_img_for_contact_information_for_communication=%s' \
               'price_for_advertising_news=%s' \
               'payment_is_made_by_card=%s' \
               'name_administrator=%s' \
               'adres_img_for_photo_admin=%s' \
               'date_of_birth=%s' \
               'place_of_birth=%s' \
               'phone_number=%s' \
               'passport=%s' \
               'drivers_license=%s' \
               'other=%s' \
               'snifer=%s' \
               'channel_partners=%s' \
               'Channels_opponents=%s' \
               'channels_that_made_reposts=%s' \
               'adres_img_for_channels_that_made_reposts=%s' \
               'channels_quoted_by_the_telegram_channel=%s' \
               'adres_img_for_channels_quoted_by_the_telegram_channel=%s)>' % (self.id,
                                                                               self.name,
                                                                               self.general_information_about_the_resource,
                                                                               self.adres_img_for_general_information_about_the_resource,
                                                                               self.date_of_resourc_creation,
                                                                               self.other_social_platforms,
                                                                               self.resource_content_date,
                                                                               self.publications_per_day,
                                                                               self.the_main_focus_of_the_channel,
                                                                               self.related_areas,
                                                                               self.channel_content,
                                                                               self.adres_img_for_views,
                                                                               self.contact_information_for_communication,
                                                                               self.adres_img_for_contact_information_for_communication,
                                                                               self.price_for_advertising_news,
                                                                               self.payment_is_made_by_card,
                                                                               self.name_administrator,
                                                                               self.adres_img_for_photo_admin,
                                                                               self.date_of_birth,
                                                                               self.place_of_birth,
                                                                               self.phone_number,
                                                                               self.passport,
                                                                               self.drivers_license,
                                                                               self.other,
                                                                               self.snifer,
                                                                               self.channel_partners,
                                                                               self.Channels_opponents,
                                                                               self.channels_that_made_reposts,
                                                                               self.adres_img_for_channels_that_made_reposts,
                                                                               self.channels_quoted_by_the_telegram_channel,
                                                                               self.adres_img_for_channels_quoted_by_the_telegram_channel
                                                                               )


def creat_all():
    db.create_all()
    db_users.create_all()

creat_all()



def get_our_dict(all_channels):
    stixs = []
    all = {}

    def check(el):
        try:
            return f'/static/images/{sanitize(el.name)}/{el.adres_img_for_photo_admin}' if f'{el.adres_img_for_photo_admin}' in os.listdir(
                f'{basedir}/static/images/{sanitize(el.name)}/') else '/static/imagebase/1535615_no-avatarku.jpg'
        except:
            return '/static/imagebase/1535615_no-avatarku.jpg'

    for el in all_channels:
        stixs.append(
            {'id': el.id,
             'name': el.name,
             'general_information_about_the_resource': el.general_information_about_the_resource,
             'adres_img_for_general_information_about_the_resource': f'/static/images/{sanitize(el.name)}/{el.adres_img_for_general_information_about_the_resource}',
             # el.adres_img_for_general_information_about_the_resource,
             'date_of_resourc_creation': el.date_of_resourc_creation,
             'other_social_platforms': el.other_social_platforms,
             'resource_content_date': el.resource_content_date,
             'publications_per_day': el.publications_per_day,
             'the_main_focus_of_the_channel': el.the_main_focus_of_the_channel,
             'related_areas': el.related_areas,
             'channel_content': el.channel_content,
             'adres_img_for_views': f'/static/images/{sanitize(el.name)}/{el.adres_img_for_views}',
             # el.adres_img_for_views,
             'contact_information_for_communication': el.contact_information_for_communication,
             'adres_img_for_contact_information_for_communication': f'/static/images/{sanitize(el.name)}/{el.adres_img_for_contact_information_for_communication}',
             'price_for_advertising_news': [e for e in el.price_for_advertising_news.split('\r\n') if e != ''],
             'payment_is_made_by_card': [e for e in el.payment_is_made_by_card.split('\r\n') if e != ''],
             'name_administrator': el.name_administrator,
             'adres_img_for_photo_admin': check(el),
             'date_of_birth': el.date_of_birth,
             'place_of_birth': el.place_of_birth,
             'phone_number': el.phone_number,
             'passport': el.passport,
             'drivers_license': el.drivers_license,
             'other': [e for e in el.other.split('\r\n') if e != ''],
             'snifer': [e for e in el.snifer.split('\r\n') if e != ''],
             'channel_partners': [e for e in el.channel_partners.split('\r\n') if e != ''],
             'Channels_opponents': [e for e in el.Channels_opponents.split('\r\n') if e != ''],
             'channels_that_made_reposts': [e for e in el.channels_that_made_reposts.split('\r\n') if e != ''],
             'adres_img_for_channels_that_made_reposts': f'/static/images/{sanitize(el.name)}/{el.adres_img_for_channels_that_made_reposts}',
             'channels_quoted_by_the_telegram_channel': [e for e in
                                                         el.channels_quoted_by_the_telegram_channel.split('\r\n') if
                                                         e != ''],
             'adres_img_for_channels_quoted_by_the_telegram_channel': f'/static/images/{sanitize(el.name)}/{el.adres_img_for_channels_quoted_by_the_telegram_channel}',
             })
        a = 0
        for el in stixs:
            a += 1
        all.update({f"channels{a}": el})
        print(all)
    return all


def delate_from_table(result, page):
    for el in result:
        b = Channels.query.filter_by(id=el)
        for file_name in b:
            try:
                shutil.rmtree(f'static/images/{sanitize(file_name.name)}/', ignore_errors=True)
            except:
                print("ERROR WHEN DELETING")
        Channels.query.filter_by(id=el).delete()
        db.session.commit()
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    all_channels = Channels.query.order_by(Channels.id)
    pages = all_channels.paginate(page=page, per_page=20)
    return pages


def save(f, result):
    print(result)
    try:
        filename = secure_filename(f.filename)
    except:
        return ''
    try:
        os.mkdir(f'static/images/{sanitize(result.getlist("name")[0])}/')
    except:
        pass
    try:
        f.save(f'static/images/{sanitize(result.getlist("name")[0])}/' + filename)
    except:
        print("ERROR SAVING")

    return filename


def add_in_channels(form):
    result = request.form
    channel = Channels(name=result.getlist('name')[0],
                       general_information_about_the_resource=result.getlist('general_information_about_the_resource')[
                           0],
                       adres_img_for_general_information_about_the_resource=
                       (save(form.adres_img_for_general_information_about_the_resource.data, result)),
                       # result.getlist('adres_img_for_general_information_about_the_resource')[0],
                       date_of_resourc_creation=result.getlist('date_of_resourc_creation')[0],
                       other_social_platforms=result.getlist('other_social_platforms')[0],
                       resource_content_date=result.getlist('resource_content_date')[0],
                       publications_per_day=result.getlist('publications_per_day')[0],
                       the_main_focus_of_the_channel=result.getlist('the_main_focus_of_the_channel')[0],
                       related_areas=result.getlist('related_areas')[0],
                       channel_content=result.getlist('channel_content')[0],
                       adres_img_for_views=save(form.adres_img_for_views.data, result),
                       # result.getlist('adres_img_for_views')[0],
                       contact_information_for_communication=result.getlist('contact_information_for_communication')[0],
                       adres_img_for_contact_information_for_communication=
                       save(form.adres_img_for_contact_information_for_communication.data, result),
                       # result.getlist('adres_img_for_contact_information_for_communication')[0],
                       price_for_advertising_news=result.getlist('price_for_advertising_news')[0],
                       payment_is_made_by_card=result.getlist('payment_is_made_by_card')[0],
                       name_administrator=result.getlist('name_administrator')[0],
                       adres_img_for_photo_admin=
                       save(form.adres_img_for_photo_admin.data, result),
                       # result.getlist('adres_img_for_photo_admin')[0],
                       date_of_birth=result.getlist('date_of_birth')[0],
                       place_of_birth=result.getlist('place_of_birth')[0],
                       phone_number=result.getlist('phone_number')[0],
                       passport=result.getlist('passport')[0],
                       drivers_license=result.getlist('drivers_license')[0],
                       other=result.getlist('other')[0],
                       snifer=result.getlist('snifer')[0],
                       channel_partners=result.getlist('channel_partners')[0],
                       Channels_opponents=result.getlist('Channels_opponents')[0],
                       channels_that_made_reposts=result.getlist('channels_that_made_reposts')[0],
                       adres_img_for_channels_that_made_reposts=
                       save(form.adres_img_for_channels_that_made_reposts.data, result),
                       # result.getlist('adres_img_for_channels_that_made_reposts')[0],
                       channels_quoted_by_the_telegram_channel=
                       result.getlist('channels_quoted_by_the_telegram_channel')[0],
                       adres_img_for_channels_quoted_by_the_telegram_channel=
                       save(form.adres_img_for_channels_quoted_by_the_telegram_channel.data, result),
                       # result.getlist('adres_img_for_channels_quoted_by_the_telegram_channel')[0]
                       )
    db.session.add_all([channel])
    db.session.commit()


def search_in_table(result):
    if Channels.query.filter_by(contact_information_for_communication=result.getlist('search')[0]).first():
        all_channels = Channels.query.filter_by(contact_information_for_communication=result.getlist('search')[0])
    else:
        all_channels = Channels.query.filter_by(name=result.getlist('search')[0])
    all_channel = get_our_dict(all_channels)
    return all_channel


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        result = request.form
        if result.getlist('delete') != ['']:
            return render_template('table.html', pages=delate_from_table(result, request.args.get('page')),
                                   page=request.args.get('page'))
    if request.method == 'GET':
        q = request.args.get('q')
        if q:
            all_channels = Channels.query.filter(Channels.name.contains(q) | Channels.name_administrator.contains(q))
        else:
            all_channels = Channels.query.order_by(Channels.id)
        page = request.args.get('page')
        if page and page.isdigit():
            page = int(page)
        else:
            page = 1
        pages = all_channels.paginate(page=page, per_page=20)
        return render_template('table.html', pages=pages)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_channel():
    form = SingUpForm()
    if form.validate_on_submit():
        try:
            add_in_channels(form)
            return redirect(url_for('home'))
        except:
            return render_template('AddChannel.html', form=form, statys="Записати не вийшло")
    else:
        return render_template('AddChannel.html', form=form)


@app.route('/channel/<int:id>')
@login_required
def get_channel(id):
    all_channels = Channels.query.filter_by(id=id).all()
    all_channel = get_our_dict(all_channels)
    return render_template('Chennel.html', all_channel=all_channel)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = request.form
    if request.method == 'POST':
        user = User.query.filter_by(login=form.getlist('inputEmail')[0]).first()
        if user is None or not user.check_password(form.getlist('inputPassword')[0]):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
