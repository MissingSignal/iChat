import sys
import yarp

from transformers import pipeline
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python" #workaround for incompatibility with protobuf versions >3.2, execution might be slower


# To print on the terminal
def info(msg):
    print("[INFO] {}".format(msg))


class Chat_Module(yarp.RFModule):
    """
    Description:
        ... insert here a description of the module ...
    Args:
        input_port  : ... insert here a description of the input port ...

    """

    def __init__(self):
        yarp.RFModule.__init__(self)
        self.process = True

        # initialize Q/A pipeline defined by model and tokenizer
        self.model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

        #initialize pipeline
        self.nlp = pipeline("sentiment-analysis", model=self.model_name, tokenizer=self.model_name)

        # handle port for the RFModule
        self.handle_port = yarp.Port()
        self.attach(self.handle_port)
        self.module_name = None

        # Define vars to receive the power values
        self.question_port = yarp.BufferedPortBottle()

        # Define a port to send a speech
        self.events_output = yarp.Port()
        self.emotions_output = yarp.Port()
      

    def configure(self, rf):

        # Module parameters
        self.module_name = rf.check("name",
                                    yarp.Value("iCub_Sentiment_Analysis"),
                                    "module name (string)").asString()

        # Opening Ports
        # Create handle port to read message
        self.handle_port.open('/' + self.module_name)

        # port to receive the textual questions
        self.question_port.open('/' + self.module_name + '/text:i')


        # Speech
        self.events_output.open('/' + self.module_name + '/sentiment:o')


        # IMPORTANT:
        # here we load the context from a .ini file
        # this file contains the text used to answer the questions
        self.context = rf.find("CONTEXT").asString()
        #print context inside a box in the terminal
        print("#"*100)
        print(self.context)
        print("#"*100)

        info("Initialization complete")

        return True
  

    def interruptModule(self):
        info("stopping the module")
        self.handle_port.interrupt()
        self.question_port.interrupt()
        self.emotions_output.interrupt()
        self.events_output.interrupt()
        

        return True


    def close(self):
        self.handle_port.close()
        self.question_port.close()
        self.emotions_output.close()
        self.events_output.close()

        return True


    def getPeriod(self):
        """
           Module refresh rate.

           Returns : The period of the module in seconds.
        """
        return 0.01


    def get_answer(self):

        answer = None

        if self.question_port.getInputCount():
            question = self.question_port.read(shouldWait=False)
            
            if question is not None:
                print("Received text: ", question.toString())
                answer = self.nlp(question.toString())

        return answer


    def updateModule(self):

        if self.process:

            answer = self.get_answer()
            
            if answer is not None:
                info("Sentiment: {}".format(answer))
                self.send_reply(answer)


        return True

  
    def send_reply(self, text):
        if self.events_output.getOutputCount():
            event_bottle = yarp.Bottle()
            event_bottle.clear()

            event_bottle.addString(text['answer'])
            self.events_output.write(event_bottle)


if __name__ == '__main__':

    # Initialise YARP
    if not yarp.Network.checkNetwork():
        info("Unable to find a yarp server exiting ...")
        sys.exit(1)

    yarp.Network.init()

    Module = Chat_Module()

    rf = yarp.ResourceFinder()
    rf.setVerbose(True)
    rf.setDefaultContext('iCub_Sentiment_Analysis') # where to find .ini files for this application
    rf.setDefaultConfigFile('iCub_Sentiment_Analysis.ini') # name of the default .ini file

    if rf.configure(sys.argv):
        Module.runModule(rf)
    sys.exit()
