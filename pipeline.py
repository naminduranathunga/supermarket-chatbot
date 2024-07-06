import chromadb, os
from gpt_models import generate_final_response
import random
import re
import math

"""
read our dataset
-- Embeddings are greate for search with meaning as it compaires the meaning of the input. No need to worry about missing words with similar meanings in the dataset.
Ex. chat understands "Greetings!" as "Hello!" and "Hi!"
"""
dataset_chats = []
dataset_products = []
# create a new database
db = chromadb.PersistentClient(path="./db")
collection_chats = db.get_or_create_collection('chats')
collection_products = db.get_or_create_collection('products')

def load_datasets():
    global dataset_chats, dataset_products
    with open('chatbot dataset.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().replace("\n", "")
            [question, answer] = line.split("\t")
            dataset_chats.append([question, answer])

    with open('products.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()
        # skip the first line
        lines = lines[1:]
        for line in lines:
            line = line.strip().replace("\n", "")
            [name, category, shelf_n] = line.split(",")
            dataset_products.append([name, category, shelf_n])


"""
Here we create embeddings for the dataset and store them in the database. Database is configuerd to store in local file system.
Once the embeddings are created, we can query the database for similar questions and get the answer.
"""
def create_embeddings_db():
    global collection_products, collection_chats
    ids = []
    docs = []
    for i in range(len(dataset_chats)):
        docs.append((dataset_chats[i][0]))
        ids.append(str(i))

    collection_chats.add(ids=ids, documents=docs)

    # adding product embeddings
    ids = []
    docs = []
    for i in range(len(dataset_products)):
        docs.append((f'{dataset_products[i][0]} ({dataset_products[i][1]})'))
        ids.append(str(i))
    
    collection_products.add(ids=ids, documents=docs)

def get_response_from_db(question, max_results=5, max_distance=0.95, temperature=0):
    response = collection_chats.query(
        query_texts=[question],
        n_results=max_results
    )
    ids = [int(x) for x in response['ids'][0]]
    dists = [float(x) for x in response['distances'][0]]

    if (len(ids) == 0 or dists[0] > max_distance):
        return "Sorry, I don't know the answer to that question. Please ask me something else."
    
    # select random id less than max_distance
    filtered_ids = []
    for i in range(len(ids)):
        if (dists[i] < max_distance):
            filtered_ids.append(ids[i])
    stop = math.floor(len(filtered_ids)*temperature)
    if (stop > 0):
        rand_index = random.randint(0, stop)
        return dataset_chats[filtered_ids[rand_index]][1]
    return dataset_chats[filtered_ids[0]][1]
    

def is_about_items(question):
    lowered = question.lower()
    special_phrases = [
        r"(i|we) (need|want)", 
        "looking for",
        "do you have", 
        "do you sell", 
        "do you have", 
        "do you offer", 
        "do you provide",  
        
    ]
    exceptional_phrases = [
        "some items",
        r"(need|want) items\s",
    ]

    # Let's do regex for better performance
    for phrase in special_phrases:
        if re.search(phrase, lowered):
            # check escape phrases present
            for e_phrase in exceptional_phrases:
                if re.search(e_phrase, lowered):
                    return False
            return True
    return False


def keywords_search(question, product):
    marks = 0
    w = product.split(" ")
    for word in w:
        if word in question:
            marks += 1
    return marks

def get_products_from_db(question):
    if (is_about_items(question) == False):
        return "", []
    
    max_distance=2
    response = collection_products.query(
        query_texts=[question],
        n_results=10
    )
    #print(response)
    products = []
    ids = [int(x) for x in response['ids'][0]]
    dists = [float(x) for x in response['distances'][0]]
    for i in range(len(ids)):
        if (dists[i] < max_distance):
            products.append(dataset_products[ids[i]])
    if (len(products) > 0):
        #print("Asistant: ", "I found the following items in the database:")
        out = "I found the following items in the database\n";
        n = 0
        related_products = []
        for i in range(len(products)):
            if (keywords_search(question, products[i][0]) < 1):
                continue
            out += (f"{n+1}. {products[i][0]} in {products[i][2]}\n")
            related_products.append(products[i])
            n += 1
        if (n == 0):
            out = "Sorry, I don't have that item in the database. Please ask me something else."
        print("Asistant: ", out)
        if (n > 0):
            return out, related_products
        else:
            return "", []
    return "", []

def generate_response(question):
    # if users asks for items in the database
    #context = is_about_items(question)
    #print(generate_final_response(question, context))
    #return;
    resp_products = get_products_from_db(question)
    if (resp_products == True):
        print(resp_products)
    else:
        print("Asistant: ", get_response_from_db(question))

def main():
    while True:
        question = input("You: ")
        generate_response(question)

def handle_request(question, model="gpt3.5x", temperature=1): #or gpt3.5
    resp_products, p = get_products_from_db(question)
    if (model == "gpt3.5"):
        context = resp_products
        if (context == ""):
            context = get_response_from_db(question, temperature=temperature)
        return generate_final_response(question, context), p
    
    if (resp_products != ""):
        return resp_products, p
    return get_response_from_db(question, temperature=temperature), p
    

if __name__ == "__main__":
    load_datasets()
    if (input("Do you want to process embeddings? (y/n)") == "y"):
        create_embeddings_db()
        print("Embeddings created successfully!")
    print("Ready to chat!")
    main()

