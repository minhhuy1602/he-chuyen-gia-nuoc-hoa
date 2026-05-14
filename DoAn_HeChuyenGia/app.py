import collections
import collections.abc
import os

# Lấy vị trí chính xác của file app.py hiện tại làm gốc
THU_MUC_GOC = os.path.dirname(os.path.abspath(__file__))
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.Iterable = collections.abc.Iterable
collections.Callable = collections.abc.Callable
import streamlit as st
import pandas as pd
import unidecode
import os
from expert_logic import ChuyenGiaNuocHoa, ThongTinNguoiDung

# --- HÀM HỖ TRỢ ---
def lay_duong_dan_anh(ten_nuoc_hoa):
    """Hàm tự động tạo tên file ảnh từ tên nước hoa, chống lỗi phân biệt hoa/thường trên Cloud"""
    ten_khong_dau = unidecode.unidecode(ten_nuoc_hoa).lower()
    ten_file = ten_khong_dau.replace(" ", "_").replace("'", "").replace("&", "")
    
    # Xác định thư mục chứa ảnh
    thu_muc_anh = os.path.join(THU_MUC_GOC, "images")
    
    # Danh sách các biến thể đuôi file có thể xảy ra
    cac_duoi_file = ['.jpg', '.JPG', '.png', '.PNG', '.jpeg', '.JPEG', '.webp', '.WEBP']
    
    for duoi in cac_duoi_file:
        duong_dan = os.path.join(thu_muc_anh, f"{ten_file}{duoi}")
        if os.path.exists(duong_dan):
            return duong_dan
            
    return None # Trả về None nếu duyệt hết vẫn không thấy

# --- GIAO DIỆN CHÍNH ---
st.set_page_config(page_title="Hệ Chuyên Gia Nước Hoa", layout="wide")

st.title("✨ Hệ Chuyên Gia Tư Vấn Nước Hoa Cá Nhân Hóa")
st.markdown("Hệ thống sử dụng **Cơ sở tri thức** và **Suy diễn tiến (Forward Chaining)** để gợi ý mùi hương hoàn hảo cho bạn.")
st.divider()

# Đọc dữ liệu
# Gọi đúng file CSV nằm cùng thư mục với app.py
duong_dan_csv = os.path.join(THU_MUC_GOC, "data_nuochoa.csv")
df = pd.read_csv(duong_dan_csv)

# Bố cục 2 cột cho Form nhập liệu
col1, col2 = st.columns(2)

with col1:
    st.subheader("Trắc nghiệm cá nhân")
    gioi_tinh = st.selectbox("Giới tính của bạn:", ["Nam", "Nữ", "Unisex"])
    hoan_canh = st.selectbox("Mục đích sử dụng chính:", ["Đi làm", "Đa dụng", "Hẹn hò", "Tiệc tùng", "Hoạt động ngoài trời"])
    mua = st.selectbox("Sử dụng vào thời tiết/mùa nào?", ["Xuân Hạ", "Thu Đông", "Mọi mùa"])

with col2:
    st.subheader("Bộ lọc bổ sung")
    phong_cach = st.selectbox("Cá tính/Phong cách của bạn:", ["Thanh lịch, Nhẹ nhàng", "Bí ẩn, Quyến rũ", "Năng động, Thể thao", "Độc lập, Tĩnh lặng"])
    # --------------------------
    luu_huong = st.slider("Yêu cầu độ lưu hương:", 1, 3, 2, format="Mức %d")
    dict_luuhuong = {1: "Trung bình", 2: "Lâu", 3: "Rất lâu"}

st.divider()

# Nút kích hoạt hệ chuyên gia
if st.button("🚀 Phân Tích & Đưa Ra Gợi Ý", use_container_width=True):
    with st.spinner('Đang phân tích tập luật (rules)...'):
        
        # 1. Khởi tạo và chạy Động cơ suy diễn
        engine = ChuyenGiaNuocHoa()
        engine.reset() # Bắt buộc phải có để reset facts
        engine.declare(ThongTinNguoiDung(gioi_tinh=gioi_tinh, hoan_canh=hoan_canh, mua=mua, phong_cach=phong_cach))
        engine.run()
        
        nhom_huong_suy_ra = engine.lay_ket_qua()
        
       # Gọi hàm lấy kết quả
        nhom_huong_suy_ra, ly_do_suy_dien = engine.lay_ket_qua()
        
        # 2. Xử lý kết quả logic
        if not nhom_huong_suy_ra:
            st.warning("Hệ thống chưa có luật cụ thể cho trường hợp này, hiển thị các lựa chọn an toàn nhất.")
            nhom_huong_suy_ra = df['Nhom_Huong'].unique().tolist() 
        else:
            st.success(f"**Kết luận từ hệ chuyên gia:** Dựa trên profile, bạn phù hợp với các nhóm hương: {', '.join(nhom_huong_suy_ra)}")
            st.info(f"🧠 **Giải thích logic suy diễn:** {ly_do_suy_dien}") # <--- DÒNG ĂN ĐIỂM
        
        # 3. Truy vấn Cơ sở tri thức (Lọc Dataframe)
        df_ket_qua = df[
            (df['Gioi_Tinh'] == gioi_tinh) &
            (df['Nhom_Huong'].isin(nhom_huong_suy_ra))
        ]
        
        # Nếu filter quá gắt (hết kết quả), nới lỏng giới tính (gợi ý Unisex)
        if df_ket_qua.empty:
             df_ket_qua = df[(df['Gioi_Tinh'] == 'Unisex') & (df['Nhom_Huong'].isin(nhom_huong_suy_ra))]
             st.info("💡 Không tìm thấy chai đặc trưng cho giới tính của bạn, gợi ý chuyển sang dòng Unisex.")

        # Hiển thị sản phẩm lên UI dạng lưới (Grid)
        if not df_ket_qua.empty:
            st.subheader("Khuyến nghị dành cho bạn:")
            cols = st.columns(3) # Hiển thị 3 chai trên 1 hàng ngang
            for index, row in df_ket_qua.iterrows():
                col_hien_tai = cols[index % 3]
                
                with col_hien_tai:
                    # Gọi hàm lấy đường dẫn ảnh
                    img_path = lay_duong_dan_anh(row['Ten_Nuoc_Hoa'])
                
                    if img_path:
                        st.image(img_path, use_column_width=True)
                    else:
                        st.image("https://via.placeholder.com/300x400?text=No+Image", use_column_width=True) # Ảnh mặc định
                        
                    st.markdown(f"**{row['Ten_Nuoc_Hoa']}**")
                    st.caption(f"Hương: {row['Nhom_Huong']} | Lưu hương: {row['Luu_Huong']}")
                    st.write("---")
        else:
            st.error("Rất tiếc, cơ sở tri thức hiện tại chưa có chai nào khớp hoàn toàn 100% với yêu cầu phức tạp này.")
