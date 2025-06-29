# 🔐 MPIN Strength Checker

A **Streamlit web application** that checks the strength of your MPIN (Mobile Banking Personal Identification Number) based on commonly used patterns and personal demographic data.

---

## 🚀 Features

- Supports both **4-digit** and **6-digit** MPINs
- Detects:
  - Commonly used MPINs (e.g., `1234`, `000000`, etc.)
  - MPINs based on personal info (DOB, spouse’s DOB, anniversary)
- Visual feedback for `STRONG`, `WEAK`, or `INVALID` MPINs
- Built-in **test case runner** for debugging and validation
- Clean, responsive UI using Streamlit

---

## 🛠️ How It Works

1. Enter a 4 or 6-digit MPIN
2. Optionally enter:
   - Your date of birth
   - Spouse's date of birth
   - Anniversary
3. Click **"Check MPIN Strength"**
4. App evaluates the MPIN based on:
   - Frequency in the common MPIN list
   - Match with any date-based pattern

---

