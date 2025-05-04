##Imports and Setup
import streamlit as st #streamlit: the web app framework.
import pandas as pd
import numpy as np
import altair as alt #altair: for plotting the prediction probabilities.
import joblib #joblib: to load the saved model.


#Load the Trained Model
pipe_lr = joblib.load(open("text_emotion_model.pkl", "rb")) #Loads a pre-trained pipeline (e.g., TfidfVectorizer + LogisticRegression) stored in text_emotion.pkl.
#pipe_lr = joblib.load(open("model/text_emotion.pkl", "rb"))

# Emojis Dictionary; Maps emotion labels to emojis for a more engaging UI.
emotions_emoji_dict = {"anger": "😠", "disgust": "🤮", "fear": "😨😱", "happy": "🤗", "joy": "😂", "neutral": "😐", "sad": "😔",
                       "sadness": "😔", "shame": "😳", "surprise": "😮"}


# Prediction Functions
def predict_emotions(docx):
    results = pipe_lr.predict([docx])
    return results[0]


def get_prediction_proba(docx):
    results = pipe_lr.predict_proba([docx])
    return results


# Main Streamlit Interface
def main():
    st.title("Text Emotion Detection")
    st.subheader("Detect Emotions In Text")
    # Input Form
    with st.form(key='my_form'):
        raw_text = st.text_area("Type Here")
        submit_text = st.form_submit_button(label='Submit')
    # Display Predictions
    if submit_text:
        col1, col2 = st.columns(2)

        prediction = predict_emotions(raw_text)
        probability = get_prediction_proba(raw_text)

        with col1:
            st.success("Original Text")
            st.write(raw_text)

            st.success("Prediction")
            emoji_icon = emotions_emoji_dict[prediction]
            st.write("{}:{}".format(prediction, emoji_icon))
            st.write("Confidence:{}".format(np.max(probability)))

        with col2:
            st.success("Prediction Probability")
            #st.write(probability)
            proba_df = pd.DataFrame(probability, columns=pipe_lr.classes_)
            #st.write(proba_df.T)
            proba_df_clean = proba_df.T.reset_index()
            proba_df_clean.columns = ["emotions", "probability"]

            fig = alt.Chart(proba_df_clean).mark_bar().encode(x='emotions', y='probability', color='emotions')
            st.altair_chart(fig, use_container_width=True)






if __name__ == '__main__':
    main()
