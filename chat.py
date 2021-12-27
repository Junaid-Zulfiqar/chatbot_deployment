import random
import json
import time
import torch
import datetime
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def msg_time():
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    seconds = datetime.datetime.now().second
    return (f'{hour}:{minute}:{seconds}')

with open('chatbot_dataset.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "matebot"

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                if intent["class"] == "4":
                    return f"{random.choice(intent['responses'])} \n for more information   <a href='https://invoicemate.net/blockchain-the-basics/'>More Info</a>", msg_time()
                elif intent["class"] == "5":
                    return f"{random.choice(intent['responses'])} \n for more information   <a href='https://invoicemate.net/what-is-invoice/'>More Info</a>", msg_time()
                elif intent["class"] == "6":
                    return f"{random.choice(intent['responses'])} \n for more information   <a href='https://invoicemate.net/understanding-defi/'>More Info</a>", msg_time()
                elif intent["class"] == "7":
                    return f"{random.choice(intent['responses'])} \n for more information   <a href='https://invoicemate.net/defi-invoice-financing-factoring/'>More Info</a>", msg_time()
                elif intent["class"] == "8":
                    return f"{random.choice(intent['responses'])} \n for more information   <a href='https://invoicemate.net/blockchain-and-the-challenges-of-traditional-invoice-automation/'>More Info</a>", msg_time()
                elif intent["class"] == "9":
                    return f"{random.choice(intent['responses'])} \n for more information   <a href='https://invoicemate.net/10-challanges-of-manual-invoice-processing/'>More Info</a>", msg_time()
                elif intent["class"] == "10":
                    return f"{random.choice(intent['responses'])} \n for more information  <a href='https://invoicemate.net/fintech-in-our-lives/'>More Info</a>", msg_time()
                elif intent["class"] == "11":
                    return f"{random.choice(intent['responses'])} \n for more information  <a href='https://invoicemate.net/eight-features-of-a-perfect-invoice-management-system/'>More Info</a>", msg_time()
                elif intent["class"] == "12":
                    return f"{random.choice(intent['responses'])} \n for more information  <a href='https://invoicemate.net/blockchain-the-fintech/'>More Info</a>", msg_time()
                elif intent["class"] == "13":
                    return f"{random.choice(intent['responses'])} \n for more information  <a href='https://invoicemate.net/accounts-receivable-the-primer-2/'>More Info</a>", msg_time()
                elif intent["class"] == "14":
                    return f"{random.choice(intent['responses'])} \n for more information  <a href='https://invoicemate.net/benefits/'>More Info</a>", msg_time()
                else:    
                    return f"{random.choice(intent['responses'])}", msg_time()
            # if tag == intent["tag"]:
            #     return random.choice(intent['responses'])
    
    return "I do not understand...", msg_time()


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)

