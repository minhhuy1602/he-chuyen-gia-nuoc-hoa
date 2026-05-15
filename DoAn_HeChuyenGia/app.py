# --- BẮT ĐẦU VÁ LỖI PYTHON 3.12 ---
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.Iterable = collections.abc.Iterable
collections.Callable = collections.abc.Callable
# --- KẾT THÚC VÁ LỖI ---

import streamlit as st
import pandas as pd
import unidecode
import os
from expert_logic import ChuyenGiaNuocHoa, ThongTinNguoiDung

# Lấy vị trí chính xác của file app.py hiện tại làm gốc (chống lỗi Cloud)
THU_MUC_GOC = os.path.dirname(os.path.abspath(__file__))

# --- HÀM HỖ TRỢ ---
def lay_duong_dan_anh(ten_nuoc_hoa):
    """Hàm tự động tạo tên file ảnh từ tên nước hoa, chống lỗi phân biệt hoa/thường trên Cloud"""
    ten_khong_dau = unidecode.unidecode(ten_nuoc_hoa).lower()
    ten_file = ten_khong_dau.replace(" ", "_").replace("'", "").replace("&", "")
    
    thu_muc_anh = os.path.join(THU_MUC_GOC, "images")
    cac_duoi_file = ['.jpg', '.JPG', '.png', '.PNG', '.jpeg', '.JPEG', '.webp', '.WEBP']
    
    for duoi in cac_duoi_file:
        duong_dan = os.path.join(thu_muc_anh, f"{ten_file}{duoi}")
        if os.path.exists(duong_dan):
            return duong_dan
    return None 

# --- GIAO DIỆN CHÍNH ---
st.set_page_config(page_title="Hệ Chuyên Gia Nước Hoa", layout="wide")

st.title("✨ Hệ Chuyên Gia Tư Vấn Nước Hoa AI")
st.markdown("Đồ án tích hợp Cơ sở tri thức cùng hai cơ chế **Suy diễn tiến (Forward Chaining)** và **Suy diễn lùi (Backward Chaining)**.")
st.divider()

# Đọc dữ liệu
duong_dan_csv = os.path.join(THU_MUC_GOC, "data_nuochoa.csv")
df = pd.read_csv(duong_dan_csv)

# TẠO 2 TAB ĐỂ TRÌNH BÀY CHO HỘI ĐỒNG
tab1, tab2 = st.tabs(["🚀 CƠ CHẾ SUY DIỄN TIẾN (Tìm kiếm)", "🔍 CƠ CHẾ SUY DIỄN LÙI (Kiểm định)"])

# ==========================================
# TAB 1: SUY DIỄN TIẾN (FORWARD CHAINING)
# ==========================================
with tab1:
    st.header("Tư vấn Nước hoa cá nhân hóa")
    col1, col2 = st.columns(2)

    with col1:
        gioi_tinh = st.selectbox("Giới tính của bạn:", ["Nam", "Nữ", "Unisex"], key="fw_gt")
        hoan_canh = st.selectbox("Mục đích sử dụng chính:", ["Đi làm", "Đa dụng", "Hẹn hò", "Tiệc tùng", "Hoạt động ngoài trời"], key="fw_hc")
        mua = st.selectbox("Thời tiết/mùa sử dụng:", ["Xuân Hạ", "Thu Đông", "Mọi mùa"], key="fw_mua")

    with col2:
        phong_cach = st.selectbox("Cá tính/Phong cách:", ["Thanh lịch, Nhẹ nhàng", "Bí ẩn, Quyến rũ", "Năng động, Thể thao", "Độc lập, Tĩnh lặng"], key="fw_pc")
        st.info("💡 Suy diễn tiến: Bắt đầu từ các **Sự kiện (Dữ liệu đầu vào)**, hệ thống sẽ kích hoạt các tập luật để đi đến **Kết luận (Gợi ý chai nước hoa)**.")

    if st.button("Chạy Suy Diễn Tiến", type="primary", use_container_width=True):
        with st.spinner('Đang kích hoạt Động cơ suy diễn (Inference Engine)...'):
            engine = ChuyenGiaNuocHoa()
            engine.reset() 
            engine.declare(ThongTinNguoiDung(gioi_tinh=gioi_tinh, hoan_canh=hoan_canh, mua=mua, phong_cach=phong_cach))
            engine.run()
            
            nhom_huong_suy_ra, ly_do_suy_dien = engine.lay_ket_qua()
            
            if not nhom_huong_suy_ra:
                st.warning("Hệ thống xử lý ngoại lệ: Không có luật khớp hoàn toàn, nới lỏng điều kiện an toàn.")
                nhom_huong_suy_ra = df['Nhom_Huong'].unique().tolist() 
            else:
                st.success(f"**Kết luận:** Nhóm hương phù hợp nhất là: {', '.join(nhom_huong_suy_ra)}")
                st.info(f"🧠 **Vết suy luận (Trace):**\n{ly_do_suy_dien}")
            
            # Lọc Database
            df_ket_qua = df[(df['Gioi_Tinh'].isin([gioi_tinh, 'Unisex'])) & (df['Nhom_Huong'].isin(nhom_huong_suy_ra))]

            if not df_ket_qua.empty:
                st.subheader("Sản phẩm gợi ý & Độ phù hợp:")
                
                # --- THUẬT TOÁN TÍNH % PHÙ HỢP ---
                def tinh_diem_phu_hop(row, user_gt, user_hc, user_mua, nhom_huong_goi_y):
                    score = 0
                    # 1. Khớp nhóm hương (40đ)
                    if row['Nhom_Huong'] in nhom_huong_goi_y: score += 40
                    # 2. Khớp hoàn cảnh (25đ)
                    if row['Hoan_Canh'] == user_hc or row['Hoan_Canh'] == 'Đa dụng': score += 25
                    # 3. Khớp mùa (20đ)
                    if row['Mua'] == user_mua or row['Mua'] == 'Mọi mùa': score += 20
                    # 4. Khớp giới tính (15đ)
                    if row['Gioi_Tinh'] == user_gt or row['Gioi_Tinh'] == 'Unisex': score += 15
                    return score

                # Tính điểm cho từng dòng
                df_ket_qua['Diem'] = df_ket_qua.apply(lambda r: tinh_diem_phu_hop(r, gioi_tinh, hoan_canh, mua, nhom_huong_suy_ra), axis=1)
                
                # Sắp xếp chai có điểm cao nhất lên đầu
                df_ket_qua = df_ket_qua.sort_values(by='Diem', ascending=False)

                cols = st.columns(4) 
                for index, (idx_row, row) in enumerate(df_ket_qua.iterrows()):
                    col_hien_tai = cols[index % 4]
                    with col_hien_tai:
                        # Hiển thị Badge % phù hợp
                        color = "green" if row['Diem'] >= 80 else "orange"
                        st.markdown(f"**<span style='color:{color}; font-size:20px;'>{row['Diem']}% Khớp</span>**", unsafe_allow_html=True)
                        
                        img_path = lay_duong_dan_anh(row['Ten_Nuoc_Hoa'])
                        if img_path:
                            st.image(img_path, use_container_width=True)
                        else:
                            import urllib.parse
                            ten_hien_thi = urllib.parse.quote(row['Ten_Nuoc_Hoa'])
                            st.image(f"https://ui-avatars.com/api/?name={ten_hien_thi}&size=400&background=random&color=fff&font-size=0.25&length=3", use_container_width=True)
                        
                        st.markdown(f"**{row['Ten_Nuoc_Hoa']}**")
                        st.progress(row['Diem'] / 100) # Thanh tiến trình nhỏ cho đẹp
                        st.caption(f"{row['Nhom_Huong']} | {row['Luu_Huong']}")

# ==========================================
# TAB 2: SUY DIỄN LÙI (BACKWARD CHAINING)
# ==========================================
with tab2:
    st.header("Kiểm định Giả thuyết (Traced Backward Evaluation)")
    
    # Người dùng chọn giả thuyết (Goal)
    danh_sach_nuoc_hoa = df['Ten_Nuoc_Hoa'].tolist()
    muc_tieu = st.selectbox("🎯 Đặt Giả thuyết (Goal): Tôi muốn sử dụng chai nước hoa sau cho hôm nay:", danh_sach_nuoc_hoa)
    
    st.markdown("---")
    st.subheader("Cung cấp dữ kiện hiện tại của bạn:")
    col3, col4 = st.columns(2)
    with col3:
        user_gt = st.radio("Giới tính của bạn:", ["Nam", "Nữ"])
    with col4:
        user_hc = st.selectbox("Bạn định dùng nó để đi đâu?", ["Đi làm", "Đa dụng", "Hẹn hò", "Tiệc tùng", "Hoạt động ngoài trời"])
        user_mua = st.selectbox("Thời tiết hôm nay thế nào?", ["Xuân Hạ", "Thu Đông"])

    if st.button("Chạy Suy Diễn Lùi", type="primary", use_container_width=True):
        st.markdown(f"### Phân giải cây logic cho mục tiêu: `{muc_tieu}`")
        
        # Truy xuất tập luật (facts) của chai nước hoa từ Cơ sở tri thức
        thong_tin_chai = df[df['Ten_Nuoc_Hoa'] == muc_tieu].iloc[0]
        dk_gioi_tinh = thong_tin_chai['Gioi_Tinh']
        dk_hoan_canh = thong_tin_chai['Hoan_Canh']
        dk_mua = thong_tin_chai['Mua']
        
        hop_le = True
        
        # BƯỚC 1: BACKTRACK GIỚI TÍNH
        with st.expander("Giai đoạn 1: Xác minh Giới tính", expanded=True):
            st.write(f"Đang tìm luật (Rule): Giới tính yêu cầu = `{dk_gioi_tinh}`")
            if dk_gioi_tinh == 'Unisex' or user_gt == dk_gioi_tinh:
                st.success(f"✅ Đạt. (Người dùng là {user_gt}, khớp với yêu cầu).")
            else:
                st.error(f"❌ Xung đột. (Chai này thiết kế cho {dk_gioi_tinh}, nhưng bạn là {user_gt}).")
                hop_le = False
                
        # BƯỚC 2: BACKTRACK HOÀN CẢNH
        with st.expander("Giai đoạn 2: Xác minh Hoàn cảnh sử dụng", expanded=True):
            st.write(f"Đang tìm luật (Rule): Hoàn cảnh tối ưu = `{dk_hoan_canh}`")
            # Logic linh hoạt: Đa dụng thì dùng đâu cũng được
            if dk_hoan_canh == 'Đa dụng' or user_hc == dk_hoan_canh or (user_hc == 'Đa dụng'):
                st.success(f"✅ Đạt. (Hoàn cảnh '{user_hc}' phù hợp với yêu cầu '{dk_hoan_canh}').")
            else:
                st.warning(f"⚠️ Cảnh báo. (Bạn dự định đi '{user_hc}', nhưng sản phẩm này tối ưu nhất cho '{dk_hoan_canh}').")
                hop_le = False

        # BƯỚC 3: BACKTRACK THỜI TIẾT
        with st.expander("Giai đoạn 3: Xác minh Thời tiết", expanded=True):
            st.write(f"Đang tìm luật (Rule): Thời tiết khuyên dùng = `{dk_mua}`")
            if dk_mua == 'Mọi mùa' or user_mua == dk_mua:
                st.success(f"✅ Đạt. (Mùa '{user_mua}' hoàn hảo để hương thơm phát huy).")
            else:
                st.error(f"❌ Xung đột. (Dùng nước hoa mùa '{dk_mua}' trong thời tiết '{user_mua}' sẽ làm hỏng cấu trúc mùi).")
                hop_le = False
                
        # KẾT LUẬN CUỐI CÙNG TỪ GOAL
        st.markdown("---")
        if hop_le:
            st.balloons()
            st.success(f"🎉 **KẾT LUẬN CUỐI CÙNG (GOAL REACHED):** Giả thuyết đúng! Bạn hoàn toàn có thể tự tin sử dụng **{muc_tieu}** cho ngày hôm nay.")
        else:
            st.error(f"⛔ **KẾT LUẬN CUỐI CÙNG (GOAL FAILED):** Giả thuyết sai! Dựa trên vết suy diễn lùi, **{muc_tieu}** không phải là sự lựa chọn an toàn cho bạn lúc này.")
