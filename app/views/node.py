from flask import Blueprint, render_template, request

from .extensions.main_ext import AdvEfficiency


node = Blueprint('node', __name__)


@node.route('/', methods=['GET'])
def route_home():
    return render_template('home.html', title='Заглавная страница')


@node.route('/adv_efficiency', methods=['GET', 'POST'])
def route_adv_efficiency():
    obj = AdvEfficiency()
    if request.method == 'GET':
        return render_template('adv_efficiency.html', title='Рассчет эффективности рекламной компании',
                               theater_lovers=obj.get_theater_lovers(),
                               avid_theatergoers=obj.get_avid_theatergoers(),
                               warm_clients=obj.get_warm_clients(),
                               someone_who_might_love_theater=obj.get_someone_who_might_love_theater())
    elif request.method == 'POST':
        result_math_growth, result_math_conversion, result_math_income = None, None, None
        result_name = None
        form_result = request.form
        if form_result['radio_b'] == 'theater_lovers':
            result_math_growth, result_math_conversion, result_math_income = obj.get_math_theater_lovers()
            result_name = 'Любителей театров'
        elif form_result['radio_b'] == 'avid_theatergoers':
            result_math_growth, result_math_conversion, result_math_income = obj.get_math_avid_theatergoers()
            result_name = '"Заядлых театралов"'
        elif form_result['radio_b'] == 'warm_clients':
            result_math_growth, result_math_conversion, result_math_income = obj.get_math_warm_clients()
            result_name = '"Теплых" клиентов'
        elif form_result['radio_b'] == 'someone_who_might_love_theater':
            result_name = 'Тех, кто мог бы полюбить театр'
            result_math_growth, result_math_conversion, result_math_income = obj.get_math_someone_who_might_love_theater()
        return render_template('adv_efficiency.html', title='Рассчет эффективности рекламной компании',
                               theater_lovers=obj.get_theater_lovers(),
                               avid_theatergoers=obj.get_avid_theatergoers(),
                               warm_clients=obj.get_warm_clients(),
                               someone_who_might_love_theater=obj.get_someone_who_might_love_theater(),
                               result_name=result_name,
                               result_math_income=result_math_income,
                               result_math_growth=result_math_growth,
                               result_math_conversion=result_math_conversion)
