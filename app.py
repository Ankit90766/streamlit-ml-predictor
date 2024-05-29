import streamlit as st
import pandas as pd
import joblib
from io import BytesIO

# Function to load the model
def load_model(model_filename):
    """Load a saved model from disk."""
    return joblib.load(model_filename)

# Function to make predictions
def make_predictions(model, input_df):
    """Make predictions using the loaded model and input dataframe."""
    predictions = model.predict(input_df)
    rounded_predictions = predictions.round().astype(int)
    return rounded_predictions

# Define the model filename
model_filename = 'random_forest_model.joblib'

# Load the model
try:
    model = load_model(model_filename)
except FileNotFoundError:
    st.error(f"Model file '{model_filename}' not found.")
    st.stop()

# Streamlit app interface
st.title("Multi-Output Prediction Model")

# File uploader for Excel files
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Read the uploaded file
        df = pd.read_excel(uploaded_file)

        # Define the input columns (make sure they match your model's training data)
        input_columns = [
            'Technology Acceptance',
            'Level of use of AI based tools',
            'Technology based Tutoring System',
            'Organisational Performance',
            'Student\'s Performance'
        ]

        # Check if all required columns are present
        if all(column in df.columns for column in input_columns):
            input_df = df[input_columns]

            # Make predictions
            predictions = make_predictions(model, input_df)

            # Define the output columns
            output_columns = [
                'Technology_Acceptance_Range',
                'Level_of_use_of_AI_based_tools_Range',
                'Technology_based_Tutoring_System_Range',
                'Organisational_Performance_Range',
                'Student\'s_Performance_Range'
            ]

            # Create a DataFrame for the predictions
            prediction_df = pd.DataFrame(predictions, columns=output_columns)

            # Concatenate the input data with the predictions
            result_df = pd.concat([df, prediction_df], axis=1)

            # Calculate frequency counts and percentages for each output column
            all_values = range(result_df[output_columns].min().min(), result_df[output_columns].max().max() + 1)
            frequency_combined_df = pd.DataFrame({'Value': all_values})

            for column in output_columns:
                frequency_counts = result_df[column].value_counts().reindex(all_values, fill_value=0)
                percentage_counts = (frequency_counts / frequency_counts.sum()) * 100
                frequency_combined_df[f'{column}_Frequency'] = frequency_counts.values
                frequency_combined_df[f'{column}_Percentage'] = percentage_counts.values

            # Display the result
            st.header("Predictions")
            st.write(result_df)

            # Display frequency counts with percentages
            st.header("Frequency Counts and Percentages")
            st.write(frequency_combined_df)

            # Option to download the result as an Excel file
            def to_excel(df, freq_combined_df):
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Predictions')
                    freq_combined_df.to_excel(writer, index=False, sheet_name='Frequency_Counts')
                processed_data = output.getvalue()
                return processed_data

            st.download_button(
                label="Download Predictions and Frequency Counts as Excel",
                data=to_excel(result_df, frequency_combined_df),
                file_name='predictions_and_frequency_counts.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            st.error("The uploaded file does not contain the required columns.")
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload an Excel file.")
