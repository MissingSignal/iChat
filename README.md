## iChat
This repository contains a chatbot model for iCub. 
The chatbot model allows users to freely chat with the robot using natural language.

## Installation
To use the chatbot robot, follow these steps:


- Clone this repository to your local machine.

- create a new virtual env with python = 3.10 (3.11 is not supported!)

- Install the required dependencies by running `pip install -r requirements.txt`.


- Run the `iChat.py` script to start the chatbot.

## Usage
At the current state of the work, the model can be used via terminal.
In the near future a verbal interaction mode will be integrated.

::: mermaid

flowchart LR

    id1((Mic.)) -- /Speech2Text/speech:i --- Speech2Text -- /Speech2Text/text:o --- iChat  -- iChat/answer:o --- id2((User))
:::

