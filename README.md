# Smart Mail Sorter — Gmail Email To-Do Organizer

## Overview
Smart Mail Sorter is a Python GUI application that connects to Gmail and converts unread emails into a structured To-Do list.  
The program automatically categorizes emails using keywords, allows users to assign priority levels, and track working status.

This project demonstrates **Object-Oriented Programming (OOP)**, **GUI development**, and **Gmail email processing** using Python.

---

## Features

- Connect to Gmail using App Password
- Scan unread emails automatically
- Sort emails into categories using keywords
- Set priority (Must / Should / Can / WGS?)
- Mark status (Working / About to / Done)
- Refresh button to load new emails
- Scrollable user interface
- Automatic priority sorting

---

## Categories

Emails are sorted into the following categories:

- Academic
- Required/Compulsory
- Deadline
- Survey
- Advertisement
- General

Sorting is based on keywords found in the email subject and content.

---

## Priority System

Users can assign a priority to each email:

- Must
- Should
- Can
- WGS?

Emails are automatically sorted by priority:

Must → highest priority  
Should → medium priority  
Can → low priority  
WGS? → lowest priority  

---

## Status System

Each email can be marked with a working status:

- 🟢 Working  
- ⚪ About to  
- ❌ Done  

This allows users to track task progress.

---

## Libraries Used

The program uses only Python standard libraries:

- `tkinter` — GUI interface
- `ttk` — dropdown menus
- `imaplib` — connect to Gmail
- `email` — parse email data
- `decode_header` — decode sender name
- `messagebox` — error handling popup

---

## Object-Oriented Design

### Classes

**BaseUI**  
Base class for UI structure.

**MailItem**  
Represents one email object.

Attributes:
- sender  
- subject  
- body  
- priority  
- status  

**MailSorterUI**  
Main application class that handles:
- Login screen  
- Fetching emails  
- Categorization  
- UI display  
- Priority sorting  
- Refresh button  

---

## Program Workflow

1. User enters Gmail and App Password  
2. Click "HAVE FUN" button  
3. Program connects to Gmail  
4. Fetch unread emails  
5. Sort emails into categories  
6. Display emails in UI  
7. User sets priority and status  
8. User refreshes to load new emails  

---

## Error Handling

The program handles:

- Invalid email login
- Wrong app password
- Internet connection error
- Gmail connection failure

An error message popup is shown when connection fails.

---

## Installation

Requirements:

- Python 3.x
- Gmail account
- Gmail App Password

No external libraries required.

---

## How to Run

Run the program:

Enter:

- Gmail address
- Gmail App Password

Click **HAVE FUN**.

---

## Project Structure

---

## State Diagram

Login Screen  
↓  
Load Emails  
↓  
Display Emails  
↓  
Set Priority / Status  
↓  
Refresh Emails  

---

## Author

Tran Trieu Vi  
Python Programming Final Project
