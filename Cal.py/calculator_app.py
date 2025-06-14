import tkinter as tk

class CalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Simple Calculator")
        master.resizable(False, False) # Make window non-resizable

        # --- State Variables ---
        self.current_input = "0"
        self.first_operand = None
        self.operator = None
        self.waiting_for_second_operand = False # True after an operator is pressed
        self.result_displayed = False # True if the current display is a result

        # --- Create GUI Widgets ---

        # Display Entry
        self.display = tk.Entry(master, width=25, borderwidth=5, font=('Arial', 24), justify='right', state='readonly')
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.update_display(self.current_input)

        # Define button layout
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0)
        ]

        # Create and place buttons
        for (button_text, row, col) in buttons:
            button = tk.Button(master, text=button_text, width=5, height=2, font=('Arial', 18))

            if button_text.isdigit():
                button.config(command=lambda text=button_text: self.on_number_click(text))
            elif button_text == '.':
                button.config(command=self.on_decimal_click)
            elif button_text in ('+', '-', '*', '/'):
                button.config(command=lambda text=button_text: self.on_operator_click(text))
            elif button_text == '=':
                button.config(command=self.on_equals_click)
            elif button_text == 'C':
                button.config(command=self.on_clear_click)

            button.grid(row=row, column=col, padx=5, pady=5)

    # --- Logic Methods ---

    def update_display(self, value):
        """Updates the text in the calculator's display."""
        # Need to temporarily change state to normal to insert/delete text
        self.display.config(state='normal') 
        self.display.delete(0, tk.END)
        self.display.insert(0, str(value))
        self.display.config(state='readonly') # Set back to readonly

    def on_number_click(self, digit):
        """Handles clicks on number buttons."""
        if self.waiting_for_second_operand or self.result_displayed:
            self.current_input = digit
            self.waiting_for_second_operand = False
            self.result_displayed = False
        else:
            if self.current_input == "0" and digit != ".": # Avoid "0123"
                self.current_input = digit
            else:
                self.current_input += digit
        self.update_display(self.current_input)

    def on_decimal_click(self):
        """Handles click on the decimal point button."""
        if self.waiting_for_second_operand or self.result_displayed:
            self.current_input = "0."
            self.waiting_for_second_operand = False
            self.result_displayed = False
        elif "." not in self.current_input:
            self.current_input += "."
        self.update_display(self.current_input)

    def on_operator_click(self, op):
        """Handles clicks on operator buttons (+, -, *, /)."""
        try:
            current_value = float(self.current_input)
            if self.first_operand is None: # First operand of the sequence
                self.first_operand = current_value
            elif not self.waiting_for_second_operand: # Chaining operations
                self.perform_calculation() # Calculate previous pending operation
                # first_operand is updated in perform_calculation

            self.operator = op
            self.waiting_for_second_operand = True
            self.result_displayed = False # Ready for new input

        except ValueError:
            self.update_display("Error")
            self.on_clear_click() # Reset if current_input is not a valid number

    def on_equals_click(self):
        """Handles click on the equals button (=)."""
        if self.first_operand is not None and self.operator is not None:
            self.perform_calculation()
            self.operator = None # Clear operator after equals
            self.waiting_for_second_operand = False
            self.result_displayed = True
        elif self.first_operand is None: # If only one number typed and equals pressed
            self.update_display(self.current_input) # Just show the number again

    def perform_calculation(self):
        """Performs the actual arithmetic calculation."""
        try:
            second_operand = float(self.current_input)
            result = 0

            if self.operator == '+':
                result = self.first_operand + second_operand
            elif self.operator == '-':
                result = self.first_operand - second_operand
            elif self.operator == '*':
                result = self.first_operand * second_operand
            elif self.operator == '/':
                if second_operand == 0:
                    self.update_display("Error")
                    self.on_clear_click()
                    return
                result = self.first_operand / second_operand

            # Update first_operand with result for chaining calculations
            self.first_operand = result
            self.current_input = str(result) # Update current_input for display
            self.update_display(self.current_input)

        except (ValueError, TypeError):
            self.update_display("Error")
            self.on_clear_click()

    def on_clear_click(self):
        """Resets the calculator to its initial state."""
        self.current_input = "0"
        self.first_operand = None
        self.operator = None
        self.waiting_for_second_operand = False
        self.result_displayed = False
        self.update_display(self.current_input)

# --- Main Application Execution ---
if __name__ == "__main__":
    root = tk.Tk() # Create the main window instance
    app = CalculatorApp(root) # Create an instance of the CalculatorApp
    root.mainloop() # Start the Tkinter event loops