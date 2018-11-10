import os
from flask import Flask, jsonify, request
from datetime import datetime

from keras.models import load_model
import numpy as np
from keras.utils.np_utils import to_categorical

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "A nossa API está <span style='color: green; font-size: 30px'>online</span> em /api/"

@app.route('/predicao/', methods=['GET'])
def predicao():

    fid = open('./dataset/test.csv', 'r')
    lines = fid.readlines()
    fid.close()

    dataset = []

    for line in lines:
        new_line = line.rstrip('\n')
        new_line = new_line.replace(',','.')
        new_line = new_line.split(';')

        #!!# Converte o dataset para float
        # dataset.append(list( new_line ))
        dataset.append(list(map(float, new_line )))
        #!!#
    dataset = np.array(dataset)

    n_test_patterns = 1000

    # Divide o dataset em entradas (X) e saídas (Y)
    X = dataset[0:n_test_patterns, 0:18]
    Y = dataset[0:n_test_patterns, 18]

    # !!# Normaliza o dataset
    X = X / np.amax(X, axis=0)
    # !!#

    # !!# Categoriza as saídas
    Y = to_categorical(Y, 2)
    # !!#

    model = load_model('./modelo/model.h5')

    pred = model.predict(x=X, batch_size=1, verbose=0)

    n_correct = 0
    n_wrong = 0

    for i in range(len(pred)):
        y_pred = int(round(pred[i][0]))

        if y_pred == int(Y[i][0]):
            n_correct += 1
        else:
            n_wrong +=1

    acc = float(n_correct) / (n_correct + n_wrong) * 100

    return "Acc: " + str(acc)  + "%"

@app.route('/api/', methods=['POST'])
def api():
    if request.headers.get('Authorization') == 'Basic bWV1dXN1YXJpbzptaW5oYXNlbmhh':
        rq_body = request.get_json()

        if rq_body['result']['metadata']['intentName'] == 'Consultar_Hora':
            response = rq_body['result']['parameters']['date-time'][11:19]

            if response == '':
                response = datetime.now().strftime('%H:%M:%S')
                response = "Sem parametro " + response
            else:
                response = "Com parametro " + response

            return jsonify(
                {
                    "speech": "Falar " + response,
                    "displayText": "Mostrar " + response,
                    "data": {
                        "facebook": {
                            "text": "Facebook " + response
                        },
                        "slack": {
                            "text": "Slack " + response
                        },
                        "telegram": {
                            "text": "Telegram " + response
                        }
                    }
                }
            )

        negativeResponse = "nao entendi"
        return jsonify(
            {
                "speech": "Falar " + negativeResponse,
                "displayText": "Mostrar " + negativeResponse,
                "data": {
                    "facebook": {
                        "text": "Facebook " + negativeResponse
                    },
                    "slack": {
                        "text": "Slack " + negativeResponse
                    },
                    "telegram": {
                        "text": "Telegram " + negativeResponse
                    }
                }
            }
        )

    return jsonify(
        {
            "message": "Nao foi possivel te autenticar"
        }
    )


#
# Metodo de predição
#

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)