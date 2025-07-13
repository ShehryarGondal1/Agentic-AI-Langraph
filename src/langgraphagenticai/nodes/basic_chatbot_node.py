# # from src.langgraphagenticai.state.state import State

# # class BasicChatbotNode:
# #     """
# #     Basic chatbot logic implementation.
# #     """
# #     def __init__(self,model):
# #         self.llm = model

# #     def process(self, state: State) -> dict:
# #         """
# #         Processes the input state and generates a chatbot response.
# #         """
# #         return {"messages":self.llm.invoke(state['messages'])}


# from langchain_core.messages import HumanMessage, AIMessage
# from src.langgraphagenticai.state.state import State
# from groq import Groq
# import os

# from dotenv import load_dotenv
# load_dotenv()

# import os
# api_key = os.getenv("GROQ_API_KEY")


# # Initialize Groq client
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# class BasicChatbotNode:
#     """
#     Basic chatbot logic using Groq + LangGraph.
#     """

#     def __init__(self, model):
#         self.model_name = model

#     def process(self, state: State) -> dict:
#         messages = state.get("messages", [])
#         if not messages:
#             return {"messages": []}

#         chat_payload = [
#             {
#                 "role": "system",
#                 "content": "You are a friendly AI assistant called Alpaca."
#             }
#         ]

#         # Convert LangChain message objects to dict format
#         for msg in messages:
#             if isinstance(msg, HumanMessage):
#                 chat_payload.append({"role": "user", "content": msg.content})
#             elif isinstance(msg, AIMessage):
#                 chat_payload.append({"role": "assistant", "content": msg.content})

#         # Groq API call
#         try:
#             response = client.chat.completions.create(
#                 model=self.model_name,
#                 messages=chat_payload
#             )
#             assistant_text = response.choices[0].message.content.strip()
#         except Exception as e:
#             assistant_text = f"Error: {e}"

#         messages.append(AIMessage(content=assistant_text))
#         return {"messages": messages}


from langchain_core.messages import HumanMessage, AIMessage
from src.langgraphagenticai.state.state import State

class BasicChatbotNode:
    """
    Basic chatbot node that supports full conversation memory using LangGraph + ChatGroq.
    """

    def __init__(self, model):
        self.llm = model  # Expecting LangChain's ChatGroq instance

    def process(self, state: State) -> dict:
        """
        Receives the current state with previous messages and returns updated messages.
        Maintains conversation history using LangGraph's state flow.
        """
        # Get full chat history
        messages = state.get("messages", [])

        # Safety check
        if not messages or not isinstance(messages, list):
            return {"messages": []}

        try:
            # Call Groq LLM with chat history
            response = self.llm.invoke(messages)  # messages is a list of HumanMessage / AIMessage

            # Append AI's reply to history
            messages.append(AIMessage(content=response.content))

        except Exception as e:
            # Append error message if anything goes wrong
            messages.append(AIMessage(content=f"Error occurred: {str(e)}"))

        # Return updated state with memory
        return {"messages": messages}
