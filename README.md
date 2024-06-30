# Chatbot Application (LangChain)

This is a Python Flask application that implements a chatbot using OpenAI's GPT-3.5 turbo model and langchain. The chatbot application is designed to process user inputs, generate responses using the GPT-3.5 model, and manage user data and conversation history with LangChain.

## License

This project is licensed under the terms of the MIT license.

## Installation

To install the application, you need to have Python installed on your machine. You also need to install the required Python packages. 

First, create a virtual environment to isolate the dependencies for this project:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Then, install the required packages:

```bash
pip install -r requirements.txt
```

Next, set up your environment variables:

```bash
cp .env.sample .env
# Open .env and replace the placeholders with your actual values
```

## Structure

The application is structured into five main Python files:

1. `app.py`: The main Flask application file.
2. `Chatbot.py`: Defines the Chatbot class for managing users.
3. `User.py`: Defines the User class for generating responses.
4. `memory.py`: Provides functions for managing conversation history.
5. `config.py`: Sets up logging and retrieves environment variables.

## Usage

To run the application:

```bash
python app.py
```

The application listens for HTTP POST requests on the `/process` endpoint. The POST request should contain a JSON object with:

- `username`: The username of the user.
- `message_input`: The message input from the user.
- `input_type`: The type of the input (currently, only 'text' is supported).

## Development Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Setup pre-commit hooks: 
   ```
   pre-commit install
   ```

## Testing

This project includes both unit tests and functional tests.

To run only unit tests:
```bash
python -m unittest tests.test_unit_all
```

To run only functional tests:
```bash
python -m unittest tests.test_functional
```

To run all tests (unit and functional):
```bash
python -m unittest discover tests
```

Note: Functional tests require a running MongoDB instance and will use your OpenAI API key.

## Development Workflow

1. Make your changes in a new git branch.
2. Ensure that the pre-commit hooks are installed (see Development Setup).
3. Commit your changes. The pre-commit hook will automatically run unit tests.
4. Push your branch and create a Pull Request to the main branch.
5. GitHub Actions will automatically run both unit and functional tests on your PR.
6. Ensure all tests pass before merging the PR.

## Continuous Integration

This project uses GitHub Actions for continuous integration. Every pull request to the main branch will trigger:

- Unit tests
- Functional tests (including database interactions)

Ensure that all tests pass before merging pull requests.

## Contributing

Contributions are welcome. Please submit a pull request if you want to propose changes.

## Support

If you encounter any issues or have any questions, please open an issue on GitHub.

## Authors and Acknowledgement

This project was created by Charles Adedotun.