import uuid
from flask import Flask, render_template, request, redirect, url_for, session
from loader import load_questions, get_categories
from quiz_engine import QuizEngine

app = Flask(__name__)
app.secret_key = "una_chiave_segreta_casuale_per_la_sessione"

# Dizionari in-memory per mantenere lo stato di sessione
active_engines = {}
active_feedback = {}

@app.route("/", methods=["GET", "POST"])
def index():
    categories = get_categories()
    current_category = session.get("category", "python")
    if "quiz_session_id" not in session:
        session["quiz_session_id"] = str(uuid.uuid4())

    session_id = session["quiz_session_id"]

    if session_id not in active_engines:
        category = session.get("category", "python")
        questions = load_questions(category)
        active_engines[session_id] = QuizEngine(questions)

    engine = active_engines[session_id]

    if request.method == "POST":
        selected_option = request.form.get("selected_option")
        
        # 1. Prendiamo la domanda CORRENTE *prima* che il motore avanzi
        current_q = engine.get_current_question()
        
        # 2. Inviamo la risposta al motore (questo incrementa l'indice)
        result = engine.submit_answer(selected_option)
        
        # 3. Troviamo il testo corrispondente all'ID della risposta corretta
        correct_text = ""
        for opt in current_q["options"]:
            if opt["id"] == result["correct"]:
                correct_text = opt["text"]
                break

        # 4. Salviamo il pacchetto di feedback per questa sessione
        active_feedback[session_id] = {
            "result": result,
            "question_text": current_q["question"],
            "correct_text": correct_text
        }
        
        return redirect(url_for("index"))

    # Se c'è un feedback in attesa per questa sessione, mostriamo la schermata di feedback
    if session_id in active_feedback:
        feedback_data = active_feedback[session_id]
        return render_template("index.html", feedback=feedback_data, question=None, categories=categories, current_category=current_category)

    # Altrimenti, mostriamo la domanda corrente del quiz
    current_q = engine.get_current_question()

    # Se non ci sono più domande, il quiz è terminato
    if current_q is None:
        score, total = engine.get_final_score()
        return render_template(
            "index.html",
            question=None,
            feedback=None,
            quiz_completed=True,
            score=score,
            total=total,
            categories=categories,
            current_category=current_category
        )

    return render_template("index.html", question=current_q, feedback=None, categories=categories, current_category=current_category)

@app.route("/select-category", methods=["POST"])
def select_category():
    category = request.form.get("category")

    print("Categoria ricevuta:", category)

    session["category"] = category

    session_id = session["quiz_session_id"]

    if session_id in active_engines:
        del active_engines[session_id]

    if session_id in active_feedback:
        del active_feedback[session_id]

    return redirect(url_for("index"))

@app.route("/next", methods=["POST"])
def next_question():
    session_id = session.get("quiz_session_id")
    # Puliamo il feedback così al prossimo GET / mostrerà la nuova domanda
    if session_id in active_feedback:
        del active_feedback[session_id]
    return redirect(url_for("index"))

@app.route("/restart", methods=["POST"])
def restart_quiz():
    session_id = session.get("quiz_session_id")

    # Rimuoviamo il motore e il feedback esistenti per questa sessione
    if session_id in active_engines:
        del active_engines[session_id]

    if session_id in active_feedback:
        del active_feedback[session_id]

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)