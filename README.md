# SkinDataExperiment

This project involves a multimodal interaction experiment with the iCub robot. Participants express emotions through touch, while the robot responds neutrally to maintain unbiased input. The project integrates pre-session interaction, GUI-based data collection from the 13 body parts of the skin.

## 📦 Build
```bash
.../SkinDataExperiment$ mkdir build && cd build
.../SkinDataExperiment$ cmake ..
.../SkinDataExperiment$ make && make install
```

## Run
```bash
.../SkinDataExperiment$ yarp rpc /skinDataExperiment
>> start
````
## stop
You can simply close the GUI or 

```bash
.../SkinDataExperiment$ yarp rpc /skinDataExperiment
>> stop
````

Remember to give the permission for .sh file under the context folder, once you rebuild the application, you need to give the permission again.
```bash
chmod +x skin_intro.sh
````


## 📦 Project Structure

- `main.py`: Entry point of the program. Initializes YARP, runs the yarp_modules.
- `yarp_modules.py`: Contains the main YARP module class `YarpPorts` which:
  - Opens/attaches required ports
  - Handles pre-session interaction (face tracker, intro speech)
  - Launches the `Introduction.py` fro introduction GUI and `SkinDataGUI` window for data collection.

- `Introduction.py`: Explain rules and input participants ID.

- `GUI.py`: Contains the `SkinDataGUI` class for the graphical interface:
  - Collects experiment duration, emotion, condition, and round
  - Provides feedback and countdown
  - Saves each expression attempt to a file
- `skin_intro.sh`: A bash script that makes the robot introduce itself, explain rules, and start interaction with participants to ensure intentionality, called the function from the interactionInterface. 

## 🎬 Workflow

1. **Pre-session**:
    - Starts the face tracker via RPC
    - Uses Acapela TTS to speak and explain the rules
    - Wave to participants and do different emotions.

2. **Introduction GUI**:
    - Show rules on the GUI and input participants ID, keep tracking.

2. **Experiment GUI stages**:
    - Emotion selection and countdown interface
    - 3 rounds: Free, Arm-only, Torso-only
    - Robot gives neutral instructions between interactions

## 🧠 Robot Behaviour build based on

  - Acapela Speech
  - InteractionInterface 
  - FaceTracker
  - Keyboard interface
  - Datadumper

## 🧾 Data Output

- Each participant's interaction data is saved under the current directory of: /results/results_<PN_ID>/result_<PN_ID>.txt
- Tactile Data from 13 skin body parts saved under their corresponding body name. 
- Recodings for interaction


## 📊 Data Analysis (Coming Soon)

- Emotion decoding accuracy
- touch dynamics with intentional agent
- Comparison between Free/Arm/Torso rounds  
- ICC reliability of participant responses  
- Reaction and preparation time  
- Moreeeeeeeeeeeeeeeee

## 📊 Dataset 

- Touch features for all participants and all conditions
- Annotation from videos for free condition
- Questionnaire results
- Video features about motion energy will update soon

  
## ⚠️ Notes

- `Tkinter` GUI is run in a separate thread to avoid blocking YARP. (For future development, it's better to change to another tool)
- Some warnings like `Tcl_AsyncDelete` may occur if GUI is closed from a non-main thread. 








