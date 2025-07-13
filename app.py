from src.langgraphagenticai.main import load_langgraph_agenticai_app


if __name__=="__main__":
    load_langgraph_agenticai_app()


# import os

# def analyze_directory(directory_path, exclude_dirs=None):
#     if exclude_dirs is None:
#         exclude_dirs = {"__pycache__", "venv", ".git"}

#     folder_count = 0
#     file_count = 0
#     folder_history = []

#     for root, dirs, files in os.walk(directory_path):
#         # Exclude unwanted folders
#         dirs[:] = [d for d in dirs if d not in exclude_dirs]

#         folder_history.append(root)
#         folder_count += len(dirs)
#         file_count += len(files)

#     return folder_history, folder_count, file_count


# # Path to your src folder
# base_path = r"D:\JupyterNotebook\Project1_Langraph_Builder\src"

# history, folders, files = analyze_directory(base_path)

# print("📁 Folder History (excluding '__pycache__'):")
# for path in history:
#     print(" -", path)

# print(f"\n📦 Total Folders (excluding '__pycache__'): {folders}")
# print(f"📄 Total Files: {files}")

