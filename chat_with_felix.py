import os
import openai
import json


def analyze_excerpt(excerpt):
    common_questions = [
        "Tell me about a time when you had to prioritize certain product features over others. How did you make your decision?",
        "Describe a situation where you had to work with a difficult stakeholder. How did you handle it?",
        "Give an example of a successful product launch you managed. What was your strategy?",
        "Tell me about a time when you used data to make a product decision. What was the outcome?",
        "Explain a scenario where you had to pivot your product strategy. What led to that decision?",
        "Describe how you work with engineering teams to meet product deadlines.",
        "Tell me about a product failure you experienced. What did you learn from it?",
        "How do you gather user feedback, and how does it influence your product decisions?",
        "Give an example of how you've handled competing priorities across different projects.",
        "Describe a time when you had to advocate for user needs that were not initially recognized by your team.",
    ]
    # Assuming you have set OPENAI_API_KEY in your environment variables
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Provide your answers to the below prompt in JSON format with the following keys: has_interview_question, interview_question, reasoning",
                },
                {
                    "role": "system",
                    "content": f"""
                    You are an intelligent assistant analyzing interview transcripts. Your task is to extract important interview questions, ignoring any clarification questions such as 'right?' or small talk like 'how are you doing today?' AND explain your reasoning. Focus on identifying substantial questions that contribute to understanding the interviewee's experience and qualifications. Here are examples for guidance:

                    Example 1:
                    User: "What projects have you worked on that you're particularly proud of?"
                    Assistant: This is an important interview question focusing on the candidate's past work.

                    Example 2:
                    User: "You're familiar with Python, right?"
                    Assistant: This is a clarification question and should be ignored.

                    Example 3:
                    User: "How are you doing today?"
                    Assistant: This is small talk and should be disregarded.
                    
                    Example 3:
                    User: "Why don't you start with a brief intro?"
                    Assistant: This is an essential interview question
                

                    Based on this guidance, analyze the following conversation excerpt for important interview questions: \"{excerpt}\"
                    """,
                },
                {
                    "role": "system",
                    "content": "You always provide your reasoning for determining the intervieq question (if applicable) by starting the explanation with 'Reasoning'",
                },
            ],
            temperature=0.7,
            max_tokens=512,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        # Extract the full response text correctly
        response_text = (
            response.choices[0].message["content"]
            if "message" in response.choices[0]
            else response.choices[0].get("text", "").strip()
        )
        response_data = json.loads(response_text)

        has_interview_question = response_data.get("has_interview_question", False)
        interview_question = response_data.get("interview_question", "")
        reasoning = response_data.get("reasoning", "No reasoning provided.")

        return {
            "has_interview_question": has_interview_question,
            "interview_question": interview_question,
            "reasoning": reasoning,
        }
    except Exception as e:
        print("Error:", str(e))
        return {
            "contains_question": False,
            "detected_question": "",
            "reasoning": "Error occurred.",
        }


if __name__ == "__main__":
    print(
        "Felix: Hi there. I am Felix, the chatbot. Please share the excerpt you would like me to analyze"
    )
    user_message = input("You: ")
    response = analyze_excerpt(user_message)
    print(
        f"Contains Question: {response['has_interview_question']}, Detected Question: '{response['interview_question']}', Reasoning: '{response['reasoning']}'"
    )
