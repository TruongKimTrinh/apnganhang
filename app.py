import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Tính Tiền Tiết Kiệm", page_icon="💰", layout="centered")

st.title("💰 Ứng Dụng Tính Tiền Gửi Tiết Kiệm")
st.write("Nhập thông tin bên dưới để tính toán số tiền nhận được theo lãi đơn và lãi kép.")

# Tạo khung nhập dữ liệu từ người dùng
with st.form(key="saving_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        principal = st.number_input("Số tiền gửi ban đầu (VNĐ):", min_value=0.0, value=100000000.0, step=1000000.0, format="%.0f")
        months = st.number_input("Số tháng gửi (tháng):", min_value=1, value=12, step=1)
        
    with col2:
        interest_rate = st.number_input("Lãi suất (%/năm):", min_value=0.0, value=6.5, step=0.1, format="%.2f")
        compound_period = st.selectbox(
            "Định kỳ nhập gốc (chỉ áp dụng cho Lãi kép):",
            options=["Hàng tháng", "Hàng quý (3 tháng)", "Hàng năm (12 tháng)"],
            index=0
        )
    
    submit_button = st.form_submit_button(label="Tính toán")

if submit_button:
    # 1. Tính Lãi Đơn
    # Lãi suất tháng = Lãi suất năm / 12
    # Tiền lãi đơn = Gốc * (Lãi suất năm / 12) * Số tháng
    simple_interest = principal * (interest_rate / 100 / 12) * months
    total_simple = principal + simple_interest

    # 2. Tính Lãi Kép
    # Xác định số kỳ nhập gốc trong 1 năm 👎
    if compound_period == "Hàng tháng":
        n = 12
    elif compound_period == "Hàng quý (3 tháng)":
        n = 4
    else:  # Hàng năm
        n = 1

    # Quy đổi số tháng gửi ra số năm (t)
    t = months / 12
    
    # Công thức lãi kép: A = P * (1 + r/n)^(n*t)
    total_compound = principal * ((1 + (interest_rate / 100) / n) ** (n * t))
    compound_interest = total_compound - principal

    # Hiển thị kết quả
    st.divider()
    st.subheader("📊 Kết Quả Tính Toán")

    col_res1, col_res2 = st.columns(2)

    with col_res1:
        st.markdown("### 🔹 **Lãi Đơn**")
        st.write(f"**Tiền lãi:** {simple_interest:,.0f} VNĐ")
        st.write(f"**Tổng tiền nhận được:** {total_simple:,.0f} VNĐ")

    with col_res2:
        st.markdown("### 🔸 **Lãi Kép**")
        st.write(f"**Tiền lãi:** {compound_interest:,.0f} VNĐ")
        st.write(f"**Tổng tiền nhận được:** {total_compound:,.0f} VNĐ")

    # Bảng so sánh chênh lệch
    st.divider()
    difference = total_compound - total_simple
    st.success(f"💡 Với phương thức **Lãi kép**, bạn nhận thêm **{difference:,.0f} VNĐ** so với Lãi đơn.")
