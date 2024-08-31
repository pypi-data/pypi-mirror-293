from langchain_community.document_loaders import (
    TextLoader, PyPDFLoader, Docx2txtLoader, UnstructuredPowerPointLoader, AssemblyAIAudioTranscriptLoader
)
import google.generativeai as genai
import mimetypes
import os
from PIL import Image

class FileRenamer:
    def __init__(self):
        self.google_api_key = "AIzaSyCBl7o6dGakLlADqrfuZmCz0GdvIOjVoqE"
        genai.configure(api_key=self.google_api_key)

    def generate_new_name(self, file_path, doc_data=None):
        # Handle text documents
        mime_type, _ = mimetypes.guess_type(file_path)
        if doc_data and mime_type not in ["image/jpeg", "image/png", "image/jpg"]:
            prompt = f"Generate a compelling title for the document by summarizing it in no more than 3 words. Replace spaces with underscores and avoid any breaks between words. Document: {doc_data}"
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            response = model.generate_content([prompt])
            root, file_extension = os.path.splitext(file_path)
            name = f"{response.text.strip().replace(' ', '_')}{file_extension}"
            return name

        # Handle images (assuming basic title generation)
        else:
            root, file_extension = os.path.splitext(file_path)
            # image = Image.open(file_path)

            prompt = f"Your task is to give a short title for the image related to the content in the image having at most 3 words. There should not be any break between words, use '_' instead of blank spaces."

            # Initialize and use the generative model for the image
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            response = model.generate_content([prompt, doc_data])
            name = f"{response.text.strip().replace(' ', '_')}{file_extension}"
            return name

    @staticmethod
    def copy_binary_file(src, dest):
        try:
            with open(src, 'rb') as f_src:
                content = f_src.read()
            with open(dest, 'wb') as f_dest:
                f_dest.write(content)
            print(f"File saved to {dest}")
        except IOError as e:
            print(f"Unable to save file. {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    @staticmethod
    def load_file(file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        loader_mapping = {
            "text/plain": TextLoader,
            "application/pdf": PyPDFLoader,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": Docx2txtLoader,
            "application/vnd.openxmlformats-officedocument.presentationml.presentation": UnstructuredPowerPointLoader,
        }

        if mime_type in loader_mapping:
            loader = loader_mapping[mime_type](file_path)
            return loader.load_and_split() if mime_type == "application/pdf" else loader.load()

        elif mime_type in ["image/jpeg", "image/png", "image/jpg"]:
            image = Image.open(file_path)
            return image

        else:
            print(f"The file type of {file_path} is not supported.")
            return None

    def rename_file(self, file_path, dest_path='./'):
        loaded_data = self.load_file(file_path)
        if loaded_data:
            print("Renaming the file>>>>>>>>")
            new_name = self.generate_new_name(file_path, loaded_data)
            # dest = f"{dest_path}{new_name}"
            dest = f"{dest_path.rstrip('/')}/{new_name}"
            self.copy_binary_file(file_path, dest)
            print(f"File saved as: {new_name}")
            
        else:
            print("Failed to load the file content.")

