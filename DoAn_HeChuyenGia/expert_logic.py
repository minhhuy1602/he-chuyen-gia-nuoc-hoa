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
        self.ly_do = "" 

    @DefFacts()
    def _initial_action(self):
        yield Fact(action="tu_van")

    # ==========================================
    # NHÓM LUẬT 1: SỰ KIỆN QUAN TRỌNG & HẸN HÒ
    # ==========================================
    
    @Rule(ThongTinNguoiDung(gioi_tinh='Nam', hoan_canh=L('Hẹn hò') | L('Tiệc tùng'), phong_cach=L('Bí ẩn, Quyến rũ')))
    def luat_nam_badboy_date(self):
        self.nhom_huong_de_xuat.extend(['Ngọt ngào', 'Gia vị'])
        self.ly_do = "Với phong cách bí ẩn và không gian tiệc tùng/hẹn hò, các note hương Gia vị ấm (như Quế, Tiêu) hoặc Ngọt ngào (Vanilla, Khói) sẽ tạo ra sự cuốn hút chết người, cực kỳ bám tỏa."

    @Rule(ThongTinNguoiDung(gioi_tinh='Nữ', hoan_canh=L('Hẹn hò'), phong_cach=L('Thanh lịch, Nhẹ nhàng')))
    def luat_nu_goodgirl_date(self):
        self.nhom_huong_de_xuat.extend(['Hoa cỏ', 'Phấn'])
        self.ly_do = "Một buổi hẹn hò với phong cách thanh lịch rất cần sự tinh tế. Hệ chuyên gia ưu tiên nhóm Hoa cỏ trắng hoặc Phấn (Powdery) để tạo lớp hương mềm mại, lướt nhẹ qua mũi đối phương mà không bị gắt."

    # ==========================================
    # NHÓM LUẬT 2: ĐỜI SỐNG HÀNG NGÀY & CÔNG VIỆC
    # ==========================================
    
    @Rule(ThongTinNguoiDung(hoan_canh=L('Đi làm') | L('Đa dụng'), phong_cach=L('Độc lập, Tĩnh lặng')))
    def luat_lam_viec_mot_minh(self):
        self.nhom_huong_de_xuat.extend(['Gỗ', 'Trái cây'])
        self.ly_do = "Khi bạn làm việc độc lập hoặc tận hưởng không gian riêng, một mùi hương Gỗ trầm ấm (Sandalwood/Cedar) hoặc Trái cây dịu nhẹ sẽ giúp tăng cường sự tập trung và mang lại cảm giác thư giãn tuyệt đối cho chính bản thân bạn."

    @Rule(ThongTinNguoiDung(gioi_tinh='Nam', hoan_canh=L('Đi làm'), phong_cach=L('Năng động, Thể thao'), mua=L('Xuân Hạ')))
    def luat_nam_office_nangdong(self):
        self.nhom_huong_de_xuat.extend(['Tươi mát'])
        self.ly_do = "Môi trường công sở cộng với cá tính năng động vào mùa nóng đòi hỏi một mùi hương cực kỳ 'Fresh'. Nhóm Tươi mát (Biển cả/Citrus) là sự lựa chọn duy nhất để giữ cơ thể luôn sảng khoái."

    # ==========================================
    # NHÓM LUẬT 3: HOẠT ĐỘNG NGOÀI TRỜI (EXTREME)
    # ==========================================
    
    @Rule(ThongTinNguoiDung(hoan_canh=L('Hoạt động ngoài trời'), phong_cach=L('Năng động, Thể thao')))
    def luat_outdoor_trekking(self):
        self.nhom_huong_de_xuat.extend(['Tươi mát', 'Gỗ'])
        self.ly_do = "Khi đối mặt với các chuyến trekking băng rừng rậm hay leo dốc đá, cơ thể vận động liên tục. Sự kết hợp giữa Gỗ (tạo độ bám dai dẳng) và Tươi mát (khử mùi, tạo sinh lực) sẽ là áo giáp hoàn hảo cho chuyến đi cùng những người bạn."

    # ==========================================
    # NHÓM LUẬT 4: LUẬT CẢNH BÁO / ĐIỀU CHỈNH (Ngoại lệ)
    # ==========================================
    
    # Nếu chọn ngọt ngào/gia vị cho mùa Hạ hoặc đi làm -> Hệ thống tự động bẻ lái
    @Rule(ThongTinNguoiDung(mua=L('Xuân Hạ'), hoan_canh=L('Đi làm') | L('Đa dụng')))
    def luat_canh_bao_mua_nong(self):
        # Nới lỏng kết quả bằng cách thêm các nhóm an toàn
        self.nhom_huong_de_xuat.extend(['Tươi mát', 'Hoa cỏ'])
        # Thêm một note nhỏ vào lý do
        self.ly_do += " (Lưu ý: Hệ thống đã tự động lọc bớt các mùi hương quá nồng ngọt vì thời tiết Xuân Hạ hoặc môi trường kín sẽ gây khó chịu cho người xung quanh)."

    def lay_ket_qua(self):
        return list(set(self.nhom_huong_de_xuat)), self.ly_do
