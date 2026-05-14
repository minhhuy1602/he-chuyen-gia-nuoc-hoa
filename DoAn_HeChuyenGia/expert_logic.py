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
        self.nhom_huong_de_xuat = [] 
        self.ly_do_list = [] # Chuyển thành list để cộng dồn các bước suy luận

    @DefFacts()
    def _initial_action(self):
        yield Fact(action="tu_van")

    # ==========================================
    # TẦNG 1: LUẬT NỀN (BASE RULES) - Đảm bảo luôn có ít nhất 1 luật kích hoạt
    # ==========================================
    
    @Rule(ThongTinNguoiDung(hoan_canh=L('Hẹn hò') | L('Tiệc tùng')))
    def luat_nen_henho_tiectung(self):
        self.nhom_huong_de_xuat.extend(['Ngọt ngào', 'Gia vị', 'Phấn'])
        self.ly_do_list.append("🎯 **Mục đích:** Không gian tiệc tùng/hẹn hò cần sự nổi bật. Kích hoạt nhóm hương có độ bám tỏa cao (Ngọt ngào, Gia vị, Phấn).")

    @Rule(ThongTinNguoiDung(hoan_canh=L('Đi làm') | L('Đa dụng')))
    def luat_nen_congso(self):
        self.nhom_huong_de_xuat.extend(['Tươi mát', 'Gỗ', 'Hoa cỏ'])
        self.ly_do_list.append("🎯 **Mục đích:** Môi trường làm việc/hàng ngày cần sự tinh tế. Lựa chọn nhóm hương an toàn, thanh lịch (Tươi mát, Gỗ, Hoa cỏ nhẹ).")

    @Rule(ThongTinNguoiDung(hoan_canh=L('Hoạt động ngoài trời')))
    def luat_nen_outdoor(self):
        self.nhom_huong_de_xuat.extend(['Tươi mát', 'Trái cây'])
        self.ly_do_list.append("🎯 **Mục đích:** Hoạt động mạnh sinh nhiệt. Ưu tiên tuyệt đối nhóm Tươi mát, Trái cây để tạo cảm giác sảng khoái, không gây ngợp.")

    # ==========================================
    # TẦNG 2: LUẬT BỔ SUNG MÙA/THỜI TIẾT (MODIFIERS)
    # ==========================================
    
    @Rule(ThongTinNguoiDung(mua=L('Thu Đông')))
    def luat_mua_lanh(self):
        self.nhom_huong_de_xuat.extend(['Gỗ', 'Gia vị'])
        self.ly_do_list.append("⛅ **Thời tiết:** Không khí lạnh làm mùi hương khó tỏa. Bổ sung thêm note Gỗ/Gia vị để tạo độ ấm áp và lưu hương lâu hơn trên da.")

    @Rule(ThongTinNguoiDung(mua=L('Xuân Hạ')))
    def luat_mua_nong(self):
        self.nhom_huong_de_xuat.extend(['Tươi mát'])
        self.ly_do_list.append("⛅ **Thời tiết:** Trời nóng dễ làm mùi hương bị nồng gắt. Hệ thống tự động tăng cường các note Tươi mát (Aquatic/Citrus) để cân bằng.")

    # ==========================================
    # TẦNG 3: LUẬT TINH CHỈNH PHONG CÁCH (FINE-TUNING)
    # ==========================================
    
    @Rule(ThongTinNguoiDung(phong_cach=L('Bí ẩn, Quyến rũ')))
    def luat_pc_quyenru(self):
        self.nhom_huong_de_xuat.extend(['Ngọt ngào', 'Gỗ'])
        self.ly_do_list.append("🎩 **Phong cách:** Để tôn lên sự bí ẩn và quyến rũ, điểm xuyết thêm các note trầm ấm, có chiều sâu.")

    @Rule(ThongTinNguoiDung(phong_cach=L('Độc lập, Tĩnh lặng')))
    def luat_pc_tinhlang(self):
        self.nhom_huong_de_xuat.extend(['Gỗ', 'Hoa cỏ'])
        self.ly_do_list.append("🧘 **Phong cách:** Hướng tới sự tĩnh lặng, an yên. Các note Gỗ đàn hương hoặc Hoa cỏ khô sẽ giúp thư giãn tinh thần.")

    # ==========================================
    # XUẤT KẾT QUẢ ĐÃ LỌC
    # ==========================================
    def lay_ket_qua(self):
        # Lọc bỏ các nhóm hương trùng lặp do nhiều luật cùng đẩy vào
        ket_qua_loai_trung = list(set(self.nhom_huong_de_xuat))
        
        # Nối các lý do lại thành một đoạn văn bản hoàn chỉnh
        ly_do_tong_hop = "\n\n".join(self.ly_do_list)
        
        return ket_qua_loai_trung, ly_do_tong_hop
