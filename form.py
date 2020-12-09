from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField,PasswordField
from flask_wtf.file import FileField

class SingUpForm(FlaskForm):
    name = StringField('Название Telegram каналу')
    general_information_about_the_resource = StringField('Загальна інформація про ресурс:')
    adres_img_for_general_information_about_the_resource = FileField("Завантажити фото")
    date_of_resourc_creation = StringField('Дата створення ресурсу:')
    other_social_platforms = StringField('Інші соціальні площадки (Facebook, Vk.com, Instagram):')

    resource_content_date = StringField('Вміст ресурсу', render_kw={'placeholder': '16.6.2020'})
    publications_per_day = StringField()
    the_main_focus_of_the_channel = StringField(render_kw={'placeholder': 'музика та реклама'})
    related_areas = StringField()
    channel_content = StringField(render_kw={'placeholder': '2010 фото, 8 відео та 121 посилання'})
    adres_img_for_views = FileField("Завантажити фото")
    contact_information_for_communication = StringField()
    adres_img_for_contact_information_for_communication = FileField("Завантажити фото")

    price_for_advertising_news = TextAreaField('Прайс на розміщення реклами, новин:')
    payment_is_made_by_card = TextAreaField('Оплата здійснюється на карти:')

    name_administrator = StringField()
    adres_img_for_photo_admin = FileField("Завантажити фото")
    date_of_birth = StringField(render_kw={'placeholder': '15.07.1989р.'})
    place_of_birth = StringField()
    phone_number = StringField()
    passport = StringField()
    drivers_license = StringField()
    other = TextAreaField('Інше')

    snifer = TextAreaField()

    channel_partners = TextAreaField('Канали партнери:')
    Channels_opponents = TextAreaField('Противників ресурсу:')

    channels_that_made_reposts = TextAreaField('Канали, які робили репости:')
    adres_img_for_channels_that_made_reposts = FileField("Завантажити фото")
    channels_quoted_by_the_telegram_channel= TextAreaField('Канали, які цитує телеграм-канал:')
    adres_img_for_channels_quoted_by_the_telegram_channel = FileField("Завантажити фото")

    submit = SubmitField('Створити')


class Admin(FlaskForm):
    fio = StringField('ФІО')
    login = StringField('Введіть логін', render_kw={'placeholder': 'user@gmail.com'})
    password1 = PasswordField('Введіть пароль')
    password2 = PasswordField('Повторіть пароль')
    submit = SubmitField('Створити')
