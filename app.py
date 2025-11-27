import streamlit as st
import random
import time
import os
import re
from openai import OpenAI

# Hàm loại bỏ emoji và ký tự đặc biệt có thể gây lỗi encoding
def remove_emoji(text):
    """Loại bỏ emoji và các ký tự đặc biệt không cần thiết"""
    if not text:
        return text
    # Loại bỏ emoji (Unicode ranges cho emoji)
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub('', text)

# Cấu hình trang
st.set_page_config(
    page_title="Dạy Chuyên Toán Lớp 2",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .exercise-box {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    .correct-answer {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 5px;
        color: #155724;
        margin: 1rem 0;
    }
    .wrong-answer {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 5px;
        color: #721c24;
        margin: 1rem 0;
    }
    .score-display {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Khởi tạo session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 0
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Trang Chủ"

# Sidebar navigation
st.sidebar.title("📚 Menu Học Tập")
page = st.sidebar.radio(
    "Chọn chủ đề:",
    ["Trang Chủ", "Phép Cộng", "Phép Trừ", "Phép Nhân", "So Sánh Số", "Bài Toán Có Lời Văn", "Hình Học", "Luyện Tập Tổng Hợp", "Đề Thi", "Trợ Lý AI"]
)

st.session_state.current_page = page

# Header
st.markdown('<h1 class="main-header">🔢 Dạy Chuyên Toán Lớp 2</h1>', unsafe_allow_html=True)

# Trang Chủ
if page == "Trang Chủ":
    st.markdown("""
    ## 👋 Chào mừng đến với ứng dụng học toán lớp 2!
    
    Ứng dụng này giúp các em học sinh lớp 2:
    - ✅ Luyện tập phép cộng
    - ✅ Luyện tập phép trừ
    - ✅ Luyện tập phép nhân
    - ✅ So sánh các số
    - ✅ Giải bài toán có lời văn
    - ✅ Nhận biết hình học
    - ✅ Luyện tập tổng hợp
    - ✅ Đề thi học kỳ 1 và học kỳ 2
    - ✅ Trợ Lý AI - Học tập thông minh
    
    ### 📊 Thống kê của bạn:
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Điểm số", st.session_state.score)
    with col2:
        st.metric("Số câu đã làm", st.session_state.total_questions)
    with col3:
        accuracy = (st.session_state.score / st.session_state.total_questions * 100) if st.session_state.total_questions > 0 else 0
        st.metric("Tỷ lệ đúng", f"{accuracy:.1f}%")
    
    st.markdown("---")
    st.info("💡 **Mẹo học tốt:** Hãy làm từng bài một cách cẩn thận và kiểm tra lại đáp án trước khi nộp bài nhé!")

# Phép Cộng
elif page == "Phép Cộng":
    st.header("➕ Phép Cộng")
    
    difficulty = st.selectbox("Chọn độ khó:", ["Dễ (1-20)", "Trung bình (1-50)", "Khó (1-100)"])
    
    if difficulty == "Dễ (1-20)":
        max_num = 20
    elif difficulty == "Trung bình (1-50)":
        max_num = 50
    else:
        max_num = 100
    
    if 'add_num1' not in st.session_state or st.button("🎲 Câu hỏi mới"):
        st.session_state.add_num1 = random.randint(1, max_num)
        st.session_state.add_num2 = random.randint(1, max_num)
        st.session_state.add_answer = None
        st.session_state.add_submitted = False
    
    st.markdown(f'<div class="exercise-box">', unsafe_allow_html=True)
    st.markdown(f"### Câu hỏi:")
    st.markdown(f"## {st.session_state.add_num1} + {st.session_state.add_num2} = ?")
    st.markdown(f'</div>', unsafe_allow_html=True)
    
    answer = st.number_input("Nhập đáp án của bạn:", min_value=0, step=1, key="add_input")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Kiểm tra", key="add_check"):
            st.session_state.add_submitted = True
            st.session_state.add_answer = answer
            st.session_state.total_questions += 1
            
            correct_answer = st.session_state.add_num1 + st.session_state.add_num2
            if answer == correct_answer:
                st.session_state.score += 1
                st.markdown(f'<div class="correct-answer">🎉 Chính xác! {st.session_state.add_num1} + {st.session_state.add_num2} = {correct_answer}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="wrong-answer">❌ Chưa đúng. Đáp án đúng là: {correct_answer}</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("💡 Xem đáp án", key="add_hint"):
            correct_answer = st.session_state.add_num1 + st.session_state.add_num2
            st.info(f"💡 Đáp án: {st.session_state.add_num1} + {st.session_state.add_num2} = {correct_answer}")

# Phép Trừ
elif page == "Phép Trừ":
    st.header("➖ Phép Trừ")
    
    difficulty = st.selectbox("Chọn độ khó:", ["Dễ (1-20)", "Trung bình (1-50)", "Khó (1-100)"])
    
    if difficulty == "Dễ (1-20)":
        max_num = 20
    elif difficulty == "Trung bình (1-50)":
        max_num = 50
    else:
        max_num = 100
    
    if 'sub_num1' not in st.session_state or st.button("🎲 Câu hỏi mới"):
        st.session_state.sub_num1 = random.randint(1, max_num)
        st.session_state.sub_num2 = random.randint(1, st.session_state.sub_num1)
        st.session_state.sub_answer = None
        st.session_state.sub_submitted = False
    
    st.markdown(f'<div class="exercise-box">', unsafe_allow_html=True)
    st.markdown(f"### Câu hỏi:")
    st.markdown(f"## {st.session_state.sub_num1} - {st.session_state.sub_num2} = ?")
    st.markdown(f'</div>', unsafe_allow_html=True)
    
    answer = st.number_input("Nhập đáp án của bạn:", min_value=0, step=1, key="sub_input")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Kiểm tra", key="sub_check"):
            st.session_state.sub_submitted = True
            st.session_state.sub_answer = answer
            st.session_state.total_questions += 1
            
            correct_answer = st.session_state.sub_num1 - st.session_state.sub_num2
            if answer == correct_answer:
                st.session_state.score += 1
                st.markdown(f'<div class="correct-answer">🎉 Chính xác! {st.session_state.sub_num1} - {st.session_state.sub_num2} = {correct_answer}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="wrong-answer">❌ Chưa đúng. Đáp án đúng là: {correct_answer}</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("💡 Xem đáp án", key="sub_hint"):
            correct_answer = st.session_state.sub_num1 - st.session_state.sub_num2
            st.info(f"💡 Đáp án: {st.session_state.sub_num1} - {st.session_state.sub_num2} = {correct_answer}")

# Phép Nhân
elif page == "Phép Nhân":
    st.header("✖️ Phép Nhân")
    
    st.markdown("### 📚 Chọn bảng nhân để luyện tập:")
    multiplication_table = st.selectbox(
        "Chọn bảng nhân:",
        ["Bảng nhân 2", "Bảng nhân 3", "Bảng nhân 4", "Bảng nhân 5", 
         "Bảng nhân 6", "Bảng nhân 7", "Bảng nhân 8", "Bảng nhân 9", "Tất cả (2-9)"]
    )
    
    # Xác định số nhân
    if multiplication_table == "Tất cả (2-9)":
        multiplier = random.randint(2, 9)
    else:
        multiplier = int(multiplication_table.split()[-1])
    
    if 'mul_num1' not in st.session_state or st.button("🎲 Câu hỏi mới"):
        if multiplication_table == "Tất cả (2-9)":
            st.session_state.mul_num1 = random.randint(2, 9)
        else:
            st.session_state.mul_num1 = multiplier
        st.session_state.mul_num2 = random.randint(1, 10)
        st.session_state.mul_answer = None
        st.session_state.mul_submitted = False
    
    st.markdown(f'<div class="exercise-box">', unsafe_allow_html=True)
    st.markdown(f"### Câu hỏi:")
    st.markdown(f"## {st.session_state.mul_num1} × {st.session_state.mul_num2} = ?")
    st.markdown(f'</div>', unsafe_allow_html=True)
    
    # Hiển thị bảng nhân nếu chọn một bảng cụ thể
    if multiplication_table != "Tất cả (2-9)":
        st.markdown("### 📖 Bảng nhân để tham khảo:")
        table_text = ""
        for i in range(1, 11):
            table_text += f"{multiplier} × {i} = {multiplier * i}  |  "
            if i % 5 == 0:
                table_text += "\n"
        st.markdown(f"**{table_text}**")
        st.markdown("---")
    
    answer = st.number_input("Nhập đáp án của bạn:", min_value=0, step=1, key="mul_input")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Kiểm tra", key="mul_check"):
            st.session_state.mul_submitted = True
            st.session_state.mul_answer = answer
            st.session_state.total_questions += 1
            
            correct_answer = st.session_state.mul_num1 * st.session_state.mul_num2
            if answer == correct_answer:
                st.session_state.score += 1
                st.markdown(f'<div class="correct-answer">🎉 Chính xác! {st.session_state.mul_num1} × {st.session_state.mul_num2} = {correct_answer}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="wrong-answer">❌ Chưa đúng. Đáp án đúng là: {correct_answer}</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("💡 Xem đáp án", key="mul_hint"):
            correct_answer = st.session_state.mul_num1 * st.session_state.mul_num2
            st.info(f"💡 Đáp án: {st.session_state.mul_num1} × {st.session_state.mul_num2} = {correct_answer}")
    
    st.markdown("---")
    st.markdown("### 💡 Mẹo học bảng nhân:")
    st.markdown("""
    - **Bảng nhân 2**: Nhân với 2 giống như cộng số đó với chính nó (ví dụ: 2 × 5 = 5 + 5 = 10)
    - **Bảng nhân 5**: Kết quả luôn kết thúc bằng 0 hoặc 5
    - **Bảng nhân 9**: Tổng các chữ số của kết quả luôn bằng 9 (ví dụ: 9 × 3 = 27, 2 + 7 = 9)
    - **Bảng nhân 10**: Chỉ cần thêm số 0 vào sau số nhân (ví dụ: 10 × 4 = 40)
    """)

# So Sánh Số
elif page == "So Sánh Số":
    st.header("⚖️ So Sánh Số")
    
    if 'compare_num1' not in st.session_state or st.button("🎲 Câu hỏi mới"):
        st.session_state.compare_num1 = random.randint(1, 100)
        st.session_state.compare_num2 = random.randint(1, 100)
        st.session_state.compare_answer = None
        st.session_state.compare_submitted = False
    
    st.markdown(f'<div class="exercise-box">', unsafe_allow_html=True)
    st.markdown(f"### Câu hỏi:")
    st.markdown(f"## So sánh: {st.session_state.compare_num1} và {st.session_state.compare_num2}")
    st.markdown(f'</div>', unsafe_allow_html=True)
    
    answer = st.radio(
        "Chọn đáp án:",
        ["Lớn hơn (>)", "Bằng nhau (=)", "Nhỏ hơn (<)"],
        key="compare_radio"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Kiểm tra", key="compare_check"):
            st.session_state.compare_submitted = True
            st.session_state.total_questions += 1
            
            num1 = st.session_state.compare_num1
            num2 = st.session_state.compare_num2
            
            if num1 > num2:
                correct = "Lớn hơn (>)"
            elif num1 < num2:
                correct = "Nhỏ hơn (<)"
            else:
                correct = "Bằng nhau (=)"
            
            if answer == correct:
                st.session_state.score += 1
                st.markdown(f'<div class="correct-answer">🎉 Chính xác! {num1} {">" if num1 > num2 else "<" if num1 < num2 else "="} {num2}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="wrong-answer">❌ Chưa đúng. Đáp án đúng là: {correct}</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("💡 Xem đáp án", key="compare_hint"):
            num1 = st.session_state.compare_num1
            num2 = st.session_state.compare_num2
            if num1 > num2:
                st.info(f"💡 Đáp án: {num1} > {num2}")
            elif num1 < num2:
                st.info(f"💡 Đáp án: {num1} < {num2}")
            else:
                st.info(f"💡 Đáp án: {num1} = {num2}")

# Bài Toán Có Lời Văn
elif page == "Bài Toán Có Lời Văn":
    st.header("📝 Bài Toán Có Lời Văn")
    
    word_problems = [
        {
            "question": "Lan có 15 cái kẹo. Mẹ cho Lan thêm 8 cái kẹo nữa. Hỏi Lan có tất cả bao nhiêu cái kẹo?",
            "answer": 23,
            "operation": "cộng"
        },
        {
            "question": "Một cửa hàng có 30 quyển vở. Họ đã bán 12 quyển vở. Hỏi cửa hàng còn lại bao nhiêu quyển vở?",
            "answer": 18,
            "operation": "trừ"
        },
        {
            "question": "Hùng có 20 viên bi. Nam có 15 viên bi. Hỏi cả hai bạn có tất cả bao nhiêu viên bi?",
            "answer": 35,
            "operation": "cộng"
        },
        {
            "question": "Một lớp học có 35 học sinh. Trong đó có 18 học sinh nam. Hỏi lớp học có bao nhiêu học sinh nữ?",
            "answer": 17,
            "operation": "trừ"
        },
        {
            "question": "Bà ngoại có 25 quả cam. Bà cho cháu 9 quả cam. Hỏi bà còn lại bao nhiêu quả cam?",
            "answer": 16,
            "operation": "trừ"
        }
    ]
    
    if 'current_problem' not in st.session_state or st.button("🎲 Bài toán mới"):
        st.session_state.current_problem = random.choice(word_problems)
        st.session_state.word_answer = None
        st.session_state.word_submitted = False
    
    problem = st.session_state.current_problem
    
    st.markdown(f'<div class="exercise-box">', unsafe_allow_html=True)
    st.markdown(f"### Bài toán:")
    st.markdown(f"**{problem['question']}**")
    st.markdown(f'</div>', unsafe_allow_html=True)
    
    answer = st.number_input("Nhập đáp án của bạn:", min_value=0, step=1, key="word_input")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Kiểm tra", key="word_check"):
            st.session_state.word_submitted = True
            st.session_state.word_answer = answer
            st.session_state.total_questions += 1
            
            if answer == problem['answer']:
                st.session_state.score += 1
                st.markdown(f'<div class="correct-answer">🎉 Chính xác! Đáp án là: {problem["answer"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="wrong-answer">❌ Chưa đúng. Đáp án đúng là: {problem["answer"]}</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("💡 Xem đáp án", key="word_hint"):
            st.info(f"💡 Đáp án: {problem['answer']}")

# Hình Học
elif page == "Hình Học":
    st.header("🔷 Hình Học")
    
    shapes = {
        "Hình vuông": {
            "description": "Có 4 cạnh bằng nhau, 4 góc vuông",
            "sides": 4,
            "image": "⬜"
        },
        "Hình chữ nhật": {
            "description": "Có 4 cạnh, 2 cạnh dài bằng nhau, 2 cạnh ngắn bằng nhau, 4 góc vuông",
            "sides": 4,
            "image": "▭"
        },
        "Hình tam giác": {
            "description": "Có 3 cạnh, 3 góc",
            "sides": 3,
            "image": "△"
        },
        "Hình tròn": {
            "description": "Không có cạnh, là một đường cong khép kín",
            "sides": 0,
            "image": "○"
        }
    }
    
    if 'current_shape' not in st.session_state or st.button("🎲 Câu hỏi mới"):
        st.session_state.current_shape = random.choice(list(shapes.keys()))
        st.session_state.shape_answer = None
        st.session_state.shape_submitted = False
    
    shape_name = st.session_state.current_shape
    shape_info = shapes[shape_name]
    
    st.markdown(f'<div class="exercise-box">', unsafe_allow_html=True)
    st.markdown(f"### Câu hỏi:")
    st.markdown(f"## {shape_info['image']} Hình này có bao nhiêu cạnh?")
    st.markdown(f"**Mô tả:** {shape_info['description']}")
    st.markdown(f'</div>', unsafe_allow_html=True)
    
    answer = st.number_input("Nhập số cạnh:", min_value=0, step=1, key="shape_input")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Kiểm tra", key="shape_check"):
            st.session_state.shape_submitted = True
            st.session_state.shape_answer = answer
            st.session_state.total_questions += 1
            
            if answer == shape_info['sides']:
                st.session_state.score += 1
                st.markdown(f'<div class="correct-answer">🎉 Chính xác! {shape_name} có {shape_info["sides"]} cạnh</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="wrong-answer">❌ Chưa đúng. {shape_name} có {shape_info["sides"]} cạnh</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("💡 Xem đáp án", key="shape_hint"):
            st.info(f"💡 Đáp án: {shape_name} có {shape_info['sides']} cạnh")
    
    st.markdown("---")
    st.subheader("📚 Kiến thức về hình học:")
    for name, info in shapes.items():
        st.markdown(f"- **{name}** {info['image']}: {info['description']}")

# Luyện Tập Tổng Hợp
elif page == "Luyện Tập Tổng Hợp":
    st.header("🎯 Luyện Tập Tổng Hợp")
    
    if 'quiz_questions' not in st.session_state:
        st.session_state.quiz_questions = []
        st.session_state.quiz_answers = []
        st.session_state.quiz_current = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_started = False
        st.session_state.quiz_finished = False
    
    if not st.session_state.quiz_started:
        num_questions = st.slider("Chọn số câu hỏi:", 5, 20, 10)
        
        if st.button("🚀 Bắt đầu luyện tập"):
            st.session_state.quiz_questions = []
            st.session_state.quiz_answers = []
            st.session_state.quiz_current = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_started = True
            st.session_state.quiz_finished = False
            
            # Tạo câu hỏi
            for i in range(num_questions):
                q_type = random.choice(["cộng", "trừ", "nhân", "so sánh"])
                
                if q_type == "cộng":
                    num1 = random.randint(1, 50)
                    num2 = random.randint(1, 50)
                    answer = num1 + num2
                    question = f"{num1} + {num2} = ?"
                elif q_type == "trừ":
                    num1 = random.randint(1, 50)
                    num2 = random.randint(1, num1)
                    answer = num1 - num2
                    question = f"{num1} - {num2} = ?"
                elif q_type == "nhân":
                    num1 = random.randint(2, 9)
                    num2 = random.randint(1, 10)
                    answer = num1 * num2
                    question = f"{num1} × {num2} = ?"
                else:  # so sánh
                    num1 = random.randint(1, 100)
                    num2 = random.randint(1, 100)
                    if num1 > num2:
                        answer = ">"
                    elif num1 < num2:
                        answer = "<"
                    else:
                        answer = "="
                    question = f"So sánh: {num1} ? {num2}"
                
                st.session_state.quiz_questions.append({
                    "question": question,
                    "answer": answer,
                    "type": q_type
                })
                st.session_state.quiz_answers.append(None)
            
            st.rerun()
    
    if st.session_state.quiz_started and not st.session_state.quiz_finished:
        current_q = st.session_state.quiz_questions[st.session_state.quiz_current]
        progress = (st.session_state.quiz_current + 1) / len(st.session_state.quiz_questions)
        
        st.progress(progress)
        st.caption(f"Câu {st.session_state.quiz_current + 1}/{len(st.session_state.quiz_questions)}")
        
        st.markdown(f'<div class="exercise-box">', unsafe_allow_html=True)
        st.markdown(f"### {current_q['question']}")
        st.markdown(f'</div>', unsafe_allow_html=True)
        
        if current_q['type'] == "so sánh":
            user_answer = st.radio(
                "Chọn đáp án:",
                [">", "=", "<"],
                key=f"quiz_radio_{st.session_state.quiz_current}"
            )
        else:
            user_answer = st.number_input("Nhập đáp án:", min_value=0, step=1, key=f"quiz_input_{st.session_state.quiz_current}")
        
        if st.button("➡️ Câu tiếp theo"):
            st.session_state.quiz_answers[st.session_state.quiz_current] = user_answer
            
            if user_answer == current_q['answer']:
                st.session_state.quiz_score += 1
            
            st.session_state.quiz_current += 1
            
            if st.session_state.quiz_current >= len(st.session_state.quiz_questions):
                st.session_state.quiz_finished = True
                st.session_state.total_questions += len(st.session_state.quiz_questions)
                st.session_state.score += st.session_state.quiz_score
            else:
                st.rerun()
    
    if st.session_state.quiz_finished:
        st.balloons()
        st.markdown(f'<div class="score-display">', unsafe_allow_html=True)
        st.markdown(f"## 🎉 Hoàn thành!")
        st.markdown(f"### Điểm số: {st.session_state.quiz_score}/{len(st.session_state.quiz_questions)}")
        accuracy = (st.session_state.quiz_score / len(st.session_state.quiz_questions)) * 100
        st.markdown(f"### Tỷ lệ đúng: {accuracy:.1f}%")
        st.markdown(f'</div>', unsafe_allow_html=True)
        
        # Hiển thị đáp án
        st.subheader("📋 Đáp án:")
        for i, q in enumerate(st.session_state.quiz_questions):
            user_ans = st.session_state.quiz_answers[i]
            is_correct = "✅" if user_ans == q['answer'] else "❌"
            st.markdown(f"{is_correct} Câu {i+1}: {q['question']} → Đáp án của bạn: {user_ans}, Đáp án đúng: {q['answer']}")
        
        if st.button("🔄 Làm lại"):
            st.session_state.quiz_started = False
            st.session_state.quiz_finished = False
            st.rerun()

# Đề Thi
elif page == "Đề Thi":
    st.header("📝 Đề Thi Toán Lớp 2")
    
    exam_type = st.radio(
        "Chọn đề thi:",
        ["Học Kỳ 1", "Học Kỳ 2"],
        horizontal=True
    )
    
    difficulty_level = st.selectbox(
        "Chọn mức độ:",
        ["Cơ bản", "Khó", "Cực khó"],
        key="exam_difficulty"
    )
    
    # Đề thi Học Kỳ 1
    if exam_type == "Học Kỳ 1":
        st.subheader(f"📚 Đề Thi Học Kỳ 1 - Toán Lớp 2 ({difficulty_level})")
        
        if 'hk1_exam_started' not in st.session_state:
            st.session_state.hk1_exam_started = False
            st.session_state.hk1_exam_finished = False
            st.session_state.hk1_answers = {}
            st.session_state.hk1_score = 0
            st.session_state.hk1_difficulty = None
        
        # Định nghĩa đề thi Học Kỳ 1 - Cơ bản
        hk1_exam_basic = [
            {
                "question": "Câu 1: Tính: 25 + 17 = ?",
                "answer": 42,
                "type": "number"
            },
            {
                "question": "Câu 2: Tính: 48 - 23 = ?",
                "answer": 25,
                "type": "number"
            },
            {
                "question": "Câu 3: So sánh: 35 và 28",
                "answer": ">",
                "type": "compare",
                "options": [">", "=", "<"]
            },
            {
                "question": "Câu 4: Tính: 16 + 24 = ?",
                "answer": 40,
                "type": "number"
            },
            {
                "question": "Câu 5: Tính: 50 - 18 = ?",
                "answer": 32,
                "type": "number"
            },
            {
                "question": "Câu 6: Lan có 32 cái kẹo. Mẹ cho Lan thêm 15 cái kẹo nữa. Hỏi Lan có tất cả bao nhiêu cái kẹo?",
                "answer": 47,
                "type": "number"
            },
            {
                "question": "Câu 7: So sánh: 42 và 42",
                "answer": "=",
                "type": "compare",
                "options": [">", "=", "<"]
            },
            {
                "question": "Câu 8: Tính: 19 + 26 = ?",
                "answer": 45,
                "type": "number"
            },
            {
                "question": "Câu 9: Một cửa hàng có 45 quyển vở. Họ đã bán 18 quyển vở. Hỏi cửa hàng còn lại bao nhiêu quyển vở?",
                "answer": 27,
                "type": "number"
            },
            {
                "question": "Câu 10: Tính: 37 - 14 = ?",
                "answer": 23,
                "type": "number"
            }
        ]
        
        # Định nghĩa đề thi Học Kỳ 1 - Khó
        hk1_exam_hard = [
            {
                "question": "Câu 1: Tính: 47 + 38 = ?",
                "answer": 85,
                "type": "number"
            },
            {
                "question": "Câu 2: Tính: 92 - 45 = ?",
                "answer": 47,
                "type": "number"
            },
            {
                "question": "Câu 3: So sánh: 35 + 28 và 28 + 35",
                "answer": "=",
                "type": "compare",
                "options": [">", "=", "<"]
            },
            {
                "question": "Câu 4: Tính: 56 + 27 = ?",
                "answer": 83,
                "type": "number"
            },
            {
                "question": "Câu 5: Tính: 81 - 39 = ?",
                "answer": 42,
                "type": "number"
            },
            {
                "question": "Câu 6: Hùng có 58 viên bi. Hùng cho Nam 24 viên bi. Hỏi Hùng còn lại bao nhiêu viên bi?",
                "answer": 34,
                "type": "number"
            },
            {
                "question": "Câu 7: So sánh: 45 + 15 và 30 + 30",
                "answer": "=",
                "type": "compare",
                "options": [">", "=", "<"]
            },
            {
                "question": "Câu 8: Tính: 39 + 46 = ?",
                "answer": 85,
                "type": "number"
            },
            {
                "question": "Câu 9: Một cửa hàng có 67 quyển vở. Họ bán được 28 quyển vở vào buổi sáng và 19 quyển vở vào buổi chiều. Hỏi cửa hàng còn lại bao nhiêu quyển vở?",
                "answer": 20,
                "type": "number"
            },
            {
                "question": "Câu 10: Tính: 74 - 28 = ?",
                "answer": 46,
                "type": "number"
            },
            {
                "question": "Câu 11: So sánh: 50 - 15 và 20 + 15",
                "answer": "=",
                "type": "compare",
                "options": [">", "=", "<"]
            },
            {
                "question": "Câu 12: Tính: 28 + 37 + 15 = ?",
                "answer": 80,
                "type": "number"
            }
        ]
        
        # Định nghĩa đề thi Học Kỳ 1 - Cực khó
        hk1_exam_very_hard = [
            {
                "question": "Câu 1: Tính: 67 + 48 = ?",
                "answer": 115,
                "type": "number"
            },
            {
                "question": "Câu 2: Tính: 95 - 57 = ?",
                "answer": 38,
                "type": "number"
            },
            {
                "question": "Câu 3: So sánh: 45 + 38 và 50 + 33",
                "answer": "=",
                "type": "compare",
                "options": [">", "=", "<"]
            },
            {
                "question": "Câu 4: Tính: 56 + 39 + 15 = ?",
                "answer": 110,
                "type": "number"
            },
            {
                "question": "Câu 5: Tính: 100 - 28 - 35 = ?",
                "answer": 37,
                "type": "number"
            },
            {
                "question": "Câu 6: Lan có 75 cái kẹo. Lan cho em 28 cái kẹo và cho bạn 19 cái kẹo. Hỏi Lan còn lại bao nhiêu cái kẹo?",
                "answer": 28,
                "type": "number"
            },
            {
                "question": "Câu 7: So sánh: 60 - 25 và 20 + 15",
                "answer": "=",
                "type": "compare",
                "options": [">", "=", "<"]
            },
            {
                "question": "Câu 8: Tính: 48 + 37 + 26 = ?",
                "answer": 111,
                "type": "number"
            },
            {
                "question": "Câu 9: Một cửa hàng có 85 quyển sách. Ngày thứ nhất bán 27 quyển, ngày thứ hai bán 35 quyển. Hỏi cửa hàng còn lại bao nhiêu quyển sách?",
                "answer": 23,
                "type": "number"
            },
            {
                "question": "Câu 10: Tính: 92 - 48 = ?",
                "answer": 44,
                "type": "number"
            },
            {
                "question": "Câu 11: Hùng có 68 viên bi. Nam có ít hơn Hùng 29 viên bi. Hỏi cả hai bạn có tất cả bao nhiêu viên bi?",
                "answer": 107,
                "type": "number"
            },
            {
                "question": "Câu 12: Tính: 35 + 28 + 19 + 18 = ?",
                "answer": 100,
                "type": "number"
            },
            {
                "question": "Câu 13: So sánh: 45 + 35 và 50 + 30",
                "answer": "=",
                "type": "compare",
                "options": [">", "=", "<"]
            },
            {
                "question": "Câu 14: Tính: 100 - 25 - 30 - 15 = ?",
                "answer": 30,
                "type": "number"
            },
            {
                "question": "Câu 15: Một lớp học có 3 tổ. Tổ 1 có 28 học sinh, tổ 2 có 32 học sinh, tổ 3 có 25 học sinh. Hỏi lớp học có tất cả bao nhiêu học sinh?",
                "answer": 85,
                "type": "number"
            }
        ]
        
        # Chọn đề thi theo mức độ
        if difficulty_level == "Cơ bản":
            hk1_exam = hk1_exam_basic
        elif difficulty_level == "Khó":
            hk1_exam = hk1_exam_hard
        else:  # Cực khó
            hk1_exam = hk1_exam_very_hard
        
        # Reset nếu thay đổi mức độ
        if st.session_state.hk1_difficulty != difficulty_level:
            st.session_state.hk1_exam_started = False
            st.session_state.hk1_exam_finished = False
            st.session_state.hk1_answers = {}
            st.session_state.hk1_difficulty = difficulty_level
        
        if not st.session_state.hk1_exam_started:
            num_questions = len(hk1_exam)
            st.info(f"📋 Đề thi gồm {num_questions} câu hỏi. Hãy đọc kỹ và làm bài cẩn thận!")
            if st.button("🚀 Bắt đầu làm bài"):
                st.session_state.hk1_exam_started = True
                st.session_state.hk1_answers = {i: None for i in range(len(hk1_exam))}
                st.session_state.hk1_score = 0
                st.session_state.hk1_exam_finished = False
                st.rerun()
        
        elif not st.session_state.hk1_exam_finished:
            st.markdown("### Làm bài thi:")
            st.markdown("---")
            
            for i, q in enumerate(hk1_exam):
                st.markdown(f'<div class="exercise-box">', unsafe_allow_html=True)
                st.markdown(f"**{q['question']}**")
                st.markdown(f'</div>', unsafe_allow_html=True)
                
                if q['type'] == "compare":
                    user_ans = st.radio(
                        "Chọn đáp án:",
                        q['options'],
                        key=f"hk1_q{i}",
                        index=q['options'].index(st.session_state.hk1_answers[i]) if st.session_state.hk1_answers[i] in q['options'] else 0
                    )
                else:
                    user_ans = st.number_input(
                        "Nhập đáp án:",
                        min_value=0,
                        step=1,
                        key=f"hk1_q{i}",
                        value=st.session_state.hk1_answers[i] if st.session_state.hk1_answers[i] is not None else 0
                    )
                
                st.session_state.hk1_answers[i] = user_ans
                st.markdown("---")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Nộp bài", type="primary"):
                    st.session_state.hk1_exam_finished = True
                    st.session_state.hk1_score = 0
                    
                    for i, q in enumerate(hk1_exam):
                        if st.session_state.hk1_answers[i] == q['answer']:
                            st.session_state.hk1_score += 1
                    
                    st.session_state.total_questions += len(hk1_exam)
                    st.session_state.score += st.session_state.hk1_score
                    st.rerun()
            
            with col2:
                if st.button("💾 Lưu tạm"):
                    st.success("Đã lưu đáp án tạm thời!")
        
        else:  # Exam finished
            st.balloons()
            st.markdown(f'<div class="score-display">', unsafe_allow_html=True)
            st.markdown(f"## 🎉 Hoàn thành đề thi!")
            st.markdown(f"### Điểm số: {st.session_state.hk1_score}/{len(hk1_exam)}")
            accuracy = (st.session_state.hk1_score / len(hk1_exam)) * 100
            st.markdown(f"### Tỷ lệ đúng: {accuracy:.1f}%")
            
            if accuracy >= 80:
                st.markdown(f"### 🏆 Xếp loại: Giỏi")
            elif accuracy >= 65:
                st.markdown(f"### 🎯 Xếp loại: Khá")
            elif accuracy >= 50:
                st.markdown(f"### 📚 Xếp loại: Trung bình")
            else:
                st.markdown(f"### 💪 Xếp loại: Cần cố gắng thêm")
            
            st.markdown(f'</div>', unsafe_allow_html=True)
            
            st.subheader("📋 Đáp án chi tiết:")
            for i, q in enumerate(hk1_exam):
                user_ans = st.session_state.hk1_answers[i]
                is_correct = "✅" if user_ans == q['answer'] else "❌"
                st.markdown(f"{is_correct} **{q['question']}**")
                st.markdown(f"   → Đáp án của bạn: **{user_ans}** | Đáp án đúng: **{q['answer']}**")
                st.markdown("")
            
            if st.button("🔄 Làm lại đề thi"):
                st.session_state.hk1_exam_started = False
                st.session_state.hk1_exam_finished = False
                st.session_state.hk1_answers = {}
                st.rerun()
    
    # Đề thi Học Kỳ 2
    else:
        st.subheader(f"📚 Đề Thi Học Kỳ 2 - Toán Lớp 2 ({difficulty_level})")
        
        if 'hk2_exam_started' not in st.session_state:
            st.session_state.hk2_exam_started = False
            st.session_state.hk2_exam_finished = False
            st.session_state.hk2_answers = {}
            st.session_state.hk2_score = 0
            st.session_state.hk2_difficulty = None
        
        # Định nghĩa đề thi Học Kỳ 2 - Cơ bản
        hk2_exam_basic = [
            {
                "question": "Câu 1: Tính: 35 + 28 = ?",
                "answer": 63,
                "type": "number"
            },
            {
                "question": "Câu 2: Tính: 2 × 5 = ?",
                "answer": 10,
                "type": "number"
            },
            {
                "question": "Câu 3: Tính: 3 × 4 = ?",
                "answer": 12,
                "type": "number"
            },
            {
                "question": "Câu 4: Tính: 67 - 29 = ?",
                "answer": 38,
                "type": "number"
            },
            {
                "question": "Câu 5: So sánh: 45 + 15 và 50 + 10",
                "answer": "=",
                "type": "compare",
                "options": [">", "=", "<"]
            },
            {
                "question": "Câu 6: Tính: 4 × 6 = ?",
                "answer": 24,
                "type": "number"
            },
            {
                "question": "Câu 7: Một lớp học có 3 tổ, mỗi tổ có 8 học sinh. Hỏi lớp học có tất cả bao nhiêu học sinh?",
                "answer": 24,
                "type": "number"
            },
            {
                "question": "Câu 8: Tính: 52 + 38 = ?",
                "answer": 90,
                "type": "number"
            },
            {
                "question": "Câu 9: Tính: 5 × 7 = ?",
                "answer": 35,
                "type": "number"
            },
            {
                "question": "Câu 10: Hùng có 45 viên bi. Nam có ít hơn Hùng 18 viên bi. Hỏi Nam có bao nhiêu viên bi?",
                "answer": 27,
                "type": "number"
            },
            {
                "question": "Câu 11: Tính: 81 - 34 = ?",
                "answer": 47,
                "type": "number"
            },
            {
                "question": "Câu 12: Một cửa hàng có 60 quyển sách. Ngày thứ nhất bán 25 quyển, ngày thứ hai bán 18 quyển. Hỏi cửa hàng còn lại bao nhiêu quyển sách?",
                "answer": 17,
                "type": "number"
            }
        ]
        
        # Định nghĩa đề thi Học Kỳ 2 - Khó
        hk2_exam_hard = [
            {
                "question": "Câu 1: Tính: 48 + 39 = ?",
                "answer": 87,
                "type": "number"
            },
            {
                "question": "Câu 2: Tính: 4 × 7 = ?",
                "answer": 28,
                "type": "number"
            },
            {
                "question": "Câu 3: Tính: 5 × 8 = ?",
                "answer": 40,
                "type": "number"
            },
            {
                "question": "Câu 4: Tính: 85 - 47 = ?",
                "answer": 38,
                "type": "number"
            },
            {
                "question": "Câu 5: So sánh: 3 × 6 và 2 × 9",
                "answer": "=",
                "type": "compare",
                "options": [">", "=", "<"]
            },
            {
                "question": "Câu 6: Tính: 6 × 5 = ?",
                "answer": 30,
                "type": "number"
            },
            {
                "question": "Câu 7: Một lớp học có 4 tổ, mỗi tổ có 7 học sinh. Hỏi lớp học có tất cả bao nhiêu học sinh?",
                "answer": 28,
                "type": "number"
            },
            {
                "question": "Câu 8: Tính: 56 + 38 = ?",
                "answer": 94,
                "type": "number"
            },
            {
                "question": "Câu 9: Tính: 7 × 4 = ?",
                "answer": 28,
                "type": "number"
            },
            {
                "question": "Câu 10: Hùng có 52 viên bi. Nam có ít hơn Hùng 25 viên bi. Hỏi Nam có bao nhiêu viên bi?",
                "answer": 27,
                "type": "number"
            },
            {
                "question": "Câu 11: Tính: 92 - 45 = ?",
                "answer": 47,
                "type": "number"
            },
            {
                "question": "Câu 12: Một cửa hàng có 75 quyển sách. Ngày thứ nhất bán 28 quyển, ngày thứ hai bán 32 quyển. Hỏi cửa hàng còn lại bao nhiêu quyển sách?",
                "answer": 15,
                "type": "number"
            },
            {
                "question": "Câu 13: Tính: 3 × 8 + 15 = ?",
                "answer": 39,
                "type": "number"
            },
            {
                "question": "Câu 14: Tính: 5 × 6 - 12 = ?",
                "answer": 18,
                "type": "number"
            }
        ]
        
        # Định nghĩa đề thi Học Kỳ 2 - Cực khó
        hk2_exam_very_hard = [
            {
                "question": "Câu 1: Tính: 67 + 48 = ?",
                "answer": 115,
                "type": "number"
            },
            {
                "question": "Câu 2: Tính: 6 × 8 = ?",
                "answer": 48,
                "type": "number"
            },
            {
                "question": "Câu 3: Tính: 7 × 7 = ?",
                "answer": 49,
                "type": "number"
            },
            {
                "question": "Câu 4: Tính: 95 - 58 = ?",
                "answer": 37,
                "type": "number"
            },
            {
                "question": "Câu 5: So sánh: 4 × 9 và 6 × 6",
                "answer": "=",
                "type": "compare",
                "options": [">", "=", "<"]
            },
            {
                "question": "Câu 6: Tính: 8 × 5 = ?",
                "answer": 40,
                "type": "number"
            },
            {
                "question": "Câu 7: Một lớp học có 5 tổ, mỗi tổ có 8 học sinh. Hỏi lớp học có tất cả bao nhiêu học sinh?",
                "answer": 40,
                "type": "number"
            },
            {
                "question": "Câu 8: Tính: 58 + 47 = ?",
                "answer": 105,
                "type": "number"
            },
            {
                "question": "Câu 9: Tính: 9 × 4 = ?",
                "answer": 36,
                "type": "number"
            },
            {
                "question": "Câu 10: Hùng có 68 viên bi. Nam có ít hơn Hùng 29 viên bi. Hỏi cả hai bạn có tất cả bao nhiêu viên bi?",
                "answer": 107,
                "type": "number"
            },
            {
                "question": "Câu 11: Tính: 100 - 38 = ?",
                "answer": 62,
                "type": "number"
            },
            {
                "question": "Câu 12: Một cửa hàng có 90 quyển sách. Ngày thứ nhất bán 35 quyển, ngày thứ hai bán 28 quyển. Hỏi cửa hàng còn lại bao nhiêu quyển sách?",
                "answer": 27,
                "type": "number"
            },
            {
                "question": "Câu 13: Tính: 4 × 8 + 25 = ?",
                "answer": 57,
                "type": "number"
            },
            {
                "question": "Câu 14: Tính: 6 × 7 - 18 = ?",
                "answer": 24,
                "type": "number"
            },
            {
                "question": "Câu 15: Một lớp học có 3 tổ. Tổ 1 có 9 học sinh, tổ 2 có 8 học sinh, tổ 3 có 7 học sinh. Hỏi lớp học có tất cả bao nhiêu học sinh?",
                "answer": 24,
                "type": "number"
            },
            {
                "question": "Câu 16: Tính: 5 × 9 + 3 × 5 = ?",
                "answer": 60,
                "type": "number"
            },
            {
                "question": "Câu 17: So sánh: 7 × 6 và 6 × 7",
                "answer": "=",
                "type": "compare",
                "options": [">", "=", "<"]
            },
            {
                "question": "Câu 18: Tính: 100 - 25 - 35 = ?",
                "answer": 40,
                "type": "number"
            }
        ]
        
        # Chọn đề thi theo mức độ
        if difficulty_level == "Cơ bản":
            hk2_exam = hk2_exam_basic
        elif difficulty_level == "Khó":
            hk2_exam = hk2_exam_hard
        else:  # Cực khó
            hk2_exam = hk2_exam_very_hard
        
        # Reset nếu thay đổi mức độ
        if st.session_state.hk2_difficulty != difficulty_level:
            st.session_state.hk2_exam_started = False
            st.session_state.hk2_exam_finished = False
            st.session_state.hk2_answers = {}
            st.session_state.hk2_difficulty = difficulty_level
        
        if not st.session_state.hk2_exam_started:
            num_questions = len(hk2_exam)
            st.info(f"📋 Đề thi gồm {num_questions} câu hỏi. Hãy đọc kỹ và làm bài cẩn thận!")
            if st.button("🚀 Bắt đầu làm bài"):
                st.session_state.hk2_exam_started = True
                st.session_state.hk2_answers = {i: None for i in range(len(hk2_exam))}
                st.session_state.hk2_score = 0
                st.session_state.hk2_exam_finished = False
                st.rerun()
        
        elif not st.session_state.hk2_exam_finished:
            st.markdown("### Làm bài thi:")
            st.markdown("---")
            
            for i, q in enumerate(hk2_exam):
                st.markdown(f'<div class="exercise-box">', unsafe_allow_html=True)
                st.markdown(f"**{q['question']}**")
                st.markdown(f'</div>', unsafe_allow_html=True)
                
                if q['type'] == "compare":
                    user_ans = st.radio(
                        "Chọn đáp án:",
                        q['options'],
                        key=f"hk2_q{i}",
                        index=q['options'].index(st.session_state.hk2_answers[i]) if st.session_state.hk2_answers[i] in q['options'] else 0
                    )
                else:
                    user_ans = st.number_input(
                        "Nhập đáp án:",
                        min_value=0,
                        step=1,
                        key=f"hk2_q{i}",
                        value=st.session_state.hk2_answers[i] if st.session_state.hk2_answers[i] is not None else 0
                    )
                
                st.session_state.hk2_answers[i] = user_ans
                st.markdown("---")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Nộp bài", type="primary"):
                    st.session_state.hk2_exam_finished = True
                    st.session_state.hk2_score = 0
                    
                    for i, q in enumerate(hk2_exam):
                        if st.session_state.hk2_answers[i] == q['answer']:
                            st.session_state.hk2_score += 1
                    
                    st.session_state.total_questions += len(hk2_exam)
                    st.session_state.score += st.session_state.hk2_score
                    st.rerun()
            
            with col2:
                if st.button("💾 Lưu tạm"):
                    st.success("Đã lưu đáp án tạm thời!")
        
        else:  # Exam finished
            st.balloons()
            st.markdown(f'<div class="score-display">', unsafe_allow_html=True)
            st.markdown(f"## 🎉 Hoàn thành đề thi!")
            st.markdown(f"### Điểm số: {st.session_state.hk2_score}/{len(hk2_exam)}")
            accuracy = (st.session_state.hk2_score / len(hk2_exam)) * 100
            st.markdown(f"### Tỷ lệ đúng: {accuracy:.1f}%")
            
            if accuracy >= 80:
                st.markdown(f"### 🏆 Xếp loại: Giỏi")
            elif accuracy >= 65:
                st.markdown(f"### 🎯 Xếp loại: Khá")
            elif accuracy >= 50:
                st.markdown(f"### 📚 Xếp loại: Trung bình")
            else:
                st.markdown(f"### 💪 Xếp loại: Cần cố gắng thêm")
            
            st.markdown(f'</div>', unsafe_allow_html=True)
            
            st.subheader("📋 Đáp án chi tiết:")
            for i, q in enumerate(hk2_exam):
                user_ans = st.session_state.hk2_answers[i]
                is_correct = "✅" if user_ans == q['answer'] else "❌"
                st.markdown(f"{is_correct} **{q['question']}**")
                st.markdown(f"   → Đáp án của bạn: **{user_ans}** | Đáp án đúng: **{q['answer']}**")
                st.markdown("")
            
            if st.button("🔄 Làm lại đề thi"):
                st.session_state.hk2_exam_started = False
                st.session_state.hk2_exam_finished = False
                st.session_state.hk2_answers = {}
                st.rerun()

# Trợ Lý AI
elif page == "Trợ Lý AI":
    st.header("🤖 Trợ Lý AI - Học Tập Thông Minh")
    
    # Khởi tạo session state cho AI
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = ""
    if 'ai_messages' not in st.session_state:
        st.session_state.ai_messages = []
    
    # Cấu hình API Key
    st.sidebar.markdown("### 🔑 Cấu hình OpenAI")
    api_key_input = st.sidebar.text_input(
        "Nhập OpenAI API Key:",
        type="password",
        value=st.session_state.openai_api_key,
        help="Bạn có thể lấy API key tại https://platform.openai.com/api-keys"
    )
    
    if api_key_input:
        st.session_state.openai_api_key = api_key_input
        st.sidebar.success("✅ API Key đã được lưu!")
    else:
        st.sidebar.warning("⚠️ Vui lòng nhập API Key để sử dụng tính năng AI")
    
    # Chọn chức năng AI
    ai_function = st.radio(
        "Chọn chức năng:",
        ["💬 Hỏi đáp với AI", "📝 Giải thích bài toán", "🎲 Tạo bài tập mới", "💡 Lời khuyên học tập"],
        horizontal=False
    )
    
    st.markdown("---")
    
    # Hỏi đáp với AI
    if ai_function == "💬 Hỏi đáp với AI":
        st.subheader("💬 Hỏi đáp với AI")
        st.info("💡 Bạn có thể hỏi AI bất kỳ câu hỏi nào về toán lớp 2, ví dụ: 'Làm thế nào để học bảng nhân 5?', 'Giải thích phép trừ có nhớ'...")
        
        if st.session_state.openai_api_key:
            user_question = st.text_area(
                "Nhập câu hỏi của bạn:",
                height=100,
                placeholder="Ví dụ: Làm thế nào để học bảng nhân 5 dễ nhớ?"
            )
            
            if st.button("🚀 Gửi câu hỏi", type="primary"):
                if user_question:
                    with st.spinner("🤔 AI đang suy nghĩ..."):
                        try:
                            client = OpenAI(api_key=st.session_state.openai_api_key)
                            
                            # Đảm bảo encoding đúng UTF-8 và loại bỏ emoji có thể gây lỗi
                            system_content = "Bạn là một giáo viên toán chuyên nghiệp, thân thiện và nhiệt tình dạy toán lớp 2. Hãy giải thích một cách đơn giản, dễ hiểu, phù hợp với học sinh lớp 2. Sử dụng ví dụ cụ thể và ngôn ngữ tiếng Việt."
                            # Loại bỏ emoji nhưng giữ lại tiếng Việt
                            user_content = remove_emoji(user_question) if user_question else ""
                            
                            response = client.chat.completions.create(
                                model="gpt-3.5-turbo",
                                messages=[
                                    {
                                        "role": "system",
                                        "content": system_content
                                    },
                                    {
                                        "role": "user",
                                        "content": user_content
                                    }
                                ],
                                temperature=0.7,
                                max_tokens=500
                            )
                            
                            ai_response = response.choices[0].message.content
                            
                            st.markdown(f'<div class="exercise-box">', unsafe_allow_html=True)
                            st.markdown(f"### ❓ Câu hỏi của bạn:")
                            st.markdown(f"**{user_question}**")
                            st.markdown(f'</div>', unsafe_allow_html=True)
                            
                            st.markdown(f'<div class="correct-answer">', unsafe_allow_html=True)
                            st.markdown(f"### 🤖 Trả lời từ AI:")
                            st.markdown(ai_response)
                            st.markdown(f'</div>', unsafe_allow_html=True)
                            
                        except Exception as e:
                            st.error(f"❌ Lỗi: {str(e)}. Vui lòng kiểm tra lại API Key.")
                else:
                    st.warning("⚠️ Vui lòng nhập câu hỏi!")
        else:
            st.warning("⚠️ Vui lòng nhập OpenAI API Key ở thanh bên trái để sử dụng tính năng này.")
    
    # Giải thích bài toán
    elif ai_function == "📝 Giải thích bài toán":
        st.subheader("📝 Giải thích bài toán")
        st.info("💡 Nhập một bài toán và AI sẽ giải thích cách giải từng bước một cách chi tiết.")
        
        if st.session_state.openai_api_key:
            problem_type = st.selectbox(
                "Chọn loại bài toán:",
                ["Phép cộng", "Phép trừ", "Phép nhân", "Bài toán có lời văn", "Tự nhập"]
            )
            
            if problem_type == "Tự nhập":
                problem_text = st.text_area(
                    "Nhập bài toán:",
                    height=100,
                    placeholder="Ví dụ: 25 + 17 = ? hoặc Lan có 15 cái kẹo, mẹ cho thêm 8 cái. Hỏi Lan có tất cả bao nhiêu cái kẹo?"
                )
            else:
                # Tạo bài toán mẫu
                if problem_type == "Phép cộng":
                    num1 = random.randint(10, 50)
                    num2 = random.randint(10, 50)
                    problem_text = f"{num1} + {num2} = ?"
                elif problem_type == "Phép trừ":
                    num1 = random.randint(20, 50)
                    num2 = random.randint(10, num1)
                    problem_text = f"{num1} - {num2} = ?"
                elif problem_type == "Phép nhân":
                    num1 = random.randint(2, 9)
                    num2 = random.randint(1, 10)
                    problem_text = f"{num1} × {num2} = ?"
                else:  # Bài toán có lời văn
                    word_problems = [
                        "Lan có 25 cái kẹo. Mẹ cho Lan thêm 18 cái kẹo nữa. Hỏi Lan có tất cả bao nhiêu cái kẹo?",
                        "Một cửa hàng có 45 quyển vở. Họ đã bán 27 quyển vở. Hỏi cửa hàng còn lại bao nhiêu quyển vở?",
                        "Một lớp học có 4 tổ, mỗi tổ có 8 học sinh. Hỏi lớp học có tất cả bao nhiêu học sinh?"
                    ]
                    problem_text = random.choice(word_problems)
                
                st.markdown(f'<div class="exercise-box">', unsafe_allow_html=True)
                st.markdown(f"### 📋 Bài toán mẫu:")
                st.markdown(f"**{problem_text}**")
                st.markdown(f'</div>', unsafe_allow_html=True)
            
            if st.button("🔍 Giải thích bài toán", type="primary"):
                if problem_text:
                    with st.spinner("🤔 AI đang phân tích và giải thích..."):
                        try:
                            client = OpenAI(api_key=st.session_state.openai_api_key)
                            
                            # Đảm bảo encoding đúng UTF-8
                            problem_text_safe = problem_text
                            
                            prompt = f"""Hãy giải thích cách giải bài toán sau một cách chi tiết, từng bước, phù hợp với học sinh lớp 2. 
Sử dụng ngôn ngữ đơn giản, dễ hiểu và đưa ra ví dụ minh họa nếu có thể.

Bài toán: {problem_text_safe}

Hãy giải thích:
1. Đây là dạng bài toán gì?
2. Các bước giải như thế nào?
3. Kết quả cuối cùng là gì?
4. Có mẹo nào để nhớ không?"""
                            
                            system_content = "Bạn là một giáo viên toán chuyên nghiệp, thân thiện và nhiệt tình dạy toán lớp 2. Hãy giải thích một cách đơn giản, dễ hiểu, phù hợp với học sinh lớp 2. Sử dụng ví dụ cụ thể và ngôn ngữ tiếng Việt."
                            
                            response = client.chat.completions.create(
                                model="gpt-3.5-turbo",
                                messages=[
                                    {
                                        "role": "system",
                                        "content": system_content
                                    },
                                    {
                                        "role": "user",
                                        "content": prompt
                                    }
                                ],
                                temperature=0.7,
                                max_tokens=800
                            )
                            
                            ai_response = response.choices[0].message.content
                            
                            st.markdown(f'<div class="correct-answer">', unsafe_allow_html=True)
                            st.markdown(f"### 🤖 Giải thích từ AI:")
                            st.markdown(ai_response)
                            st.markdown(f'</div>', unsafe_allow_html=True)
                            
                        except UnicodeEncodeError as e:
                            st.error(f"Loi: Co ky tu dac biet khong the xu ly. Vui long thu lai.")
                        except Exception as e:
                            error_msg = str(e).encode('ascii', errors='ignore').decode('ascii')
                            st.error(f"Loi: {error_msg}. Vui long kiem tra lai API Key.")
                else:
                    st.warning("⚠️ Vui lòng nhập bài toán!")
        else:
            st.warning("⚠️ Vui lòng nhập OpenAI API Key ở thanh bên trái để sử dụng tính năng này.")
    
    # Tạo bài tập mới
    elif ai_function == "🎲 Tạo bài tập mới":
        st.subheader("🎲 Tạo bài tập mới")
        st.info("💡 AI sẽ tạo bài tập mới phù hợp với trình độ của bạn.")
        
        if st.session_state.openai_api_key:
            col1, col2 = st.columns(2)
            with col1:
                topic = st.selectbox(
                    "Chọn chủ đề:",
                    ["Phép cộng", "Phép trừ", "Phép nhân", "Bài toán có lời văn", "Tổng hợp"]
                )
            with col2:
                difficulty = st.selectbox(
                    "Chọn độ khó:",
                    ["Dễ", "Trung bình", "Khó"]
                )
            
            num_questions = st.slider("Số lượng câu hỏi:", 1, 10, 5)
            
            if st.button("🎲 Tạo bài tập", type="primary"):
                with st.spinner("🤔 AI đang tạo bài tập cho bạn..."):
                    try:
                        client = OpenAI(api_key=st.session_state.openai_api_key)
                        
                        # Đảm bảo encoding đúng UTF-8
                        topic_safe = topic
                        difficulty_safe = difficulty
                        
                        prompt = f"""Hãy tạo {num_questions} câu hỏi toán lớp 2 về chủ đề {topic_safe} với độ khó {difficulty_safe}.
Mỗi câu hỏi phải:
- Phù hợp với học sinh lớp 2
- Có đáp án rõ ràng
- Được đánh số thứ tự

Định dạng:
Câu 1: [câu hỏi]
Đáp án: [đáp án]

Câu 2: [câu hỏi]
Đáp án: [đáp án]
..."""
                        
                        system_content = "Bạn là một giáo viên toán chuyên nghiệp tạo bài tập cho học sinh lớp 2. Hãy tạo bài tập phù hợp, rõ ràng và có đáp án."
                        
                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {
                                    "role": "system",
                                    "content": system_content
                                },
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ],
                            temperature=0.8,
                            max_tokens=1000
                        )
                        
                        ai_response = response.choices[0].message.content
                        
                        st.markdown(f'<div class="exercise-box">', unsafe_allow_html=True)
                        st.markdown(f"### 📝 Bài tập mới ({topic} - {difficulty}):")
                        st.markdown(ai_response)
                        st.markdown(f'</div>', unsafe_allow_html=True)
                        
                    except UnicodeEncodeError as e:
                        st.error(f"Loi: Co ky tu dac biet khong the xu ly. Vui long thu lai.")
                    except Exception as e:
                        error_msg = str(e).encode('ascii', errors='ignore').decode('ascii')
                        st.error(f"Loi: {error_msg}. Vui long kiem tra lai API Key.")
        else:
            st.warning("⚠️ Vui lòng nhập OpenAI API Key ở thanh bên trái để sử dụng tính năng này.")
    
    # Lời khuyên học tập
    else:  # Lời khuyên học tập
        st.subheader("💡 Lời khuyên học tập")
        st.info("💡 AI sẽ đưa ra lời khuyên học tập dựa trên thống kê và mục tiêu của bạn.")
        
        if st.session_state.openai_api_key:
            # Hiển thị thống kê
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Điểm số", st.session_state.score)
            with col2:
                st.metric("Số câu đã làm", st.session_state.total_questions)
            with col3:
                accuracy = (st.session_state.score / st.session_state.total_questions * 100) if st.session_state.total_questions > 0 else 0
                st.metric("Tỷ lệ đúng", f"{accuracy:.1f}%")
            
            learning_goal = st.selectbox(
                "Mục tiêu học tập của bạn:",
                ["Cải thiện điểm số", "Học nhanh hơn", "Nắm vững kiến thức cơ bản", "Chuẩn bị cho kỳ thi", "Tự nhập"]
            )
            
            if learning_goal == "Tự nhập":
                custom_goal = st.text_input("Nhập mục tiêu của bạn:")
                goal_text = custom_goal if custom_goal else "Cải thiện kỹ năng toán học"
            else:
                goal_text = learning_goal
            
            if st.button("💡 Nhận lời khuyên", type="primary"):
                with st.spinner("🤔 AI đang phân tích và đưa ra lời khuyên..."):
                    try:
                        client = OpenAI(api_key=st.session_state.openai_api_key)
                        
                        # Đảm bảo encoding đúng UTF-8
                        goal_text_safe = goal_text
                        
                        stats_info = f"""
Thống kê hiện tại:
- Điểm số: {st.session_state.score}
- Số câu đã làm: {st.session_state.total_questions}
- Tỷ lệ đúng: {accuracy:.1f}%
"""
                        
                        prompt = f"""Dựa trên thống kê học tập sau và mục tiêu của học sinh, hãy đưa ra lời khuyên học tập cụ thể, thực tế và khuyến khích.

{stats_info}

Mục tiêu: {goal_text_safe}

Hãy đưa ra:
1. Đánh giá về tình hình học tập hiện tại
2. Lời khuyên cụ thể để cải thiện
3. Kế hoạch học tập đề xuất
4. Lời động viên tích cực"""
                        
                        system_content = "Bạn là một giáo viên toán chuyên nghiệp, thân thiện và nhiệt tình. Hãy đưa ra lời khuyên học tập tích cực, khuyến khích và thực tế cho học sinh lớp 2."
                        
                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {
                                    "role": "system",
                                    "content": system_content
                                },
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ],
                            temperature=0.7,
                            max_tokens=600
                        )
                        
                        ai_response = response.choices[0].message.content
                        
                        st.markdown(f'<div class="correct-answer">', unsafe_allow_html=True)
                        st.markdown(f"### 🤖 Lời khuyên từ AI:")
                        st.markdown(ai_response)
                        st.markdown(f'</div>', unsafe_allow_html=True)
                        
                    except UnicodeEncodeError as e:
                        st.error(f"Loi: Co ky tu dac biet khong the xu ly. Vui long thu lai.")
                    except Exception as e:
                        error_msg = str(e).encode('ascii', errors='ignore').decode('ascii')
                        st.error(f"Loi: {error_msg}. Vui long kiem tra lai API Key.")
        else:
            st.warning("⚠️ Vui lòng nhập OpenAI API Key ở thanh bên trái để sử dụng tính năng này.")
    
    st.markdown("---")
    st.markdown("""
    ### 📌 Lưu ý:
    - 🔑 Bạn cần có OpenAI API Key để sử dụng tính năng AI
    - 💰 Sử dụng API có thể phát sinh chi phí (rất nhỏ)
    - 🎯 AI sẽ giúp bạn học tập hiệu quả hơn với giải thích chi tiết và lời khuyên cá nhân hóa
    - 🔒 API Key của bạn chỉ được lưu trong phiên làm việc hiện tại, không được lưu vĩnh viễn
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🔢 Ứng dụng Dạy Chuyên Toán Lớp 2</p>
    <p>Chúc các em học tốt! 💪</p>
</div>
""", unsafe_allow_html=True)

