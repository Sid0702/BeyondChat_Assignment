import os
import sys
import praw
import google.generativeai as genai
from dotenv import load_dotenv

# --- CONFIGURATION & CONSTANTS ---

# Load environment variables from a .env file
load_dotenv()

# Updated constant for the LLM prompt based on the new template
PERSONA_PROMPT_TEMPLATE = """
Based on the following Reddit posts and comments for the user '{username}', create a detailed user persona.
Analyze the provided data to infer the user's demographics, personality, behaviors, motivations, goals, and frustrations.
For every piece of information you infer, you MUST provide a direct citation link (the permalink provided with each piece of content) as the source.
If a specific piece of information (like Age or Location) cannot be found, state "Not specified in data".
Synthesize a representative quote based on the overall tone and content of their comments.

**IMPORTANT**: Structure your output *exactly* as follows. Do not add any extra sections or commentary.

==================================================
        USER PERSONA: {username}
==================================================

QUOTE:
"[A concise, representative quote synthesized by the LLM]"
(Source: General sentiment from multiple comments)

---

DEMOGRAPHICS:
* AGE: [e.g., Estimated 25-30 or "Not specified in data"] (Source: [permalink] or "N/A")
* LOCATION: [e.g., Likely USA West Coast or "Not specified in data"] (Source: [permalink] or "N/A")
* OCCUPATION: [e.g., Software Developer or "Not specified in data"] (Source: [permalink] or "N/A")
* STATUS: [e.g., Student or "Not specified in data"] (Source: [permalink] or "N/A")

---

PERSONALITY SUMMARY:
* The user appears to be [analytical, helpful, and detail-oriented]. (Source: [permalink], [permalink], ...)
* They exhibit traits of an [e.g., Introvert], preferring to engage in focused, topic-specific discussions. (Source: [permalink], ...)

---

BEHAVIOUR & HABITS:
* Actively contributes to subreddits related to [e.g., Python programming and data science]. (Source: [permalink], ...)
* [Describe another habit, e.g., "Often helps beginners by answering their technical questions."]. (Source: [permalink], ...)
* [Describe another habit, e.g., "Seems to be a nocturnal user, with most activity occurring during late-night hours UTC."]. (Source: Analysis of post timestamps)

---

MOTIVATIONS:
* KNOWLEDGE SHARING: Driven by a desire to help others and share their expertise. (Source: [permalink], ...)
* PROBLEM SOLVING: Enjoys tackling complex logical problems presented in posts. (Source: [permalink], ...)
* COMMUNITY: Values being part of a community of like-minded individuals. (Source: [permalink], ...)

---

GOALS & NEEDS:
* GOAL: Seems to be building a reputation as an expert in their field. (Source: [permalink], ...)
* NEED: Requires clear, well-defined problems to engage with. (Source: [permalink], ...)

---

FRUSTRATIONS:
* Dislikes vague or poorly-asked questions. (Source: [permalink], ...)
* Expresses frustration with misinformation or incorrect technical advice. (Source: [permalink], ...)

---
**Reddit Data provided for analysis:**
{reddit_data}
"""

# --- API CLIENT SETUP ---

def initialize_clients():
    """Initializes and returns the PRAW and Gemini API clients."""
    try:
        reddit_client = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT"),
        )
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        llm_client = genai.GenerativeModel('gemini-1.5-flash')
        return reddit_client, llm_client
    except Exception as e:
        print(f"Error: Failed to initialize API clients. Check .env file and credentials. Details: {e}")
        sys.exit(1)

# --- CORE FUNCTIONS ---

def scrape_reddit_data(reddit_client, username: str, limit: int = 50) -> list:
    """Scrapes a user's recent posts and comments."""
    print(f"Scraping data for user: {username}...")
    try:
        redditor = reddit_client.redditor(username)
        data = set()
        for post in redditor.submissions.new(limit=limit):
            content = f"Post Title: {post.title}\nPost Body: {post.selftext}"
            data.add(f"Content: {content}\nCitation: https://www.reddit.com{post.permalink}\n---")
        for comment in redditor.comments.new(limit=limit):
            data.add(f"Content: Comment: {comment.body}\nCitation: https://www.reddit.com{comment.permalink}\n---")
        
        print(f"Scraping complete. Found {len(data)} unique items.")
        return list(data)
    except Exception as e:
        print(f"Error: Could not scrape data for user '{username}'. Details: {e}")
        return []

def generate_user_persona(llm_client, username: str, user_data: list) -> str:
    """Generates a user persona using the LLM."""
    if not user_data:
        return "Could not generate persona due to lack of data."

    print("Generating user persona with the language model...")
    prompt = PERSONA_PROMPT_TEMPLATE.format(username=username, reddit_data="\n".join(user_data))
    
    try:
        response = llm_client.generate_content(prompt)
        print("Persona generated.")
        return response.text
    except Exception as e:
        return f"Error: LLM failed to generate persona. Details: {e}"

# --- SCRIPT EXECUTION ---

def main():
    """Main function to run the script."""
    if len(sys.argv) != 2:
        print("Usage: python main.py <reddit_user_url>")
        print("Example: python main.py https://www.reddit.com/user/kojied/")
        return

    try:
        reddit_url = sys.argv[1]
        # Robustly extracts username, handling trailing slashes
        username = reddit_url.strip('/').split('/user/')[1]
    except IndexError:
        print("Error: Invalid Reddit user URL format. Must be like 'https://www.reddit.com/user/username/'.")
        return

    reddit_client, llm_client = initialize_clients()
    
    scraped_content = scrape_reddit_data(reddit_client, username)
    if not scraped_content:
        return

    persona = generate_user_persona(llm_client, username, scraped_content)

    output_filename = f"{username}_persona.txt" # Changed to .md for better readability
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(persona)
    print(f"Success! Persona saved to '{output_filename}'")


if __name__ == "__main__":
    main()