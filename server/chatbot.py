from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_linkedin_reply(comment, context="professional"):
    if not comment or not comment.strip():
        raise ValueError("Comment must not be empty.")

    try:
        prompt = f"""
You are replying to a LinkedIn post in a {context} tone.

Original comment:
\"\"\"{comment}\"\"\"

[Start by acknowledging the key challenge, trend, or insight raised by the poster—especially as it relates to legal workflows, client demands, or operational inefficiencies. Then, share a concise perspective on how AI-powered tools—like Retrieval-Augmented Generation (RAG), workflow automation, intelligent intake systems, or data-driven web applications—can streamline legal processes, reduce risk, and improve client experience. Highlight how combining AI engineering, data analytics, and custom app development creates scalable, compliant solutions that empower legal teams. End with a subtle, approachable mention that you help law firms unlock these efficiencies through tailored, end-to-end AI and tech solutions.]
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional LinkedIn engagement expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        raise Exception(f"Failed to generate reply: {str(e)}")
