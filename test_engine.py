from quiz_engine import QuizEngine


domande_di_prova = [
    {
        "id": "test-01",
        "question": "Quanto fa 2 + 2?",
        "topic_id": "fundamentals",
        "subtopic_id": "basics",
        "options": [
            {"id": "opt_a", "text": "3"},
            {"id": "opt_b", "text": "4"}
        ],
        "answer": "opt_b",
        "explanation": "2 + 2 fa matematicamente 4."
    },
    {
        "id": "test-02",
        "question": "Python è un linguaggio compilato o interpretato?",
        "topic_id": "fundamentals",
        "subtopic_id": "basics",
        "options": [
            {"id": "opt_a", "text": "Compilato"},
            {"id": "opt_b", "text": "Interpretato"}
        ],
        "answer": "opt_b",
        "explanation": "Python viene eseguito tramite un interprete."
    }
]


def esegui_test_radiografia():

    print("🚀 Avvio test con radiografia dello stato (self)...\n")

    # 1. CREAZIONE DELL'OGGETTO
    engine = QuizEngine(domande_di_prova)

    print("📍 [CREAZIONE] Stato iniziale dell'istanza 'engine':")
    print(f"  - self.current_index = {engine.current_index}")
    print(f"  - self.score = {engine.score}")
    print(f"  - self.history = {engine.history}\n" + "-" * 50 + "\n")

    # 2. CICLO DELLE DOMANDE
    while engine.has_more_questions():

        q = engine.get_current_question()

        print(f"➡️ Domanda attiva (Indice corrente: {engine.current_index})")
        print(f"   Testo: {q['question']}")

        # Simuliamo la risposta dell'utente in base all'indice
        if engine.current_index == 0:

            scelta_utente = "opt_b"
            print("   👉 [SIMULAZIONE] L'utente sceglie: opt_b (Corretta)")

        else:

            scelta_utente = "opt_a"
            print("   👉 [SIMULAZIONE] L'utente sceglie: opt_a (Sbagliata)")

        # 3. CHIAMATA AL METODO SUBMIT_ANSWER
        risultato = engine.submit_answer(scelta_utente)

        print("\n   🔍 [STATO DOPO SUBMIT_ANSWER]")
        print(f"   Indice aggiornato: {engine.current_index}")
        print(f"   Punteggio aggiornato: {engine.score}")

        print(f"   History accumulata (lunghezza {len(engine.history)}):")

        for h_item in engine.history:

            print(
                f"     -> Domanda: {h_item['question_id']} | "
                f"Topic: {h_item['topic_id']} | "
                f"Subtopic: {h_item['subtopic_id']} | "
                f"Scelta: {h_item['selected']} | "
                f"Corretta?: {h_item['is_correct']}"
            )

        print("\n" + "-" * 50 + "\n")

    # 4. RISULTATO FINALE
    punti, totali = engine.get_final_score()

    print(
        f"🏁 Test completato con successo! "
        f"Punteggio finale: {punti}/{totali}"
    )
     # 5. STATISTICHE
    statistiche = engine.get_statistics()

    print("\n📊 STATISTICHE:")
    print(statistiche)

if __name__ == "__main__":
    esegui_test_radiografia()