from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .service import TaskService


class TodoApp:
    """Small Tkinter view. Keep UI code here, not in the service or repository."""

    def __init__(self, service: TaskService) -> None:
        self.service = service
        self.root = tk.Tk()
        self.root.title("Todo Manager Starter")
        self.root.geometry("850x560")
        self.selected_id: int | None = None

        self.title_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.priority_var = tk.StringVar(value="Medium")
        self.due_date_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="All")
        self._build_widgets()
        self.refresh()

    def _build_widgets(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        form = ttk.LabelFrame(frame, text="Task")
        form.pack(fill=tk.X, pady=(0, 8))
        ttk.Label(form, text="Title").grid(row=0, column=0, padx=6, pady=6)
        ttk.Entry(form, textvariable=self.title_var, width=36).grid(
            row=0, column=1, padx=6, pady=6
        )
        ttk.Label(form, text="Description").grid(row=0, column=2, padx=6, pady=6)
        ttk.Entry(form, textvariable=self.description_var, width=36).grid(
            row=0, column=3, padx=6, pady=6
        )
        ttk.Label(form, text="Priority").grid(row=1, column=0, padx=6, pady=6)
        ttk.Combobox(
            form,
            textvariable=self.priority_var,
            values=("High", "Medium", "Low"),
            state="readonly",
            width=12,
        ).grid(row=1, column=1, sticky="w", padx=6, pady=6)
        ttk.Label(form, text="Due date").grid(row=1, column=2, padx=6, pady=6)
        ttk.Entry(form, textvariable=self.due_date_var, width=16).grid(
            row=1, column=3, sticky="w", padx=6, pady=6
        )

        filters = ttk.Frame(frame)
        filters.pack(fill=tk.X, pady=(0, 8))
        ttk.Label(filters, text="Search").pack(side=tk.LEFT)
        search = ttk.Entry(filters, textvariable=self.search_var, width=28)
        search.pack(side=tk.LEFT, padx=6)
        search.bind("<KeyRelease>", lambda _event: self.refresh())
        ttk.Label(filters, text="Status").pack(side=tk.LEFT, padx=(12, 0))
        status = ttk.Combobox(
            filters,
            textvariable=self.status_var,
            values=("All", "Active", "Completed"),
            state="readonly",
            width=12,
        )
        status.pack(side=tk.LEFT, padx=6)
        status.bind("<<ComboboxSelected>>", lambda _event: self.refresh())

        columns = ("id", "title", "priority", "due_date", "completed")
        self.table = ttk.Treeview(
            frame, columns=columns, show="headings", selectmode="browse"
        )
        headings = {
            "id": "ID",
            "title": "Title",
            "priority": "Priority",
            "due_date": "Due date",
            "completed": "Status",
        }
        widths = {
            "id": 50,
            "title": 300,
            "priority": 100,
            "due_date": 120,
            "completed": 100,
        }
        for column in columns:
            self.table.heading(column, text=headings[column])
            self.table.column(column, width=widths[column])
        self.table.pack(fill=tk.BOTH, expand=True)
        self.table.bind("<<TreeviewSelect>>", self._on_select)

        actions = ttk.Frame(frame)
        actions.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(actions, text="Add", command=self.add).pack(side=tk.LEFT, padx=3)
        ttk.Button(actions, text="Edit selected", command=self.edit).pack(
            side=tk.LEFT, padx=3
        )
        ttk.Button(actions, text="Toggle complete", command=self.toggle).pack(
            side=tk.LEFT, padx=3
        )
        ttk.Button(actions, text="Delete selected", command=self.delete).pack(
            side=tk.LEFT, padx=3
        )
        ttk.Button(actions, text="Clear form", command=self.clear_form).pack(
            side=tk.RIGHT, padx=3
        )

    def _on_select(self, _event=None) -> None:
        selection = self.table.selection()
        if not selection:
            self.selected_id = None
            return
        values = self.table.item(selection[0], "values")
        self.selected_id = int(values[0])
        task = self.service.get_task(self.selected_id)
        self.title_var.set(task.title)
        self.description_var.set(task.description)
        self.priority_var.set(task.priority)
        self.due_date_var.set(task.due_date or "")

    def refresh(self) -> None:
        for item in self.table.get_children():
            self.table.delete(item)
        tasks = self.service.list_tasks(self.search_var.get(), self.status_var.get())
        for task in tasks:
            status = "Completed" if task.completed else "Active"
            self.table.insert(
                "",
                tk.END,
                values=(
                    task.id,
                    task.title,
                    task.priority,
                    task.due_date or "",
                    status,
                ),
            )

    def _input_values(self) -> tuple[str, str, str, str]:
        return (
            self.title_var.get(),
            self.description_var.get(),
            self.priority_var.get(),
            self.due_date_var.get(),
        )

    def add(self) -> None:
        try:
            self.service.add_task(*self._input_values())
        except (ValueError, KeyError) as exc:
            messagebox.showwarning("Invalid task", str(exc))
            return
        self.clear_form()
        self.refresh()

    def edit(self) -> None:
        if self.selected_id is None:
            messagebox.showwarning("Edit task", "Select a task first.")
            return
        try:
            self.service.update_task(self.selected_id, *self._input_values())
        except (ValueError, KeyError) as exc:
            messagebox.showwarning("Invalid task", str(exc))
            return
        self.refresh()

    def toggle(self) -> None:
        if self.selected_id is None:
            messagebox.showwarning("Complete task", "Select a task first.")
            return
        self.service.toggle_completed(self.selected_id)
        self.refresh()

    def delete(self) -> None:
        if self.selected_id is None:
            messagebox.showwarning("Delete task", "Select a task first.")
            return
        if messagebox.askyesno("Delete task", "Delete the selected task?"):
            self.service.delete_task(self.selected_id)
            self.clear_form()
            self.refresh()

    def clear_form(self) -> None:
        self.selected_id = None
        self.title_var.set("")
        self.description_var.set("")
        self.priority_var.set("Medium")
        self.due_date_var.set("")
        for item in self.table.selection():
            self.table.selection_remove(item)

    def run(self) -> None:
        self.root.mainloop()
