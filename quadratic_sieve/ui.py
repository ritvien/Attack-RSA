import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from quadratic_sieve import *
import quadratic_sieve
class QuadraticSieveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quadratic Sieve - RSA Factorization")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Setup variables
        self.number_to_factor = tk.StringVar()
        self.factor_base_size = tk.StringVar(value="20")
        self.bound = tk.StringVar(value="100")
        self.result_text = tk.StringVar()
        self.is_factoring = False
        self.progress_var = tk.DoubleVar()
        
        # RSA variables
        self.rsa_n = tk.StringVar()
        self.rsa_e = tk.StringVar(value="65537")
        self.rsa_c = tk.StringVar()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.factor_tab = ttk.Frame(self.notebook)
        self.rsa_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.factor_tab, text="Integer Factorization")
        self.notebook.add(self.rsa_tab, text="RSA Decryption")
        
        # Create factorization tab
        self.create_factorization_tab()
        
        # Create RSA tab
        self.create_rsa_tab()
        
        # Create status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#ccc")
        self.style.configure("TLabel", background="#f0f0f0")
        self.style.configure("TFrame", background="#f0f0f0")
        
    def create_factorization_tab(self):
        # Input frame
        input_frame = ttk.LabelFrame(self.factor_tab, text="Input", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Number to factor
        ttk.Label(input_frame, text="Number to factor:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.number_to_factor, width=50).grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Parameters frame
        param_frame = ttk.LabelFrame(self.factor_tab, text="Algorithm Parameters", padding=10)
        param_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Factor base size
        ttk.Label(param_frame, text="Factor Base Size:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(param_frame, textvariable=self.factor_base_size, width=10).grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Label(param_frame, text="(higher = better chance but slower)").grid(row=0, column=2, sticky=tk.W, pady=5)
        
        # Bound
        ttk.Label(param_frame, text="Search Bound:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(param_frame, textvariable=self.bound, width=10).grid(row=1, column=1, sticky=tk.W, pady=5)
        ttk.Label(param_frame, text="(higher = more smooth numbers but slower)").grid(row=1, column=2, sticky=tk.W, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(self.factor_tab)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Start factorization button
        self.factor_button = ttk.Button(button_frame, text="Start Factorization", command=self.start_factorization)
        self.factor_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        ttk.Button(button_frame, text="Clear", command=self.clear_factorization).pack(side=tk.LEFT, padx=5)
        
        # Example button
        ttk.Button(button_frame, text="Load Example", 
                  command=lambda: self.number_to_factor.set("8927")).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.factor_tab, orient=tk.HORIZONTAL, 
                                       length=100, mode='indeterminate', variable=self.progress_var)
        self.progress.pack(fill=tk.X, padx=10, pady=10)
        
        # Results frame
        result_frame = ttk.LabelFrame(self.factor_tab, text="Results", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=10)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
    def create_rsa_tab(self):
        # Input frame
        rsa_input_frame = ttk.LabelFrame(self.rsa_tab, text="RSA Parameters", padding=10)
        rsa_input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # RSA modulus N
        ttk.Label(rsa_input_frame, text="Modulus (N):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(rsa_input_frame, textvariable=self.rsa_n, width=50).grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Public exponent e
        ttk.Label(rsa_input_frame, text="Public Exponent (e):").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(rsa_input_frame, textvariable=self.rsa_e, width=50).grid(row=1, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Ciphertext c
        ttk.Label(rsa_input_frame, text="Ciphertext (c):").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(rsa_input_frame, textvariable=self.rsa_c, width=50).grid(row=2, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Button frame
        rsa_button_frame = ttk.Frame(self.rsa_tab)
        rsa_button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Decrypt button
        self.decrypt_button = ttk.Button(rsa_button_frame, text="Factor and Decrypt", command=self.start_rsa_decryption)
        self.decrypt_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        ttk.Button(rsa_button_frame, text="Clear", command=self.clear_rsa).pack(side=tk.LEFT, padx=5)
        
        # Example button
        ttk.Button(rsa_button_frame, text="Load Example", 
                  command=lambda: [self.rsa_n.set("8927"), self.rsa_e.set("3"), self.rsa_c.set("13")]).pack(side=tk.LEFT, padx=5)
        
        # Progress bar for RSA
        self.rsa_progress = ttk.Progressbar(self.rsa_tab, orient=tk.HORIZONTAL, 
                                           length=100, mode='indeterminate', variable=self.progress_var)
        self.rsa_progress.pack(fill=tk.X, padx=10, pady=10)
        
        # Results frame
        rsa_result_frame = ttk.LabelFrame(self.rsa_tab, text="RSA Decryption Results", padding=10)
        rsa_result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Output text area for RSA
        self.rsa_output_text = scrolledtext.ScrolledText(rsa_result_frame, wrap=tk.WORD, height=10)
        self.rsa_output_text.pack(fill=tk.BOTH, expand=True)
        
    def start_factorization(self):
        if self.is_factoring:
            messagebox.showinfo("Info", "Factorization already in progress!")
            return
        
        try:
            n = int(self.number_to_factor.get())
            factor_base_size = int(self.factor_base_size.get())
            bound = int(self.bound.get())
            
            if n <= 1:
                messagebox.showerror("Error", "Please enter a number greater than 1.")
                return
            
            # Clear previous results
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Starting factorization of {n}...\n")
            
            # Start progress bar
            self.progress.start()
            self.is_factoring = True
            self.factor_button.state(['disabled'])
            self.status_var.set("Factoring...")
            
            # Run factorization in a separate thread
            threading.Thread(target=self.run_factorization, args=(n, factor_base_size, bound)).start()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer values.")
            
    def run_factorization(self, n, factor_base_size, bound):
        try:
            start_time = time.time()
            factors = quadratic_sieve.factorize(n, bound, factor_base_size)
            elapsed_time = time.time() - start_time
            
            # Update UI in the main thread
            self.root.after(0, self.update_factorization_results, n, factors, elapsed_time)
            
        except Exception as e:
            self.root.after(0, self.show_error, f"Error during factorization: {str(e)}")
        finally:
            self.root.after(0, self.reset_factorization_ui)
            
    def update_factorization_results(self, n, factors, elapsed_time):
        self.output_text.insert(tk.END, f"\nFactorization completed in {elapsed_time:.4f} seconds\n")
        self.output_text.insert(tk.END, f"\nFactors of {n} are:\n")
        
        # Display factors
        if factors:
            factors_dict = {}
            for factor in factors:
                if factor in factors_dict:
                    factors_dict[factor] += 1
                else:
                    factors_dict[factor] = 1
            
            # Display in prime power form
            result_str = " × ".join([f"{factor}^{power}" if power > 1 else str(factor) 
                                    for factor, power in factors_dict.items()])
            self.output_text.insert(tk.END, result_str + "\n")
            
            # Verify the result
            product = 1
            for factor, power in factors_dict.items():
                product *= factor ** power
                
            if product == n:
                self.output_text.insert(tk.END, "\nVerification: CORRECT ✓\n")
            else:
                self.output_text.insert(tk.END, f"\nVerification: INCORRECT ✗ (product = {product})\n")
        else:
            self.output_text.insert(tk.END, "No factors found. The number might be prime or too large for this implementation.\n")
            
    def reset_factorization_ui(self):
        self.progress.stop()
        self.is_factoring = False
        self.factor_button.state(['!disabled'])
        self.status_var.set("Ready")
        
    def clear_factorization(self):
        self.number_to_factor.set("")
        self.output_text.delete(1.0, tk.END)
        self.factor_base_size.set("20")
        self.bound.set("100")
        
    def start_rsa_decryption(self):
        if self.is_factoring:
            messagebox.showinfo("Info", "Operation already in progress!")
            return
        
        try:
            n = int(self.rsa_n.get())
            e = int(self.rsa_e.get())
            c = int(self.rsa_c.get())
            
            if n <= 1:
                messagebox.showerror("Error", "Please enter a valid modulus N greater than 1.")
                return
            
            # Clear previous results
            self.rsa_output_text.delete(1.0, tk.END)
            self.rsa_output_text.insert(tk.END, f"Starting RSA decryption with N={n}, e={e}, c={c}...\n")
            self.rsa_output_text.insert(tk.END, "First step: Factoring N using Quadratic Sieve...\n")
            
            # Start progress bar
            self.rsa_progress.start()
            self.is_factoring = True
            self.decrypt_button.state(['disabled'])
            self.status_var.set("Factoring for RSA...")
            
            # Run decryption in a separate thread
            threading.Thread(target=self.run_rsa_decryption, args=(n, e, c)).start()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer values.")
            
    def run_rsa_decryption(self, n, e, c):
        try:
            start_time = time.time()
            
            # Step 1: Factor N
            factors = factorize(n)
            factoring_time = time.time() - start_time
            
            # Step 2: Use factors to decrypt
            if len(factors) >= 2:
                # Assuming N is a product of two primes p and q
                # If more factors, we'll need to combine them
                if len(factors) == 2:
                    p, q = factors
                else:
                    # In case we have more than 2 factors (e.g., p^a * q^b)
                    # Group them to form p and q
                    from sympy import factorint
                    factor_dict = factorint(n)
                    p = list(factor_dict.keys())[0]
                    q = n // p
                
                # Decrypt
                plaintext, d = rsa_decrypt_with_factors(n, e, c, p, q)
                total_time = time.time() - start_time
                
                # Update UI in the main thread
                self.root.after(0, self.update_rsa_results, n, e, c, p, q, plaintext, d, factoring_time, total_time)
            else:
                self.root.after(0, lambda: self.rsa_output_text.insert(
                    tk.END, "\nCould not factor N into two distinct primes. RSA decryption failed.\n"))
                
        except Exception as e:
            self.root.after(0, self.show_error, f"Error during RSA decryption: {str(e)}")
        finally:
            self.root.after(0, self.reset_rsa_ui)
            
    def update_rsa_results(self, n, e, c, p, q, plaintext, d, factoring_time, total_time):
        self.rsa_output_text.insert(tk.END, f"\nFactorization completed in {factoring_time:.4f} seconds\n")
        self.rsa_output_text.insert(tk.END, f"N = {n} = {p} × {q}\n")
        self.rsa_output_text.insert(tk.END, f"\nCalculating private key d...\n")
        self.rsa_output_text.insert(tk.END, f"φ(N) = (p-1)(q-1) = {(p-1)*(q-1)}\n")
        self.rsa_output_text.insert(tk.END, f"d = e^(-1) mod φ(N) = {d}\n")
        self.rsa_output_text.insert(tk.END, f"\nDecrypting ciphertext: m = c^d mod N\n")
        self.rsa_output_text.insert(tk.END, f"Plaintext (decimal): {plaintext}\n")
        
        # Try to interpret as ASCII if in range
        try:
            ascii_text = ""
            temp = plaintext
            while temp > 0:
                char = temp % 256
                if 32 <= char <= 126:  # Printable ASCII range
                    ascii_text = chr(char) + ascii_text
                temp //= 256
            
            if ascii_text:
                self.rsa_output_text.insert(tk.END, f"Potential ASCII interpretation: {ascii_text}\n")
        except:
            pass
            
        self.rsa_output_text.insert(tk.END, f"\nTotal operation completed in {total_time:.4f} seconds\n")
            
    def reset_rsa_ui(self):
        self.rsa_progress.stop()
        self.is_factoring = False
        self.decrypt_button.state(['!disabled'])
        self.status_var.set("Ready")
        
    def clear_rsa(self):
        self.rsa_n.set("")
        self.rsa_e.set("65537")
        self.rsa_c.set("")
        self.rsa_output_text.delete(1.0, tk.END)
        
    def show_error(self, message):
        messagebox.showerror("Error", message)
        self.status_var.set("Error occurred")

def main():
    root = tk.Tk()
    app = QuadraticSieveApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()