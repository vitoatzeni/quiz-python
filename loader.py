import json
import os


def load_questions(category: str) -> list:
    """
    Carica le domande di una categoria dal relativo file JSON
    e le restituisce come lista piatta.
    """

    file_path = os.path.join("data", f"{category}.json")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    except FileNotFoundError:
        print(
            f"Errore: il file per la categoria '{category}' "
            f"non è stato trovato in {file_path}"
        )
        return []

    except json.JSONDecodeError:
        print(f"Errore: il file {file_path} non è un JSON valido.")
        return []

    questions = []

    for topic in data["topics"]:
        topic_id = topic["id"]

        for subtopic in topic["subtopics"]:
            subtopic_id = subtopic["id"]

            for level, level_questions in subtopic["levels"].items():

                for question in level_questions:

                    question["topic_id"] = topic_id
                    question["subtopic_id"] = subtopic_id

                    questions.append(question)

    return questions


def get_categories() -> list:
    """
    Cerca nella cartella data/ tutti i file JSON
    e restituisce i nomi delle categorie.
    """

    data_folder = "data"

    categories = []

    for filename in os.listdir(data_folder):

        if filename.endswith(".json"):

            category = filename[:-5]

            categories.append(category)

    return sorted(categories)