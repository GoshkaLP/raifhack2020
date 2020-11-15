from os import path, getcwd

import pandas as pd


class MVP:
    def __init__(self):
        self.datasets_path = path.join(getcwd(), 'datasets')
        self.clients_last_2_fixed = pd.read_csv(path.join(self.datasets_path,
                                                     'clients_last_2_fixed.csv'), sep=';')
        self.theater_potential_visitors = pd.read_csv(path.join(self.datasets_path,
                                                                'theater_potential_visitors.csv'), sep=';',
                                                      encoding='cp1251')
        self.theater_visitors = pd.read_csv(path.join(self.datasets_path, 'theater_visitors.csv'), sep=';',
                                            encoding='cp1251')
        self.theater_list = ['0XHKAX4 EA17EJ1 0XN-X994', '0XHKAX4 EA17EJ1 37KK7 4K',
                        '0XHKAX4 EA17EJ1 37KK7 DX', '"""0XHKAX4 EA17EJ1 X9 JL',
                        '0XHKAX4 EA17EJ1 X9 JL', '0XHKAX4 EA17EJ1 X9 JLK',
                        '0XHKAX4 EA17EJ1 X9 JLKK4', '"0XHKAX4 EA17EJ1 X9 JLKK4;V;CXKIXU;JLK;6SBB;SF',
                        '0XHKAX4 EA17EJ1 K7HXD', '0XHKAX4O', 'AEEW://0XHKAX4.JL', 'UUU.0XHKAX4.JL']

    def get_warm_clients(self):
        grand_theatre_visitors = self.theater_visitors[
            self.theater_visitors['mrchname'].isin(self.theater_list)
        ]

        grand_theatre_grouped = grand_theatre_visitors.groupby('cnum')['purchdate'] \
            .count().to_frame('count').reset_index()

        grand_theatre_result = grand_theatre_grouped[grand_theatre_grouped['count'] == 1]

        # Должно вернуть 1089
        return grand_theatre_result['cnum'].count()

    def get_avid_theatergoers(self):
        theater_visitors_grouped = self.theater_visitors.groupby('cnum')['purchdate'] \
            .count().to_frame('count').reset_index()

        theater_visitors_result = theater_visitors_grouped[theater_visitors_grouped['count'] > 1]

        grand_theatre_visitors = self.theater_visitors[
            self.theater_visitors['mrchname'].isin(self.theater_list)
        ]

        grand_theatre_grouped = grand_theatre_visitors.groupby('cnum')['purchdate'] \
            .count().to_frame('count').reset_index()

        grand_theatre_result = grand_theatre_grouped[grand_theatre_grouped['count'] > 1]

        result_avid_theatergoers = theater_visitors_result[
            ~theater_visitors_result['cnum'].isin(grand_theatre_result['cnum'])
        ]

        # Должно вернуть 38509
        return result_avid_theatergoers['cnum'].count()

    def get_theater_lovers(self):
        grand_theatre_visitors = self.theater_visitors[
            self.theater_visitors['mrchname'].isin(self.theater_list)
        ]

        result_theater_lovers = self.theater_visitors[
            ~self.theater_visitors['cnum'].isin(grand_theatre_visitors['cnum'])
        ]

        # Должно вернуть 101248
        return result_theater_lovers['cnum'].drop_duplicates().count()

    def get_someone_who_might_love_theater(self):
        potential_visitors = self.theater_potential_visitors[
            ~self.theater_potential_visitors['cnum'].isin(self.theater_visitors['cnum'])
        ]

        potential_clients = self.clients_last_2_fixed[
            self.clients_last_2_fixed['cnum_'].isin(potential_visitors['cnum'])
        ]

        result_potential_clients = potential_clients[
            ((potential_clients['gender'] == 'F') &
             (potential_clients['age'] >= 32) &
             (potential_clients['age'] <= 52)) |
            (potential_clients['gender'] == 'M') &
            (potential_clients['age'] >= 35) &
            (potential_clients['age'] <= 55)
            ]

        # Должно вернуть 94425
        return result_potential_clients['cnum_'].drop_duplicates().count()

    def get_math_warm_clients(self):
        warm_clients_counts = self.get_warm_clients()

        grand_theatre_visitors = self.theater_visitors[
            self.theater_visitors['mrchname'].isin(self.theater_list)
        ]

        grand_theatre_grouped = grand_theatre_visitors.groupby('cnum')['purchdate'] \
            .count().to_frame('count').reset_index()

        grand_theatre_result_1 = grand_theatre_grouped[grand_theatre_grouped['count'] >= 1]['cnum'].count()
        grand_theatre_result_2 = grand_theatre_grouped[grand_theatre_grouped['count'] > 2]['cnum'].count()

        result_math_growth = grand_theatre_result_2 / grand_theatre_result_1 * warm_clients_counts
        result_math_growth = int(result_math_growth)

        result_math_conversion = round(grand_theatre_result_2 / grand_theatre_result_1, 4) * 100

        result_math_income = round((grand_theatre_visitors['amount'].mean() * 0.8) * result_math_growth, 2)

        return result_math_growth, result_math_conversion, result_math_income

    def get_math_avid_theatergoers(self):
        avid_theatergoers_counts = self.get_avid_theatergoers()

        theater_visitors_grouped = self.theater_visitors.groupby('cnum')['purchdate'] \
            .count().to_frame('count').reset_index()

        theater_visitors_result = theater_visitors_grouped[theater_visitors_grouped['count'] >= 3]['cnum'].count()

        grand_theatre_visitors = self.theater_visitors[
            self.theater_visitors['mrchname'].isin(self.theater_list)
        ]

        grand_theatre_grouped = grand_theatre_visitors.groupby('cnum')['purchdate'] \
            .count().to_frame('count').reset_index()

        grand_theatre_result_2 = grand_theatre_grouped[grand_theatre_grouped['count'] >= 2]['cnum'].count()

        result_math_growth = grand_theatre_result_2 / theater_visitors_result * avid_theatergoers_counts
        result_math_growth = int(result_math_growth)

        result_math_conversion = round(grand_theatre_result_2 / theater_visitors_result, 4) * 100

        result_math_income = round((grand_theatre_visitors['amount'].mean() * 0.8) * result_math_growth, 2)

        return result_math_growth, result_math_conversion, result_math_income

    def get_math_theater_lovers(self):
        theater_lovers_counts = self.get_theater_lovers()

        theater_visitors_grouped = self.theater_visitors.groupby('cnum')['purchdate'] \
            .count().to_frame('count').reset_index()

        theater_visitors_result = theater_visitors_grouped[theater_visitors_grouped['count'] >= 1]['cnum'].count()

        grand_theatre_visitors = self.theater_visitors[
            self.theater_visitors['mrchname'].isin(self.theater_list)
        ]

        grand_theatre_grouped = grand_theatre_visitors.groupby('cnum')['purchdate'] \
            .count().to_frame('count').reset_index()

        grand_theatre_result_2 = grand_theatre_grouped[grand_theatre_grouped['count'] > 1]['cnum'].count()

        result_math_growth = grand_theatre_result_2 / theater_visitors_result * theater_lovers_counts
        result_math_growth = int(result_math_growth)

        result_math_conversion = round(grand_theatre_result_2 / theater_visitors_result, 4) * 100

        result_math_income = round((grand_theatre_visitors['amount'].mean() * 0.8) * result_math_growth, 2)

        return result_math_growth, result_math_conversion, result_math_income

    def get_math_someone_who_might_love_theater(self):
        someone_who_might_love_theater_counts = self.get_someone_who_might_love_theater()

        theater_visitors_grouped = self.theater_visitors.groupby('cnum')['purchdate'] \
            .count().to_frame('count').reset_index()

        theater_visitors_result = theater_visitors_grouped[theater_visitors_grouped['count'] >= 1]['cnum'].count()


        grand_theatre_visitors = self.theater_visitors[
            self.theater_visitors['mrchname'].isin(self.theater_list)
        ]

        grand_theatre_grouped = grand_theatre_visitors.groupby('cnum')['purchdate'] \
            .count().to_frame('count').reset_index()

        grand_theatre_result_2 = grand_theatre_grouped[grand_theatre_grouped['count'] > 1]['cnum'].count()

        result_math_growth = grand_theatre_result_2 / theater_visitors_result * someone_who_might_love_theater_counts
        result_math_growth = int(result_math_growth)

        result_math_conversion = round(grand_theatre_result_2 / theater_visitors_result, 4) * 100

        result_math_income = round((grand_theatre_visitors['amount'].mean() * 0.8) * result_math_growth, 2)

        return result_math_growth, result_math_conversion, result_math_income

    def get_conv_branch_all(self):
        theater_visitors_grouped = self.theater_visitors.groupby('cnum')['purchdate'] \
            .count().to_frame('count').reset_index()

        grand_theatre_visitors = self.theater_visitors[
            self.theater_visitors['mrchname'].isin(self.theater_list)
        ]

        grand_theatre_grouped = grand_theatre_visitors.groupby('cnum')['purchdate'] \
            .count().to_frame('count').reset_index()

        conv_branch_all = grand_theatre_grouped['cnum'].count() / theater_visitors_grouped['cnum'].count()
        conv_branch_all = round(round(conv_branch_all, 3) * 100, 1)

        return conv_branch_all

    def get_conv_branch_nov(self):
        self.theater_visitors['purchdate'] = pd.to_datetime(self.theater_visitors['purchdate'], format='%Y-%m-%d %H:%M:%S')

        date_start = pd.to_datetime('2019-11-01 00:00:00', format='%Y-%m-%d %H:%M:%S')
        date_end = pd.to_datetime('2019-11-30 00:00:00', format='%Y-%m-%d %H:%M:%S')

        theater_visitors = self.theater_visitors[
            (self.theater_visitors['purchdate'] >= date_start) &
            (self.theater_visitors['purchdate'] <= date_end)
            ]

        theater_visitors_grouped = theater_visitors.groupby('cnum')['purchdate'] \
            .count().to_frame('count').reset_index()

        grand_theatre_visitors = theater_visitors[
            theater_visitors['mrchname'].isin(self.theater_list)
        ]

        grand_theatre_grouped = grand_theatre_visitors.groupby('cnum')['purchdate'] \
            .count().to_frame('count').reset_index()

        conv_branch_all = grand_theatre_grouped['cnum'].count() / theater_visitors_grouped['cnum'].count()
        conv_branch_all = round(round(conv_branch_all, 3) * 100, 1)

        return conv_branch_all

    def get_conv_professionals_all(self):
        theater_visitors_grouped = self.theater_visitors.groupby('cnum')['purchdate'] \
            .count().to_frame('count').reset_index()

        theater_visitors_grouped = theater_visitors_grouped[
            theater_visitors_grouped['count'] > 2
            ]

        grand_theatre_visitors = self.theater_visitors[
            self.theater_visitors['mrchname'].isin(self.theater_list)
        ]

        grand_theatre_grouped = grand_theatre_visitors.groupby('cnum')['purchdate'] \
            .count().to_frame('count').reset_index()

        grand_theatre_grouped = grand_theatre_grouped[
            grand_theatre_grouped['count'] > 2
            ]

        conv_branch_all = grand_theatre_grouped['cnum'].count() / theater_visitors_grouped['cnum'].count()
        conv_branch_all = round(round(conv_branch_all, 3) * 100, 1)

        return conv_branch_all

    def get_conv_professionals_nov(self):
        self.theater_visitors['purchdate'] = pd.to_datetime(self.theater_visitors['purchdate'], format='%Y-%m-%d %H:%M:%S')

        date_start = pd.to_datetime('2019-11-01 00:00:00', format='%Y-%m-%d %H:%M:%S')
        date_end = pd.to_datetime('2019-11-30 00:00:00', format='%Y-%m-%d %H:%M:%S')

        theater_visitors = self.theater_visitors[
            (self.theater_visitors['purchdate'] >= date_start) &
            (self.theater_visitors['purchdate'] <= date_end)
            ]

        theater_visitors_grouped = theater_visitors.groupby('cnum')['purchdate'] \
            .count().to_frame('count').reset_index()

        theater_visitors_grouped = theater_visitors_grouped[
            theater_visitors_grouped['count'] > 2
            ]

        grand_theatre_visitors = theater_visitors[
            theater_visitors['mrchname'].isin(self.theater_list)
        ]

        grand_theatre_grouped = grand_theatre_visitors.groupby('cnum')['purchdate'] \
            .count().to_frame('count').reset_index()

        grand_theatre_grouped = grand_theatre_grouped[
            grand_theatre_grouped['count'] > 2
            ]

        conv_branch_all = grand_theatre_grouped['cnum'].count() / theater_visitors_grouped['cnum'].count()
        conv_branch_all = round(round(conv_branch_all, 3) * 100, 1)

        return conv_branch_all
