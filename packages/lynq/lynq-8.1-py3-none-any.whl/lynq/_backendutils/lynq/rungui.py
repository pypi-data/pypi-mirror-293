"""
This file is part of Lynq (elemenom/lynq).

Lynq is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lynq is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lynq. If not, see <https://www.gnu.org/licenses/>.
"""

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