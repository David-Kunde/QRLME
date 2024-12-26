import os
import random

def generate_dataset(folder_name, file_prefix, num_files, min_file_size_kb, max_file_size_kb, min_num_length, max_num_length):
    """
    Generates multiple text files of random sizes filled with random numbers.

    Args:
        folder_name (str): Name of the folder to save the files in.
        file_prefix (str): Prefix for the generated file names.
        num_files (int): Number of files to generate.
        min_file_size_kb (int): Minimum file size in kilobytes.
        max_file_size_kb (int): Maximum file size in kilobytes.
        min_num_length (int): Minimum length of the random numbers.
        max_num_length (int): Maximum length of the random numbers.
    """
    if min_file_size_kb > max_file_size_kb:
        raise ValueError("min_file_size_kb must be less than or equal to max_file_size_kb.")
    if min_num_length > max_num_length or not (5 <= min_num_length <= 20 and 5 <= max_num_length <= 20):
        raise ValueError("min_num_length and max_num_length must be between 5 and 20, and min_num_length <= max_num_length.")

    # Ensure the folder exists
    os.makedirs(folder_name, exist_ok=True)

    for i in range(1, num_files + 1):
        # Generate a random file size within the specified range
        target_size_kb = random.randint(min_file_size_kb, max_file_size_kb)
        target_size_bytes = target_size_kb * 1024

        file_name = os.path.join(folder_name, f"{file_prefix}_{i}.txt")
        with open(file_name, "w") as file:
            while os.path.getsize(file_name) < target_size_bytes:
                # Generate a random number length within the specified range
                num_length = random.randint(min_num_length, max_num_length)
                random_number = str(random.randint(10**(num_length-1), 10**num_length - 1))
                file.write(random_number + "\n")
        
        print(f"File '{file_name}' created with size approximately {target_size_kb} KB.")

generate_dataset(
    folder_name="dataset",
    file_prefix="data",
    num_files=20,
    min_file_size_kb=1,
    max_file_size_kb=50,
    min_num_length=5,
    max_num_length=18
)
