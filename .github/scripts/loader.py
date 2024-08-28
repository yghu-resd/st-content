import sys
from cryptography.fernet import Fernet
import tempfile
import os
import base64

def main():

    encryption_key = sys.argv[1]
    new_value_e = "1" if sys.argv[2].lower() == "true" else "0"
    new_value_l = sys.argv[3]
    input_image_path = sys.argv[4]
    output_image_path = sys.argv[5]


    # Initialize the Fernet cipher with the provided key
    cipher = Fernet(encryption_key)

    relative_path = os.path.join(os.path.dirname(__file__), './main.dat')

    # Read the encrypted script from main.dat
    with open(relative_path, 'rb') as encrypted_file:
        encrypted_script = encrypted_file.read()

    # Decrypt the script
    decrypted_script = cipher.decrypt(encrypted_script)

    # Determine the directory where the loader script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Convert input and output image paths to absolute paths
    input_image_abs_path = os.path.abspath(os.path.join(script_dir, input_image_path))
    output_image_abs_path = os.path.abspath(os.path.join(script_dir, output_image_path))

    # Create the temporary file in the same directory as the loader script

    temp_file_path = os.path.join(os.path.dirname(__file__), './temp_script.py')

    with open(temp_file_path, 'wb') as temp_file:
        temp_file.write(decrypted_script)

    new_value_l_encoded = base64.b64encode(new_value_l.encode()).decode()

    # Execute the decrypted script and pass new_value_e and new_value_l as arguments
    os.system(f"python {temp_file_path} {input_image_abs_path} {output_image_abs_path} {new_value_e} {new_value_l_encoded}")

    # Optionally, delete the temp file after execution
    os.remove(temp_file_path)

if __name__ == "__main__":
    main()
