import streamlit as st
import time

st.sidebar.title('Menu')
selection = st.sidebar.radio("Go to", ["Home", "Chạy game Maze", "Chạy game 8-puzzle", "Chạy game 2048", "Chạy game Connect Four","Chạy game Tic-toc-toe", "Mô hình phân loại Naive Bayes để phân loại cảm xúc của các bình luận về phim"])

# Hiển thị nội dung tương ứng
if selection == "Home":
    st.write("<h1 style='color: #F7418F;'><span style='color: #F7418F;'>📜</span> BÁO CÁO ĐỒ ÁN CUỐI KỲ</h1>", unsafe_allow_html=True)
    st.image(r'logo.png', width=100)
    st.write("<h2 style='color: #FF407D;'>THUẬT TOÁN:</h2>", unsafe_allow_html=True)
    st.write("<h3 style='color: #FC819E;'>Môn:    Trí tuệ nhân tạo</h3>", unsafe_allow_html=True)
    st.write("<h3 style='color: #FC819E;'>GVHD:   Trần Tiến Đức</h3>", unsafe_allow_html=True)
    st.write("<h3 style='color: #FC819E;'>Họ tên: Trần Diễm Quỳnh - MSSV: 22133046</h3>", unsafe_allow_html=True)
    
    st.caption('Thủ Đức, ngày 15 tháng 5 năm 2023')
    
    st.markdown('---')

    st.markdown('<span style="font-size: 20px; color: #F4538A;">🎥 Video demo chạy trên Desktop</span>', unsafe_allow_html=True)

    # Hiển thị video
    video_file = open(r'Demo_desktop.mp4', 'rb')  
    video_bytes = video_file.read()
    st.video(video_bytes)

    st.markdown('---')

    st.markdown('<span style="font-size: 20px; color: #F4538A;">🎥 Video demo chạy trên Streamlit</span>', unsafe_allow_html=True)

    # Hiển thị video
    video_file = open(r'Demo_streamlit.mp4', 'rb')  
    video_bytes = video_file.read()
    st.video(video_bytes)

    st.markdown('---')

    st.markdown('<span style="font-size: 20px; color: #F4538A;">📌 Mô tả thuật toán A*:</span>', unsafe_allow_html=True)
    st.caption('')

    st.markdown('---')

    st.markdown('<span style="font-size: 20px; color: #F4538A;">📌 Mô tả thuật toán Minimax:</span>', unsafe_allow_html=True)
    st.caption('Các chi tiết có trong sách')

    st.markdown('---')

    st.markdown('<span style="font-size: 20px; color: #F4538A;">📌 Mô tả thuật toán Naive Bayes Classifier:</span>', unsafe_allow_html=True)
    st.caption('Các chi tiết có trong sách')

if selection == "Chạy game Maze":
    st.markdown('<span style="font-size: 30px; color: #F7418F;"><b>📍 CHẠY GAME MAZE TRÊN STREAMLIT</b></span>', unsafe_allow_html=True)

    path = r'Maze\test16.py'
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    exec(content)

elif selection == "Chạy game 8-puzzle":
    st.markdown('<span style="font-size: 30px; color: #F7418F;"><b>📍 CHẠY GAME 8 PUZZLE TRÊN STREAMLIT</b></span>', unsafe_allow_html=True)

    path = r'Eight_puzzle\eight_puzzle_streamlit.py'
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    exec(content)

elif selection == "Chạy game 2048":
    st.markdown('<span style="font-size: 30px; color: #F7418F;"><b>📍 CHẠY GAME 2048 TRÊN STREAMLIT</b></span>', unsafe_allow_html=True)

    path = r'2048\test8.py'
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    exec(content)

elif selection == "Chạy game Connect Four":
    st.markdown('<span style="font-size: 30px; color: #F7418F;"><b>📍 CHẠY GAME CONNECT FOUR TRÊN STREAMLIT</b></span>', unsafe_allow_html=True)

    path = r'Connect Four\test3.py'
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    exec(content)

elif selection == "Chạy game Tic-toc-toe":
    st.markdown('<span style="font-size: 30px; color: #F7418F;"><b>📍 CHẠY GAME TIC-TOC-TOE TRÊN STREAMLIT</b></span>', unsafe_allow_html=True)

    game_option = st.radio("Chọn chương trình để chạy:", ["Người đấu với người", "Máy đấu với người"])

    if game_option == "Người đấu với người":
        path_1 = r'Tic_tac_toe\test12.py'
        with open(path_1, 'r', encoding='utf-8') as file:
            content = file.read()
        exec(content)

    elif game_option == "Máy đấu với người":
        path_2 = r'Tic_tac_toe\test14.py'
        with open(path_2, 'r', encoding='utf-8') as file:
            content = file.read()
        exec(content)

elif selection == "Mô hình phân loại Naive Bayes để phân loại cảm xúc của các bình luận về phim":
    st.markdown('<span style="font-size: 30px; color: #F7418F;"><b>📍 CHẠY MÔ HÌNH PHÂN LOẠI NAIVE BAYES ĐỂ PHÂN LOẠI CẢM XÚC CỦA CÁC BÌNH LUẬN VỀ PHIM TRÊN STREAMLIT</b></span>', unsafe_allow_html=True)
    path = r'Naive Bayes Classifier\test1.py'
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    exec(content)



