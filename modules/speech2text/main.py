import sys
import yarp

import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import queue
import tempfile
import os
import threading
import torch
import numpy as np

# To use the command line, this bypass YARP's RFModule parser
# @click.command()
# @click.option("--model", default="base", help="Model to use", type=click.Choice(["tiny","base", "small","medium","large"]))
# @click.option("--english", default=True, help="Whether to use English model",is_flag=True, type=bool)
# @click.option("--verbose", default=False, help="Whether to print verbose output", is_flag=True,type=bool)
# @click.option("--energy", default=300, help="Energy level for mic to detect", type=int)
# @click.option("--dynamic_energy", default=False,is_flag=True, help="Flag to enable dynamic engergy", type=bool)
# @click.option("--pause", default=0.8, help="Pause time before entry ends", type=float)
# @click.option("--save_file",default=False, help="Flag to save file", is_flag=True,type=bool)


# To print on the terminal
def info(msg):
    print("[INFO] {}".format(msg))


class Speech2text_Module(yarp.RFModule):
    """
    Description:
        ... insert here a description of the module ...
    Args:
        input_port  : ... insert here a description of the input port ...

    """

    def __init__(self):
        yarp.RFModule.__init__(self)
        self.process = True

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
        # self.module_name = rf.check("name",
        #                     yarp.Value("iChat"),
        #                     "module name (string)").asString()

        #TODO read the parameters  using the RFModule
        model = "base"
        english = True
        verbose = False
        energy = 300
        dynamic_energy = False
        pause = 0.8
        save_file = False

        ################ APPLICATION SPECIFIC VARIABLES ######################
        temp_dir = tempfile.mkdtemp() if save_file else None
        #there are no english models for large
        if model != "large" and english:
            model = model + ".en"
        self.audio_model = whisper.load_model(model)
        self.audio_queue = queue.Queue()
        self.result_queue = queue.Queue()
        threading.Thread(target=self.record_audio,
                        args=(self.audio_queue, energy, pause, dynamic_energy, save_file, temp_dir)).start()
        threading.Thread(target=self.transcribe_forever,
                        args=(self.audio_queue, self.result_queue, self.audio_model, english, verbose, save_file)).start()
        ######################################################################

        # Module parameters
        self.module_name = rf.check("name",
                                    yarp.Value("speech2text"),
                                    "module name (string)").asString()

        ### Opening Ports ###
        # Create handle port to read message
        self.handle_port.open('/' + self.module_name)
        # port to receive the verbal questions
        self.question_port.open('/' + self.module_name + '/speech:i')
        # text transcription port
        self.events_output.open('/' + self.module_name + '/text:o')
        #####################
        print("ports opened")

        # IMPORTANT:
        # here we load the context from a .ini file
        # this file contains the text used to answer the questions
        self.context = rf.find("context").asString()

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
                print("Received question: ", question.toString())
                QA_input = {'question': question.toString(), 'context': self.context}
                answer = self.nlp(QA_input)

        return answer


    def updateModule(self):

        if self.process:
            
            #print the result
            question = self.result_queue.get()
            print(question)
            self.send_bottle(question)

            # answer = self.get_answer()
            
            # if answer is not None:
            #     info("Answering: {}".format(answer))
            #     self.send_reply(answer)


        return True


    def send_bottle(self, text):
        event_bottle = yarp.Bottle()
        event_bottle.clear()
        event_bottle.addString(text)
        self.events_output.write(event_bottle)
        return


    # This function is the first thread that records audio and puts it in a queue
    def record_audio(self, audio_queue, energy, pause, dynamic_energy, save_file, temp_dir):
        #load the speech recognizer and set the initial energy threshold and pause threshold
        r = sr.Recognizer()
        r.energy_threshold = energy
        r.pause_threshold = pause
        r.dynamic_energy_threshold = dynamic_energy

        with sr.Microphone(sample_rate=16000) as source:
            print("Say something!")
            i = 0
            while True:
                #get and save audio to wav file
                audio = r.listen(source)
                if save_file:
                    data = io.BytesIO(audio.get_wav_data())
                    audio_clip = AudioSegment.from_file(data)
                    filename = os.path.join(temp_dir, f"temp{i}.wav")
                    audio_clip.export(filename, format="wav")
                    audio_data = filename
                else:
                    torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
                    audio_data = torch_audio

                audio_queue.put_nowait(audio_data)
                i += 1

    # This function is the second thread that transcribes audio and puts it in a queue
    def transcribe_forever(self, audio_queue, result_queue, audio_model, english, verbose, save_file):
        while True:
            audio_data = audio_queue.get()
            if english:
                result = audio_model.transcribe(audio_data,language='english')
            else:
                result = audio_model.transcribe(audio_data)

            if not verbose:
                predicted_text = result["text"]
                result_queue.put_nowait(predicted_text)
            else:
                result_queue.put_nowait(result)

            if save_file:
                os.remove(audio_data)


if __name__ == '__main__':

    # Initialise YARP
    if not yarp.Network.checkNetwork():
        info("Unable to find a yarp server exiting ...")
        sys.exit(1)

    yarp.Network.init()

    Module = Speech2text_Module()

    rf = yarp.ResourceFinder()
    rf.setVerbose(True)
    rf.setDefaultContext('speech2text') # where to find .ini files for this application
    rf.setDefaultConfigFile('speech2text.ini') # name of the default .ini file

    if rf.configure(sys.argv):
        Module.runModule(rf)
    sys.exit()
