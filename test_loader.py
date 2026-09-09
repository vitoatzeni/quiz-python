from loader import load_questions


questions = load_questions("questions.json")

print(f"Domande caricate: {len(questions)}")

for question in questions:
    print(question["id"])
    print(f"  Topic: {question['topic_id']}")
    print(f"  Subtopic: {question['subtopic_id']}")