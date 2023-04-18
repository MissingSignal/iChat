# iChat
This repository contains a conversational framework for iCub. 
This app allows users to freely chat with the robot using natural language.

## Modules
The chatbot model is composed of the following modules:
### 1. yarpdev
The yarpdev module is used to start the recording of the audio stream from the microphone.
By default it is run on iCub-head but you are warmly encouraged to run it on a differente pc, hence to use an external microphone.

### 2. Speech2Text
The Speech2Text module is used to convert the audio stream into text. It is based on [Open-AI whisper](https://github.com/openai/whisper), a speech-to-text model that is able to convert speech into text in real-time.

### 3. iCubQA
This is a conversational agent that is able to answer questions.
Given a context file (i.e. a file containing a list of questions and answers), the agent is able to answer questions about the iCub robot.
It is based on [HuggingFace's transformers](https://huggingface.co/) library.

### 4. sentimentAnalysis
This module is used to perform sentiment analysis on the user's vocal input.

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
    B --> C[sentiment Analysis]
    B --> E[iCub QA]
    E --> D(Acapella)
    C --> F(FaceExpressionDuo)
:::

