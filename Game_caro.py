"""
GAME CỜ CARO - PHIÊN BẢN DÙNG CLASS (OOP CƠ BẢN)

Luật chơi: 2 người thay nhau đánh X và O.
Ai có 5 quân liên tiếp (ngang/dọc/chéo) trước thì thắng.

Class là 1 cách "gói" dữ liệu (bàn cờ, lượt chơi...) và các hàm
liên quan (vẽ, kiểm tra thắng...) vào chung 1 "đối tượng".
- self  = chính đối tượng đang được thao tác (giống như "cái này")
- __init__ = hàm chạy đầu tiên khi tạo đối tượng, dùng để khởi tạo dữ liệu
"""

import tkinter as tk
from tkinter import messagebox

#  THÔNG SỐ CỐ ĐỊNH 
SO_O = 15          # Bàn cờ 15x15 ô
KICH_THUOC_O = 40  # Mỗi ô rộng 40 pixel
SO_QUAN_THANG = 5  # Cần 5 quân liên tiếp để thắng


class CoCaro:
    """Class này chứa toàn bộ logic và giao diện của trò chơi cờ caro."""

    def __init__(self, cua_so):
        """Hàm khởi tạo: chạy khi ta viết CoCaro(cua_so) để tạo game mới."""
        self.cua_so = cua_so
        self.cua_so.title("Cờ Caro - Dạng Class")
        self.cua_so.resizable(False, False)

        # Dữ liệu trạng thái game (lưu trong self để hàm nào cũng dùng được)
        self.ban_co = self.tao_ban_co_rong()
        self.nguoi_hien_tai = "X"
        self.da_ket_thuc = False

        #  Nhãn hiện lượt chơi
        self.nhan_thong_bao = tk.Label(
            cua_so, text="Lượt của: X", font=("Arial", 14, "bold")
        )
        self.nhan_thong_bao.pack(pady=8)

        # Canvas để vẽ bàn cờ
        kich_thuoc_canvas = SO_O * KICH_THUOC_O
        self.canvas = tk.Canvas(
            cua_so, width=kich_thuoc_canvas, height=kich_thuoc_canvas, bg="#f0d9b5"
        )
        self.canvas.pack(padx=10, pady=10)

        # Khi click chuột trái vào canvas -> gọi hàm self.xu_ly_click
        self.canvas.bind("<Button-1>", self.xu_ly_click)

        #  Nút chơi lại 
        self.nut_choi_lai = tk.Button(
            cua_so, text="Chơi lại", font=("Arial", 11), command=self.choi_lai
        )
        self.nut_choi_lai.pack(pady=10)

        # Vẽ lưới bàn cờ lần đầu
        self.ve_luoi_ban_co()

    #  CÁC HÀM (gọi là "phương thức") CỦA CLASS 

    def tao_ban_co_rong(self):
        """Tạo 1 danh sách 2 chiều toàn None (đại diện cho ô trống)."""
        ban_co = []
        for hang in range(SO_O):
            dong_moi = []
            for cot in range(SO_O):
                dong_moi.append(None)
            ban_co.append(dong_moi)
        return ban_co

    def ve_luoi_ban_co(self):
        """Vẽ các đường kẻ ngang dọc tạo thành bàn cờ."""
        kich_thuoc_canvas = SO_O * KICH_THUOC_O
        for i in range(SO_O + 1):
            self.canvas.create_line(0, i * KICH_THUOC_O, kich_thuoc_canvas, i * KICH_THUOC_O)
            self.canvas.create_line(i * KICH_THUOC_O, 0, i * KICH_THUOC_O, kich_thuoc_canvas)

    def cap_nhat_thong_bao(self):
        """Hiện chữ 'Lượt của: X' hoặc 'Lượt của: O' ở trên."""
        self.nhan_thong_bao.config(text=f"Lượt của: {self.nguoi_hien_tai}")

    def ve_quan_co(self, hang, cot, nguoi_choi):
        """Vẽ chữ X hoặc vòng tròn O tại ô (hang, cot)."""
        x1 = cot * KICH_THUOC_O + 6
        y1 = hang * KICH_THUOC_O + 6
        x2 = (cot + 1) * KICH_THUOC_O - 6
        y2 = (hang + 1) * KICH_THUOC_O - 6

        if nguoi_choi == "X":
            self.canvas.create_line(x1, y1, x2, y2, width=3, fill="red")
            self.canvas.create_line(x1, y2, x2, y1, width=3, fill="red")
        else:
            self.canvas.create_oval(x1, y1, x2, y2, width=3, outline="blue")

    def dem_quan_lien_tiep(self, hang, cot, nguoi_choi, huong_hang, huong_cot):
        """
        Đếm có bao nhiêu quân liên tiếp cùng loại,
        tính từ ô (hang, cot) theo 1 hướng cho trước.
        """
        dem = 0
        h = hang + huong_hang
        c = cot + huong_cot

        while 0 <= h < SO_O and 0 <= c < SO_O and self.ban_co[h][c] == nguoi_choi:
            dem += 1
            h += huong_hang
            c += huong_cot

        return dem

    def kiem_tra_thang(self, hang, cot, nguoi_choi):
        """Kiểm tra nước đi vừa rồi có tạo thành 5 quân liên tiếp không."""
        danh_sach_huong = [
            (0, 1),   # ngang
            (1, 0),   # dọc
            (1, 1),   # chéo \
            (1, -1),  # chéo /
        ]

        for buoc_hang, buoc_cot in danh_sach_huong:
            so_ben_truoc = self.dem_quan_lien_tiep(hang, cot, nguoi_choi, buoc_hang, buoc_cot)
            so_ben_sau = self.dem_quan_lien_tiep(hang, cot, nguoi_choi, -buoc_hang, -buoc_cot)
            tong = so_ben_truoc + so_ben_sau + 1

            if tong >= SO_QUAN_THANG:
                return True

        return False

    def ban_co_da_day(self):
        """Kiểm tra tất cả các ô đã có quân chưa (để báo hòa)."""
        for hang in range(SO_O):
            for cot in range(SO_O):
                if self.ban_co[hang][cot] is None:
                    return False
        return True

    def doi_luot(self):
        """Đổi lượt chơi từ X sang O hoặc ngược lại."""
        if self.nguoi_hien_tai == "X":
            self.nguoi_hien_tai = "O"
        else:
            self.nguoi_hien_tai = "X"

    def xu_ly_click(self, event):
        """Chạy mỗi khi người chơi click chuột vào bàn cờ."""
        if self.da_ket_thuc:
            return

        cot = event.x // KICH_THUOC_O
        hang = event.y // KICH_THUOC_O

        if self.ban_co[hang][cot] is not None:
            return  # Ô đã có quân rồi thì bỏ qua

        # Đánh quân vào ô đó
        self.ban_co[hang][cot] = self.nguoi_hien_tai
        self.ve_quan_co(hang, cot, self.nguoi_hien_tai)

        # Kiểm tra thắng
        if self.kiem_tra_thang(hang, cot, self.nguoi_hien_tai):
            self.da_ket_thuc = True
            self.nhan_thong_bao.config(text=f"{self.nguoi_hien_tai} đã thắng!")
            messagebox.showinfo("Kết thúc", f"Người chơi {self.nguoi_hien_tai} thắng!")
            return

        # Kiểm tra hòa
        if self.ban_co_da_day():
            self.da_ket_thuc = True
            self.nhan_thong_bao.config(text="Hòa!")
            messagebox.showinfo("Kết thúc", "Ván cờ hòa!")
            return

        # Chưa ai thắng thì đổi lượt
        self.doi_luot()
        self.cap_nhat_thong_bao()

    def choi_lai(self):
        """Xóa bàn cờ, chơi lại từ đầu."""
        self.ban_co = self.tao_ban_co_rong()
        self.nguoi_hien_tai = "X"
        self.da_ket_thuc = False

        self.canvas.delete("all")
        self.ve_luoi_ban_co()
        self.cap_nhat_thong_bao()


#  CHẠY CHƯƠNG TRÌNH 
if __name__ == "__main__":
    cua_so = tk.Tk()
    game = CoCaro(cua_so)   # Tạo 1 đối tượng game từ class CoCaro
    cua_so.mainloop()