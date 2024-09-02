import numpy as np
from gensim.models import Word2Vec
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# =====================================================================
# Input Data Preparation
# =====================================================================
# Sample data for features and labels
features = [
    {'word_count': 10, 'class_attribute': 'page-title',
        'text': 'KARRIERE BEI DER BMW GROUP'},
    {'word_count': 15, 'class_attribute': 'color-fg-default',
        'text': 'Discover your place in our world-changing work.'},
    {'word_count': 8, 'class_attribute': 'LC20lb MBeuO DKV0Md',
        'text': 'Solution Architect - Digital Manufacturing Center of Excellence (f/m/d)'},
    {'word_count': 12, 'class_attribute': 'css-19bg7qi',
        'text': 'Specific activities would include'},
]

labels = ['tagline', 'heroline', 'tagline', 'heroline']

# =====================================================================
# Create Features
# =====================================================================
# Convert class attributes and text to word vectors
class_attributes = [feature['class_attribute'] for feature in features]
text_data = [feature['text'] for feature in features]

# Load a pre-trained Word2Vec model
# (you need to download or train one)
word2vec_model = Word2Vec(sentences=[
                          class_attributes, text_data], vector_size=100, window=5, min_count=1, workers=4)


def features_to_vector(features, model):
    # Function to convert class attributes and text to a feature vector
    vectors = [np.concatenate([model.wv[feature['class_attribute']],
                              model.wv[feature['text']]]) for feature in features]
    return np.array(vectors)


# Convert features to word vectors
X = features_to_vector(features, word2vec_model)

# =====================================================================
# Train/Test split
# =====================================================================
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.25, random_state=42)

# =====================================================================
# Training
# =====================================================================
# Initialize and fit a classifier
classifier = RandomForestClassifier(random_state=42)
classifier.fit(X_train, y_train)
print("DONE Fitting")

# =====================================================================
# Eval
# =====================================================================
# Make predictions
y_pred = classifier.predict(X_test)
print(f"DONE PREDICTION: x={X_test}")
print(f"DONE PREDICTION: {y_pred}")

# Evaluate the accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
