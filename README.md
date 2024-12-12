# Nexagen-Task

A tool that connects to an email server, retrieves unread emails, processes them to extract key information (like subject, sender, and timestamp), and stores the data in a local database.

## Running Instructions

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/Nexagen-Task.git
    cd Nexagen-Task
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables for your email credentials:

    ```sh
    export IMAP_EMAIL=your-email@example.com
    export IMAP_PASSWORD=your-email-password
    ```

5. Run the application:

    ```sh
    python app.py
    ```

6. Access the application in your browser at `http://127.0.0.1:5000/`

7. Logs can be found in the `scheduler.log` file.
