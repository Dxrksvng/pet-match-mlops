import gradio as gr
import requests
from loguru import logger
import os

env_BACKEND_URL = os.environ.get('BACKEND_URL', '127.0.0.1') # Adjust the default port if necessary
# URL for the backend FastAPI server
BACKEND_URL_1 = "http://"+env_BACKEND_URL+":8088/recommend"
BACKEND_URL_2 = "http://"+env_BACKEND_URL+":8088/chat"


def change_tab(id):
    return gr.Tabs(selected=id)
def clear_history():
    return [], []

# Function to send preferences to the backend
def get_pet_recommendation(preferences):
    try:
        response = requests.post(BACKEND_URL_1, json={"preferences": preferences})
        if response.status_code == 200:
            result = response.json()
            return result['recommendation']
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"
    
def get_chat_response(input_text, history):
    try:
        response = requests.post(BACKEND_URL_2, json={"input_text": input_text, "history": history})
        if response.status_code == 200:
            result = response.json()
            return result['history']
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"
    
# ---  Question and Answer Options ---
questions = [
    ("size", "อยากได้สัตว์เลี้ยงที่มีขนาดเป็นอย่างไร?"),
    ("playfulness", "คุณต้องการสัตว์เลี้ยงที่มีระดับความขี้เล่นระดับไหน?"),
    ("children friendly", "สัตว์เลี้ยงต้องเข้ากับเด็กได้หรือไม่?"),
    ("grooming", "คุณสามารถแปรงขนให้สัตว์เลี้ยงได้บ่อยแค่ไหน?"),
    ("intelligence", "คุณอยากได้สัตว์เลี้ยงที่ฉลาดประมาณไหน?"),
    ("other pets friendly", "ต้องสามารถอยู่ร่วมกับสัตว์เลี้ยงตัวอื่นของคุณได้หรือไม่?"),
    ("life span", "อยากได้สัตว์เลี้ยงที่มีอายุยืนเพียงไหน?"),
    ("exercise requirements", "คุณมีเวลาเล่นกับสัตว์เลี้ยงหรือพาสัตว์เลี้ยงไปเดินเล่นต่อวันมากเพียงใด?"),
    ("purchase price", "ราคาสัตว์เลี้ยงที่คุณสนใจต้องไม่เกินเท่าไหร่?"),
    ("barking", "คุณสามารถทนเสียงเห่าของสัตว์เลี้ยงได้มากน้อยเพียงใด?"),
]

question_options = [
    [("Skip", "ขนาดใดก็ได้"), ("Small", "ขนาดเล็ก"), ("Medium", "ขนาดกลาง"), ("Large-Giant", "ขนาดใหญ่")],
    [("Low", "ชอบให้สัตว์เลี้ยงอยู่ด้วยตัวมันเองได้"), ("Moderate", "ชอบให้มีเล่นบ้างเป็นบางเวลา"), ("High", "ชอบให้เล่นตลอดเวลา")],
    [("Skip", "ไม่จำเป็น"), ("Moderate-High", "จำเป็นต้องเข้ากับเด็กได้")],
    [("Low", "สัปดาห์ละครั้ง"), ("Moderate", "2-4 วันครั้ง"), ("High", "วันละครัั้ง")],
    [("Skip", "ไม่ได้สนใจความฉลาด"), ("Moderate", "ฉลาดแบบปกติทั่วไป"), ("High-Very High", "ต้องฉลาดมาก")],
    [("Skip", "ไม่จำเป็น"), ("High", "จำเป็นต้องอยู่ร่วมกับสัตว์เลี้ยงตัวอื่น")],
    [("Skip", "เท่าไหร่ก็ได้"), ("Short", "สั้น (5-8 ปี)"), ("Medium", "ปานกลาง (9-12 ปี)"), ("Long", "ยาว (13+ ปี)")],
    [("Low", "น้อยกว่า 1 ชม./วัน"), ("Moderate", "ประมาณ 1 ชม./วัน"), ("High", "มากกว่า 1.5 ชม./วัน")],
    [("Cheap", "น้อยกว่า 500 บาท"), ("Moderate", "500-1000 บาท"), ("Expensive", "มากกว่า 1000 บาท")],
    [("Skip", "ไม่ได้สนใจเรื่องการเห่า"), ("Low", "ไม่ชอบให้เห่า"), ("Moderate", "เห่าได้บ้าง")]
]
with gr.Blocks(css=""" 
    @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Varela+Round&display=swap');
    @import url('https://fonts.google.com/share?selection.family=Sarabun:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800');
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai+Looped:wght@100;200;300;400;500;600;700;800;900&family=Sarabun:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800&display=swap');
   .my-radio-btn {
    width: 100%;
    margin-bottom: 6px;
    font-size: 20px;
    padding: 6px;
    background-color: #ef9aa4;  /* เปลี่ยนสีพื้นหลังปุ่ม */
    color: white;
    border: none;
    border-radius: 32px;
    font-family: "Varela Round", sans-serif;
    font-weight: 700;
    letter-spacing: 1.3px;
    }
    .my-radio-btn:hover {
        background-color: #D2665A;  /* คงสีเมื่อ hover */
    }
    .my-radio-btn-start{width: 30%;
    margin-bottom: 6px;
    font-size: 20px;
    padding: 6px;
    background-color: #ef9aa4;  /* เปลี่ยนสีพื้นหลังปุ่ม */
    color: white;
    border: none;
    border-radius: 32px;
    font-family: "Varela Round", sans-serif;
    font-weight: 700;
    letter-spacing: 1.3px;
    display: block;  /* Makes the button a block element */
    margin-left: auto;  /* Centers the button horizontally */
    margin-right: auto;  /* Centers the button horizontally */
               
               }

.dropdown-container .gradio-dropdown .choice {
    padding: 12px;
    border: 2px solid #ef9aa4;  /* เปลี่ยนสีขอบของ dropdown */
    border-radius: 8px;
    background-color: white;
    color: #333;
    font-size: 16px;
    text-align: center;
    font-family: "Varela Round", sans-serif;
    font-weight: 600;
    cursor: pointer;
}

.dropdown-container .gradio-dropdown .choice:hover {
    background-color: #D2665A;
    color: white;
    font-family: "Noto Sans Thai Looped", sans-serif;
  font-weight: 200;
  font-style: normal;
}

/* เพิ่มพื้นที่ว่างด้านบนและพื้นหลังสีครีมอ่อน */
.gradio-container {
    padding-top: 50px;  /* เพิ่มพื้นที่ว่างด้านบน */

    background-color: #fff2d8;  /* ตั้งค่าสีพื้นหลังเป็นสีครีมอ่อน */
    font-family: "Noto Sans Thai Looped", sans-serif;
  font-weight: 200;
  font-style: normal;
}
#title {
        text-align: center;
        margin-top: -10;
        color: black;
        border: none;
        font-family: "Varela Round", sans-serif;
        font-weight: 900;
        font-size: 1em;
    }
.chatbot-container {
    font-family: "Noto Sans Thai Looped", sans-serif;
    font-weight: 400;
    font-style: normal;
    font-size: 16px;
    color: #333;
}
.chatbot-container .gradio-textbox, 
.chatbot-container .gradio-chatbot, 
.chatbot-container .gradio-radio          {
    font-family: "Noto Sans Thai Looped", sans-serif;
    font-weight: 400;
    font-style: normal;
}
.logo {
        background-color: #fff2d8;  /* Change this to the desired color */
    }
.logo img {
        width: 500px;  /* Set the width to a larger size */
        height: auto;   /* The height will scale proportionally */
    }
}
    
""") as demo:
    logger.info("Starting Demo...")

    with gr.Tabs() as tabs:
        with gr.TabItem("Main Page", id=0):  # First tab
            with gr.Row():
                gr.Markdown('<h1 style="font-size: 50px;">🐶 Pet Match 🐱</h1>', elem_id="title")
            with gr.Row():
                with gr.Column(scale=1):
                    logo = gr.Image(value=r"logo.gif", elem_classes="logo", show_label=False)
                    start_button = gr.Button("Start", elem_classes="my-radio-btn-start", variant= "primary-100 #ef9aa4")
                    start_button.click(change_tab, gr.Number(1, visible=False), tabs)  # Switch to the second tab (id=1)

        with gr.TabItem("Next Page", id=1):  # Second tab
            with gr.Row():
                gr.Markdown('<h1 style="font-size: 50px;">🐶 Find Your Perfect Pet 🐱</h1>', elem_id="title")
            with gr.Row():
                with gr.Column(scale=1):
                    logo = gr.Image(value=r"logo.gif", elem_classes="logo", scale=1, show_label=False)
                    mode_chatbot = gr.Button("Paws & Claws Chat", elem_classes="my-radio-btn", variant= "primary-100 #ef9aa4")
                    mode_qa = gr.Button("Match Your Pet", elem_classes="my-radio-btn", variant= "primary-100 #ef9aa4")
                    clear_btn = gr.Button("Clear History", elem_classes="my-radio-btn", variant= "secondary-300")

                with gr.Column(scale=3, elem_classes="chatbot-container"):
                    chatbot = gr.Chatbot(label="Pet Adoption Assistant", height=500, type='tuples')
                    state = gr.State([])  # Store chat history
                    state_choice = gr.State([]) 

                    txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter", container=False, elem_classes="chatbot-container")
                    qa_select = gr.Radio(choices=[i[1] for i in question_options[0]], label="Select an answer", visible=False)
                    current_question_index = gr.State(0)


    # --- Gradio Event Handlers (Modified to use RAG) ---

    def update_dropdown(index):
        if index < len(questions):
            return gr.update(choices=[i[1] for i in question_options[index]], visible=True)
        else:
            return gr.update(visible=False)


    async def handle_dropdown_select(selected_value, history, list_choice, index):
        selected_level = next((key for key, value in question_options[index] if value == selected_value), "Unknown")
        list_choice.append(selected_level)
        history.append((selected_value, None))  # Append user selection
        index += 1
        
        if index < len(questions):
            next_question = questions[index][1]
            history.append((None, next_question))
            return gr.update(choices=[i[1] for i in question_options[index]], visible=True), history, index, gr.update(visible=False)
        else:
            # All questions answered:  Summarize and suggest.  CRUCIAL CHANGE HERE
            history.append((None, "Generating pet suggestion...")) # Add a temporary message
            # Create a summary of the user's preferences
            join_qna = [list_choice[i]+" "+questions[i][0] for i in range(len(questions)) if list_choice[i] != "Skip"]
            user_preferences = ", ".join(join_qna)
            # Call the RAG chain with a summarizing prompt
            summary_prompt = f"Suggest a type and breeds of pet based on these preferences : {user_preferences}"
            recommendation = get_pet_recommendation(summary_prompt)
            formatted_answer = f"💓💗Recommended Breeds💗💓\n\n{recommendation}"  # Format the answer
            history[-1] = (None, formatted_answer)  # Replace the temporary message
            return gr.update(visible=False), history, index, gr.update(visible=True)


    def show_textbox(history):
        return gr.update(visible=True), [(None, "สวัสดีค่ะ! 😊 มีอะไรให้ช่วยไหมคะ? ถ้าคุณกำลังมองหาข้อมูลเกี่ยวกับสัตว์เลี้ยงหรือคำแนะนำใด ๆ ยินดีช่วยเสมอค่ะ 🐾💖")], gr.update(visible=False), [(None, "สวัสดีค่ะ! 😊 มีอะไรให้ช่วยไหมคะ? ถ้าคุณกำลังมองหาข้อมูลเกี่ยวกับสัตว์เลี้ยงหรือคำแนะนำใด ๆ ยินดีช่วยเสมอค่ะ 🐾💖")], []
    
    def show_qa_select(history):
        history=[(None, questions[0][1])]
        return gr.update(visible=False), history, gr.update(choices=[i[1] for i in question_options[0]], visible=True), [(None, questions[0][1])], 0, []    
    
    #Select Mode
    mode_chatbot.click(show_textbox, inputs=[state], outputs=[txt, chatbot, qa_select, state])
    mode_qa.click(show_qa_select, inputs=[state], outputs=[txt, chatbot, qa_select, state, current_question_index, state_choice])
    
    #QA Mode
    qa_select.change(handle_dropdown_select, inputs=[qa_select, state, state_choice, current_question_index],
                     outputs=[qa_select, chatbot, current_question_index, txt])
    #Chatbot Mode
    async def handle_textbox_input(input_text, history):
        if not input_text:
            return history, history, None
        else:
            if "i want" in input_text or "i need" in input_text or "i like" in input_text or "pets that" in input_text or "อยากได้" in input_text or "สัตว์เลี้ยงที่" in input_text:
                recommendation = get_pet_recommendation(input_text)
                formatted_answer = f"💓💗Recommended Breeds💗💓\n\n{recommendation}"  # Format the answer
                history.append((input_text, formatted_answer))
                return history, history, None
            else:
                response = get_chat_response(input_text, history)
                history.append((input_text, response))
                return history, history, None
                

    txt.submit(handle_textbox_input, inputs=[txt, state], outputs=[chatbot, state, txt])

    def clear_history():
        return [], [(None, "สวัสดีค่ะ! 😊 มีอะไรให้ช่วยไหมคะ? ถ้าคุณกำลังมองหาข้อมูลเกี่ยวกับสัตว์เลี้ยงหรือคำแนะนำใด ๆ ยินดีช่วยเสมอค่ะ 🐾💖")], [], 0, gr.update(value="", visible=True), gr.update(choices=[i[1] for i in question_options[0]], visible=False)

    clear_btn.click(clear_history, outputs=[state, chatbot, state_choice, current_question_index, txt,  qa_select])

demo.launch(server_name="0.0.0.0", server_port=7860)