import tkinter as tk
from tkinter import *
from tkinter import messagebox
import src # Keep src.py unchanged
import time
import textwrap # For wrapping long numbers

#__________________________________________________________CUSTOM WINDOW____________________________________________________#
def show_key_generation_details(message):
    """Displays the detailed RSA key generation steps in a custom window."""
    dialog = tk.Toplevel(root)
    dialog.title("Chi tiết tạo khóa RSA")
    dialog.geometry("650x500") # Adjust size if needed

    label = tk.Label(dialog, text="Quá trình tạo khóa và kết quả:", font=('Arial', 12, 'bold'))
    label.pack(pady=10)

    text_box = tk.Text(dialog, wrap='word', height=25, width=80, font=('Courier New', 10)) # Use Courier for alignment
    text_box.pack(padx=10, pady=5, fill="both", expand=True)
    text_box.insert('1.0', message)
    text_box.config(state='disabled') # Make text read-only

    # Add a scrollbar
    scrollbar = tk.Scrollbar(text_box, command=text_box.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_box.config(yscrollcommand=scrollbar.set)


    close_button = tk.Button(dialog, text="Đóng", command=dialog.destroy, width=10)
    close_button.pack(pady=10)

    # Center the dialog window
    dialog.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() // 2) - (dialog.winfo_width() // 2)
    y = root.winfo_y() + (root.winfo_height() // 2) - (dialog.winfo_height() // 2)
    dialog.geometry(f"+{x}+{y}")
    dialog.transient(root) # Keep dialog on top of main window
    dialog.grab_set() # Modal dialog
    root.wait_window(dialog) # Wait until dialog is closed

# --- NEW FUNCTION ---
def show_ciphertext_window(ciphertext):
    """Displays the generated ciphertext in a custom window."""
    dialog = tk.Toplevel(root)
    dialog.title("Bản mã (Ciphertext)")
    dialog.geometry("650x300") # Adjust size as needed

    label = tk.Label(dialog, text="Giá trị bản mã (c):", font=('Arial', 12, 'bold'))
    label.pack(pady=10)

    text_box = tk.Text(dialog, wrap='word', height=15, width=80, font=('Courier New', 10)) # Use Courier for alignment
    text_box.pack(padx=10, pady=5, fill="both", expand=True)

    # Wrap the ciphertext before inserting
    wrapped_ciphertext = wrap_number(ciphertext, 75) # Adjust wrap width if needed
    text_box.insert('1.0', wrapped_ciphertext)
    text_box.config(state='disabled') # Make text read-only

    # Add a scrollbar
    scrollbar = tk.Scrollbar(text_box, command=text_box.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_box.config(yscrollcommand=scrollbar.set)

    close_button = tk.Button(dialog, text="Đóng", command=dialog.destroy, width=10)
    close_button.pack(pady=10)

    # Center the dialog window
    dialog.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() // 2) - (dialog.winfo_width() // 2)
    y = root.winfo_y() + (root.winfo_height() // 2) - (dialog.winfo_height() // 2)
    dialog.geometry(f"+{x}+{y}")
    dialog.transient(root) # Keep dialog on top of main window
    dialog.grab_set() # Modal dialog
    root.wait_window(dialog) # Wait until dialog is closed


def show_custom_dialog(message, option1_callback, option2_callback):
    dialog = tk.Toplevel(root)
    dialog.title("Cảnh báo")
    dialog.geometry("400x180") # Increased height slightly

    label = tk.Label(dialog, text=message, wraplength=380, justify="center") # Increased wraplength
    label.pack(padx=20, pady=20)

    button_frame = tk.Frame(dialog)
    button_frame.pack(pady=15) # Increased padding

    option1_button = tk.Button(button_frame, text="Chọn lại độ dài khóa", command=lambda: [option1_callback(), dialog.destroy()])
    option1_button.pack(side="left", padx=15) # Increased padding

    option2_button = tk.Button(button_frame, text="Mã hóa số đã giảm", command=lambda: [option2_callback(), dialog.destroy()]) # Clarified text
    option2_button.pack(side="right", padx=15) # Increased padding

    # Center the dialog window
    dialog.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() // 2) - (dialog.winfo_width() // 2)
    y = root.winfo_y() + (root.winfo_height() // 2) - (dialog.winfo_height() // 2)
    dialog.geometry(f"+{x}+{y}")
    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)

# --- Function to safely hide widgets using place_forget ---
# Modified to only hide, not destroy or set to None unless specified
def hide_widget(widget):
    """Safely hides a widget using place_forget if it exists and is placed."""
    if widget is not None and widget.winfo_manager(): # Check if it exists and is managed (placed/packed/gridded)
        widget.place_forget()

# --- Function to wrap long numbers ---
def wrap_number(number, width=40):
    """Wraps a long integer (as string) for better display."""
    s = str(number)
    return '\n'.join(textwrap.wrap(s, width))

#_____________________________________________________________EXCEPTION_____________________________________________________#

class Bigger_than_key(Exception):
    @staticmethod
    def regenerate_key():
        global public_key, private_key, public_key_label, time_gen_key_label
        # Re-enable key generation widgets
        entry_bitlength_key.config(state='normal')
        button_gen_key.config(state='normal')
        # Hide the previous key display and related info
        hide_widget(public_key_label) # Vẫn gọi hide để đảm bảo nếu nó từng tồn tại
        hide_widget(time_gen_key_label)
        hide_widget(number_encoded_label)
        hide_widget(time_encrypt_label)
        hide_widget(number_decrypted_label)
        hide_widget(result_status_label)
        hide_widget(time_decrypt_label)

        # Reset key variables
        public_key = None
        private_key = None

        # Disable subsequent steps until new key is generated
        button_encrypt.config(state='disabled')
        start_decrypt_btn.config(state='disabled')
        hide_widget(start_decrypt_btn) # Also hide the button
        # Hide decryption input widgets if they are visible
        display_entry_private_key(hide_only=True)


    @staticmethod
    def encode_with_reduced_number():
        global num_to_encode, number_encoded, public_key, time_encrypt, number_encoded_label, time_encrypt_label
        e,n = public_key
        original_num_display = num_to_encode # Store original for display
        num_to_encode_reduced = num_to_encode % n # Reduce the number

        # Hide previous results before displaying new ones
        hide_widget(public_key_label) # Vẫn gọi hide để đảm bảo nếu nó từng tồn tại
        hide_widget(time_gen_key_label) # Hide time label if reducing number
        hide_widget(number_encoded_label)
        hide_widget(time_encrypt_label)
        hide_widget(number_decrypted_label) # Hide potential old decryption results
        hide_widget(result_status_label)
        hide_widget(time_decrypt_label)
        display_entry_private_key(hide_only=True) # Hide decrypt inputs

        start_time = time.time()
        # Encrypt the REDUCED number
        number_encoded = src.encrypt(num_to_encode_reduced, public_key)
        end_time = time.time()
        time_encrypt = end_time - start_time

        # --- ADDED CALL: Show ciphertext in its own window ---
        show_ciphertext_window(number_encoded)
        # ----------------------------------------------------

        wrapped_encoded_num = wrap_number(number_encoded, 45) # Wrap potentially long number

        # Reconfigure or create labels if they were None
        if number_encoded_label is None:
             number_encoded_label = tk.Label(col1_frame, fg='green', font=('Arial', 9), wraplength=330, justify="left", bg='light blue')
        number_encoded_label.config(text=f"Số {original_num_display} (giảm còn {num_to_encode_reduced})\nsau khi mã hóa là:\n{wrapped_encoded_num}")
        number_encoded_label.place(x=0, y=ENCRYPT_RESULT_Y, anchor='nw')

        if time_encrypt_label is None:
            time_encrypt_label = tk.Label(col1_frame, bg="#f7b681")
        # --- SỬA Ở ĐÂY: Đặt time_encrypt_label vào vị trí của KEY_INFO_Y ---
        time_encrypt_label.config(text=f'T.gian mã hóa: {time_encrypt:.4f}s')
        time_encrypt_label.place(x=0, y=KEY_INFO_Y, anchor='nw') # Place where key info used to be

        start_decrypt_btn.config(state='normal') # Enable decrypt button
        start_decrypt_btn.place(x=0, y=DECRYPT_BUTTON_Y, anchor='nw') # Place in col2_frame

        button_encrypt.config(state='disabled') # Disable encrypt after use


#_______________________________________________________________DISPLAY___________________________________________________#

def display_gen_key():
    global public_key, private_key, p_val, q_val, phi_val, public_key_label, time_gen_key_label, time_gen_key
    try:
        bit_size = int(entry_bitlength_key.get())
        if bit_size < 16 or bit_size > 4096:
            raise ValueError("Key size must be between 16 and 4096 bits.")

        # Disable UI during generation & hide old stuff
        entry_bitlength_key.config(state='disabled')
        button_gen_key.config(state='disabled')
        hide_widget(public_key_label) # Hide any previous label if exists
        hide_widget(time_gen_key_label)
        hide_widget(number_encoded_label)
        hide_widget(time_encrypt_label)
        hide_widget(number_decrypted_label)
        hide_widget(result_status_label)
        hide_widget(time_decrypt_label)
        button_encrypt.config(state='disabled')
        start_decrypt_btn.config(state='disabled')
        hide_widget(start_decrypt_btn)
        display_entry_private_key(hide_only=True) # Hide decrypt inputs
        root.update_idletasks()

        start_time = time.time()
        key_data = src.generate_rsa_keys(bit_size)
        end_time = time.time()
        time_gen_key = end_time - start_time

        if key_data is None:
             messagebox.showerror("Lỗi Tạo Khóa", "Không thể tạo khóa RSA. Hãy thử lại.")
             entry_bitlength_key.config(state='normal')
             button_gen_key.config(state='normal')
             return

        public_key, private_key, p_val, q_val, phi_val = key_data
        e_val, n_val = public_key
        d_val = private_key[0]

        details_content = f"""--- Quá Trình Tạo Khóa RSA ( {bit_size}-bit ) ---

1. Chọn số nguyên tố p:
   {p_val}

2. Chọn số nguyên tố q (khác p):
   {q_val}

3. Tính modulus n = p * q:
   {n_val}

4. Tính Euler's totient phi(n) = (p-1)*(q-1):
   {phi_val}

5. Chọn số mũ công khai e (1 < e < phi, gcd(e,phi)=1):
   {e_val}

6. Tính số mũ bí mật d (d * e ≡ 1 (mod phi)):
   {d_val}

--- Kết Quả ---
Khóa công khai (e, n): ({e_val}, {n_val})
Khóa bí mật (d, n): ({d_val}, {n_val}) <-- GIỮ BÍ MẬT!
"""
        show_key_generation_details(details_content)

        # --- SỬA Ở ĐÂY: Xóa hoặc comment phần hiển thị public_key_label ---
        # # Display public key confirmation and time on main window
        # # Create labels if they don't exist, otherwise configure
        # if public_key_label is None:
        #     public_key_label = tk.Label(col1_frame, fg='blue', font=('Arial', 9), wraplength=330, bg='light blue', justify='left')
        # public_key_label.config(text=f"Đã tạo khóa {bit_size}-bit.\nKhóa công khai (e, n): ({e_val}, {n_val})")
        # public_key_label.place(x=0, y=KEY_INFO_Y, anchor='nw') # Use constant Y

        # Chỉ hiển thị thời gian tạo khóa
        if time_gen_key_label is None:
            time_gen_key_label = tk.Label(col1_frame, bg="#f7b681")
        time_gen_key_label.config(text=f'Đã tạo khóa {bit_size}-bit.\nT.gian tạo khóa: {time_gen_key:.4f}s')
        # --- SỬA Ở ĐÂY: Đặt time_gen_key_label vào vị trí KEY_INFO_Y ---
        time_gen_key_label.place(x=0, y=KEY_INFO_Y, anchor='nw') # Đặt ở vị trí cũ của thông tin khóa

        # Enable encrypt button only if number to encode has also been entered
        if num_to_encode is not None:
            button_encrypt.config(state='normal')
        else:
             button_encrypt.config(state='disabled') # Keep disabled if number not entered yet

        # Keep decrypt button disabled until encryption happens
        start_decrypt_btn.config(state='disabled')
        hide_widget(start_decrypt_btn) # Ensure it's hidden

    except ValueError as ve:
        messagebox.showerror("Lỗi Đầu Vào", f"Lỗi: {ve}")
        entry_bitlength_key.config(state='normal')
        button_gen_key.config(state='normal')
    except Exception as e:
        messagebox.showerror("Lỗi Không Xác Định", f"Đã xảy ra lỗi: {e}")
        entry_bitlength_key.config(state='normal')
        button_gen_key.config(state='normal')

def display_get_num_to_encode():
    global num_to_encode
    try:
        num_str = entry_num_to_encode.get()
        if not num_str:
            raise ValueError("Chưa nhập số.")
        num_to_encode = int(num_str)

        if num_to_encode < 0:
            messagebox.showwarning("Cảnh báo", "Số âm sẽ được mã hóa giá trị tuyệt đối.")
            num_to_encode = abs(num_to_encode)

        check_num_label.config(text=f"Số đã nhập: {num_to_encode} ✅")
        # check_num_label is already placed
        entry_num_to_encode.config(state='disabled')
        button_start_encode.config(state='disabled')

        # Enable encrypt button only if key has also been generated
        if public_key is not None:
            button_encrypt.config(state='normal')
        else:
            button_encrypt.config(state='disabled') # Keep disabled if key not generated yet

    except ValueError as e:
        messagebox.showerror("Lỗi", f"Vui lòng nhập một số nguyên hợp lệ. {e}")
        entry_num_to_encode.config(state='normal') # Allow re-entry
        button_start_encode.config(state='normal')
        num_to_encode = None # Reset if invalid

def display_start_encrypt():
    global num_to_encode, number_encoded, public_key, time_encrypt, number_encoded_label, time_encrypt_label
    if public_key is None:
         messagebox.showerror("Lỗi", "Vui lòng tạo khóa RSA trước!")
         return
    if num_to_encode is None:
         messagebox.showerror("Lỗi", "Vui lòng nhập số cần mã hóa trước!")
         return

    e, n = public_key
    try:
        # Hide previous encryption/decryption results
        hide_widget(number_encoded_label)
        hide_widget(time_encrypt_label)
        hide_widget(number_decrypted_label)
        hide_widget(result_status_label)
        hide_widget(time_decrypt_label)
        display_entry_private_key(hide_only=True) # Hide decrypt inputs
        # --- SỬA Ở ĐÂY: Cũng ẩn time_gen_key_label khi bắt đầu mã hóa mới ---
        hide_widget(time_gen_key_label) # Ẩn thông tin thời gian tạo khóa cũ

        if num_to_encode >= n:
            # Raise exception to trigger custom dialog
            raise Bigger_than_key()

        # Encrypt if number is smaller than n
        start_time = time.time()
        number_encoded = src.encrypt(num_to_encode, public_key)
        end_time = time.time()
        time_encrypt = end_time - start_time

        # --- ADDED CALL: Show ciphertext in its own window ---
        show_ciphertext_window(number_encoded)
        # ----------------------------------------------------

        wrapped_encoded_num = wrap_number(number_encoded, 45) # Wrap potentially long number

        # Reconfigure or create labels
        if number_encoded_label is None:
            number_encoded_label = tk.Label(col1_frame, fg='green', font=('Arial', 9), wraplength=330, justify="left", bg='light blue')
        number_encoded_label.config(text=f"Số {num_to_encode} sau khi mã hóa là:\n{wrapped_encoded_num}")
        number_encoded_label.place(x=0, y=ENCRYPT_RESULT_Y, anchor='nw')

        # Hiển thị thời gian mã hóa
        if time_encrypt_label is None:
             time_encrypt_label = tk.Label(col1_frame, bg="#f7b681")
        time_encrypt_label.config(text=f'T.gian mã hóa: {time_encrypt:.4f}s')
        # --- SỬA Ở ĐÂY: Đặt time_encrypt_label vào vị trí KEY_INFO_Y ---
        time_encrypt_label.place(x=0, y=KEY_INFO_Y, anchor='nw') # Đặt ở vị trí cũ của thông tin khóa

        # Enable and place decrypt button
        start_decrypt_btn.config(state='normal')
        start_decrypt_btn.place(x=0, y=DECRYPT_BUTTON_Y, anchor='nw') # Place in col2_frame

        button_encrypt.config(state='disabled') # Disable encrypt button after use

    except Bigger_than_key:
        # This exception is now handled by calling the dialog
        show_custom_dialog(
            f"Số cần mã hóa ({num_to_encode}) lớn hơn hoặc bằng modulus n ({n}).\nChọn lại độ dài khóa (để có n lớn hơn) hoặc mã hóa giá trị {num_to_encode} mod {n} = {num_to_encode % n}?",
            Bigger_than_key.regenerate_key,
            Bigger_than_key.encode_with_reduced_number
        )
    except ValueError as ve:
         messagebox.showerror("Lỗi Mã Hóa", f"Lỗi trong quá trình mã hóa: {ve}")
         button_encrypt.config(state='normal') # Allow retry maybe?
    except Exception as e:
         messagebox.showerror("Lỗi Không Xác Định", f"Đã xảy ra lỗi khi mã hóa: {e}")
         button_encrypt.config(state='normal') # Allow retry maybe?

# --- SỬA Ở ĐÂY: Đổi tên tham số và bỏ globals() lookup ---
def display_button_check_integer(key_type, entry_widget, check_label_widget):
    """Checks D or N input, updates UI, and enables decrypt button if both are valid."""
    global d_number_private, n_number_private, decrypt_btn_enabled_status

    entry_str = entry_widget.get()
    # Removed: check_label_widget = globals()[check_label_var_name]

    try:
        num_entry = int(entry_str)
        if num_entry <= 0:
             raise ValueError("Khóa phải là số nguyên dương.")

        check_label_config = {'fg': 'green', 'font': ('Arial', 8), 'bg': 'light blue'}
        # Sử dụng trực tiếp check_label_widget
        check_label_widget.config(text=f"✅", **check_label_config) # Chỉ hiển thị dấu check
        check_label_widget.place(x=250, y=DECRYPT_INPUT_START_Y + (30 if key_type == 'd' else 55), anchor='nw') # Đảm bảo nó được place

        entry_widget.config(state='disabled')

        if key_type == 'd':
            d_number_private = num_entry
            d_private_key_button.config(state='disabled')
            decrypt_btn_enabled_status['d'] = True
        elif key_type == 'n':
            n_number_private = num_entry
            n_private_key_button.config(state='disabled')
            decrypt_btn_enabled_status['n'] = True
        else: # Should not happen with current calls
            raise ValueError("Loại khóa không xác định.")

        # Check if BOTH d and n are now validly entered
        if decrypt_btn_enabled_status['d'] and decrypt_btn_enabled_status['n']:
            decrypt_btn.config(state='normal')
            hide_widget(click_n_to_start_decrypt_label) # Hide prompt if visible
        # Optional: Show prompt if only one is entered (example for d entered, n needed)
        elif decrypt_btn_enabled_status['d'] or decrypt_btn_enabled_status['n']:
            prompt_text = "Nhập n để giải mã" if decrypt_btn_enabled_status['d'] else "Nhập d để giải mã"
            if click_n_to_start_decrypt_label is None:
                 click_n_to_start_decrypt_label = tk.Label(col2_frame, wraplength=100, bg='light blue', fg='blue')
            click_n_to_start_decrypt_label.config(text=prompt_text)
            click_n_to_start_decrypt_label.place(x=150, y=DECRYPT_INPUT_START_Y + 85, anchor='nw') # Adjust position if needed


    except ValueError as e:
        messagebox.showerror("Lỗi", f"Lỗi nhập số {key_type}: {e}\nVui lòng nhập số nguyên dương.")
        entry_widget.config(state='normal') # Allow re-entry
        # Reset the corresponding status if input is invalid
        if key_type == 'd':
            d_number_private = None
            decrypt_btn_enabled_status['d'] = False
            d_private_key_button.config(state='normal') # Re-enable button
        elif key_type == 'n':
            n_number_private = None
            decrypt_btn_enabled_status['n'] = False
            n_private_key_button.config(state='normal') # Re-enable button

        # Sử dụng trực tiếp check_label_widget
        check_label_widget.config(text="") # Clear checkmark text
        hide_widget(check_label_widget) # Hide the label

        decrypt_btn.config(state='disabled') # Ensure decrypt is disabled
        hide_widget(click_n_to_start_decrypt_label) # Hide prompt


def display_decrypt():
    global number_encoded, private_key, d_number_private, n_number_private, time_decrypt
    global number_decrypted_label, result_status_label, time_decrypt_label # Make labels global

    if d_number_private is None or n_number_private is None:
        messagebox.showerror("Lỗi", "Vui lòng nhập và xác nhận cả hai phần của khóa bí mật (d và n).")
        return
    if number_encoded is None:
         messagebox.showerror("Lỗi", "Chưa có số nào được mã hóa để giải mã.")
         return

    # Disable button during decryption
    decrypt_btn.config(state='disabled')

    # Hide previous results before displaying new ones
    hide_widget(number_decrypted_label)
    hide_widget(result_status_label)
    hide_widget(time_decrypt_label)

    try:
        user_private_key = (d_number_private, n_number_private)

        start_time = time.time()
        number_decrypted = src.decrypt(number_encoded, user_private_key)
        end_time = time.time()
        time_decrypt = end_time - start_time

        wrapped_decrypted_num = wrap_number(number_decrypted, 45) # Wrap result

        # Reconfigure or create labels
        if number_decrypted_label is None:
            number_decrypted_label = tk.Label(col2_frame, fg='blue', font=('Arial', 9), wraplength=380, bg='light blue', justify='left')
        number_decrypted_label.config(text=f"Số sau khi giải mã là:\n{wrapped_decrypted_num}")
        number_decrypted_label.place(x=0, y=DECRYPT_RESULT_Y, anchor='nw')

        # Verification logic
        status_text = "Giải mã hoàn tất."
        status_color = 'blue'
        correct_decryption = True # Assume correct unless proven otherwise

        if private_key: # Check if original key exists for comparison
            orig_d, orig_n = private_key
            # Compare n first, as it's fundamental
            if n_number_private != orig_n:
                correct_decryption = False
                status_text = f"Giải mã xong, nhưng N ({n_number_private}) KHÔNG KHỚP N khóa gốc ({orig_n})!"
                status_color = 'red'
            # If n matches, compare d
            elif d_number_private != orig_d:
                correct_decryption = False
                # Check if it still decrypts correctly (might be equivalent d mod phi(n))
                # Re-encrypt the decrypted result with the *original* public key to verify
                if public_key:
                    re_encrypted = src.encrypt(number_decrypted, public_key)
                    if re_encrypted == number_encoded:
                        status_text = "Giải mã xong (cùng N), nhưng D ({}) KHÔNG KHỚP D khóa gốc ({}).\nTuy nhiên, kết quả giải mã ĐÚNG (d tương đương).".format(d_number_private, orig_d)
                        status_color = 'orange' # Warning, but functionally correct
                    else:
                         status_text = "Giải mã xong (cùng N), nhưng D ({}) KHÔNG KHỚP D khóa gốc ({}) và kết quả giải mã SAI.".format(d_number_private, orig_d)
                         status_color = 'red' # Definitely wrong
                else:
                    # Can't verify correctness if public key isn't available, just warn about D mismatch
                    status_text = "Giải mã xong (cùng N), nhưng D ({}) KHÔNG KHỚP D khóa gốc ({}). Không thể xác minh kết quả.".format(d_number_private, orig_d)
                    status_color = 'orange'
            else:
                 # Keys match completely
                 status_text = "Khóa khớp, giải mã thành công!"
                 status_color = 'green'
        else:
            status_text = "Không thể xác minh khóa (khóa gốc không có sẵn)."
            status_color = 'gray'

        # Create or configure status label
        if result_status_label is None:
            result_status_label = tk.Label(col2_frame, font=('Arial', 9, 'bold'), wraplength=380, bg='light blue', justify='left')
        result_status_label.config(text=status_text, fg=status_color)
        result_status_label.place(x=0, y=DECRYPT_STATUS_Y, anchor='nw')

        # Create or configure time label
        if time_decrypt_label is None:
            time_decrypt_label = tk.Label(col2_frame, bg="#f7b681")
        time_decrypt_label.config(text=f'T.gian giải mã: {time_decrypt:.4f}s')
        time_decrypt_label.place(x=0, y=DECRYPT_TIME_Y, anchor='nw')

        close_button.place(x=CENTER_X, y=WINDOW_HEIGHT - 30, anchor='center') # Keep close button at bottom

        # Only re-enable inputs if decryption failed verification due to wrong key
        if not correct_decryption and status_color == 'red': # Only re-enable if keys definitely wrong/result is wrong
             messagebox.showwarning("Cảnh báo Khóa", status_text + "\nVui lòng kiểm tra lại khóa bí mật.")
             # Re-enable inputs for correction
             d_private_key_entry.config(state='normal')
             n_private_key_entry.config(state='normal')
             d_private_key_button.config(state='normal')
             n_private_key_button.config(state='normal')
             decrypt_btn_enabled_status['d'] = False # Reset status
             decrypt_btn_enabled_status['n'] = False
             check_d_label.config(text="") # Clear checkmark
             check_n_label.config(text="")
             hide_widget(check_d_label)
             hide_widget(check_n_label)
             decrypt_btn.config(state='disabled') # Disable decrypt button again
             hide_widget(click_n_to_start_decrypt_label)


    except ValueError as ve:
         messagebox.showerror("Lỗi Giải Mã", f"Lỗi trong quá trình giải mã: {ve}\nKiểm tra lại khóa bí mật và số đã mã hóa.")
         # Re-enable entry for correction if needed
         d_private_key_entry.config(state='normal')
         n_private_key_entry.config(state='normal')
         d_private_key_button.config(state='normal')
         n_private_key_button.config(state='normal')
         decrypt_btn_enabled_status['d'] = False # Reset status
         decrypt_btn_enabled_status['n'] = False
         check_d_label.config(text="") # Clear checkmark
         check_n_label.config(text="")
         hide_widget(check_d_label)
         hide_widget(check_n_label)
         decrypt_btn.config(state='disabled') # Disable decrypt button again
         hide_widget(click_n_to_start_decrypt_label)

    except Exception as e:
         messagebox.showerror("Lỗi Không Xác Định", f"Đã xảy ra lỗi khi giải mã: {e}")
         # Consider re-enabling inputs/buttons for retry
         d_private_key_entry.config(state='normal')
         n_private_key_entry.config(state='normal')
         d_private_key_button.config(state='normal')
         n_private_key_button.config(state='normal')
         decrypt_btn_enabled_status['d'] = False
         decrypt_btn_enabled_status['n'] = False
         check_d_label.config(text="")
         check_n_label.config(text="")
         hide_widget(check_d_label)
         hide_widget(check_n_label)
         decrypt_btn.config(state='disabled')
         hide_widget(click_n_to_start_decrypt_label)


def display_entry_private_key(hide_only=False):
    """Shows or hides the private key entry widgets."""
    widgets_to_manage = [
        entry_private_key_label, d_private_key_entry, n_private_key_entry,
        d_private_key_button, n_private_key_button, check_d_label, check_n_label,
        decrypt_btn, click_n_to_start_decrypt_label
    ]

    if hide_only:
        for widget in widgets_to_manage:
            hide_widget(widget) # Use the safe hide function
        # Also hide the results from previous decryption
        hide_widget(number_decrypted_label)
        hide_widget(result_status_label)
        hide_widget(time_decrypt_label)
        return

    global d_number_private, n_number_private, decrypt_btn_enabled_status
    d_number_private = None
    n_number_private = None
    decrypt_btn_enabled_status = {'d': False, 'n': False} # Reset status tracker

    # Disable button that triggers this view
    hide_widget(start_decrypt_btn) # Use hide_widget

    # Hide previous results labels from decryption area
    hide_widget(number_decrypted_label)
    hide_widget(result_status_label)
    hide_widget(time_decrypt_label)
    hide_widget(click_n_to_start_decrypt_label) # Hide prompt initially

    # --- Place widgets for Decryption Input ---
    entry_private_key_label.place(x=0, y=DECRYPT_INPUT_START_Y, anchor='nw')

    d_private_key_entry.config(state='normal')
    d_private_key_entry.delete(0, tk.END)
    d_private_key_entry.place(x=0, y=DECRYPT_INPUT_START_Y + 30, anchor='nw', width=180) # Adjusted width

    n_private_key_entry.config(state='normal')
    n_private_key_entry.delete(0, tk.END)
    n_private_key_entry.place(x=0, y=DECRYPT_INPUT_START_Y + 55, anchor='nw', width=180) # Adjusted width

    d_private_key_button.config(state='normal')
    d_private_key_button.place(x=190, y=DECRYPT_INPUT_START_Y + 28, anchor='nw') # Adjusted position

    n_private_key_button.config(state='normal')
    n_private_key_button.place(x=190, y=DECRYPT_INPUT_START_Y + 53, anchor='nw') # Adjusted position

    # Configure and place checkmark labels (initially empty)
    check_d_label.config(text="")
    check_n_label.config(text="")
    hide_widget(check_d_label) # Hide initially
    hide_widget(check_n_label) # Hide initially

    # Place decrypt button but keep disabled
    decrypt_btn.config(state='disabled')
    decrypt_btn.place(x=0, y=DECRYPT_INPUT_START_Y + 85, anchor='nw')


# ================== MAIN WINDOW SETUP ==================
root = Tk()
root.title("Chương trình Mã hóa RSA - 20227019")
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
root.resizable(0,0)
root.configure(bg='light blue')

# Define layout constants
CENTER_X = WINDOW_WIDTH // 2
LEFT_MARGIN = 20
RIGHT_MARGIN = 420 # Start of right column (col2_frame)
COL_WIDTH = 360 # Width for each column frame

# --- Frames for layout ---
col1_frame = tk.Frame(root, width=COL_WIDTH, height=WINDOW_HEIGHT - 100, bg='light blue')
col1_frame.place(x=LEFT_MARGIN, y=100, anchor='nw')

col2_frame = tk.Frame(root, width=COL_WIDTH, height=WINDOW_HEIGHT - 100, bg='light blue')
col2_frame.place(x=RIGHT_MARGIN, y=100, anchor='nw')

# --- Constants for Y positions within frames ---
INPUT_NUM_Y = 0
INPUT_KEY_Y = 90
# --- SỬA Ở ĐÂY: KEY_INFO_Y giờ là vị trí cho thông báo/thời gian ---
KEY_INFO_Y = 160 # Where key gen confirmation/time or encrypt time is displayed
# --- Bỏ TIME_INFO_Y vì đã gộp vào KEY_INFO_Y ---
# TIME_INFO_Y = KEY_INFO_Y + 45
ENCRYPT_BTN_Y = 230
ENCRYPT_RESULT_Y = 270 # Where encoded number is displayed

DECRYPT_BUTTON_Y = 0 # "Bắt đầu giải mã" button Y in col2
DECRYPT_INPUT_START_Y = 40 # Start of d/n input elements in col2
DECRYPT_RESULT_Y = DECRYPT_INPUT_START_Y + 130 # Where decoded number is displayed
DECRYPT_STATUS_Y = DECRYPT_RESULT_Y + 45 # Status below result
DECRYPT_TIME_Y = DECRYPT_STATUS_Y + 30 # Time below status


# --- Header ---
hust_label = tk.Label(root, text="ĐẠI HỌC BÁCH KHOA HÀ NỘI", fg='red',font=('Arial', 12, 'bold'), bg='light blue')
hust_label.place(x=CENTER_X, y=20, anchor='center')
info_label = tk.Label(root, text="Nguyễn Việt Hoàng - Nguyễn Đức Mạnh - Lê Cảnh Hải - Vũ Hoàng Dương", fg='dark blue',font=('Arial', 9), bg='light blue')
info_label.place(x=CENTER_X, y=45, anchor='center')

# --- RSA Title ---
rsa_label = tk.Label(root, text="MÃ HÓA / GIẢI MÃ RSA", fg='black',bg='#05ff16',font=('Arial', 11, 'bold'))
rsa_label.place(x=CENTER_X, y=80, anchor='center')

# ================== Widgets Column 1 (Input, KeyGen, Encrypt) ==================

# 1. Input number to encode
label_input_num_to_encode = tk.Label(col1_frame, text="1. Nhập số nguyên cần mã hóa:",bg='sky blue')
label_input_num_to_encode.place(x=0, y=INPUT_NUM_Y, anchor='nw')
entry_num_to_encode = tk.Entry(col1_frame, width=30)
entry_num_to_encode.place(x=0, y=INPUT_NUM_Y + 25, anchor='nw')
button_start_encode = tk.Button(col1_frame, text="Xác nhận số", command=display_get_num_to_encode, activebackground='red')
button_start_encode.place(x=200, y=INPUT_NUM_Y + 23, anchor='nw')
check_num_label = tk.Label(col1_frame, text="", fg='green', font=('Arial', 9), bg='light blue')
check_num_label.place(x=0, y=INPUT_NUM_Y + 55, anchor='nw')

# 2. Generate Keys
label_input_bitlength_key = tk.Label(col1_frame, text="2. Nhập độ dài khóa (bit):",bg='sky blue')
label_input_bitlength_key.place(x=0, y=INPUT_KEY_Y, anchor='nw')
entry_bitlength_key = tk.Entry(col1_frame, width=10)
entry_bitlength_key.insert(0, "1024") # Default value
entry_bitlength_key.place(x=150, y=INPUT_KEY_Y, anchor='nw')
button_gen_key = tk.Button(col1_frame, text="Sinh khóa", command=display_gen_key, activebackground='red')
button_gen_key.place(x=230, y=INPUT_KEY_Y - 2, anchor='nw')
label_rcm_bitlength = tk.Label(col1_frame, text="Gợi ý: [16-4096], phổ biến 1024, 2048.", bg='yellow', wraplength=150, justify='left')
label_rcm_bitlength.place(x=0, y=INPUT_KEY_Y + 30, anchor='nw')

# 3. Encrypt Button
button_encrypt = tk.Button(col1_frame,
                           text="3. Mã hóa số đã nhập",
                           bg='#ff8a05',
                           command=display_start_encrypt,
                           activebackground='green',
                           state='disabled') # Initially disabled
button_encrypt.place(x=0, y=ENCRYPT_BTN_Y, anchor='nw')

# Placeholder labels for dynamic content in Column 1 (initialize as None)
# --- SỬA Ở ĐÂY: Vẫn giữ public_key_label = None để hide_widget không lỗi ---
public_key_label = None # Sẽ không được tạo hoặc hiển thị trực tiếp nữa
time_gen_key_label = None # Sẽ được đặt ở vị trí KEY_INFO_Y
number_encoded_label = None
time_encrypt_label = None # Sẽ được đặt ở vị trí KEY_INFO_Y khi mã hóa


# ================== Widgets Column 2 (Decrypt) ==================

# 4. Decrypt Button (Starts the process)
start_decrypt_btn = tk.Button(col2_frame,
                              text="4. Bắt đầu giải mã >>",
                              fg='black', bg='#87CEEB', # Sky blue background
                              command=lambda: display_entry_private_key(hide_only=False), # Call without hide_only
                              state='disabled') # Initially disabled
# Don't place it initially, placed by display_start_encrypt

# Widgets for entering private key (managed by display_entry_private_key)
entry_private_key_label = tk.Label(col2_frame, text="Nhập khóa bí mật:", fg='black',font=('Arial', 10), bg='light blue')
d_private_key_entry = tk.Entry(col2_frame, width=30)
n_private_key_entry = tk.Entry(col2_frame, width=30)
# Create check labels here
check_d_label = tk.Label(col2_frame, text="", fg='green', font=('Arial', 8), bg='light blue')
check_n_label = tk.Label(col2_frame, text="", fg='green', font=('Arial', 8), bg='light blue')
click_n_to_start_decrypt_label = None # Initialize as None, created on demand

# --- SỬA Ở ĐÂY: Sửa lỗi chính tả và truyền widget ---
d_private_key_button = tk.Button(col2_frame,
                                 text="Nhập d",
                                 # Gọi đúng tên hàm, truyền widget check_d_label
                                 command=lambda: display_button_check_integer('d', d_private_key_entry, check_d_label),
                                 activebackground='red')
n_private_key_button = tk.Button(col2_frame,
                                 text="Nhập n",
                                 # Gọi đúng tên hàm, truyền widget check_n_label
                                 command=lambda: display_button_check_integer('n', n_private_key_entry, check_n_label),
                                 activebackground='red')

# 5. Decrypt Button (Final step)
decrypt_btn = tk.Button(col2_frame, text="5. Giải mã 👈 ", fg='black', bg='#ff8a05', command=display_decrypt, state='disabled')

# Placeholder labels for dynamic content in Column 2 (initialize as None)
number_decrypted_label = None
result_status_label = None
time_decrypt_label = None


# ================== Shared Widgets ==================
# Close button (shared)
close_button = tk.Button(root, text="Đóng Chương Trình", command=root.destroy, width=20, bg='pink')
close_button.place(x=CENTER_X, y=WINDOW_HEIGHT - 30, anchor='center') # Place at bottom center


# ================== Global variables ==================
public_key = None
private_key = None # Store the original private key for verification
p_val, q_val, phi_val = None, None, None
num_to_encode = None
number_encoded = None
d_number_private = None # User input D
n_number_private = None # User input N
decrypt_btn_enabled_status = {'d': False, 'n': False} # Tracks if d and n inputs are valid

time_gen_key = None
time_encrypt = None
time_decrypt = None

# --- Hide decrypt inputs initially ---
display_entry_private_key(hide_only=True)


root.mainloop()