from sentence_transformers import SentenceTransformer, util, InputExample, losses
from torch.utils.data import DataLoader
import random
import sys
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Load the data
print("Loading the data...", file=sys.stderr, flush=True)
data = dict()
current_poem = ""
with open("lm_data", 'r') as file:
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

# Load the model
print("Loading the model...", file=sys.stderr, flush=True)
model = SentenceTransformer('ufal/robeczech-base') # stsb-xlm-r-multilingual # ufal/robeczech-base # all-MiniLM-L6-v2 nomic-ai/nomic-embed-text-v1

# Generate training triplets
print("Generating training triplets...", file=sys.stderr)
training_triplets = []
authors = list(data.keys())
for i in range(100000):
    a1 = random.choice(authors)
    a2 = random.choice(authors)
    while a1 == a2:
        a2 = random.choice(authors)
    p1 = random.choice(data[a1])
    p2 = random.choice(data[a1])
    p3 = random.choice(data[a2])
    training_triplets.append(InputExample(texts=[p1,p2,p3]))
    #print([p1,p2,p3])

# Create a PyTorch dataloader and the train loss
train_dataloader = DataLoader(training_triplets, shuffle=True, batch_size=16)
#train_loss = losses.CosineSimilarityLoss(model)
train_loss = losses.TripletLoss(model=model)

# Finetune the model
print("Finetuning the model...", file=sys.stderr)
model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=1, warmup_steps=100)
model.save('robeczech-100000')

# Visualize data using T-SNE
embeddings = []

print("Computing T-SNE...", file=sys.stderr)

investigated_authors = ["Auředníček, Otakar", "Březina, Otokar", "Kollár, Jan", "Dyk, Viktor", "Erben, Karel Jaromír", "Neruda, Jan", "Mácha, Karel Hynek", "Zeyer, Julius", "Dostál-Lutinov, Karel", "Puchmajer, Antonín Jaroslav", "Hálek, Vítězslav", "Čelakovský, Ladislav"]

colors = ListedColormap(['r','g','b','c','m','y','k','greenyellow','orange','silver','gold','pink'])
values = []
labels = []

for i, author in enumerate(investigated_authors): 
    for poem in data[author]:
        emb = model.encode(poem)
        embeddings.append(emb)
        values.append(i)
        labels.append(author)

X = np.array(embeddings)
X_embedded = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=3).fit_transform(X)
dfx = X_embedded[:, 0]
dfy = X_embedded[:, 1]

fig, ax = plt.subplots()
scatter = ax.scatter(dfx, dfy, c=values, cmap=colors, s=2, label=labels)
ax.legend()
#legend = ax.legend(*scatter.legend_elements()[0], labels=investigated_authors)
plt.savefig('clusters_robeczech_10000triplets.png')




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

