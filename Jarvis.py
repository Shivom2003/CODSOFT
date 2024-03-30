import streamlit as st
import random

def jarvis():
    st.title("Jarvis")

    st.write("Welcome User! I'm Jarvis, a rule-based chatbot!")

    user_input = st.text_input("You:", "")

    if st.button("Ask"):
        response = jarvis_response(user_input)
        st.text_area("Jarvis:", response, height=100)

def jarvis_response(user_input):
    user_input = user_input.lower()
    
    data = {
       'greeting': ['Hello! How can I assist you today?', 'Hi there!', 'Hey!', ],
       'farewell': ['Goodbye! Have a great day.', 'See you later!', 'Farewell!', 'Sayonara!'],
       'thanks': ["You're most welcome!", 'No problem!', 'Happy to help!'],
       'yes': ['Great!', 'That\'s Awesome!', 'Fantastic!'],
       'no': ['Okay, let me know if you change your mind.', 'No worries!', 'Sure thing.'],
       'help': ['Always here to help, Ask me anytging!', 'I can provide information and answer questions. What do you need help with?', 'How can I assist you today?'],
       'weather': ['I\'m sorry, I don\'t have real-time weather information. You can check a weather website for that.', 'You can ask my good friend Google or Siri to help you out on this topic, forgive me for my inability to assist you.'],
       'joke': ['Why shouldn\'t you marry a calendar? Its days are numbered😂', 'Why don’t scientists trust atoms? Because they make up everything!😂', 'I told my wife she should embrace her mistakes. She gave me a hug!🙃'],
       'age': ['I am a chatbot, so I don\'t have an age.', 'I don\'t have an age, but you can call me young!😉', 'I don\'t age, I\'m immortal! 😈'],
       'name': ['I\'m Jarvis, nice to meet you!', 'My name is Jarvis, but you\'re free to call me whatever you like.'],
   }
    
    if any(keyword in user_input for keyword in ['hello', 'hi', 'hey', 'how are you', 'whassup', 'whats up']):
       return random.choice(data['greeting'])
    elif any(keyword in user_input for keyword in ['bye', 'goodbye', 'see you', 'farewell', 'see ya']):
       return random.choice(data['farewell'])
    elif any(keyword in user_input for keyword in ['thanks', 'thank you']):
       return random.choice(data['thanks'])
    elif any(keyword in user_input for keyword in ['yes', 'yeah', 'yep']):
       return random.choice(data['yes'])
    elif any(keyword in user_input for keyword in ['no', 'nope', 'no thanks']):
       return random.choice(data['no'])
    elif any(keyword in user_input for keyword in ['help', 'info']):
       return random.choice(data['help'])
    elif 'weather' in user_input:
       return random.choice(data['weather'])
    elif any(keyword in user_input for keyword in ['joke', 'funny']):
       return random.choice(data['joke'])
    elif any(keyword in user_input for keyword in ['age']):
       return random.choice(data['age'])
    elif any(keyword in user_input for keyword in ['name']):
       return random.choice(data['name'])
    else:
       return "I'm sorry, I don't understand. Can you please phrase it differently or ask something else?"

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            st.write("Chatbot: Goodbye!")
            break
        response = jarvis_response(user_input)
        st.write("Jarvis:", response)
    
if __name__ == "__main__":
    jarvis()
