from customtkinter import *
from PIL import Image, ImageTk, ImageSequence
from tkinter import messagebox
import warnings
import pyautogui as pag
from voice.TTS import text_to_speech
from voice.STT import SpeechToTextListener
from brain.basicLogic import process_query
import threading

warnings.simplefilter("ignore")

root = CTk()
root.title("JARVIS")
root.attributes('-fullscreen', True)
root.state('zoomed')
root.resizable(width=False, height=False)
frame = CTkFrame(master=root, fg_color='black', corner_radius=0)
frame.pack(fill=BOTH, expand=True)

# jarvis = Chatbot()
original_y_position = None

# --------------------------------------------------------------------- #

def closeApp():
    x = messagebox.askokcancel(title='Closing Jarvis', message='This will close jarvis. Do you want to close it?')
    if x:
        root.destroy()
    else:
        pass

def update_chat_log(message):
    current_text = chat_log.cget("text")
    new_text = current_text + message
    chat_log.configure(text=new_text)

# Initializing STT
mic = SpeechToTextListener(language='en-IN') # hi-IN, zh-CN , en-US hi-IN en-IN en-US en-GB en-AU

listening = False

def micOnOff():
    global listening, original_y_position

    if micButton.cget('image') == micOffImg:
        micButton.configure(image=micImg)
        listening = True

        def threaded_function():
            global listening

            while listening:
                try:
                    audio = mic.listen()

                    if len(audio) == 0:
                        text_to_speech(text="Sorry, I didn't get that. Can you repeat?")
                    else:
                        end_convo = ('goodbye', 'bye', 'cya', 'stop', 'bye-bye')
                        if audio in end_convo:
                            listening = False
                            update_chat_log(f'User : {audio}\n\nJarvis : Okay have a great day!\n\n')
                            text_to_speech(text='Okay have a great day!')
                            micButton.configure(image=micOffImg)
                            listening = False
                            break
                        else:
                            reply = process_query(query=audio)
                            print(audio)
                            update_chat_log(f'User : {audio}\n\nJarvis : {reply}\n\n')
                            text_to_speech(text=reply)

                except Exception as e:
                    print('Error :', e)
                    update_chat_log("User : Error?? \n\nJarvis : Sorry, I didn't get that. Can you repeat?\n\n")
                    text_to_speech(text="Sorry, I didn't get that. Can you repeat?")

        threading.Thread(target=threaded_function).start()

    elif micButton.cget('image') == micImg:
        micButton.configure(image=micOffImg)
        listening = False
    else:
        print('unknown mic image error!')

# --------------------------------------------------------------------- #

labelFrame = CTkFrame(master=frame, fg_color='black', corner_radius=0, height=80)
labelFrame.pack(fill=X)
CTkLabel(master=labelFrame, text='J.A.R.V.I.S', font=('Eavm', 50), text_color='azure3').pack(side=BOTTOM)

micImg = CTkImage(light_image=Image.open(r'assets/micIconOnBluee.png'), size=(60, 60))
micOffImg = CTkImage(light_image=Image.open(r'assets/micIconOff.png'), size=(60, 60))
deleteImg = CTkImage(light_image=Image.open(r'assets/whiteDelete.png'), size=(10, 10))
chatLog = CTkImage(light_image=Image.open(r'assets/chatLogGray.png'), size=(550, 650)) # 550, 650

micButton = CTkButton(master=frame, width=30, height=60, corner_radius=10, fg_color='black', text='', image=micOffImg, border_width=0, hover=True, hover_color="gray", command=micOnOff)
micButton.pack(side=BOTTOM, pady=40)

delButton = CTkButton(master=labelFrame, width=20, height=20, corner_radius=0, fg_color='black', text='', image=deleteImg, border_width=2, hover=True, hover_color="gray", border_color="black", command=closeApp)
delButton.pack(side=TOP, anchor=E)

chatlogFrame = CTkFrame(master=frame, fg_color='black', corner_radius=0, width=600, height=800)
chatlogFrame.pack(side=LEFT, padx=20, pady=20) # IMPORTANT FOR CHATLOG
chatlogLabel = CTkLabel(master=chatlogFrame, corner_radius=0, image=chatLog, text='')
chatlogLabel.pack()

scrollFrame = CTkFrame(master=chatlogLabel, fg_color='black', corner_radius=0, width=333, height=480)
scrollFrame.grid(row=0, column=0)
scrollable_frame = CTkScrollableFrame(master=scrollFrame, fg_color="black", width=310, height=440, scrollbar_button_color="gray", scrollbar_button_hover_color="azure4", scrollbar_fg_color="black", orientation=VERTICAL, label_anchor=N, label_fg_color="black", label_font=("Eavm", 20), label_text="CHAT-LOG", label_text_color="white", corner_radius=0, border_width=0)
scrollable_frame.pack()

chat_log = CTkLabel(master=scrollable_frame, text='', text_color="white", font=('Arial', 14), wraplength=240, anchor='w', justify=LEFT)
chat_log.pack(side=LEFT, anchor='w')

# --------------------------------------------------------------------- #

def update_frame(index):
    global gif_frames
    global gif_label
    gif_label.configure(image=gif_frames[index])
    root.after(40, update_frame, (index + 1) % len(gif_frames))

gif_path = r'assets/ui6.gif' #ui, ui2, ui6, ui7
gif_image = Image.open(gif_path)
gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif_image)]

gif_label = CTkLabel(master=frame, corner_radius=0, text='')
gif_label.pack(pady=130)

# --------------------------------------------------------------------- #

update_frame(0)

root.mainloop()
