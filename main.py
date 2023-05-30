import streamlit as st

from langchain import PromptTemplate
from langchain.llms import OpenAI


# Set the page configuration
st.set_page_config(page_title="PRO-EMAIL", page_icon=":robot:")

# Add a colorful header
st.title("PRO-EMAIL")
st.markdown("<h3 style='color: purple;'>A tool for improving your email</h3>", unsafe_allow_html=True)

# Add a colorful section with description
st.markdown("<h4 style='color: blue;'>Description:</h4>", unsafe_allow_html=True)
st.markdown("This is a tool for improving your email. Just write in your own words and see the magic.")
st.markdown("This tool will help you improve your email skills by converting your emails into a more professional format.")
st.markdown("This tool is powered by <a href='https://langchain.com/'>LangChain</a>.", unsafe_allow_html=True)

# Add an attractive image
st.image("TweetScreenshot.png", width=500, caption="Source: https://twitter.com/DannyRichman/status/1598254671591723008")

# Add a colorful section for user inputs
st.markdown("<h4 style='color: green;'>User Inputs:</h4>", unsafe_allow_html=True)

template = """
    Below is an email that may be poorly worded.
    Your goal is to:
    - Properly format the email
    - Convert the input text to a specified tone
    - Convert the input text to a specified dialect

    Here are some examples different Tones:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
    - Informal: Went to Barcelona for the weekend. Lots to tell you.  

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
    - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.

    Please start the email with a warm introduction. Add the introduction if you need to.
    
    Below is the email, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    EMAIL: {email}
    
    YOUR {dialect} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "email"],
    template=template,
)

def load_LLM(openai_api_key,temp):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=temp, openai_api_key=openai_api_key)
    return llm




st.markdown("### Describe your email in short words") 

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()
    
col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your email to have?',
        ('Formal', 'Informal'))
    
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))
    
# Add a slider for temperature input
temperature = st.slider("Temperature(For more Randomness)", min_value=0.5, max_value=0.7, step=0.1)



def get_text():
    input_text=st.text_area(label="",placeholder="Enter your thoughts..",key="email_input")
    return input_text
    
email_input = get_text()
 
 
if len(email_input.split(" ")) > 500:
    st.write("Please enter a shorter email. The maximum length is 500 words.")
    st.stop()
    
def update_text_with_example():
    print ("in updated")
    st.session_state.email_input = "Sally I am starts work at yours monday from dave"
    

st.button("*See An Example*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)


st.markdown('#### Your Converted Email :')    



if email_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key,temp=temperature)

    prompt_with_email = prompt.format(tone=option_tone, dialect=option_dialect, email=email_input)

    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)