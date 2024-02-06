from flask import Flask, request, jsonify
from main import convo, query
app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    user_input = request.get_json()
    print(user_input)
    user_input = user_input["text"]
    output = query({
        "inputs": user_input,
    })

    output_label = output[0][0]["label"]

    query_not_address = ['audio', 'iot', 'email', 'music_settings', 'social_post', 'transport_taxi', 'takeaway_order',
                         'transport', 'datetime']

    found_keyword = False
    for keyword in query_not_address:
        if keyword in output_label.lower():
            found_keyword = True
            break

    if found_keyword:
        response = jsonify({"error": "The model cannot do the task"})
    else:
        convo.send_message(user_input)
        response = jsonify({"output": convo.last.text})

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')

    return response


if __name__ == '__main__':
    app.run(debug=True)