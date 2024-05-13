from . import cursor, database


def add_prompt(sentence):
    cursor.execute(
        "INSERT INTO PromptSentence(sentence_text) VALUES(?)", (sentence,),
    )
    database.commit()
