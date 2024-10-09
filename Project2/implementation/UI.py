import random
import tkinter as tk

class ProverVerifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prover-Verifier Protocol")

        self.PRIMENO = tk.StringVar()
        self.generator = tk.StringVar()
        self.secretVal = None
        self.X = None
        self.y = None
        self.Y = None
        self.z = None

        self.label_params = tk.Label(root, text="Set Protocol Parameters")
        self.label_params.grid(row=0, column=0, columnspan=2)

        self.label_PRIMENO = tk.Label(root, text="PRIMENO:")
        self.label_PRIMENO.grid(row=1, column=0)
        self.entry_PRIMENO = tk.Entry(root, textvariable=self.PRIMENO)
        self.entry_PRIMENO.grid(row=1, column=1)

        self.label_generator = tk.Label(root, text="Generator:")
        self.label_generator.grid(row=2, column=0)
        self.entry_generator = tk.Entry(root, textvariable=self.generator)
        self.entry_generator.grid(row=2, column=1)

        self.button_set_params = tk.Button(root, text="Set Parameters", command=self.set_params)
        self.button_set_params.grid(row=3, column=0, columnspan=2)

    def set_params(self):
        try:
            PRIMENO = int(self.PRIMENO.get())
            generator = int(self.generator.get())
            self.secretVal, self.X = self.generate_values(generator, PRIMENO)

            self.label_params.config(text=f"Protocol Parameters Set - secretVal: {self.secretVal}, X: {self.X}")

            self.label_sender = tk.Label(self.root, text="Sender (Prover)")
            self.label_sender.grid(row=4, column=0, columnspan=2)

            self.label_secretVal = tk.Label(self.root, text=f"Secret Value (secretVal): {self.secretVal}")
            self.label_secretVal.grid(row=5, column=0, columnspan=2)

            self.label_X = tk.Label(self.root, text=f"X: {self.X}")
            self.label_X.grid(row=6, column=0, columnspan=2)

            self.label_y = tk.Label(self.root, text="Enter y:")
            self.label_y.grid(row=7, column=0)

            self.entry_y = tk.Entry(self.root)
            self.entry_y.grid(row=7, column=1)

            self.button_generate_Y = tk.Button(self.root, text="Generate Y", command=self.generate_Y)
            self.button_generate_Y.grid(row=8, column=0, columnspan=2)

            self.label_generated_Y = tk.Label(self.root, text="")
            self.label_generated_Y.grid(row=9, column=0, columnspan=2)

            self.label_receiver = tk.Label(self.root, text="Receiver (Verifier)")
            self.label_receiver.grid(row=4, column=3, columnspan=2)

            self.label_c = tk.Label(self.root, text="Random Value (c):")
            self.label_c.grid(row=5, column=3)

            self.entry_c = tk.Entry(self.root)
            self.entry_c.grid(row=5, column=4)

            self.button_prove = tk.Button(self.root, text="Prove Knowledge", command=self.prove)
            self.button_prove.grid(row=6, column=3, columnspan=2)

            self.label_result = tk.Label(self.root, text="")
            self.label_result.grid(row=7, column=3, columnspan=2)

            self.label_z = tk.Label(self.root, text="")
            self.label_z.grid(row=8, column=3, columnspan=2)

            self.label_val1 = tk.Label(self.root, text="")
            self.label_val1.grid(row=9, column=3, columnspan=2)

            self.label_val2 = tk.Label(self.root, text="")
            self.label_val2.grid(row=10, column=3, columnspan=2)

        except ValueError:
            self.label_params.config(text="Invalid input for PRIMENO or generator")

    def generate_values(self, generator, PRIMENO):
        secretVal = 5
        X = pow(generator, secretVal) % PRIMENO
        return secretVal, X

    def generate_Y(self):
        try:
            self.y = int(self.entry_y.get())
            self.Y = pow(int(self.generator.get()), self.y) % int(self.PRIMENO.get())
            self.label_generated_Y.config(text=f"Generated Y: {self.Y}")
        except ValueError:
            self.label_result.config(text="Invalid input for 'y'")
            self.label_generated_Y.config(text="")

    def prove(self):
        try:
            if self.y is None:
                self.label_result.config(text="Please generate Y first.")
                return

            c = int(self.entry_c.get())
            self.z, val1, val2 = self.prove_knowledge(int(self.PRIMENO.get()), int(self.X), self.y, self.Y, c)
            self.label_z.config(text=f"Calculated z: {self.z}")
            self.label_val1.config(text=f"Calculated val1: {val1}")
            self.label_val2.config(text=f"Calculated val2: {val2}")

            if val1 == val2:
                self.label_result.config(text="Alice has proven that she knows x")
            else:
                self.label_result.config(text="Failure to prove")
        except ValueError:
            self.label_result.config(text="Invalid input for 'c'")

    def prove_knowledge(self, PRIMENO, X, y, Y, c):
        z = (y + c * self.secretVal)
        val1 = pow(int(self.generator.get()), z) % PRIMENO
        val2 = (Y * (X**c)) % PRIMENO
        return z, val1, val2


if __name__ == "__main__":
    root = tk.Tk()
    app = ProverVerifierApp(root)
    root.mainloop()
