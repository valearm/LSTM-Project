# Import necessary libraries
from collections import Counter
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
from art import text2art
from tensorflow.keras import regularizers


# Function to print the introduction of the program
def start_print():
    print("============================================================")
    print("Created by: valearm")
    print("============================================================")

# Function to load data from a file and preprocess it
def load_data(x):

    # Load data from file, ignoring white spaces and accepting unlimited length numbers
    data = np.genfromtxt('data.txt', delimiter=',', dtype=int)
    # Replace all -1 values with 0
    data[data == -1] = 0
    # Split data into training and validation sets
    # train_data = data[:int(x*len(data))]
    train_data = data
    val_data = data[int(x*len(data)):]
    # val_data = data
    # Get the maximum value in the data
    max_value = np.max(data)
    return train_data, val_data, max_value

# Function to create the model
def create_model(num_features, max_value):
    # Create a sequential model
    model = keras.Sequential()
    # Add an Embedding layer, LSTM layer, and Dense layer to the model
    model.add(layers.Embedding(input_dim=max_value+1, output_dim=64))
    model.add(layers.LSTM(256))
    model.add(layers.Dense(num_features, activation='softmax'))

    # Compile the model with categorical crossentropy loss, adam optimizer, and accuracy metric
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Function to train the model
def train_model(model, train_data, val_data):
    # Fit the model on the training data and validate on the validation data for 100 epochs
    history = model.fit(train_data, train_data, validation_data=(val_data, val_data), epochs=100, verbose=0)

# Function to predict numbers using the trained model
def predict_numbers(model, val_data, num_features):
    # Predict on the validation data using the model
    predictions = model.predict(val_data)
    # Get the indices of the top 'num_features' predictions for each sample in validation data
    indices = np.argsort(predictions, axis=1)[:, -num_features:]
    # Get the predicted numbers using these indices from validation data
    predicted_numbers = np.take_along_axis(val_data, indices, axis=1)
    return predicted_numbers

# Function to print the predicted numbers
def print_predicted_numbers(predicted_numbers):
   # Print a separator line and "Predicted Numbers:"
   print("============================================================")
   print("Predicted Numbers:")
   # Print only the first row of predicted numbers
   print(', '.join(map(str, predicted_numbers[0])))

# Main function to run everything   
def main():
   
   # Print introduction of program 
   start_print()
   pred=[]

   for x in range(6,10):
        # Load and preprocess data 
        x = x * 0.1
        train_data, val_data, max_value = load_data(x)
        
        # Get number of features from training data 
        num_features = train_data.shape[1]
        
        # Create and compile model 
        model = create_model(num_features, max_value)
        
        # Train model 
        train_model(model, train_data, val_data)
        
        # Predict numbers using trained model 
        predicted_numbers = predict_numbers(model, val_data, num_features)

        prediction = [c.tolist() for c in predicted_numbers[:int(0.1*len(predicted_numbers))]] 
        
        # Print predicted numbers 
        print(f"Prediction with x={x}")
        print_predicted_numbers(predicted_numbers)

        flat_list = [item for sublist in prediction for item in sublist]
        counter = Counter(flat_list)
        print(f"Print dictionary {counter}")
   

# Run main function if this script is run directly (not imported as a module)
if __name__ == "__main__":
   main()
