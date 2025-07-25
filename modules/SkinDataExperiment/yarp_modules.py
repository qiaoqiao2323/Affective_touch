import sys
import os
import yarp
import yarp
import time
import threading
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import os, inspect
import subprocess
from GUI import SkinDataGUI
from Introduction import introduction




# sys.stderr = open(os.devnull, 'w')


def yarpInfo(msg):
    print("[INFO] {}".format(msg))


def yarpError(msg):
    print("\033[91m[ERROR] {}\033[00m".format(msg))


def yarpWarning(msg):
    print("\033[93m[WARNING] {}\033[00m".format(msg))


class YarpPorts(yarp.RFModule):
    """
    Description:
        Object to read yarp image recongnize face landmarks, detect if the lips are moving, and stream the results

    Args:
        input_port  : input port of image
        output_port : output port for streaming recognized landmarks
        display_port: output port for image with recognized faces+emotions
    """

    def __init__(self):
        super().__init__()
        yarp.RFModule.__init__(self)
        self.handle_port = yarp.Port()
        self.attach(self.handle_port)
        self.input_port = yarp.BufferedPortBottle()
        self.pn_entry_value = ""

        self.rpc_port = yarp.Port()
        self.attach(self.rpc_port)
        # self.rpc_port.open("/my_rpc_port")
        # yarp.Network.connect("/my_rpc_port", "/acapelaSpeak")

        # 2. Port to control iCub's face emotion
        self.emotion_port = yarp.Port()
        self.attach(self.emotion_port)
        # self.emotion_port.open("/my_emotion_port")
        # yarp.Network.connect("/my_emotion_port", "/icub/face/emotions/in")

        # 3. Port to send speech
        self.speech_port = yarp.Port()
        self.attach(self.speech_port)
        # self.speech_port.open("/my_speech_port")

        # self.use_camera_port = yarp.Port()
        # self.attach(self.use_camera_port)

        self.viewer_port = yarp.Port()
        self.attach(self.viewer_port)



        self.face_tracker_client = yarp.RpcClient()
        self.interaction_client = yarp.RpcClient()


        self.state = "default"
        self.intro_started = False
        self.active_intro = False

        self.gui_started = False
        self.active_gui = False
        # self.gui_thread = threading.Thread(target=lambda: SkinDataGUI(self.pn_entry_value, self))
        self.introduction_class = None
        self.introduction_thread = None

        self.gui_class = None
        self.gui_thread = None





    def stop_intro(self):
        print("stopping the introduction")
        self.introduction_class.stop_window()
        self.introduction_thread.join()


    def stop_gui(self):

        print("stopping gui\n")

        self.gui_class.stop_window()
        self.gui_thread.join()

        print("gui stopped\n")




    def send_rpc_command(self,client_port: yarp.RpcClient,*args):
        if client_port.getOutputCount():
            cmd = yarp.Bottle()
            reply = yarp.Bottle()

            for arg in args:
                cmd.addString(arg)

            client_port.write(cmd, reply)
            print(f"🗨️  Reply: {reply.toString()}")
        else:
            print("ERROR: Client Port Not Connected!")




    def configure(self, rf: yarp.ResourceFinder) -> bool:

        if rf.check('help') or rf.check('h'):
            print("Face Landmark options:")
            print("\t--name (default skinDataExperiment) module name")
            print("\t--help print this help")
            return False

        self.param_module_name = rf.findGroup("module").check("name",
                                                              yarp.Value("skinDataExperiment"),
                                                              "module name (string)").asString()
        print(self.param_module_name)

        # --- Handle port (for commands like quit/help) ---
        main_port = f"/{self.param_module_name}"
        if not self.handle_port.open(main_port):
            yarpError(f"Failed to open module handle port {main_port}")
            return False
        yarpInfo(f"Opened main RPC handle port {main_port}")


        skinGui_out = f"/{self.param_module_name}/skinGui/read:i"
        if not self.input_port.open(skinGui_out):
            yarpError(f"Failed to open {skinGui_out}")
            return False
        yarpInfo(f"Opened port {skinGui_out}")


        # --- RPC port for speech control ---
        rpc_name = f"/{self.param_module_name}/rpc"
        if not self.rpc_port.open(rpc_name):
            yarpError(f"Failed to open {rpc_name}")
            return False
        yarpInfo(f"Opened port {rpc_name}")

        # --- Emotion control port ---
        emotion_name = f"/{self.param_module_name}/emotion:o"
        if not self.emotion_port.open(emotion_name):
            yarpError(f"Failed to open {emotion_name}")
            return False
        yarpInfo(f"Opened port {emotion_name}")

        # --- Speech output port ---
        speech_name = f"/{self.param_module_name}/speech:o"
        if not self.speech_port.open(speech_name):
            yarpError(f"Failed to open {speech_name}")
            return False
        yarpInfo(f"Opened port {speech_name}")

        # camera_name = "/grabberUsb1"
        # if not self.use_camera_port.open(camera_name):
        #     yarpError(f"Failed to open {camera_name}")
        #     return False
        # yarpInfo(f"Opened port {camera_name}")

        # --- External RPC client: faceTracker ---
        ft_name = f"/{self.param_module_name}/client/faceTracker"
        if not self.face_tracker_client.open(ft_name):
            yarpError(f"Failed to open {ft_name}")
            return False
        yarpInfo(f"Opened RPC client {ft_name}")

        # --- External RPC client: interactionInterface ---
        int_name = f"/{self.param_module_name}/client/interactionInterface"
        if not self.interaction_client.open(int_name):
            yarpError(f"Failed to open {int_name}")
            return False
        yarpInfo(f"Opened RPC client {int_name}")



        self.print_parameters()

        return True

    def pre_session(self):
        # ---- Step 1: Start faceTracker ----
        self.send_rpc_command(self.face_tracker_client,  "run")
        time.sleep(1)  # Let it stabilize

        # ---- Step 2: Trigger interactionInterface ----
        self.send_rpc_command(self.interaction_client,  "exe", "introskin")
        time.sleep(2)  # Adjust as needed for real scenario

        # ---- Step 3: Stop faceTracker ----
        self.send_rpc_command(self.face_tracker_client,  "sus")

        time.sleep(3)
        self.state = "introduction"


    def print_parameters(self):
        print("Module Parameters:")
        print(f"  Module Name: {self.param_module_name}")


    def interruptModule(self):
        print("stopping the module \n")
        self.handle_port.interrupt()
        self.emotion_port.interrupt()
        self.rpc_port.interrupt()
        self.input_port.interrupt()
        self.speech_port.interrupt()
        # self.use_camera_port.interrupt()
        self.face_tracker_client.interrupt()
        self.interaction_client.interrupt()
        if self.active_gui:
            self.stop_gui()

        if self.active_intro:
            self.stop_intro()
        print("stopping the module finished\n")

        # self.next()

        return True

    def close(self):
        print("closing the module \n")
        # self.next()
        # print("closing the interface \n")

        self.handle_port.close()
        print("close the port")
        self.emotion_port.close()
        self.rpc_port.close()
        self.input_port.close()
        self.speech_port.close()
        # self.use_camera_port.close()
        self.face_tracker_client.close()
        self.interaction_client.close()

        print("closing the module finished\n")

        # self.next()

        return True


    def getPeriod(self):
        """
           Module refresh rate.
           Returns : The period of the module in seconds.
        """
        return 0.01

    def respond(self, command, reply):
        reply.clear()

        if command.get(0).asString() == "quit":
            reply.addString("quitting")
            self.quit()
            return False

        elif command.get(0).asString() == "help":
            reply.addString(" skinDataExperiment module commands are:\n")
            reply.addString(" quit to quit the module \n")

        elif command.get(0).asString() == "start":
            self.state = "pre_session"
            reply.addString(" okay \n")
        elif command.get(0).asString() == "stop":
            self.gui_class.next()

        else:
            reply.addString("nack unknown command \n")

        return True

    def deactivate_intro(self):
        self.active_intro = False

    def deactivate_gui(self):
        self.active_gui = False




    def updateModule(self):
        # print("Listening to YARP keyboard...")
        # while True:
        if self.state == "pre_session":
            self.pre_session()
        elif self.state == "introduction" and self.intro_started == False:

            self.introduction_class = introduction(self)
            print("the introduction initialized")
            self.intro_started = True
            self.active_intro = True
            self.introduction_thread = self.introduction_class.start_the_window()

            print("the introduction started")

        elif self.state == "experiment" and self.state != "stop":
            # print("the gui started")

            if self.active_gui == False:
                self.gui_class = SkinDataGUI(self.pn_entry_value,self)
                self.gui_started = True
                self.active_gui = True
                self.gui_thread = self.gui_class.start_the_window()
                print("the gui started")
            if self.input_port.getInputCount():
                print("the start_skinData started")
                print(self.input_port.getInputCount)
                bottle = self.input_port.read(True)  # Blocking read
                if bottle is not None and bottle.size() > 0:
                    values = []
                    print(f"[YARP] Bottle size: {bottle.size()}")
                    for i in range(bottle.size()):
                        item = bottle.get(i)
                        if item.isString():
                            val = item.asString()
                        elif item.isInt32():
                            val = str(item.asInt32())
                        elif item.isFloat64():
                            val = str(item.asFloat64())
                        else:
                            val = item.toString()
                        values.append(val)
                        print(f"[YARP] Element {i}: {val}")
                    final_string = " ".join(values)
                    print(f"[YARP] Full string: {final_string}")
                    # self.root.after(0, self.update_label, final_string)
                    # self.waiting_for_key = True
                    self.gui_class.handle_yarp_key(final_string)
                    if final_string == "t":
                        # self.gui_class.icub_speech("Thank you, let's move to the main experiment")
                        self.gui_class.icub_speech("Grazie, passiamo all'esperimento principale.")

                else:
                    print("[YARP] Empty or invalid bottle")


        # if self.state == "stop":
        #     if self.active_gui == True:
        #         self.stop_gui()
        #         self.interruptModule()
        #         self.close()
        #     return False


        return True


    def icub_speak_emotion(self, text, emotion):
        # 1. Set voice via RPC
        bottle_voice = yarp.Bottle()
        bottle_voice.addString("set")
        bottle_voice.addString("voice")
        bottle_voice.addString("sharona")  # make this dynamic if needed
        self.rpc_port.write(bottle_voice, yarp.Bottle())

        # 2. Set facial emotion
        emotion_bottle = yarp.Bottle()
        emotion_bottle.addString(emotion)
        self.emotion_port.write(emotion_bottle)

        # 3. Send speech
        next_emotion_index = (self.current_emotion_index+1) % len(self.emotion_sequence)
        next_emotion = self.emotion_sequence[next_emotion_index]


        # number_index = self.current_emotion_index + 1
        number = self.number_words[next_emotion_index]

        # speech = r"\rspd=90\ \pau=300\ " + text + (f" Now you need to express '{next_emotion}' to me. you have time to think about expression, you can"
        #                                            f"press number {number}' if you are prepared, and then I will start count.")

        speech = r"\rspd=90\ \pau=300\ " + text + (f" '{next_emotion}', press number '{number}' .")


        # LAUGH01#
        speech_bottle = yarp.Bottle()
        speech_bottle.addString(speech)
        self.speech_port.write(speech_bottle)

    def icub_speech_start(self, emotion="happy"):
        # 1. Set voice via RPC
        bottle_voice = yarp.Bottle()
        bottle_voice.addString("set")
        bottle_voice.addString("voice")
        bottle_voice.addString("sharona")  # make this dynamic if needed
        self.rpc_port.write(bottle_voice, yarp.Bottle())

        # 2. Set facial emotion
        emotion_bottle = yarp.Bottle()
        emotion_bottle.addString(emotion)
        self.emotion_port.write(emotion_bottle)

        # 3. Send speech
        # next_emotion = self.emotion_sequence[self.current_emotion_index+1]

        if self.current_round == "Round_1":
            speech = r"\rspd=90\ \pau=300\ " + (f"Let's start, now you need to express happiness to me, you have time to think about expression, you can "
                                            f"press number one if you are prepared, and then I will start count. ")
            speech_bottle = yarp.Bottle()
            speech_bottle.addString(speech)
            self.speech_port.write(speech_bottle)

        if self.current_round == "Round_2":
            speech = r"\rspd=90\ \pau=300\ " + (f"Let's start the second rounds, now you need to express happiness to me, you have time to think about expression, you can "
                                            f"press number one if you are prepared, and then I will start count. ")
            speech_bottle = yarp.Bottle()
            speech_bottle.addString(speech)
            self.speech_port.write(speech_bottle)

        if self.current_round == "Round_3":
            speech = r"\rspd=90\ \pau=300\ " + (f"Let's start the last round for this session, now you need to express happiness to me, you have time to think about expression, you can "
                                            f"press number one if you are prepared, and then I will start count. ")
            speech_bottle = yarp.Bottle()
            speech_bottle.addString(speech)
            self.speech_port.write(speech_bottle)

        # LAUGH01#









