import collections
import collections.abc
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.Iterable = collections.abc.Iterable
collections.Callable = collections.abc.Callable

from experta import *

class ThongTinNguoiDung(Fact):
    pass

class ChuyenGiaNuocHoa(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        # Điểm CF ban đầu của mọi nhóm hương là 0
        self.certainty_scores = {
            'Tươi mát': 0.0, 'Gỗ': 0.0, 'Ngọt ngào': 0.0, 
            'Gia vị': 0.0, 'Hoa cỏ': 0.0, 'Phấn': 0.0, 'Trái cây': 0.0
        }
        self.ly_do_list = []

    # --- HÀM TÍNH TOÁN CF CHUẨN MYCIN (ĐỒNG KẾT LUẬN) ---
    def cap_nhat_cf(self, nhom_huong, cf_luat_moi):
        cf_hien_tai = self.certainty_scores[nhom_huong]
        
        # Áp dụng công thức: CF_combine = CF1 + CF2 - (CF1 * CF2)
        cf_cap_nhat = cf_hien_tai + cf_luat_moi - (cf_hien_tai * cf_luat_moi)
        
        self.certainty_scores[nhom_huong] = round(cf_cap_nhat, 4) # Làm tròn 4 chữ số

    @DefFacts()
    def _initial_action(self):
        yield Fact(action="tu_van")

    # --- TẦNG 1: LUẬT NỀN ---
    @Rule(ThongTinNguoiDung(hoan_canh=L('Hẹn hò') | L('Tiệc tùng')))
    def luat_nen_henho(self):
        # Gọi hàm cập nhật CF thay vì dùng phép +=
        self.cap_nhat_cf('Ngọt ngào', 0.5)
        self.cap_nhat_cf('Gia vị', 0.4)
        self.ly_do_list.append("🔹 Bối cảnh Tiệc tùng/Hẹn hò: Khởi tạo CF nhóm Ngọt ngào (0.5), Gia vị (0.4)")

    @Rule(ThongTinNguoiDung(hoan_canh=L('Hoạt động ngoài trời')))
    def luat_nen_outdoor(self):
        self.cap_nhat_cf('Tươi mát', 0.6)
        self.cap_nhat_cf('Trái cây', 0.4)
        self.ly_do_list.append("🔹 Hoạt động ngoài trời: Khởi tạo CF nhóm Tươi mát (0.6), Trái cây (0.4)")

    # --- TẦNG 2: LUẬT CỦNG CỐ THỜI TIẾT ---
    @Rule(ThongTinNguoiDung(mua=L('Thu Đông')))
    def luat_mua_lanh(self):
        self.cap_nhat_cf('Gỗ', 0.4)
        self.cap_nhat_cf('Gia vị', 0.3)
        self.ly_do_list.append("🔹 Thời tiết Lạnh: Củng cố thêm CF cho nhóm Gỗ (0.4), Gia vị (0.3)")

    @Rule(ThongTinNguoiDung(mua=L('Xuân Hạ')))
    def luat_mua_nong(self):
        self.cap_nhat_cf('Tươi mát', 0.4)
        self.ly_do_list.append("🔹 Thời tiết Nóng: Củng cố thêm CF cho nhóm Tươi mát (0.4)")

    # --- TẦNG 3: LUẬT TINH CHỈNH PHONG CÁCH ---
    @Rule(ThongTinNguoiDung(phong_cach=L('Bí ẩn, Quyến rũ')))
    def luat_pc_quyenru(self):
        self.cap_nhat_cf('Ngọt ngào', 0.3)
        self.cap_nhat_cf('Gỗ', 0.2)
        self.ly_do_list.append("🔹 Phong cách Bí ẩn: Củng cố thêm CF cho nhóm Ngọt ngào (0.3), Gỗ (0.2)")

    @Rule(ThongTinNguoiDung(phong_cach=L('Năng động, Thể thao')))
    def luat_pc_nang_dong(self):
        self.cap_nhat_cf('Tươi mát', 0.3)
        self.ly_do_list.append("🔹 Cá tính Năng động: Củng cố thêm CF cho nhóm Tươi mát (0.3)")

    def lay_ket_qua(self):
        # Lấy các nhóm hương có CF > 0 và quy đổi ra thang điểm 100%
        ket_qua_final = {k: int(v * 100) for k, v in self.certainty_scores.items() if v > 0}
        return ket_qua_final, "\n\n".join(self.ly_do_list)
