from sentence_transformers import SentenceTransformer, util, InputExample, losses
from torch.utils.data import DataLoader
import random
import sys
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from sklearn.neighbors import NearestNeighbors
import pickle


def load_anotated_poems_from_file(filename):
    data = dict()
    current_poem = ""
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("<|begin_of_text|>"):
                author = line[17:].split(":")[0]
            elif line.startswith("<|end_of_text|>"):
                if not author in data:
                    data[author] = [current_poem]
                else:
                    data[author].append(current_poem)
                current_poem = ""
            else:
                current_poem += line
    return data

def generate_training_triplets(data):
    training_triplets = []
    authors = list(data.keys())
    for i in range(10000):
        a1 = random.choice(authors)
        a2 = random.choice(authors)
        while a1 == a2:
            a2 = random.choice(authors)
        p1 = random.choice(data[a1])
        p2 = random.choice(data[a1])
        p3 = random.choice(data[a2])
        training_triplets.append(InputExample(texts=[p1,p2,p3]))
    return training_triplets

def get_embeddings_for_selected_authors(data, model, authors):
    embeddings = []
    values = []
    for i, author in enumerate(authors):
        if author in data:
            for poem in data[author]:
                emb = model.encode(poem)
                embeddings.append(emb)
                values.append(i)
    return np.array(embeddings), values


EXPERIMENT_NAME="robeczech-10k"

# Load the training data
print("Loading the training data...", file=sys.stderr, flush=True)
data = load_anotated_poems_from_file("lm_data")

# Load the test data
print("Loading the test data...", file=sys.stderr, flush=True)
test_data = load_anotated_poems_from_file("matka10000.txt")

# Load the model
print("Loading the model...", file=sys.stderr, flush=True)
model = SentenceTransformer('ufal/robeczech-base') # stsb-xlm-r-multilingual # ufal/robeczech-base # all-MiniLM-L6-v2 nomic-ai/nomic-embed-text-v1

# Generate training triplets
print("Generating training triplets...", file=sys.stderr)
training_triplets = generate_training_triplets(data)
train_dataloader = DataLoader(training_triplets, shuffle=True, batch_size=16)
train_loss = losses.TripletLoss(model=model) #train_loss = losses.CosineSimilarityLoss(model)

# Finetune the model
print("Finetuning the model...", file=sys.stderr)
model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=1, warmup_steps=100)
model.save(EXPERIMENT_NAME+'sbert.model')

# Get the embeddings for selected authors
authors = ["Auředníček, Otakar", "Březina, Otokar", "Kollár, Jan", "Dyk, Viktor", "Erben, Karel Jaromír", "Neruda, Jan", "Mácha, Karel Hynek", "Zeyer, Julius", "Dostál-Lutinov, Karel", "Puchmajer, Antonín Jaroslav", "Hálek, Vítězslav", "Čelakovský, Ladislav"]
colors = ['r','g','b','c','m','y','k','greenyellow','orange','silver','gold','pink']

print("Computing the embeddings...", file=sys.stderr, flush=True)
X, values = get_embeddings_for_selected_authors(data, model, authors)
X_test, values_test = get_embeddings_for_selected_authors(test_data, model, authors)

print("Training KNN model...", file=sys.stderr)
# Initialize the NearestNeighbors model
knn_model = NearestNeighbors(n_neighbors=5, metric='cosine')
# Fit the model to the data
knn_model.fit(X)

#Save the model
with open(EXPERIMENT_NAME+'_knn_model.pkl', 'wb') as file:
    pickle.dump(knn_model, file)
with open(EXPERIMENT_NAME+'_values.pkl', 'wb') as file:
    pickle.dump(values, file)

#Load the model
with open(EXPERIMENT_NAME+'_knn_model.pkl', 'rb') as file:
    knn_model = pickle.load(file)
with open(EXPERIMENT_NAME+'_values.pkl', 'rb') as file:
    values = pickle.load(file)


print("Predicting...", file=sys.stderr)
distances, indices = knn_model.kneighbors(X_test)
print(distances)
print(indices)
size, neighbors = distances.shape
print(size, neighbors)
for i in range(size):
    print ('Gold:', authors[values_test[i]]) 
    for j in range(neighbors):
        print ('   Predicted:', authors[values[indices[i,j]]], 'Distance:', distances[i,j])

exit()

# Computing T-SNE
print("Computing T-SNE...", file=sys.stderr)
X_embedded = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=3).fit_transform(X)
plt.figure(figsize=(15, 10))
i = 0
for j, author in enumerate(authors):
    aex = []
    aey = []
    for poem in data[author]:
        aex.append(X_embedded[i,0])
        aey.append(X_embedded[i,1])
        i += 1
    plt.scatter(aex, aey, color=colors[j], label=authors[j], s=2)

plt.legend(title="Authors", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout(rect=[0, 0, 0.75, 1])
plt.savefig(EXPERIMENT_NAME+'tsnee.png')



#train_examples = [InputExample(texts=['My first sentence', 'My second sentence', 'Unrelated sentence']),
#    InputExample(texts=['My first sentence', 'My second sentence' 'Unrelated sentence'])]
#train_loss = sentence_transformers.losses.TripletLoss(model=model)

#We get the embeddings by calling model.encode()
#emb1 = model.encode("This is a red cat with a hat.")
#emb2 = model.encode("Have you seen my red cat?")
#Get the cosine similarity score between sentences
#cos_sim = util.cos_sim(emb1, emb2)
#print("Cosine-Similarity:", cos_sim)

#Using Cosine SimilarityLoss
#Define your train examples. You need more than just two examples...
#Inputs are wrapped around InputExample class which the model expects
#train_examples = [InputExample(texts=['My first sentence', 'My second sentence'], label=0.8),
#    InputExample(texts=['Another pair', 'Unrelated sentence'], label=0.3)]


#data
#/net/projects/EduPo/tomas/lm_data
