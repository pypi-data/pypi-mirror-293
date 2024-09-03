from tkinter import Tk, Label, Entry, Button

from lynq._backendutils.lynq.msie import pwsh

def run_process(entry: Entry) -> None:
    text: str = entry.get()

    if text.startswith("lynq://app/"):
        pwsh(f"python {text.removeprefix("lynq://app/")}.py")

    elif text.startswith("lynq://"):
        text = f"http://localhost:{text.removeprefix("lynq://")}/"

        pwsh(f"start {text}")

    else:
        pwsh(f"start {text}")

def run_gui() -> None:
    root: Tk = Tk()

    root.title("Run using Lynq")
    root.geometry("400x150")
    root.resizable(False, False)

    Label(root, text="Run a new process using Lynq").pack()
    entry: Entry = Entry(root, width=80)
    entry.pack(padx=10, pady=10)
    Button(root, text="Submit", command=lambda: run_process(entry)).pack(pady=10)

    root.mainloop()