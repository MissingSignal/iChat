# source di ogni cartella, ogni cartella figlio (modules) ha un file .sh che attiva il venv (ereditato) e poi esegue il file .py

set(MODULE_NAME iCubQA) #custom name of the module #TODO: change this to the name of the script

message("Installing ${MODULE_NAME}")

# attach ".sh" to the end of the module name
set(PATH_TO_SCRIPT path/to/script.py)
set(PATH_TO_VENV path/to/venv) # inherited from parent CMakeLists.txt


## Create a .sh file that activate the shared virtual environment and run the module ##

# Set the name of the script file to be generated
set(SCRIPT_FILE_NAME ${MODULE_NAME})

# Set the command to activate the virtual environment and run the Python script
set(SCRIPT_CONTENT "#!/bin/bash\nsource path/to/venv/bin/activate\npython ${SCRIPT_FILE_NAME}.py")

# Generate the script file
file(WRITE ${CMAKE_BINARY_DIR}/bin/${SCRIPT_FILE_NAME} ${SCRIPT_CONTENT})

# Make the script file executable
execute_process(COMMAND chmod +x ${SCRIPT_FILE_NAME})

# Output instructions to the user
message("Your ${SCRIPT_FILE_NAME} script has been created. You can now run it from terminal or yarpmanager.")

## Install the .sh file in the bin directory ##
#add_executable(${PROJECT_NAME} ${SCRIPT_FILE_NAME})


install(FILES ${CMAKE_BINARY_DIR}/bin/${SCRIPT_FILE_NAME} PERMISSIONS ${PROGRAM_PERMISSIONS_DEFAULT} DESTINATION bin)
#add_custom_target(build-python ALL DEPENDS ${SCRIPT_FILE_NAME})
#install(TARGETS ${PROJECT_NAME} DESTINATION bin)