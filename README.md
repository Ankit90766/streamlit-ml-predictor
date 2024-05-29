# Streamlit ML Predictor

This is a Streamlit web application that predicts multiple outputs based on user inputs from an Excel file using a pre-trained machine learning model.

## Features

- Load a pre-trained machine learning model
- Upload an Excel file with required input columns
- Make predictions based on the input data
- Display predictions and frequency counts with percentages
- Download predictions and frequency counts as an Excel file

## Requirements

- Python 3.x
- Streamlit
- pandas
- joblib
- openpyxl
- xlsxwriter

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/<your-username>/streamlit-ml-predictor.git
    ```

2. Install the required packages:
    ```sh
    pip install streamlit pandas joblib openpyxl xlsxwriter
    ```

3. Ensure you have your pre-trained model file named `random_forest_model.joblib` in the project directory.

## Usage

Run the Streamlit app:
```sh
streamlit run your_script_name.py
