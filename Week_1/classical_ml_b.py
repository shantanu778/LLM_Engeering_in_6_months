import pandas as pd
from bnlp import BasicTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from transformers import AutoTokenizer, AutoModel
import torch
from tqdm import tqdm
import numpy as np
# 1. Load a Bangla BERT model

def visualize_word_closeness(x_train_tfidf, vectorizer):
     # 1. Transpose the matrix so rows = words, columns = sentences
    # .toarray() converts the sparse matrix into a normal numpy array
    word_vectors = x_train_tfidf.T.toarray()

    # 2. Get the actual Bangla words list matching the columns
    words = vectorizer.get_feature_names_out()

    # 3. Reduce dimensions from thousands down to 2 using PCA
    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(word_vectors)

    # 4. Create a clean DataFrame for plotting
    df_plot = pd.DataFrame({
        'word': words,
        'x': coords[:, 0],
        'y': coords[:, 1]
    })

    # 5. Plot the words
    plt.figure(figsize=(10, 8))
    plt.scatter(df_plot['x'], df_plot['y'], alpha=0.5, color='purple')

    # Annotate the points with the actual Bangla words
    # (Only plotting top 30 words so the graph isn't overcrowded)
    for i, row in df_plot.head(30).iterrows():
        plt.annotate(row['word'], (row['x'], row['y']), fontsize=12)

    plt.title("Visualizing Bangla Word Closeness using TF-IDF + PCA")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.grid(True)
    plt.show()
class TextProcessor:
    def __init__(self, df):
        self.df = df
        # bnlp টোকেনাইজার ইনিশিয়ালাইজ করুন
        self.bnlp_tokenizer = BasicTokenizer()
        self.preprocess()

    # কাস্টম টোকেনাইজেশন ফাংশন যা Scikit-learn গ্রহণ করবে
    def custom_tokenizer(self, text):
        return self.bnlp_tokenizer.tokenize(text)

    def preprocess(self):
        # Basic preprocessing steps
        self.df = self.df.dropna()  # Remove missing values
        self.df['text'] = self.df['text'].apply(self.custom_tokenizer)  # Convert to lowercase and tokenize
        print("Preprocessing completed. Sample tokenized text:")
        print(self.df['text'][0])

    def __getitem__(self, idx):
        text = self.df.iloc[idx]['text']
        label = self.df.iloc[idx]['label']
        return text, label

# def load_dataset(self, file_path):
    


if __name__ == "__main__":
    TF_IDF = False  # Set to False to use BERT embeddings instead of TF-IDF
    file_path = "BSMDD_v3_textcleaned - 21K.xlsx"  # Update with your dataset path
    df = pd.read_excel(file_path)
    print(f"Dataset loaded with {len(df)} records.")
    # print(" First 5 records:")
    # print(df.head())
    # processor = TextProcessor(df)

    X, y = df['text'], df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training set size: {len(X_train)} samples")
    print(f"Test set size: {len(X_test)} samples")

    if TF_IDF:

        # Custom token pattern to cleanly match Bangla script characters
        bangla_pattern = r"[\u0980-\u09FF]+"

        # Initialize TfidfVectorizer with the custom tokenizer and Bangla pattern
        vectorizer = TfidfVectorizer(tokenizer=BasicTokenizer().tokenize, token_pattern=bangla_pattern)
        X_train_tfidf = vectorizer.fit_transform(X_train)
        print(f"TF-IDF matrix shape: {X_train_tfidf.shape}")
        # Train a simple Logistic Regression model
        model = LogisticRegression(max_iter=1000, random_state=42)
        model.fit(X_train_tfidf, y_train)

        # Transform the test set and evaluate
        X_test_tfidf = vectorizer.transform(X_test)
        y_pred = model.predict(X_test_tfidf)
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        # TF-IDF matrix shape: (17528, 54612)
        # Classification Report:
        #             precision    recall  f1-score   support

        #         0       0.88      0.88      0.88      2186
        #         1       0.88      0.88      0.88      2196

        #  accuracy                           0.88      4382
        # macro avg       0.88      0.88      0.88      4382
        # weighted avg       0.88      0.88      0.88      4382
        # Accuracy: 0.8784

    else:
        device = torch.device("mps") if torch.mps.is_available() else torch.device("cpu")
        tokenizer = AutoTokenizer.from_pretrained("sagorsarker/bangla-bert-base")
        bert_model = AutoModel.from_pretrained("sagorsarker/bangla-bert-base").to(device)

        # 2. Tokenize and get embeddings (done in batches)
        inputs = tokenizer(X_train.tolist(), padding=True, truncation=True, max_length=512,return_tensors="pt")
        
        inputs = {key: value.to(bert_model.device) for key, value in inputs.items()}  # Move to the same device as the model
        print(f"Input shape: {inputs['input_ids'].shape}")  # Check the shape of the inputs

        batch_size = 32
        all_embeddings = []

        # Loop through the dataset in chunks
        for i in tqdm(range(0, len(X_train), batch_size)):
            # Slice out a mini-batch of token IDs and attention masks
            batch_input_ids = inputs['input_ids'][i : i + batch_size].to(device)
            batch_attention_mask = inputs['attention_mask'][i : i + batch_size].to(device)

            with torch.no_grad(): # Tell PyTorch not to track gradients (saves massive memory)
                outputs = bert_model(input_ids=batch_input_ids, attention_mask=batch_attention_mask)
                
                # Pull out the [CLS] token vector (index 0) for the whole batch
                # This represents the "sentence embedding"
                cls_embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
                
            all_embeddings.append(cls_embeddings)

        # MERGE STEP: Stack all batch arrays vertically into one giant matrix
        X_train_bert = np.vstack(all_embeddings)

        print(f"Final shape for Logistic Regression: {X_train_bert.shape} {y_train.shape} (should be [num_samples, 768])")
        # Train a simple Logistic Regression model
        model = LogisticRegression(max_iter=1000, random_state=42)
        model.fit(X_train_bert, y_train)  # Train on the first 100 samples for speed

        # Transform the test set and evaluate
        X_test_bert = tokenizer(X_test.to_list(), padding=True, truncation=True, max_length=512, return_tensors="pt").to(device)
        X_test_bert = {key: value.to(bert_model.device) for key, value in X_test_bert.items()}  # Move to the same device as the model
        test_embeddings = []
        for i in tqdm(range(0, len(X_test), batch_size)):
            batch_input_ids = X_test_bert['input_ids'][i : i + batch_size].to(device)
            batch_attention_mask = X_test_bert['attention_mask'][i : i + batch_size].to(device)

            with torch.no_grad():
                outputs = bert_model(input_ids=batch_input_ids,  attention_mask=batch_attention_mask)
                cls_embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
                test_embeddings.append(cls_embeddings)

        X_test_bert = np.vstack(test_embeddings)
        y_pred = model.predict(X_test_bert)
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        # Embeddings shape: (17528, 768)
        # Classification Report:
        #             precision    recall  f1-score   support

        #         0       0.85      0.83      0.84      2186
        #         1       0.83      0.85      0.84      2196

        #     accuracy                           0.84      4382
        # macro avg       0.84      0.84      0.84      4382
        # weighted avg       0.84      0.84      0.84      4382

        # Accuracy: 0.8389
            

    

   