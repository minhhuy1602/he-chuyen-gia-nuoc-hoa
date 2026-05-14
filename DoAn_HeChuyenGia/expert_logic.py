from experta import *

# Định nghĩa dữ kiện đầu vào từ người dùng
class ThongTinNguoiDung(Fact):
    pass

# Xây dựng Động cơ suy diễn
class ChuyenGiaNuocHoa(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.nhom_huong_de_xuat = [] 
        self.ly_do = "" # Lưu trữ diễn giải logic để báo cáo với người dùng

    @DefFacts()
    def _initial_action(self):
        yield Fact(action="tu_van")

    # --- TẬP LUẬT CHO NAM ---

    # LUẬT 1: Nam + Văn phòng/Đa dụng + Thời tiết nóng/Mọi mùa
    @Rule(ThongTinNguoiDung(gioi_tinh='Nam', hoan_canh=L('Đi làm') | L('Đa dụng'), mua=L('Xuân Hạ') | L('Mọi mùa')))
    def luat_nam_vanphong_antoan(self):
        self.nhom_huong_de_xuat.extend(['Tươi mát', 'Gỗ'])
        self.ly_do = "Môi trường văn phòng hoặc sử dụng hàng ngày cần sự tinh tế, không làm phiền người xung quanh. Nhóm hương Tươi mát (Citrus/Aquatic) hoặc Gỗ nhẹ (như Versace Pour Homme hay Bleu De Chanel) là lựa chọn an toàn và thanh lịch nhất."

    # LUẬT 2: Nam + Hẹn hò/Tiệc tùng + Thời tiết lạnh
    @Rule(ThongTinNguoiDung(gioi_tinh='Nam', hoan_canh=L('Hẹn hò') | L('Tiệc tùng'), mua=L('Thu Đông')))
    def luat_nam_quyenru_lanh(self):
        self.nhom_huong_de_xuat.extend(['Ngọt ngào', 'Gia vị', 'Gỗ'])
        self.ly_do = "Không khí lạnh của Thu Đông có xu hướng làm 'chìm' mùi hương. Để tạo ấn tượng mạnh trong buổi hẹn hò hay tiệc tùng, hệ thống kích hoạt luật khuyên dùng nhóm hương Ngọt ngào hoặc Gia vị ấm (như JPG Ultra Male, YSL La Nuit L'Homme) để tăng độ tỏa hương."

    # LUẬT 3: Nam + Hoạt động ngoài trời (Đi phượt, Trekking)
    @Rule(ThongTinNguoiDung(gioi_tinh='Nam', hoan_canh=L('Hoạt động ngoài trời')))
    def luat_nam_outdoor(self):
        self.nhom_huong_de_xuat.extend(['Tươi mát', 'Trái cây'])
        self.ly_do = "Khi tham gia các chuyến đi dã ngoại, trekking hoặc hoạt động thể chất cùng hội bạn, cơ thể tỏa nhiệt nhiều. Những tone mùi quá nồng sẽ gây ngợp. Nhóm Tươi mát, sảng khoái (như Armaf Club De Nuit Iconic) sẽ giúp giữ năng lượng bền bỉ suốt chặng đường."

    # --- TẬP LUẬT CHO NỮ ---

    # LUẬT 4: Nữ + Hẹn hò/Tiệc tùng 
    @Rule(ThongTinNguoiDung(gioi_tinh='Nữ', hoan_canh=L('Hẹn hò') | L('Tiệc tùng')))
    def luat_nu_quyenru(self):
        self.nhom_huong_de_xuat.extend(['Ngọt ngào', 'Hoa cỏ', 'Phấn'])
        self.ly_do = "Sự kết hợp giữa không gian tiệc tùng/hẹn hò đòi hỏi sự nữ tính và lưu luyến. Nhóm hương Phấn (như Narciso Poudrée) hoặc Hoa cỏ đậm đặc sẽ tôn lên nét quyến rũ tuyệt đối."

    # LUẬT 5: Nữ + Văn phòng/Đa dụng
    @Rule(ThongTinNguoiDung(gioi_tinh='Nữ', hoan_canh=L('Đi làm') | L('Đa dụng')))
    def luat_nu_thanhlich(self):
        self.nhom_huong_de_xuat.extend(['Hoa cỏ', 'Trái cây', 'Tươi mát'])
        self.ly_do = "Môi trường công sở cần sự nhẹ nhàng, chuyên nghiệp. Nhóm hương Hoa cỏ trắng hoặc Trái cây nhẹ nhàng sẽ tạo cảm giác dễ chịu, thanh tao."

    # --- TẬP LUẬT CHO UNISEX ---

    # LUẬT 6: Unisex + Thời tiết lạnh
    @Rule(ThongTinNguoiDung(gioi_tinh='Unisex', mua=L('Thu Đông')))
    def luat_unisex_lanh(self):
        self.nhom_huong_de_xuat.extend(['Gỗ', 'Ngọt ngào', 'Gia vị'])
        self.ly_do = "Dòng Unisex vào mùa lạnh thường khai thác chiều sâu của Gỗ và Gia vị, tạo ra một lớp hương ấm áp, bí ẩn, phù hợp cho những ai có cá tính độc lập, phá cách."
        
    # LUẬT 7: Unisex + Thời tiết nóng
    @Rule(ThongTinNguoiDung(gioi_tinh='Unisex', mua=L('Xuân Hạ') | L('Mọi mùa')))
    def luat_unisex_nong(self):
        self.nhom_huong_de_xuat.extend(['Tươi mát', 'Trái cây'])
        self.ly_do = "Mùi hương Unisex cho mùa nóng thiên về sự sạch sẽ, tối giản. Các note hương Trái cây hoặc Tươi mát sẽ mang lại cảm giác 'fresh out of the shower' (vừa tắm xong) cực kỳ nịnh mũi."

    # Hàm lấy kết quả và lý do
    def lay_ket_qua(self):
        return list(set(self.nhom_huong_de_xuat)), self.ly_do