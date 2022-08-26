# import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import pandas as pd
import numpy as np
from random import choice

import warnings

warnings.filterwarnings('ignore')

# read DATA_CORRELATION data
df = pd.read_csv('DATA_CORR.csv', index_col=['Unnamed: 0'])

# read KODE_PRODUK data
df2 = pd.read_csv('Kode_produk.csv')


def execute(produk, data):
    recomend_n = []
    for i in data:
        if i != produk:
            i = i.split('_')[1]
            recomend_n.append(i)
    return recomend_n


def random_choice(condition, data):
    list = []
    for i in range(condition):
        n_rekomendasi_lain = choice(data)
        list.append(n_rekomendasi_lain)
    return list


class Test(Resource):
    def post(self):
        try:
            x = request.json['product']
            text = 'Produk_' + x

            if len(df[df.columns == text]) != 0:
                product_recomend = df[df[text] > 0][[text]].head(10).index
                recomend_lain = df2['produk'].values

                recomend_sementara = execute(text, product_recomend)

                n_recomend = 10
                condition = n_recomend - len(recomend_sementara)

                if condition > 0:
                    list_rekomendasi_lain = random_choice(
                        condition, recomend_lain)
                    recomend = np.concatenate(
                        recomend_sementara, list_rekomendasi_lain)

                else:
                    recomend = recomend_sementara

                result = recomend
                return {'value': result}

            else:
                recomend_lain = df2['produk'].values
                condition = 10

                recomend = random_choice(condition, recomend_lain)

                result = recomend
                return {'values': result}

        except:
            result = 'Terdapat Kesalahan'
            return {'value': result}


# inisiasi objeck flask
app = Flask(__name__)

# inisasi object flask_restful
api = Api(app)

# inisiasi object flask_cors
CORS(app)

# setup resource
api.add_resource(Test, "/api/predict", methods=["GET", "POST"])

# if __name__ == "__main__":
#     app.run()
