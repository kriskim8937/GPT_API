from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    # Fetch texts from XCom
    from airflow.models import TaskInstance
    from airflow.utils.session import create_session

    dag_id = 'generate_text_dag'
    task_id = 'generate_texts'
    execution_date = datetime.now().date()

    with create_session() as session:
        ti = session.query(TaskInstance).filter(
            TaskInstance.dag_id == dag_id,
            TaskInstance.task_id == task_id,
            TaskInstance.execution_date == execution_date
        ).first()

        texts = ti.xcom_pull(key='generated_texts')
    
    return render_template('index.html', texts=texts)

@app.route('/select', methods=['POST'])
def select():
    selected_text = request.form['text']
    # Store the selected text to the database
    store_selected_text(selected_text)
    return "Text selected and stored!"

def store_selected_text(text):
    # Implement your database storage logic here
    pass

if __name__ == '__main__':
    app.run(debug=True)