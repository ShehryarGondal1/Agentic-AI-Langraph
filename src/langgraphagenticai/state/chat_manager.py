# class ChatManager:
#     def __init__(self, session_state):
#         self.session_state = session_state
#         if "chat_history" not in self.session_state:
#             self.session_state["chat_history"] = []

#     def get_history(self):
#         return self.session_state["chat_history"]

#     def add_user_message(self, content):
#         self.session_state["chat_history"].append({"role": "user", "content": content})

#     def add_bot_message(self, content):
#         self.session_state["chat_history"].append({"role": "bot", "content": content})


class ChatManager:
    def __init__(self, session_state):
        self.session_state = session_state
        if "chat_history" not in self.session_state:
            self.session_state["chat_history"] = []

    def add_user_message(self, content):
        self.session_state["chat_history"].append({
            "role": "user",
            "content": content
        })

    def add_bot_message(self, content):
        self.session_state["chat_history"].append({
            "role": "bot",
            "content": content
        })

    def get_history(self):
        return self.session_state["chat_history"]

