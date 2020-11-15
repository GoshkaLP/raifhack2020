from flask import Blueprint, render_template, request

from .extensions.main_ext import MVP


node = Blueprint('node', __name__)
obj = MVP()


@node.route('/', methods=['GET'])
def route_home():
    return render_template('home.html', title='Заглавная страница')


@node.route('/adv_efficiency', methods=['GET', 'POST'])
def route_adv_efficiency():
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


@node.route('/sales_efficiency', methods=['GET'])
def route_sales_efficiency():
    conv_branch_all, conv_branch_nov = obj.get_conv_branch_all(), obj.get_conv_branch_nov()
    conv_professionals_all, conv_professionals_nov = obj.get_conv_professionals_all(), obj.get_conv_professionals_nov()
    return render_template('sales_efficiency.html', title='Анализ эффеективности продаж',
                           conv_branch_all=conv_branch_all,
                           conv_branch_nov=conv_branch_nov,
                           color1='#28a745' * (conv_branch_all < conv_branch_nov) + '#dc3545' * (
                                   conv_branch_all > conv_branch_nov),
                           fig1_type=int(conv_branch_all < conv_branch_nov),
                           conv_professionals_all=conv_professionals_all,
                           conv_professionals_nov=conv_professionals_nov,
                           color2='#28a745' * (conv_professionals_all < conv_professionals_nov) + '#dc3545' * (
                                       conv_professionals_all > conv_professionals_nov),
                           fig2_type=int(conv_professionals_all < conv_professionals_nov)
                           )
