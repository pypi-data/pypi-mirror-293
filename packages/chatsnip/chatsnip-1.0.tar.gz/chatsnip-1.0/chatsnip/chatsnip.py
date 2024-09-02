import sys
import threading
import subprocess
from chatsnip.flask_app import app as flask_app  # Import the Flask app

def run_flask():
    """Function to run the Flask app."""
    # Set the FLASK_APP environment variable
    env = {"FLASK_ENV": "development", "FLASK_APP": "chatsnip.flask_app"}
    flask_process = subprocess.Popen([sys.executable, '-m', 'flask', 'run'], env=env)
    flask_process.wait()  # Wait for the Flask process to finish

def run_streamlit():
    """Function to run the Streamlit app."""
    subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'chatsnip/streamlit_ui.py'])

def main():
    # Create threads for both Flask and Streamlit
    flask_thread = threading.Thread(target=run_flask)
    streamlit_thread = threading.Thread(target=run_streamlit)

    # Start the threads
    flask_thread.start()
    streamlit_thread.start()

    # Wait for both threads to complete
    flask_thread.join()
    streamlit_thread.join()

if __name__ == "__main__":
    main()