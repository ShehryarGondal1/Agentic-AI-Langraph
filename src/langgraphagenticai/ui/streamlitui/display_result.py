# # # # # import streamlit as st
# # # # # from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
# # # # # import json


# # # # # class DisplayResultStreamlit:
# # # # #     def __init__(self,usecase,graph,user_message):
# # # # #         self.usecase= usecase
# # # # #         self.graph = graph
# # # # #         self.user_message = user_message

# # # # #     def display_result_on_ui(self):
# # # # #         usecase= self.usecase
# # # # #         graph = self.graph
# # # # #         user_message = self.user_message
# # # # #         if usecase =="Basic Chatbot":
# # # # #                 for event in graph.stream({'messages':("user",user_message)}):
# # # # #                     print(event.values())
# # # # #                     for value in event.values():
# # # # #                         print(value['messages'])
# # # # #                         with st.chat_message("user"):
# # # # #                             st.write(user_message)
# # # # #                         with st.chat_message("assistant"):
# # # # #                             st.write(value["messages"].content)

# # # # #         elif usecase=="Chatbot with Tool":
# # # # #              # Prepare state and invoke the graph
# # # # #             initial_state = {"messages": [user_message]}
# # # # #             res = graph.invoke(initial_state)
# # # # #             for message in res['messages']:
# # # # #                 if type(message) == HumanMessage:
# # # # #                     with st.chat_message("user"):
# # # # #                         st.write(message.content)
# # # # #                 elif type(message)==ToolMessage:
# # # # #                     with st.chat_message("ai"):
# # # # #                         st.write("Tool Call Start")
# # # # #                         st.write(message.content)
# # # # #                         st.write("Tool Call End")
# # # # #                 elif type(message)==AIMessage and message.content:
# # # # #                     with st.chat_message("assistant"):
# # # # #                         st.write(message.content)

# # # # #         elif usecase == "AI News":
# # # # #             frequency = self.user_message
# # # # #             with st.spinner("Fetching and summarizing news... ⏳"):
# # # # #                 result = graph.invoke({"messages": frequency})
# # # # #                 try:
# # # # #                     # Read the markdown file
# # # # #                     AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
# # # # #                     with open(AI_NEWS_PATH, "r") as file:
# # # # #                         markdown_content = file.read()

# # # # #                     # Display the markdown content in Streamlit
# # # # #                     st.markdown(markdown_content, unsafe_allow_html=True)
# # # # #                 except FileNotFoundError:
# # # # #                     st.error(f"News Not Generated or File not found: {AI_NEWS_PATH}")
# # # # #                 except Exception as e:
# # # # #                     st.error(f"An error occurred: {str(e)}")
                    
                
# # # # #                 with open(AI_NEWS_PATH, 'r') as f:
# # # # #                     st.download_button(
# # # # #                         "💾 Download Summary",
# # # # #                         f.read(),
# # # # #                         file_name=AI_NEWS_PATH,
# # # # #                         mime="text/markdown"
# # # # #                     )
# # # # #                 st.success(f"✅ Summary saved to {AI_NEWS_PATH}")
             

# ## Recent Code Changes
# import streamlit as st
# from langchain_core.messages import HumanMessage, AIMessage
# from src.langgraphagenticai.state.chat_manager import ChatManager

# class DisplayResultStreamlit:
#     def __init__(self, usecase, graph, user_message, chat_history=None):
#         self.usecase = usecase
#         self.graph = graph
#         self.user_message = user_message
#         self.chat_history = chat_history or []

#     def display_result_on_ui(self):
#         chat_manager = ChatManager(st.session_state)

#         # Optional: Clear button (only clears session, doesn't reload page)
#         if st.button("🧹 Clear Chat"):
#             st.session_state["chat_history"] = []
#             st.experimental_rerun()

#         # Convert session history to LangChain messages for model
#         full_history = []
#         for msg in self.chat_history:
#             if msg["role"] == "user":
#                 full_history.append(HumanMessage(content=msg["content"]))
#             elif msg["role"] == "bot":
#                 full_history.append(AIMessage(content=msg["content"]))

#         # Add current message to prompt for model
#         full_history.append(HumanMessage(content=self.user_message))
#         initial_state = {"messages": full_history}

#         # Display ONLY the current user message
#         with st.chat_message("user"):
#             st.write(self.user_message)

#         # Call the model
#         result = self.graph.invoke(initial_state)

#         # Extract and display only the assistant's latest response
#         latest_reply = ""
#         for msg in result["messages"]:
#             if isinstance(msg, AIMessage) and msg.content:
#                 latest_reply = msg.content

#         if latest_reply:
#             with st.chat_message("assistant"):
#                 st.write(latest_reply)

#         # Store only the current exchange in memory
#         chat_manager.add_user_message(self.user_message)
#         chat_manager.add_bot_message(latest_reply)



import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from src.langgraphagenticai.state.chat_manager import ChatManager

class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message, chat_history=None):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message
        self.chat_history = chat_history or []

    def display_result_on_ui(self):
        chat_manager = ChatManager(st.session_state)

        # Clear button (resets frontend UI state only)
        if st.button("🧹 Clear Chat"):
            st.session_state["chat_history"] = []
            st.experimental_rerun()

        # Convert session history to LangChain messages
        full_history = []
        for msg in self.chat_history:
            if msg["role"] == "user":
                full_history.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "bot":
                full_history.append(AIMessage(content=msg["content"]))

        # Add the current user input
        full_history.append(HumanMessage(content=self.user_message))
        initial_state = {"messages": full_history}

        # Only display current user message
        with st.chat_message("user"):
            st.write(self.user_message)

        # Process by use case
        if self.usecase == "Basic Chatbot":
            result = self.graph.invoke(initial_state)
            latest_reply = ""
            for msg in result["messages"]:
                if isinstance(msg, AIMessage) and msg.content:
                    latest_reply = msg.content

            if latest_reply:
                with st.chat_message("assistant"):
                    st.write(latest_reply)
                chat_manager.add_user_message(self.user_message)
                chat_manager.add_bot_message(latest_reply)

        elif self.usecase == "Chatbot with Tool":
            result = self.graph.invoke(initial_state)
            latest_reply = ""

            for msg in result["messages"]:
                if isinstance(msg, ToolMessage):
                    with st.chat_message("ai"):
                        st.write("🔧 Tool Call Start")
                        st.write(msg.content)
                        st.write("🔧 Tool Call End")
                    chat_manager.add_bot_message(f"[Tool Response]: {msg.content}")
                elif isinstance(msg, AIMessage) and msg.content:
                    latest_reply = msg.content

            if latest_reply:
                with st.chat_message("assistant"):
                    st.write(latest_reply)
                chat_manager.add_user_message(self.user_message)
                chat_manager.add_bot_message(latest_reply)

        elif self.usecase == "AI News":
            freq = self.user_message
            with st.spinner("📰 Fetching and summarizing news..."):
                result = self.graph.invoke({"messages": freq})
                AI_NEWS_PATH = f"./AINews/{freq.lower()}_summary.md"
                try:
                    with open(AI_NEWS_PATH, "r") as f:
                        content = f.read()
                        st.markdown(content, unsafe_allow_html=True)
                        st.download_button("💾 Download Summary", content, file_name=AI_NEWS_PATH, mime="text/markdown")
                        chat_manager.add_user_message(freq)
                        chat_manager.add_bot_message(content)
                except Exception as e:
                    st.error(f"Error reading summary: {e}")
