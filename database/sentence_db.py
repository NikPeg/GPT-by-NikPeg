from . import cursor, database


def add_sentence(sentence):
    cursor.execute(
        "INSERT INTO PromptSentence(sentence_text) VALUES(?)", (sentence,),
    )
    database.commit()


def random_sentence():
    cursor.execute("SELECT sentence_text FROM PromptSentence ORDER BY RANDOM() LIMIT 1;")
    return cursor.fetchone()[0]
