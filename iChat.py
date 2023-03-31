from transformers import pipeline

qa_model = pipeline("question-answering")
question = "What's the weather like?"
context = "My name is Merve and I live in İstanbul."
answer = qa_model(question = question, context = context)
## {'answer': 'İstanbul', 'end': 39, 'score': 0.953, 'start': 31}

if answer['score'] > 0.7:
    print(answer['answer'])
else:
    print("I'm not sure about the answer, it might be " + answer['answer'])
    print("Am I right?")
    # wait for user reply (yes or no), if no ask the correct answer and save it to the context

#TODO
# 1. Create a function that ask the user the correct answer to the question if the answer is wrong or the confidence is low.
