class QuizEngine:
    def __init__(self, questions_list):
        """Inizializza il motore con una lista di domande validate."""
        self.questions = questions_list
        self.current_index = 0
        self.score = 0
        self.history = []

    def has_more_questions(self):
        """Restituisce True se ci sono ancora domande nel quiz."""
        return self.current_index < len(self.questions)

    def get_current_question(self):
        """Restituisce la domanda attiva in questo momento."""
        if not self.has_more_questions():
            return None
        return self.questions[self.current_index]

    def submit_answer(self, selected_option_id):
        """
        Verifica la risposta data dall'utente confrontando l'ID scelto
        con l'ID corretto della domanda.
        Registra il risultato e avanza l'indice.
        """
        current_q = self.get_current_question()

        if not current_q:
            return None

        correct_id = current_q["answer"]
        is_correct = selected_option_id == correct_id

        if is_correct:
            self.score += 1

        result_record = {
            "question_id": current_q["id"],
            "topic_id": current_q["topic_id"],
            "subtopic_id": current_q["subtopic_id"],
            "selected": selected_option_id,
            "correct": correct_id,
            "is_correct": is_correct,
            "explanation": current_q["explanation"]
        }

        self.history.append(result_record)

        self.current_index += 1

        return result_record

    def get_statistics(self):
        """
        Analizza la history e restituisce le statistiche
        raggruppate per topic e subtopic.
        """

        stats = {}

        for item in self.history:

            topic = item["topic_id"]
            subtopic = item["subtopic_id"]
            is_correct = item["is_correct"]

            # Crea il topic se non esiste
            if topic not in stats:
                stats[topic] = {}

            # Crea il subtopic se non esiste
            if subtopic not in stats[topic]:
                stats[topic][subtopic] = {
                    "correct": 0,
                    "wrong": 0,
                    "total": 0
                }

            # Aggiorna il contatore delle risposte
            if is_correct:
                stats[topic][subtopic]["correct"] += 1
            else:
                stats[topic][subtopic]["wrong"] += 1

            # Aggiorna il totale
            stats[topic][subtopic]["total"] += 1

        return stats

    def get_final_score(self):
        """Restituisce il punteggio finale e il totale delle domande."""
        return self.score, len(self.questions)