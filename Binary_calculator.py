import tkinter as tk
from tkinter import messagebox, filedialog

# ---------- LOGIC ----------

def normalize_4bit(a, b):
    return a.zfill(4), b.zfill(4)

def ones_complement(binary):
    return ''.join('1' if bit == '0' else '0' for bit in binary)

def binary_addition(a, b):
    a, b = normalize_4bit(a, b)
    result = ''
    carry = 0
    carries = []

    for i in range(3, -1, -1):
        total = int(a[i]) + int(b[i]) + carry
        result = str(total % 2) + result
        carry = total // 2
        carries.insert(0, carry)

    overflow = carries[0] ^ carry
    return result, carry, overflow

def twos_complement(binary):
    ones = ones_complement(binary)
    result, _, _ = binary_addition(ones, '0001')
    return result

def binary_subtraction(a, b):
    b_twos = twos_complement(b)
    result, carry, overflow = binary_addition(a, b_twos)
    return result, overflow

# ---------- GUI FUNCTIONS ----------

def press(num):
    if current_entry.get() == "A":
        entryA.set(entryA.get() + num)
    else:
        entryB.set(entryB.get() + num)

def select_A():
    current_entry.set("A")

def select_B():
    current_entry.set("B")

def clear():
    entryA.set("")
    entryB.set("")
    result_var.set("")
    overflow_var.set("")
    update_leds("0000")
    update_carry_led(0)

def calculate(op):
    a = entryA.get()
    b = entryB.get()

    if len(a) > 4 or len(b) > 4:
        messagebox.showerror("Error", "Only 4-bit allowed!")
        return

    a, b = normalize_4bit(a, b)

    if op == "ADD":
        res, carry, ov = binary_addition(a, b)

    elif op == "SUB":
        res, ov = binary_subtraction(a, b)
        carry = 0

    elif op == "1C":
        res = ones_complement(a)
        carry = 0
        ov = 0

    elif op == "2C":
        res = twos_complement(a)
        carry = 0
        ov = 0

    result_var.set(res)
    overflow_var.set(f"Overflow: {ov}")

    update_leds(res)
    update_carry_led(carry)

def export():
    data = f"A: {entryA.get()}\nB: {entryB.get()}\nResult: {result_var.get()}\n{overflow_var.get()}"
    file = filedialog.asksaveasfilename(defaultextension=".txt")
    if file:
        with open(file, "w") as f:
            f.write(data)
        messagebox.showinfo("Saved", "Results exported!")

# ---------- LED FUNCTIONS ----------

def update_leds(binary):
    for i, bit in enumerate(binary):
        if bit == '1':
            canvas.itemconfig(leds[i], fill="lime")
        else:
            canvas.itemconfig(leds[i], fill="black")

def update_carry_led(carry):
    if carry == 1:
        canvas.itemconfig(carry_led, fill="red")
    else:
        canvas.itemconfig(carry_led, fill="black")

# ---------- WINDOW ----------

root = tk.Tk()
root.title("Binary Calculator with LED Display")
root.geometry("480x650")
root.configure(bg="#1e1e1e")

entryA = tk.StringVar()
entryB = tk.StringVar()
result_var = tk.StringVar()
overflow_var = tk.StringVar()
current_entry = tk.StringVar(value="A")

# ---------- TITLE ----------

tk.Label(root, text="4-Bit Binary Calculator", fg="white",
         bg="#1e1e1e", font=("Arial", 16)).pack(pady=10)

# ---------- INPUT ----------

tk.Label(root, text="Input A", fg="white", bg="#1e1e1e").pack()
tk.Entry(root, textvariable=entryA, bg="#333", fg="white", font=("Arial", 14)).pack(pady=5)

tk.Label(root, text="Input B", fg="white", bg="#1e1e1e").pack()
tk.Entry(root, textvariable=entryB, bg="#333", fg="white", font=("Arial", 14)).pack(pady=5)

tk.Button(root, text="Edit A", command=select_A, bg="#444", fg="white").pack(pady=2)
tk.Button(root, text="Edit B", command=select_B, bg="#444", fg="white").pack(pady=2)

# ---------- KEYPAD ----------

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(pady=10)

tk.Button(frame, text="0", width=10, height=2, bg="#555", fg="white",
          command=lambda: press("0")).grid(row=0, column=0, padx=5, pady=5)

tk.Button(frame, text="1", width=10, height=2, bg="#555", fg="white",
          command=lambda: press("1")).grid(row=0, column=1, padx=5, pady=5)

# ---------- OPERATIONS ----------

tk.Button(root, text="ADD", width=15, bg="#007acc", fg="white",
          command=lambda: calculate("ADD")).pack(pady=5)

tk.Button(root, text="SUB", width=15, bg="#007acc", fg="white",
          command=lambda: calculate("SUB")).pack(pady=5)

tk.Button(root, text="1's Complement", width=15, bg="#007acc", fg="white",
          command=lambda: calculate("1C")).pack(pady=5)

tk.Button(root, text="2's Complement", width=15, bg="#007acc", fg="white",
          command=lambda: calculate("2C")).pack(pady=5)

tk.Button(root, text="Clear", width=15, bg="red", fg="white",
          command=clear).pack(pady=5)

tk.Button(root, text="Export Result", width=15, bg="green", fg="white",
          command=export).pack(pady=5)

# ---------- OUTPUT ----------

tk.Label(root, text="Result", fg="white", bg="#1e1e1e").pack()
tk.Entry(root, textvariable=result_var, bg="#222", fg="lime",
         font=("Arial", 14)).pack(pady=5)

tk.Label(root, textvariable=overflow_var, fg="yellow",
         bg="#1e1e1e", font=("Arial", 12)).pack(pady=5)

# ---------- LED PANEL ----------

tk.Label(root, text="Carry   S3   S2   S1   S0", fg="white",
         bg="#1e1e1e", font=("Arial", 12)).pack(pady=10)

canvas = tk.Canvas(root, width=300, height=70,
                   bg="#1e1e1e", highlightthickness=0)
canvas.pack()

# Carry LED (RED)
carry_led = canvas.create_oval(10, 10, 50, 50, fill="black")

# Result LEDs
leds = []
positions = [70, 130, 190, 250]

for pos in positions:
    leds.append(canvas.create_oval(pos, 10, pos+40, 50, fill="black"))

# Initialize LEDs
update_leds("0000")
update_carry_led(0)

# ---------- RUN ----------

root.mainloop()