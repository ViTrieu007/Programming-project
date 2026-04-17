import tkinter as tk 
from tkinter import ttk, messagebox
import imaplib
import email
from email.header import decode_header


# =========================
# OOP: Base Class (Inheritance)
# =========================
class BaseUI:
    def __init__(self, root):
        self.root = root


# =========================
# OOP: Mail Object (Encapsulation)
# =========================
class MailItem:
    def __init__(self, sender, subject, body):
        self.sender = sender
        self.subject = subject
        self.body = body
        self.priority = "Priority"
        self.status = "Status"


CATEGORY_ORDER = [
    "Academic",
    "Required/Compulsory",
    "Deadline",
    "Survey",
    "Advertisement",
    "General"
]

CATEGORIES = {
    "Academic": ["academic", "course", "assignment", "lecture", "exam", "project", "homework", "basic internship", "class", "examination"],
    "Required/Compulsory": ["required", "mandatory", "compulsory"],
    "Deadline": ["deadline", "due", "before"],
    "Survey": ["survey", "questionnaire"],
    "Advertisement": ["sale", "discount", "offer"]
}

PRIORITY_ORDER = {
    "Must": 0,
    "Should": 1,
    "Can": 2,
    "WGS?": 3,
    "Priority": 4
}

PRIORITY_VALUES = ["Must", "Should", "Can", "WGS?"]

STATUS = ["🟢 Working", "⚪ About to", "❌ Done"]


def decode_text(value):
    decoded, encoding = decode_header(value)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(encoding if encoding else "utf-8", errors="ignore")
    return decoded


# =========================
# Modular function
# =========================
def fetch_unread_emails(email_account, app_password):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_account, app_password)
    mail.select("inbox")

    status, messages = mail.search(None, "UNSEEN")

    email_list = []

    for num in messages[0].split():
        status, msg_data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        sender = decode_text(msg.get("From"))
        subject = decode_text(msg.get("Subject"))

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        # OOP: use MailItem instead of dict
        email_list.append(MailItem(sender, subject, body))

    mail.logout()
    return email_list


# =========================
# UI Class with Inheritance
# =========================
class MailSorterUI(BaseUI):

    def __init__(self, root):
        super().__init__(root)

        root.title("Smart Mail Sorter")
        root.geometry("950x650")

        self.category_frames = {}
        self.category_mails = {}

        # LOGIN UI
        center_frame = tk.Frame(root)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="Email").pack()
        self.email_entry = tk.Entry(center_frame, width=40)
        self.email_entry.pack(pady=5)

        tk.Label(center_frame, text="App Password").pack()
        self.password_entry = tk.Entry(center_frame, width=40, show="*")
        self.password_entry.pack(pady=5)

        button_border = tk.Frame(
            center_frame,
            highlightbackground="black",
            highlightthickness=3
        )
        button_border.pack(pady=10)

        self.fun_button = tk.Button(
            button_border,
            text="HAVE FUN!",
            font=("Arial", 24, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=40,
            pady=20,
            command=self.load_emails,
            relief="flat"
        )
        self.fun_button.pack()

        # SCROLL AREA
        self.canvas = tk.Canvas(root)
        self.scroll = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)

        self.frame = tk.Frame(self.canvas)

        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)

    def load_emails(self):
        self.email = self.email_entry.get()
        self.password = self.password_entry.get()

        self.fun_button.master.master.destroy()

        # REFRESH BUTTON
        top_bar = tk.Frame(self.root)
        top_bar.pack(fill="x")

        refresh_btn = tk.Button(
            top_bar,
            text="REFRESH",
            font=("Arial", 10, "bold"),
            command=self.refresh_emails
        )
        refresh_btn.pack(anchor="e", padx=10, pady=5)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y")

        self.refresh_emails()

    # =========================
    # Reliability: try/except
    # =========================
    def refresh_emails(self):
        try:
            emails = fetch_unread_emails(self.email, self.password)
        except Exception:
            messagebox.showerror(
                "Connection Error",
                "Invalid email, app password, or internet connection."
            )
            return

        categorized = self.sort_emails(emails)

        for category in CATEGORY_ORDER:
            if category not in self.category_frames:
                tk.Label(
                    self.frame,
                    text=category,
                    font=("Arial", 14, "bold")
                ).pack(anchor="w", pady=10)

                cat_frame = tk.Frame(self.frame)
                cat_frame.pack(fill="x")

                self.category_frames[category] = cat_frame
                self.category_mails[category] = []

            for mail in categorized[category]:
                self.create_mail_box(mail, category)

    def create_mail_box(self, mail, category):
        box = tk.Frame(
            self.category_frames[category],
            bd=2,
            relief="solid",
            padx=10,
            pady=10
        )

        tk.Label(
            box,
            text=mail.sender,
            font=("Arial", 10, "bold"),
            anchor="w"
        ).pack(fill="x")

        tk.Label(
            box,
            text=f"Subject: {mail.subject}",
            anchor="w"
        ).pack(fill="x", pady=(5, 0))

        tk.Label(
            box,
            text=f"Content: {mail.body[:400]}",
            wraplength=800,
            justify="left",
            anchor="w"
        ).pack(fill="x", pady=(5, 10))

        controls = tk.Frame(box)
        controls.pack(anchor="e")

        priority = ttk.Combobox(
            controls,
            values=PRIORITY_VALUES,
            width=8,
            state="readonly"
        )
        priority.set("Priority")
        priority.pack(side="left", padx=5)

        priority.bind(
            "<<ComboboxSelected>>",
            lambda e, c=category: self.on_priority_change(c)
        )

        status = ttk.Combobox(
            controls,
            values=STATUS,
            width=15,
            state="readonly"
        )
        status.set("Status")
        status.pack(side="left")

        status.bind(
            "<<ComboboxSelected>>",
            lambda e: self.root.after(10, lambda: self.root.focus_set())
        )

        box.pack(fill="x", padx=20, pady=5)

        self.category_mails[category].append({
            "frame": box,
            "priority": priority
        })

    def on_priority_change(self, category):
        self.root.after(10, lambda: self.root.focus_set())
        self.sort_category(category)

    def sort_category(self, category):
        mails = self.category_mails[category]

        mails.sort(
            key=lambda x: PRIORITY_ORDER.get(x["priority"].get(), 4)
        )

        for item in mails:
            item["frame"].pack_forget()

        for item in mails:
            item["frame"].pack(fill="x", padx=20, pady=5)

    def sort_emails(self, emails):
        result = {cat: [] for cat in CATEGORY_ORDER}

        for mail in emails:
            text = (mail.subject + " " + mail.body).lower()
            placed = False

            for category, keywords in CATEGORIES.items():
                for word in keywords:
                    if word in text:
                        result[category].append(mail)
                        placed = True
                        break
                if placed:
                    break

            if not placed:
                result["General"].append(mail)

        return result


root = tk.Tk()
app = MailSorterUI(root)
root.mainloop()