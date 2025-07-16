# AI/LLM Engineer Intern Assignment - Reddit User Persona Generator

This project is a submission for the AI/LLM Engineer internship assignment at BeyondChats. It is a Python script that takes a Reddit user's profile URL, scrapes their recent posts and comments, and uses Google's Gemini LLM to generate a detailed user persona with citations for each characteristic.

## Features

-   **Reddit Scraping**: Utilizes PRAW to fetch user posts and comments.
-   **AI-Powered Persona**: Leverages the Gemini 1.5 Flash model to analyze text and generate an insightful user persona.
-   **Cited Conclusions**: Each point in the persona is backed by a citation (a permalink to the source post or comment).
-   **Secure**: Manages API keys securely using a `.env` file.
-   **CLI Interface**: Easy to run from the command line with a single argument.

## Project Structure

```
.
├── .env                  # Stores API keys (not for commit)
├── .gitignore            # Specifies files to ignore for Git
├── README.md             # This file
├── main.py               # The main executable Python script
├── requirements.txt      # Project dependencies
├── kojied_persona.txt
```

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Prerequisites

-   Python 3.8+
-   Git

### 2. Clone the Repository

```bash
git clone <your-github-repo-link>
cd beyondchats-assignment
```

### 3. Set Up a Virtual Environment (Recommended)

```bash
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API Keys

You need API keys from both Reddit and Google AI.

1.  Create a file named `.env` in the root of the project directory.
2.  Add your credentials to the `.env` file in the following format:

    ```env
    REDDIT_CLIENT_ID='YOUR_REDDIT_CLIENT_ID'
    REDDIT_CLIENT_SECRET='YOUR_REDDIT_CLIENT_SECRET'
    REDDIT_USER_AGENT='u/YourUsername' # Replace with your Reddit username
    GEMINI_API_KEY='YOUR_GEMINI_API_KEY'
    ```


## How to Execute the Script

Run the script from your terminal using the following command, replacing the URL with your target Reddit user profile:

```bash
python main.py <reddit_user_url>
```

**Examples:**

```bash
python main.py https://www.reddit.com/user/kojied/

```bash
python main.py https://www.reddit.com/user/Hungry-Move-6603/

The script will:
1.  Scrape the user's data.
2.  Call the LLM to generate the persona.
3.  Create a text file (e.g., `kojied_persona.txt`) in the root directory with the final output.