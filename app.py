from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config.chat_config import ChatConfig
from config.database_config import DatabaseConfig
from src.chat_controller import ChatController
from src.db_controller import DatabaseController
from src.utils import Utility
from dotenv import load_dotenv
import uuid
import json
from datetime import datetime

load_dotenv(override=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///response.db"
db = SQLAlchemy(app)

class Response(db.Model):
    id = db.Column(db.String(30), primary_key=True)
    object = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    choice = db.Column(db.Text, nullable=False)
    usage = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

chat_config = ChatConfig()
database_config = DatabaseConfig()
chat_controller = ChatController(chat_config)
database_controller = DatabaseController(database_config)

@app.route("/", methods=['POST', 'GET'])
def index():
    query = ""
    results = []

    if request.method == 'POST':
        input_prompt = request.form.get("question", "").strip()
        try:
            prepare_messages = chat_controller.prepare_messages
            prepare_messages.append({
                "role": "user",
                "content": input_prompt
            })
            response = chat_controller.generate_sql_statement(prepare_messages).to_dict()
            new_response = Response(
                id=response['id'],
                object=response['object'],
                model=response['model'],
                choice=json.dumps(response.get("choices")[0]),
                usage=json.dumps(response['usage']),
                date_created=datetime.fromtimestamp(response['created'])
            )

            try:
                db.session.add(new_response)
                db.session.commit()
                return redirect(f"/?id={new_response.id}")
            
            except Exception as e:
                return str(e), 500
        
        except Exception as e:
            return str(e), 500

    else:
        response_id = request.args.get("id", "")
        response = Response.query.get(response_id)
        print(response)
        # print(json.loads(response.choice)['message']['content']) if response else None
        # query = Utility.clean_unexpected_message(json.loads(response.choice)['message']['content']) if response else ''
        query = json.loads(response.choice)['message']['content'] if response else ''
        # print(query)
        if query:
            try:
                results = database_controller.execute_query(query, include_cols=True) if query else []
                return render_template("index.html", query=query, results=results)
            except Exception as e:
                # flash(f"Query error: {str(e)}", "danger")
                results = []
                return render_template("index.html", query=query, error=e)
        else:
            return render_template("index.html", query=query, results=results)
        


if __name__ == "__main__":
    with app.app_context():
        if db.Model != Response():
            db.drop_all()
        db.create_all()
    app.run(debug=True)