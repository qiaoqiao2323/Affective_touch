#!/usr/bin/python3
import sys
import os
import yarp
import yarp
import tkinter as tk
import tkinter.ttk as ttk
import threading
import tkinter.messagebox
import os, inspect
import subprocess
import time
import datetime
import random
import signal
import sys
import ctypes
from tkinter import font
# import keyboard  # make sure this is installed with: pip install keyboard
absol = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])) + "/data.txt"
#
path = os.path.realpath(
    os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])) + "/results/results_"




class SkinDataGUI:
    def __init__(self, pn_entry_value, module_ref):

        self.module = module_ref  # Reference to skinDataExperimentModule
        self.pn_entry_value = pn_entry_value
        self.emotion_sequence = ["Felicità", "Tristezza", "Rabbia",
                                 "Attirare l'attenzione", "Conforto", "Amore", "Empatia", "Gratitudine"]
        self.number_words = ["one", "two", "three", "four", "five", "six", "seven", "eight"]
        self.emotion_key_map = {word: emo for word, emo in zip(self.number_words, self.emotion_sequence)}

        self.current_emotion_index = 0
        self.current_emotion = self.emotion_sequence[self.current_emotion_index]
        self.current_number_words = self.number_words[self.current_emotion_index]
        self.next_number_words = self.number_words[self.current_emotion_index + 1]


    def start_the_window(self):
        # self.intro_thread = threading.Thread(target=self._run_gui)
        self.gui_thread = threading.Thread(target=self._run_gui)
        self.gui_thread.start()
        return self.gui_thread

    def _run_gui(self):

        self.window = tkinter.Tk()

        self.window.title("Data collection")
        self.frame = tkinter.Frame(self.window)
        self.frame.pack()

        self.user_input_frame = tkinter.LabelFrame(self.frame, text="Durata")
        self.user_input_frame.grid(row=0, column=0, padx=20, pady=20)

        self.body_font = font.Font(family="Georgia", size=14)
        self.time_entry = tkinter.Entry(self.user_input_frame, font=self.body_font)
        self.time_entry.grid(row=0, column=0, padx=20, pady=20)
        self.time_type = tkinter.StringVar()
        self.time_type_combo = ttk.Combobox(self.user_input_frame, textvariable=self.time_type,
                                            # values=["minutes", "hours", "seconds"], font=self.body_font)
                                            values = ["minuti", "ore", "secondi"], font = self.body_font)



        self.time_type_combo.current(0)
        self.time_type_combo.grid(row=0, column=1, padx=20, pady=20)
        self.preset_time = "1"
        self.preset_time_type = "secondi"
        self.time_entry.insert(0, self.preset_time)
        self.time_type.set(self.preset_time_type)

        self.duration_frame = tkinter.LabelFrame(self.frame, text="Progress")
        self.duration_frame.grid(row=1, column=0)
        self.canvas = tkinter.Canvas(self.duration_frame, width=400, height=400, highlightthickness=0)
        self.canvas.pack()
        self.remaining_time_label = tkinter.Label(self.duration_frame, text="", font=("Georgia", 14))
        self.remaining_time_label.pack(pady=5)

        self.buttons_frame = tkinter.LabelFrame(self.frame)
        self.buttons_frame.grid(row=2, column=0, padx=20, pady=20)
        self.after_id = None

        self.start_button = tkinter.Button(self.buttons_frame, text="Premi per iniziare",  font=self.body_font, command=self.start_countdown)
        self.start_button.grid(row=0, column=0)
        self.cancel_button = tkinter.Button(self.buttons_frame, text="Annulla", font=self.body_font,  command=self.stop_countdown)
        self.cancel_button.grid(row=0, column=1)
        self.retry_button = tkinter.Button(self.buttons_frame, text="Riprova",  font=self.body_font, command=self.retry)
        self.retry_button.grid(row=0, column=2)

        self.emotion_frame = tkinter.LabelFrame(self.frame, text="Intenzioni")
        self.emotion_frame.grid(row=3, column=0, padx=20, pady=20)
        self.emotion_type = tkinter.StringVar()
        # self.emotion_type_combo = ttk.Combobox(self.emotion_frame, textvariable=self.emotion_type,
        #                                        values=["Happiness", "Sadness", "Anger",
        #                                                "Grab attention", "Comfort", "Love", "Empathy", "Gratitude"])

        self.emotion_type_combo = ttk.Combobox(self.emotion_frame, textvariable=self.emotion_type,
                                               values=["Felicità", "Tristezza", "Rabbia",
                                                       "Attirare l'attenzione", "Conforto", "Amore", "Empatia", "Gratitudine"],  font=self.body_font)

        self.emotion_type_combo.current(0)
        self.emotion_type_combo.grid(row=3, column=0, padx=20, pady=20)

        # self.gesture_type = tkinter.StringVar()
        # self.gesture_type_combo = ttk.Combobox(self.emotion_frame, textvariable=self.gesture_type,
        #                                        values=["Hold", "Rub", "Tickle", "Poke", "Pat", "Tap", " "])
        # self.gesture_type_combo.grid(row=3, column=1, padx=20, pady=20)

        self.condition_type = tkinter.StringVar()
        self.condition_type_combo = ttk.Combobox(self.emotion_frame, textvariable=self.condition_type,
                                                 values=["Tocca pure", "Torso", "Braccio destro"],  font=self.body_font)
        self.condition_index = 0
        # self.condition = ["Free", "Torso", "Arm"]
        # random shuffle the second and third text. the first keeps the same
        second_third = ["Torso", "Braccio destro"]
        random.shuffle(second_third)
        self.condition = ["Tocca pure"] + second_third

        self.current_condition = self.condition[self.condition_index]

        self.condition_type_combo.grid(row=3, column=1, padx=20, pady=20)
        self.condition_type_combo.current(0)

        self.round_type = tkinter.StringVar()

        # self.round_type_combo = ttk.Combobox(self.emotion_frame, textvariable=self.round_type,
        #                                      values=["Round_1", "Round_2", "Round_3"])

        self.round_type_combo = ttk.Combobox(self.emotion_frame, textvariable=self.round_type,
                                             values=["Turno_1", "Turno_2", "Turno_3"],font=self.body_font)

        self.round_type_combo.current(0)
        self.round_type_combo.grid(row=3, column=2, padx=20, pady=20)
        self.rounds_index = 0
        self.rounds = ["Turno_1", "Turno_2", "Turno_3"]

        self.current_round = self.rounds[self.rounds_index]

        self.q_frame = tkinter.LabelFrame(self.frame)
        self.q_frame.grid(row=6, column=0, padx=30, pady=30)
        self.q_button = tkinter.Button(self.q_frame, text="Finish", command=self.next, font=self.body_font)
        self.q_button.grid(row=0, column=0)
        self.q_button.config(state=tkinter.NORMAL)

        # self.emotion_sequence = ["Happiness", "Sadness", "Fear", "Disgust", "Anger",
        #                          "Surprise", "Comfort", "Attention", "Calming", "Confusion"]
        # self.emotion_key_map = {str(i + 1 if i < 9 else 0): emo for i, emo in enumerate(self.emotion_sequence)}
        # self.emotion_sequence = ["Felicità", "Tristezza", "Rabbia",
                                 # "Attirare l'attenzione", "Conforto", "Amore", "Empatia", "Gratitudine"]


        # self.number_words = ["one", "two", "three", "four", "five", "six", "seven", "eight"]

        # self.number_words = ["Uno", "Due", "Tre", "Quattro", "Cinque", "Sei", "Sette", "Otto"]

        # self.emotion_key_map = {word: emo for word, emo in zip(self.number_words, self.emotion_sequence)}
        #
        # self.current_emotion_index = 0
        # self.current_emotion = self.emotion_sequence[self.current_emotion_index]
        # self.current_number_words = self.number_words[self.current_emotion_index]
        # self.next_number_words = self.number_words[self.current_emotion_index + 1]
        self.emotion_type_combo.set(self.current_emotion)  # Sync UI with first emotion
        self.waiting_for_key = False

        # self.prompt_label = tkinter.Label(self.frame, text="Press 1-8 to select an emotion", font=("Georgia", 18))

        self.prompt_sentence = tkinter.Label(self.frame, text="Ora devi esprimere delle emozioni al Berry attraverso il tocco. Iniziamo.",
                                          font=("Georgia", 18), fg="red")  # 设置字体颜色为红色)
        self.prompt_sentence.grid(row=4, column=0, padx=20, pady=20)

        self.prompt_label = tkinter.Label(self.frame, text="Premi da 1 a 8 per selezionare un'emozione", font=("Georgia", 18))
        self.prompt_label.grid(row=5, column=0, padx=20, pady=20)

        self.instructions = [
                "Abbiamo finito questo turno. Possiamo andare avanti.",
                "Grazie! Procediamo con il prossimo.",
                "Ricevuto! Quando vuoi, possiamo continuare.",
                "Va bene, puoi continuare.",
                "Segnale ricevuto. Procedi pure quando sei pronto.",
                "Tutto fatto qui. Passiamo oltre.",
                "Questo passaggio è completato. Quando sei pronto, iniziamo il prossimo.",
                "Perfetto. Aspetto la prossima interazione.",
                "Ho registrato il tuo tocco. Procediamo.",
                "Ecco, è finito. Possiamo andare avanti.",
                "Tutto a posto. Possiamo passare al prossimo.",
                "Anche questa fase è completata. Continuiamo.",
                "Interazione registrata. Procedi pure.",
                "Va bene così. Passiamo al prossimo.",
                "Fatto! Iniziamo quello successivo.",
                "Sono pronto per ricevere il prossimo tocco.",
                "Registrato correttamente. Procedi pure.",
                "tocco acquisito. Andiamo avanti.",
                "Puoi ora iniziare con la prossima emozione.",
                "Aspetto il prossimo segnale.",
                "Tutto pronto per il prossimo.",
                "Questo turno è terminato. Possiamo continuare.",
                "Dati salvati. Procediamo con il prossimo.",
                "Fase completata. Avanti così.",
                "Quando vuoi, passiamo al prossimo.",
                "Puoi procedere con il prossimo tocco.",
                "Stiamo continuando.",
                "Procedi pure con il prossimo.",
                "Sono pronto per proseguire.",
                "Quando vuoi, iniziamo la prossima interazione."

        ]
        self.remaining_instructions = random.sample(self.instructions, len(self.instructions))
        print(len(self.remaining_instructions))
        self.used_instructions = []

        # choose one random instructions from the list
        # self.instructions = self.instructions[:10]

        self.list = []
        self.PNID_path = path + self.pn_entry_value + "/" + "result_" + self.pn_entry_value + ".txt"
        print(self.PNID_path)
        with open(self.PNID_path, "a") as f:
            f.write("Sequence, Start_time, Ready time, End_time, Condition, Emotion, Rounds\n")
            # f.write("Sequence, Start_time, Ready time, End_time, Emotion, Rounds\n")

        # self.thread = threading.Thread(target=self.listen_to_yarp_keyboard, daemon=True)
        # self.thread.start()
        # print("✅ Thread start called.")
        # self.text =("This is the exploration phase. Feel free to interact with the robot through touch in any way you like. When you're ready, press 's' to start. Once you've finished expressing, press 't' to stop. After that, we'll begin the main experiment.")
        self.text = (
            "Questa è la fase di esplorazione. Sentiti libero di interagire con il robot tramite il tatto come preferisci. Quando sei pronto, premi 's' per iniziare. Una volta terminata l’espressione, premi 't' per fermarti. Dopo di ciò, inizieremo l’esperimento principale.")
        self.icub_speech(self.text)
        self.window.attributes("-fullscreen", True)
        self.window.bind("<Escape>", lambda e: self.window.attributes("-fullscreen", False))

        self.window.mainloop()



    def get_next_instruction(self):

        if len(self.remaining_instructions) == 0:
            self.remaining_instructions = self.used_instructions
            self.used_instructions = []

            # 可选：打乱顺序防止固定模式
            random.shuffle(self.remaining_instructions)

            # 取出一条指令
        next_instruction = self.remaining_instructions.pop()
        self.used_instructions.append(next_instruction)

        return next_instruction



    def show_preparation_window(self, emotion_name):
        self.prompt_sentence.config(
            # text=f"Now you need to express '{emotion_name}' to berry, press number {self.current_emotion_index+1} if you are prepared. ")
            text=f"Ora devi esprimere '{emotion_name}' a Berry, premi il numero {self.current_emotion_index + 1} se sei pronto.")

        # prep_window = tkinter.Toplevel(self.window)
        # prep_window.title("Preparation")
        # # Optional: Keep it non-topmost
        # # prep_window.attributes("-topmost", False)
        #
        # frame = tkinter.Frame(prep_window)
        # frame.pack(padx=40, pady=30)
        #
        # label = tkinter.Label(frame, text=f"Now you need to express '{emotion_name}' to the robot.",
        #                       font=("Arial", 14), justify="center")
        # label.pack(pady=20)
        #
        # self.ready_btn = tkinter.Button(
        #     frame,
        #     text="I am prepared",
        #     font=("Arial", 12, "bold"),
        #     command=lambda: self.on_prepared(prep_window)
        # )
        # self.ready_btn.pack(pady=10)
        self.waiting_for_key = True



    def handle_yarp_key(self, key):
        if key in self.emotion_key_map:
            if self.emotion_key_map[key] == self.current_emotion:
                self.prompt_label.config(text=f"[Feedback] '{key}' abbinamento '{self.current_emotion}'")
                self.on_prepared()
                # self.ready_btn.invoke()
            else:
                self.prompt_label.config(text=f"[Feedback] Hai premuto il tasto sbagliato. '{key}', atteso '{self.current_emotion}'")

    def on_key_press(self, event, ready_btn):
        key = event.char
        if self.waiting_for_key and key in self.emotion_key_map:
            if self.emotion_key_map[key] == self.current_emotion:
                self.waiting_for_key = False
                # self.prompt_label.config(text=f"'{self.current_emotion}' key confirmed. Starting countdown.")
                self.prompt_label.config(
                    text=f"Tasto '{self.current_emotion}' confermato. Avvio del conto alla rovescia.")
                ready_btn.invoke()
            else:
                print(f"Wrong key '{key}' for emotion '{self.current_emotion}'")

    def start_countdown(self):
        self.start_time = datetime.datetime.now()

        self.emotion_type_input = self.emotion_type_combo.get()
        self.condition_type_input = self.condition_type_combo.get()
        self.round_type_input = self.round_type_combo.get()

        if self.emotion_type_input != "" and self.condition_type_input != "" and self.round_type_input != "":
        # if self.emotion_type_input != "" and self.round_type_input != "":
            combined = self.condition_type_input + self.emotion_type_input + self.round_type_input
            # combined = self.emotion_type_input + self.round_type_input
            if self.emotion_type_input == "Felicità":
                self.icub_speech_start()
            if combined in self.list:
                self.delete()
                return
            else:
                self.list.append(combined)
                # self.robot_response()
                self.show_preparation_window(self.current_emotion)

    # def on_prepared(self, prep_window):
    #     self.ready_time = datetime.datetime.now()
    #     # prep_window.destroy()
    #     self._start_countdown_after_ready()

    def on_prepared(self):
        self.ready_time = datetime.datetime.now()
        self._start_countdown_after_ready()


    def _start_countdown_after_ready(self):
        self.start_button.config(state=tkinter.DISABLED)
        time_val = self.time_entry.get()
        time_type = self.time_type_combo.get()

        try:
            time_val = int(time_val)
            if time_type == "minuti":
                time_val *= 60
            elif time_type == "ore":
                time_val *= 3600
            if time_val <= 0:
                raise ValueError("Time must be greater than 0")

            t = threading.Thread(target=self.countdown, args=(time_val, time_val))
            t.start()

        except ValueError:
            self.stop_countdown()

    def countdown(self, remaining_time, total_time):
        remaining_time -= 1
        hours = remaining_time // 3600
        seconds = remaining_time % 3600
        minutes = seconds // 60
        seconds = seconds % 60
        self.remaining_time_label.config(text="{} ore {} minuti {} secondi".format(hours, minutes, seconds))
        self.canvas.delete("all")
        self.canvas.create_arc(10, 10, 390, 390, start=90, extent=360 * (remaining_time / total_time), fill="#16c5f5",width=4)
        if remaining_time <= 0:
            self.end_time = datetime.datetime.now()
            self.time_entry.delete(0, tkinter.END)
            self.time_entry.insert(0, self.preset_time)
            self.time_type.set(self.preset_time_type)
            with open(self.PNID_path, "a") as f:
                f.write("%d , %s, %s, %s , %s , %s ,%s \n" % (
                    self.current_emotion_index+1, self.start_time, self.ready_time, self.end_time, self.condition_type_input, self.emotion_type_input, self.round_type_input))
                # f.write("%d , %s, %s, %s , %s ,%s \n" % (
                #     self.current_emotion_index + 1, self.start_time, self.ready_time, self.end_time, self.emotion_type_input, self.round_type_input))
            text = self.get_next_instruction()
            # print(text)
            self.icub_speak_emotion(text,"happy")
            if len(self.list) < 72:
                self.current_emotion_index = (self.current_emotion_index + 1) % len(self.emotion_sequence)
                self.current_emotion = self.emotion_sequence[self.current_emotion_index]
                self.emotion_type_combo.set(self.current_emotion)

                if self.current_emotion_index == 0:
                    # self.current_round = self.rounds[self.rounds_index]
                    self.round_type_combo.set(self.current_round)
                    self.condition_type_combo.set(self.current_condition)
                if self.current_emotion_index == 7:
                    if self.current_round == "Turno_3":
                        self.condition_type_combo.current()
                        self.condition_index = (self.condition_index + 1) % len(self.condition)
                        self.current_condition = self.condition[self.condition_index]
                    self.rounds_index = (self.rounds_index + 1) % len(self.rounds)
                    self.current_round = self.rounds[self.rounds_index]
                    # print(self.current_emotion_index)
                self.start_countdown()
            else:
                self.q_button.config(state=tkinter.NORMAL)
                # tkinter.messagebox.showinfo("End of data collection",
                #                             "This is the end of the data collection.\nIf you are not satisfied with the last try,\nclick 'Retry' to start again. Otherwise, click 'Finish' to end this task.")
                tkinter.messagebox.showinfo("Fine della raccolta dati",
                                    "Questa è la fine della raccolta dati.\nSe non sei soddisfatto dell'ultima prova,\nclicca 'Riprova' per ricominciare. Altrimenti, clicca 'Fine' per terminare questo compito.")

        else:
            self.after_id = self.window.after(1000, self.countdown, remaining_time, total_time)

    def icub_speech_start(self, emotion="happy"):
        # 1. Set voice via RPC
        bottle_voice = yarp.Bottle()
        bottle_voice.addString("set")
        bottle_voice.addString("voice")
        bottle_voice.addString("sharona")  # make this dynamic if needed
        self.module.rpc_port.write(bottle_voice, yarp.Bottle())

        # 2. Set facial emotion
        emotion_bottle = yarp.Bottle()
        emotion_bottle.addString(emotion)
        self.module.emotion_port.write(emotion_bottle)

        # 3. Send speech
        # next_emotion = self.emotion_sequence[self.current_emotion_index+1]
        if self.current_condition == "Tocca pure":
            if self.current_round == "Turno_1":
                # speech = r"\rspd=90\ \pau=300\ " + (f"Let's start, now you need to express Felicità to me, you are free to touch any part of me."
                #                                     f"And you have time to think about expression for each emotion, you can "
                #                                 f"press number one if you are prepared, and then I will start count. ")
                speech = r"\rspd=90\ \pau=300\ " + (
                    f"Iniziamo, ora devi esprimere Felicità nei miei confronti, sei libero di toccare qualsiasi parte di me. "
                    f"Hai tempo per riflettere su come esprimere ciascuna emozione. "
                    f"Puoi premere il numero uno quando sei pronto, e poi inizierò il conto alla rovescia."
                )

                speech_bottle = yarp.Bottle()
                speech_bottle.addString(speech)
                self.module.speech_port.write(speech_bottle)
                # print(speech)

            if self.current_round == "Turno_2":
                # speech = r"\rspd=90\ \pau=300\ " + (f"Welcome to the second round, now you need to express Felicità to me, you have time to think about expression, you can "
                #                                 f"press number one if you are prepared, and then I will start count. ")

                speech = r"\rspd=90\ \pau=300\ " + (
                    f"Benvenuto al secondo turno. Ora devi esprimere Felicità nei miei confronti. Hai tempo per pensare a come esprimere l'emozione. "
                    f"Puoi premere il numero uno quando sei pronto, e poi inizierò il conto alla rovescia."
                )

                speech_bottle = yarp.Bottle()
                speech_bottle.addString(speech)
                self.module.speech_port.write(speech_bottle)
                # print(speech)

            if self.current_round == "Turno_3":
                # speech = r"\rspd=90\ \pau=300\ " + (f"Let's start the last round for this session, now you need to express Felicità to me, you have time to think about expression, you can "
                #                                 f"press number one if you are prepared, and then I will start count. ")
                speech = r"\rspd=90\ \pau=300\ " + (
                    f"Iniziamo l'ultimo turno di questa sessione. Ora devi esprimere Felicità nei miei confronti. Hai tempo per pensare a come esprimere l'emozione. "
                    f"Puoi premere il numero uno quando sei pronto, e poi inizierò il conto alla rovescia.")

                speech_bottle = yarp.Bottle()
                speech_bottle.addString(speech)
                self.module.speech_port.write(speech_bottle)
                # print(speech)

        elif self.current_condition != "Tocca pure":
            current_condition = self.current_condition
            if self.current_round == "Turno_1":
                # speech = r"\rspd=90\ \pau=300\ " + (
                #     f"Let's start a new session, in this session, you are only allowed to touch my {current_condition}, now you need to express Felicità to me, you have time to think about expression for each emotion, you can "
                #     f"press number one if you are prepared, and then I will start count. ")
                speech = r"\rspd=90\ \pau=300\ " + (
                    f"Iniziamo una nuova sessione. In questa sessione, puoi toccare solo il mio {current_condition}. Ora devi esprimere Felicità nei miei confronti. Hai tempo per pensare a come esprimere ogni emozione. "
                    f"Puoi premere il numero uno quando sei pronto, e poi inizierò il conto alla rovescia.")

                speech_bottle = yarp.Bottle()
                speech_bottle.addString(speech)
                self.module.speech_port.write(speech_bottle)
                # print(speech)

            if self.current_round == "Turno_2":
                # speech = r"\rspd=90\ \pau=300\ " + (
                #     f"This is the second round, now you need to express Felicità to me, please remember only touch my {current_condition}, you have time to think about expression, you can "
                #     f"press number one if you are prepared, and then I will start count. ")
                speech = r"\rspd=90\ \pau=300\ " + (
                    f"Questo è il secondo turno. Ora devi esprimere Felicità nei miei confronti. Per favore, ricorda di toccare solo il mio {current_condition}. Hai tempo per pensare a come esprimere l'emozione. "
                    f"Puoi premere il numero uno quando sei pronto, e poi inizierò il conto alla rovescia.")

                speech_bottle = yarp.Bottle()
                speech_bottle.addString(speech)
                self.module.speech_port.write(speech_bottle)
                # print(speech)

            if self.current_round == "Turno_3":
                # speech = r"\rspd=90\ \pau=300\ " + (
                #     f"Let's start the last round for this session, now you need to express Felicità to me by touching my {current_condition}, you have time to think about expression, you can "
                #     f"press number one if you are prepared, and then I will start count. ")
                speech = r"\rspd=90\ \pau=300\ " + (
                    f"Iniziamo l'ultimo turno di questa sessione. Ora devi esprimere Felicità nei miei confronti toccando il mio {current_condition}. Hai tempo per pensare a come esprimere l'emozione. "
                    f"Puoi premere il numero uno quando sei pronto, e poi inizierò il conto alla rovescia.")

                speech_bottle = yarp.Bottle()
                speech_bottle.addString(speech)
                self.module.speech_port.write(speech_bottle)
                # print(speech)

        # LAUGH01#

    def icub_speak_emotion(self, text, emotion):
        # 1. Set voice via RPC
        bottle_voice = yarp.Bottle()
        bottle_voice.addString("set")
        bottle_voice.addString("voice")
        bottle_voice.addString("sharona")  # make this dynamic if needed
        self.module.rpc_port.write(bottle_voice, yarp.Bottle())

        # 2. Set facial emotion
        emotion_bottle = yarp.Bottle()
        emotion_bottle.addString(emotion)
        self.module.emotion_port.write(emotion_bottle)

        # 3. Send speech
        next_emotion_index = (self.current_emotion_index+1) % len(self.emotion_sequence)
        next_emotion = self.emotion_sequence[next_emotion_index]


        # number_index = self.current_emotion_index + 1
        number = self.number_words[next_emotion_index]
        if next_emotion != "Felicità":
            # speech = r"\rspd=90\ \pau=300\ " + text + (f" Now you need to express '{next_emotion}' to me. you can"
            #                                        f"press number {number}' if you are prepared.")

            speech = r"\rspd=90\ \pau=300\ " + text + (
                f" Ora devi esprimere '{next_emotion}' nei miei confronti. "
                f"Puoi premere il numero {number} se sei pronto.")

            # LAUGH01#
            speech_bottle = yarp.Bottle()
            speech_bottle.addString(speech)
            self.module.speech_port.write(speech_bottle)

            # print(speech)

    def icub_speech(self, text):            # LAUGH01#
        speech_bottle = yarp.Bottle()
        speech_bottle.addString(text)
        self.module.speech_port.write(speech_bottle)
        # print(speech)

    def stop_countdown(self):
        self.start_button.config(state=tkinter.NORMAL)
        if self.after_id:
            self.window.after_cancel(self.after_id)
            self.after_id = None
            self.canvas.delete("all")
            self.remaining_time_label.config(text="")

    def delete(self):
        self.start_button.config(state=tkinter.NORMAL)
        if self.after_id:
            self.window.after_cancel(self.after_id)
            self.after_id = None
            self.canvas.delete("all")
            self.remaining_time_label.config(text="")

    def retry(self):
        self.start_button.config(state=tkinter.NORMAL)
        self.canvas.delete("all")
        self.remaining_time_label.config(text="")
        self.list.pop()

    # def stop_window(self):
    #     if hasattr(self, "window") and self.window:
    #         self.window.after(0, self._on_close)
    #         # atexit.register(self.suppress_async_delete_crash)
    #
    # def _on_close(self):
    #     self.should_stop = True
    #     self.window.quit()
    #     self.window.destroy()

    # def handle_yarp_key(self, key):
    #     if key in self.emotion_key_map:
    #         if self.emotion_key_map[key] == self.current_emotion:
    #             self.prompt_label.config(text=f"[YARP] '{key}' abbinamento '{self.current_emotion}'")
    #             self.ready_btn.invoke()
    #         else:
    #             self.prompt_label.config(text=f"[YARP] Hai premuto il tasto sbagliato. '{key}', atteso '{self.current_emotion}'")


    def stop_window(self):
        print("stop Window")
        self.window.after(10, self.window.destroy)
        print("Window stopped")
        # self.module.interruptModule()
        # self.module.close()
        os._exit(0)  # 强制退出所有线程（不推荐用 sys.exit()，因为在子线程中可能无效）



    # Before destroying the window or exiting

    def next(self):
        # ✅ Set module state to stop
        self.module.state = "stop"
        self.module.deactivate_gui()

        # ✅ Stop YARP ports
        self.module.interruptModule()
        self.module.close()
        # self.module.should_update = False
        # self.module.stop_thread()
        self.stop_window()
        # self.gui_thread.join()
        # ✅ 结束整个程序（可选，如果你是 main loop 线程）
        os._exit(0)  # 强制退出所有线程（不推荐用 sys.exit()，因为在子线程中可能无效）
        # # ✅ Close the Tkinter window
        self.window.quit()  # stop the mainloop if running
        self.window.destroy()




