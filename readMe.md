# Affective Virtual Agent 

## Set-up

- To set-up the environment for the application, ensure you have Python 3.5> installed on your machine.
- Once installed, run the following command `pip install -r requirements.txt`
- Access the config.py file in the directory root, here, alter the variable `packageDir` to the full path of the root directory (Virtual Agent)
- Open terminal/command prompt on your machine (navigate to Virtual Agent Directory), and enter the following command `py main.py` or `python main.py`, to initialise the FLASK application.
- Naviagate to the URL outined in the terminal - e.g. **127.0.0.1:5000** (root)
- Each of the Virtual Agents can be conversed with; Enjoy.

## Testing 

- The Javascript section of the application was tested utilising the Jasmine framework. To see the test logs, navigate to the url **127.0.0.1:5000/jasmineTests** - *Disclaimer - numerous tests are being carried out, thus, the page takes along time to load*.

- The Affectiva APK testing section of the application utilsies User Testing. To test, navigate to the url **127.0.0.1:5000/affectivaTests** - *Results of the testing are displayed within the footer of the page*

- The FLASK Testing section can only be carried out in the **terminal**. Enter the command `pytest`, while in the Affective Virtual Agent directory.