# Record conversation between Agent A and Agent B and save it to a .txt file

import os

# Get input from user
agent_a_name = input("Enter Agent A's name: ")
agent_b_name = "iCub" #input("Enter Agent B's name: ")
conversation_file_name = input("Enter the name of the file to save the conversation: ")

# Start recording the conversation
conversation = []
print("Recording the conversation. Press Ctrl+C to stop.")
while True:
    try:
        message = input(f"{agent_a_name}: ")
        conversation.append(f"{agent_a_name}: {message}")
        message = input(f"{agent_b_name}: ")
        conversation.append(f"{agent_b_name}: {message}")
    except KeyboardInterrupt:
        break

# Save the conversation to a text file
conversation_text = "\n".join(conversation)
with open(conversation_file_name, "w") as file:
    file.write(conversation_text)

print(f"Conversation saved to {os.path.abspath(conversation_file_name)}")