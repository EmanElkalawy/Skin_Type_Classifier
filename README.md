# Skin Type Classifier

A Python-based machine learning project to classify skin types using deep learning models.  
The project includes a Jupyter notebook, a saved model, and a Streamlit app for easy interaction.

## 🔍 Project Overview

This project allows users to:

- Predict skin type from an image.
- Easily run the model through a web interface using Streamlit.
- Explore the training process in the provided Jupyter notebook.


## 📥 Dataset

The dataset is **not included** in this repository due to size constraints.  
You can download it here:  
[Dataset Link](https://universe.roboflow.com/skins-aup8m/skin-type-l6qra/dataset/10)


## ⚙️ Setup Instructions

1. Clone this repository:

git clone https://github.com/YOUR_USERNAME/Skin-Type-Classifier.git
cd Skin-Type-Classifier
Install required packages:

pip install -r requirements.txt
🚀 Running the Streamlit App
Run the app locally using:

streamlit run app.py
Then open the provided local URL in your browser.


## 📝 How to Use

Open the Streamlit app.

Upload an image of the skin you want to classify.

The app will predict the skin type using the trained model.

## 📊 Model
The project uses a deep learning model (stored in saved_model/) trained on the provided dataset.

The notebook contains preprocessing, training, and evaluation steps.

## 💻 Dependencies
Some of the main Python packages used:

Python 3.8+

TensorFlow / PyTorch (depending on your model)

NumPy

Pandas

Streamlit

scikit-learn

Matplotlib / Seaborn

All dependencies are listed in requirements.txt.

## ⚠️ Notes
Make sure your dataset is organized according to the notebook instructions.

The saved model is compatible with the Streamlit app provided.

Large files are excluded from this repository; use the dataset link to download them.

## 📜 License
This project is open-source and free to use.
Feel free to contribute or modify it for educational purposes.
