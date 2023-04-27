from transformers import pipeline


model_name = "deepset/roberta-base-squad2"
qa_model = pipeline('question-answering', model=model_name, tokenizer=model_name) #pipeline("question-answering")
question = "do you have a battery?"
context = "I am not yet able to have feelings. However, I can tell what emotion you are feeling by watching your facial expressions with my cameras. I can also imitate your expression and, for example, use my LEDs to look sad if you are sad too. I have many different teachers! There are many girls and boys who work with me. Each of them is set on teaching me a different thing! We are in my my room. Here I play many games! I can also learn new things. I have a lot of toys and I can play with them. I can also play with you!It is not easy to transport me. I am precious and you have to be careful! More than one person accompanies me. Usually my trusted technician also comes, so that if something stops working he can fix me right away. I have a battery in my backpack, it lasts about 3 hours, depending on how many things you ask me to do! However, if I am in my lab I usually stay plugged in, so I can work for many hours in a row. As many as they teach me! If you give me the right dictionary I can learn Chinese overnight too! Actually my voice is artificial and the things I am telling you about I have tried before with my two colleagues! I happen to use English very often. Here at IIT there are people of all nationalities! My memory is super. These are the advantages of having a computer inside my head. My favorite color is red But I can match any color. I can also change my color in a few seconds! I was born on September 1st 2004, when the European project that led to my creation started!  My favorite game is treasure hunting. I like to talk to visitors coming from all over the world. I already have so many brothers and sisters! There are more than 40 of us all over the world!"

answer = qa_model(question = question, context = context)
## {'answer': 'İstanbul', 'end': 39, 'score': 0.953, 'start': 31}

if answer['score'] > 0.2:
    print(answer['answer'])
else:
    print("I'm not sure about the answer, it might be " + answer['answer'])
    print("Am I right?")
    # wait for user reply (yes or no), if no ask the correct answer and save it to the context

#TODO
# 1. Create a function that ask the user the correct answer to the question if the answer is wrong or the confidence is low.
