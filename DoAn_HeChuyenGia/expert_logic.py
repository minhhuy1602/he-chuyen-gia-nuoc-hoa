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
        # Lưu trữ điểm tin cậy cho từng nhóm hương
        self.certainty_scores = {
            'Tươi mát': 0, 'Gỗ': 0, 'Ngọt ngào': 0, 
            'Gia vị': 0, 'Hoa cỏ': 0, 'Phấn': 0, 'Trái cây': 0
        }
        self.ly_do_list = []

    @DefFacts()
    def _initial_action(self):
        yield Fact(action="tu_van")

    # --- TẦNG 1: LUẬT NỀN (TRỌNG SỐ CAO: 0.5) ---
    @Rule(ThongTinNguoiDung(hoan_canh=L('Hẹn hò') | L('Tiệc tùng')))
    def luat_nen_henho(self):
        self.certainty_scores['Ngọt ngào'] += 0.5
        self.certainty_scores['Gia vị'] += 0.4
        self.ly_do_list.append("🔹 Bối cảnh Tiệc tùng/Hẹn hò xác lập niềm tin cơ bản vào nhóm hương bám tỏa (CF: +0.5)")

    @Rule(ThongTinNguoiDung(hoan_canh=L('Hoạt động ngoài trời')))
    def luat_nen_outdoor(self):
        self.certainty_scores['Tươi mát'] += 0.5
        self.certainty_scores['Trái cây'] += 0.3
        self.ly_do_list.append("🔹 Hoạt động ngoài trời sinh nhiệt, ưu tiên nhóm hương giải nhiệt (CF: +0.5)")

    # --- TẦNG 2: LUẬT CỦNG CỐ THỜI TIẾT (TRỌNG SỐ: 0.3) ---
    @Rule(ThongTinNguoiDung(mua=L('Thu Đông')))
    def luat_mua_lanh(self):
        self.certainty_scores['Gỗ'] += 0.3
        self.certainty_scores['Gia vị'] += 0.2
        self.ly_do_list.append("🔹 Thời tiết lạnh củng cố sự phù hợp của nhóm hương ấm (CF: +0.3)")

    @Rule(ThongTinNguoiDung(mua=L('Xuân Hạ')))
    def luat_mua_nong(self):
        self.certainty_scores['Tươi mát'] += 0.3
        self.ly_do_list.append("🔹 Thời tiết nóng gia tăng điểm số cho nhóm hương thanh khiết (CF: +0.3)")

    # --- TẦNG 3: LUẬT TINH CHỈNH PHONG CÁCH (TRỌNG SỐ: 0.2) ---
    @Rule(ThongTinNguoiDung(phong_cach=L('Bí ẩn, Quyến rũ')))
    def luat_pc_quyenru(self):
        self.certainty_scores['Ngọt ngào'] += 0.2
        self.certainty_scores['Gỗ'] += 0.2
        self.ly_do_list.append("🔹 Phong cách quyến rũ bổ trợ thêm trọng số cho các note hương trầm (CF: +0.2)")

    @Rule(ThongTinNguoiDung(phong_cach=L('Năng động, Thể thao')))
    def luat_pc_nang_dong(self):
        self.certainty_scores['Tươi mát'] += 0.2
        self.ly_do_list.append("🔹 Cá tính năng động yêu cầu sự sảng khoái tối đa (CF: +0.2)")

    def lay_ket_qua(self):
        # Chỉ lấy những nhóm hương có điểm tin cậy > 0
        ket_qua_co_diem = {k: v for k, v in self.certainty_scores.items() if v > 0}
        
        # Chuyển đổi sang định dạng % (max điểm có thể đạt là 1.0)
        ket_qua_final = {k: min(int(v * 100), 100) for k, v in ket_qua_co_diem.items()}
        
        return ket_qua_final, "\n\n".join(self.ly_do_list)
