

#create virtual environment
python -m venv venv

# Run the virtual environment
.venv\Scripts\activate.bat

#Install the required packages
pip install -r requirements.txt

#Deactivate the virtual environment
deactivate


if __name__ == "__main__":