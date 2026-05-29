import tkinter as tk
from tkinter import messagebox
import numpy as np

# ==========================================
# สร้างช่องกรอก Matrix
# ==========================================
def create_matrix():
    global entries

    for widget in matrix_frame.winfo_children():
        widget.destroy()

    size = int(size_var.get())

    entries = []

    for i in range(size):
        row = []

        for j in range(size):
            e = tk.Entry(
                matrix_frame,
                width=8,
                font=("Arial", 16),
                justify="center"
            )

            e.grid(row=i, column=j, padx=5, pady=5)

            row.append(e)

        entries.append(row)


# ==========================================
# คำนวณ
# ==========================================
def calculate():

    try:

        size = int(size_var.get())

        A = []

        # รับค่า Matrix
        for i in range(size):

            row = []

            for j in range(size):

                value = float(entries[i][j].get())

                row.append(value)

            A.append(row)

        A = np.array(A)

        # ======================================
        # หา Eigenvalues และ Eigenvectors
        # ======================================

        eigenvalues, eigenvectors = np.linalg.eig(A)

        # ล้างผลลัพธ์เดิม
        result_text.delete(1.0, tk.END)

        result_text.insert(tk.END, "====================================\n")
        result_text.insert(tk.END, "เมทริกซ์ A\n")
        result_text.insert(tk.END, "====================================\n")
        result_text.insert(tk.END, f"{A}\n\n")

        # ======================================
        # 1) Eigenvalues
        # ======================================

        result_text.insert(tk.END, "====================================\n")
        result_text.insert(tk.END, "1) ค่าเจาะจง (Eigenvalues)\n")
        result_text.insert(tk.END, "====================================\n")

        for i, val in enumerate(eigenvalues):

            result_text.insert(
                tk.END,
                f"λ{i+1} = {val:.4f}\n"
            )

        result_text.insert(tk.END, "\n")

        # ======================================
        # 2) Eigenvectors
        # ======================================

        result_text.insert(tk.END, "====================================\n")
        result_text.insert(tk.END, "2) ค่าเวกเตอร์เจาะจง (Eigenvectors)\n")
        result_text.insert(tk.END, "====================================\n")

        for i in range(size):

            vec = eigenvectors[:, i]

            result_text.insert(
                tk.END,
                f"Eigenvector ของ λ{i+1}\n"
            )

            result_text.insert(
                tk.END,
                f"{vec}\n\n"
            )

        # ======================================
        # 3) ตรวจสอบ Diagonalizable
        # ======================================

        result_text.insert(tk.END, "====================================\n")
        result_text.insert(tk.END, "3) ตรวจสอบว่าแปลงเป็นเมทริกซ์ทแยงมุมได้หรือไม่\n")
        result_text.insert(tk.END, "====================================\n")

        rank = np.linalg.matrix_rank(eigenvectors)

        if rank == size:

            result_text.insert(
                tk.END,
                "เมทริกซ์นี้สามารถแปลงเป็นเมทริกซ์ทแยงมุมได้\n\n"
            )

            # ==================================
            # 4) หา P, P^-1 และ D
            # ==================================

            P = eigenvectors

            P_inv = np.linalg.inv(P)

            D = P_inv @ A @ P

            result_text.insert(tk.END, "====================================\n")
            result_text.insert(tk.END, "4) หา P , P^-1 และ D\n")
            result_text.insert(tk.END, "====================================\n")

            result_text.insert(tk.END, "Matrix P\n")
            result_text.insert(tk.END, f"{P}\n\n")

            result_text.insert(tk.END, "Matrix P^-1\n")
            result_text.insert(tk.END, f"{P_inv}\n\n")

            result_text.insert(tk.END, "Matrix D = P^-1 A P\n")
            result_text.insert(tk.END, f"{D}\n\n")

        else:

            result_text.insert(
                tk.END,
                "เมทริกซ์นี้ไม่สามารถแปลงเป็นเมทริกซ์ทแยงมุมได้\n\n"
            )

            # ==================================
            # 5) เหตุผล
            # ==================================

            result_text.insert(tk.END, "====================================\n")
            result_text.insert(tk.END, "5) เหตุผล\n")
            result_text.insert(tk.END, "====================================\n")

            result_text.insert(
                tk.END,
                "จำนวน Eigenvectors อิสระเชิงเส้นไม่เพียงพอ\n"
            )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# ==========================================
# GUI
# ==========================================

root = tk.Tk()

root.title("Eigenvalue & Diagonalization Calculator")

root.geometry("950x750")

# ==========================================
# หัวข้อ
# ==========================================

title = tk.Label(
    root,
    text="โปรแกรมหา Eigenvalue / Eigenvector / Diagonalization",
    font=("Arial", 20, "bold")
)

title.pack(pady=10)

# ==========================================
# เลือกขนาด Matrix
# ==========================================

top_frame = tk.Frame(root)

top_frame.pack()

label_size = tk.Label(
    top_frame,
    text="เลือกขนาด Matrix:",
    font=("Arial", 14)
)

label_size.pack(side=tk.LEFT, padx=5)

size_var = tk.StringVar(value="2")

size_menu = tk.OptionMenu(
    top_frame,
    size_var,
    "2",
    "3"
)

size_menu.config(font=("Arial", 12))

size_menu.pack(side=tk.LEFT)

create_btn = tk.Button(
    top_frame,
    text="สร้าง Matrix",
    font=("Arial", 12),
    command=create_matrix
)

create_btn.pack(side=tk.LEFT, padx=10)

# ==========================================
# พื้นที่กรอก Matrix
# ==========================================

matrix_frame = tk.Frame(root)

matrix_frame.pack(pady=20)

create_matrix()

# ==========================================
# ปุ่มคำนวณ
# ==========================================

calc_btn = tk.Button(
    root,
    text="คำนวณ",
    font=("Arial", 16, "bold"),
    bg="lightblue",
    command=calculate
)

calc_btn.pack(pady=10)

# ==========================================
# พื้นที่แสดงผล
# ==========================================

result_text = tk.Text(
    root,
    width=110,
    height=28,
    font=("Consolas", 11)
)

result_text.pack(pady=10)

# ==========================================
# เริ่มโปรแกรม
# ==========================================

root.mainloop()
