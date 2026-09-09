import json


ALLOWED_TYPES = {
    "knowledge",
    "output",
    "debugging",
    "code_completion",
    "code_reading",
}

ALLOWED_LEVELS = {
    "beginner",
    "intermediate",
    "advanced",
}


def validate_questions_file(filepath):

    errors = []
    question_ids = set()

    # Legge il JSON
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        return [f"Errore nella lettura del file: {e}"]

    # Controllo radice
    if not isinstance(data, dict):
        return ["La radice del JSON deve essere un oggetto."]

    if data.get("version") != "1.0":
        errors.append("Manca 'version': '1.0' oppure la versione è errata.")

    topics = data.get("topics")

    if not isinstance(topics, list) or not topics:
        errors.append("'topics' deve essere una lista non vuota.")
        return errors

    # Topics
    for topic in topics:

        if not isinstance(topic, dict):
            errors.append("Un topic non è un oggetto.")
            continue

        for field in ["id", "title", "description", "subtopics"]:
            if field not in topic:
                errors.append(f"Manca il campo '{field}' nel topic.")

        subtopics = topic.get("subtopics")

        if not isinstance(subtopics, list):
            errors.append("'subtopics' deve essere una lista.")
            continue

        # Subtopics
        for subtopic in subtopics:

            if not isinstance(subtopic, dict):
                errors.append("Un subtopic non è un oggetto.")
                continue

            for field in ["id", "title", "levels"]:
                if field not in subtopic:
                    errors.append(f"Manca il campo '{field}' nel subtopic.")

            levels = subtopic.get("levels")

            if not isinstance(levels, dict):
                errors.append("'levels' deve essere un oggetto.")
                continue

            # Livelli
            for level in ALLOWED_LEVELS:

                if level not in levels:
                    errors.append(
                        f"Manca il livello '{level}' nel subtopic."
                    )
                    continue

                questions = levels[level]

                if not isinstance(questions, list):
                    errors.append(
                        f"Il livello '{level}' deve contenere una lista."
                    )
                    continue

                # Domande
                for question in questions:

                    if not isinstance(question, dict):
                        errors.append("Una domanda non è un oggetto.")
                        continue

                    required_fields = [
                        "id",
                        "question",
                        "type",
                        "difficulty",
                        "options",
                        "answer",
                        "explanation",
                        "tags",
                    ]

                    for field in required_fields:
                        if field not in question:
                            errors.append(
                                f"Manca il campo '{field}' nella domanda."
                            )

                    q_id = question.get("id")

                    # ID domanda
                    if q_id in question_ids:
                        errors.append(
                            f"ID domanda duplicato: '{q_id}'."
                        )
                    else:
                        question_ids.add(q_id)

                    # Tipo domanda
                    if question.get("type") not in ALLOWED_TYPES:
                        errors.append(
                            f"Tipo domanda non valido: "
                            f"'{question.get('type')}'."
                        )

                    # Difficoltà
                    difficulty = question.get("difficulty")

                    if (
                        isinstance(difficulty, bool)
                        or not isinstance(difficulty, int)
                        or not 1 <= difficulty <= 5
                    ):
                        errors.append(
                            f"Difficoltà non valida nella domanda '{q_id}'. "
                            "Deve essere un numero da 1 a 5."
                        )

                    # Opzioni
                    options = question.get("options", [])
                    option_ids = set()

                    if not isinstance(options, list) or len(options) < 2:
                        errors.append(
                            f"La domanda '{q_id}' deve avere almeno "
                            "2 opzioni."
                        )
                    else:
                        for option in options:

                            if not isinstance(option, dict):
                                errors.append(
                                    f"Opzione non valida nella domanda '{q_id}'."
                                )
                                continue

                            if "id" not in option or "text" not in option:
                                errors.append(
                                    f"Un'opzione della domanda '{q_id}' "
                                    "deve avere 'id' e 'text'."
                                )
                                continue

                            option_id = option["id"]

                            if option_id in option_ids:
                                errors.append(
                                    f"ID opzione duplicato nella domanda "
                                    f"'{q_id}': '{option_id}'."
                                )

                            option_ids.add(option_id)

                        # Risposta corretta
                        if question.get("answer") not in option_ids:
                            errors.append(
                                f"La risposta della domanda '{q_id}' "
                                "non corrisponde a nessuna opzione."
                            )

    return errors


if __name__ == "__main__":

    print("🔍 Avvio validazione di 'questions.json'...")

    errors = validate_questions_file("questions.json")

    if not errors:
        print("✅ VALIDAZIONE SUPERATA!")
        print("Il file JSON è valido.")
    else:
        print("❌ VALIDAZIONE FALLITA!")

        for error in errors:
            print(f"  - {error}")