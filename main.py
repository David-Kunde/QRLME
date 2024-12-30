import random
import time
import os
import csv
from datetime import datetime

class QRLME:
    def __init__(self, primes):
        self.primes = primes
        self.secret_key = self.generate_secret_key()

    def generate_secret_key(self):
        """Generate the secret key as the product of primes."""
        key = 1
        for p in self.primes:
            key *= p
        return key

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using modular arithmetic.
        Adds a small random noise to enhance security.
        """
        noise = random.randint(1, 10)  # Add a small random noise
        ciphertext = {}
        for p in self.primes:
            ciphertext[p] = (plaintext + noise * self.secret_key) % p
        return ciphertext

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext by finding common values across primes.
        Uses brute force to match modular equivalences.
        """
        for possible_plaintext in range(self.secret_key):
            valid = True
            for p in self.primes:
                if possible_plaintext % p != ciphertext[p]:
                    valid = False
                    break
            if valid:
                return possible_plaintext
        return None  # Shouldn't happen if ciphertext is valid

    def add(self, ciphertext1, ciphertext2):
        """
        Additive homomorphism:
        Performs modular addition of two ciphertexts.
        """
        result = {}
        for p in self.primes:
            result[p] = (ciphertext1[p] + ciphertext2[p]) % p
        return result

    def multiply(self, ciphertext1, ciphertext2):
        """
        Multiplicative homomorphism:
        Performs modular multiplication of two ciphertexts.
        """
        result = {}
        for p in self.primes:
            result[p] = (ciphertext1[p] * ciphertext2[p]) % p
        return result

    def encrypt_file(self, filename):
        """Encrypts a file, line by line, and times the whole process."""
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Start timing the encryption process
        start_time = time.time()
        ciphertexts = []
        for line in lines:
            plaintext = int(line.strip())  # Assuming the file has integers on each line
            ciphertext = self.encrypt(plaintext)
            ciphertexts.append(ciphertext)
        
        # End timing the encryption process
        end_time = time.time()
        encryption_time = end_time - start_time

        return ciphertexts, encryption_time

    def decrypt_file(self, ciphertexts):
        """Decrypts a list of ciphertexts and times the whole process."""
        start_time = time.time()
        decrypted_values = []
        for ciphertext in ciphertexts:
            decrypted = self.decrypt(ciphertext)
            decrypted_values.append(decrypted)
        
        end_time = time.time()
        decryption_time = end_time - start_time

        return decrypted_values, decryption_time

    def process_multiple_files(self, folder_path):
        """Process all files in the folder, record file details, and times."""
        results = []

        # Get all .txt files in the specified folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                filepath = os.path.join(folder_path, filename)
                file_size = os.path.getsize(filepath)  # Get file size in bytes

                # Encrypt and decrypt the file
                ciphertexts, encryption_time = self.encrypt_file(filepath)
                decrypted_values, decryption_time = self.decrypt_file(ciphertexts)

                # Store results for the file
                results.append({
                    'file_name': filename,
                    'file_size (in bytes)': file_size,
                    'encryption_time (in seconds)': encryption_time,
                    'decryption_time (in seconds)': decryption_time
                })

        return results

    def save_results_to_csv(self, results):
        """Save the results to a CSV file with a timestamped filename."""
        try:
            # Generate a timestamp for the file name
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            output_file = f'QRLME_{timestamp}.csv'

            # Ensure the folder exists or create it
            os.makedirs('output', exist_ok=True)

            # Save results to CSV in the 'output' directory
            with open(os.path.join('output', output_file), mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['file_name', 'file_size (in bytes)', 'encryption_time (in seconds)', 'decryption_time (in seconds)'])
                writer.writeheader()
                for result in results:
                    writer.writerow(result)

            print(f"\nResults saved to {os.path.join('output', output_file)}")

        except Exception as e:
            print(f"Error saving results: {e}")


if __name__ == "__main__":
    # Initialize with small primes
    primes = [2, 3, 5, 7, 11]
    qrlme = QRLME(primes)

    #  folder where dataset is located
    folder_path = 'dataset'

    # Process all files in the folder
    results = qrlme.process_multiple_files(folder_path)

    # Print results to the console
    for result in results:
        print(f"File: {result['file_name']}, Size: {result['file_size (in bytes)']} bytes, "
              f"Encryption Time: {result['encryption_time (in seconds)']:.5f} seconds, "
              f"Decryption Time: {result['decryption_time (in seconds)']:.5f} seconds")

    # Save results to CSV
    qrlme.save_results_to_csv(results)
