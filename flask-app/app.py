from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

@app.route('/')
def index():
    texts = ["text1", "text2", "text3"]
    return render_template_string('''
        <form action="/select" method="post">
            {% for text in texts %}
                <input type="radio" id="{{ text }}" name="selected_text" value="{{ text }}">
                <label for="{{ text }}">{{ text }}</label><br>
            {% endfor %}
            <input type="submit" value="Submit">
        </form>
    ''', texts=texts)

@app.route('/select', methods=['POST'])
def select():
    selected_text = request.form['selected_text']
    # Call an Airflow endpoint to update the database
    response = requests.post('http://airflow-webserver:8080/api/v1/dags/text_selection_dag/dag_runs', json={
        "conf": {"selected_text": selected_text}
    })
    return f"User selected: {selected_text}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)