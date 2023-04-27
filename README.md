# iChat
This repository contains a conversational framework for iCub. 
This app allows users to freely chat with the robot using natural language.

## Modules
The chatbot is composed of the following modules:

### 1. yarpdev
The yarpdev module is used to start the recording of the audio stream from the microphone.
By default it is run on iCub-head but you are warmly encouraged to run it on a differente pc, hence to use an external microphone.
 **_NOTE:_**  This module is temporaly useless since speech2text records audio directly from the mic (not through YARP) 

| port | in/out | description | connects to |
| --- | --- | --- | --- |
| `/audioRecorderWrapper/audio:o`  | output | audio stream from iCub's microphone`) | `/speech2Text/speech:i` |

### 2. Speech2Text
The Speech2Text module is used to convert the audio stream into text. It is based on [Open-AI whisper](https://github.com/openai/whisper), a speech-to-text model that is able to convert speech into text in real-time.

| port | in/out | description | connects to |
| --- | --- | --- | --- |
| `/speech2Text/speech:i` | input | acquire audio from the microphone port | `/audioRecorderWrapper/audio:o` |
| `/CardClassifier/text:o`  | output | publishes bottle with a string, the trancript of the speech | `/iCubQA/question:i` `/sentimentAnalysis/text:i` |

### 3. iCubQA
This is a conversational agent that is able to answer questions.
Given a context file (i.e. a file containing a list of questions and answers), the agent is able to answer questions about the iCub robot.
It is based on [HuggingFace's transformers](https://huggingface.co/) library.

| port | in/out | description | connects to |
| --- | --- | --- | --- |
| `/iCubQA/question:i` | input | acquire vocal trascript from speech2text module  | `/speech2Text/text:o` |
| `/iCubQA/answer:o`  | output | publishes bottle with a string, the robot's answer | `/acapelaSpeak/speech:i` |

### 4. sentimentAnalysis
This module is used to perform sentiment analysis on the user's vocal transcript. This operates on the transcript, hence the tone of the voice is not taken into account.

| port | in/out | description | connects to |
| --- | --- | --- | --- |
| `/sentimentAnalysis/text:i` | input | reads bottle with a string, the trancript of the speech |  `/speech2Text/text:o` |
| `/sentimentAnalysis/sentiment:o` | output | sentiment calssification in range [0 1] where 1 is very positive  |  `//` |
| `/sentimentAnalysis/facialEmotion:o` | output | a VOCAB that sets iCub's face to [sad - neutral - happy] depending on user's sentiment |  `/icub/face/emotions/in` |


## Installation
- Clone this repository to your local machine ( preferably in  `../src/robot/CognitiveInteraction` ).

- Compile and and install the framwork:
```bash
cd ../iChat

mkdir build && cd build

cmake ../

make

make install
```

- Customize the `iChat.xml.template` in the `ICUBCONTRIB` folder with your own paths and save it as `iChat.xml`

- Run the app from yarpmanager

***Note:*** *the new virtual env must have python = 3.10 (3.11 is not yet supported by whisper!)*

## Architecture
At the moment the architecture is composed of the following modules:


::: mermaid

flowchart TD
    A(Microphone) --> B[speech2text]
    B --> C[sentimentAnalysis]
    B --> E[iCubQA]
    E --> D(acapela)
:::
    
    
    
    C --> F(Face
