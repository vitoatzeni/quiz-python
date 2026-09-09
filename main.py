from loader import load_questions
from quiz_engine import QuizEngine


def main():

    print("🎯 Avvio del quiz...\n")

    # Carica le domande
    try:
        questions = load_questions("questions.json")
    except ValueError as e:
        print(f"❌ Errore:\n{e}")
        return

    print(f"✅ Caricate {len(questions)} domande.\n")

    # Crea il motore
    engine = QuizEngine(questions)

    print("=" * 50)

    # Ciclo del quiz
    while engine.has_more_questions():

        question = engine.get_current_question()

        print(f"\n{question['question']}\n")

        for option in question["options"]:
            print(f"{option['id']}: {option['text']}")

        selected = input("\nRisposta: ").strip()

        result = engine.submit_answer(selected)

        if result["is_correct"]:
            print("✅ Corretto!")
        else:
            print("❌ Sbagliato!")
            print(f"Risposta corretta: {result['correct']}")

        print(f"💡 {result['explanation']}")

    # Risultato finale
    score, total = engine.get_final_score()

    print("\n" + "=" * 50)
    print(f"🏁 Quiz terminato: {score}/{total}")
    print("=" * 50)


if __name__ == "__main__":
    main()