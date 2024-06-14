import streamlit as st
import os
from PIL import Image
import base64

# 定義圖片根目錄
IMAGE_ROOT = 'C:/Users/xtbal/Desktop/多媒體/HM-Recommendation/images'  # 請替換為你的圖片根目錄

# 獲取所有資料夾名稱
folders = sorted([folder for folder in os.listdir(IMAGE_ROOT) if os.path.isdir(os.path.join(IMAGE_ROOT, folder))])

# 設置每行顯示的資料夾數量和每頁顯示的資料夾數量
folders_per_row = 10
folders_per_page = 20
images_per_row = 10
images_per_page = 20

def display_folder(folder_path):
    # 獲取資料夾內的所有圖片
    images = sorted([img for img in os.listdir(folder_path) if img.endswith(('jpg', 'jpeg', 'png'))])
    if not images:
        return None
    
    first_image_path = os.path.join(folder_path, images[0])
    return first_image_path, images

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

st.set_page_config(layout="wide")  # 設置頁面為最寬

st.title('H&M Personalized Fashion Recommendations')

# 添加CSS樣式
st.markdown("""
    <style>
    .image-button-container {
        position: relative;
        display: inline-block;
    }
    .image-button-container img {
        width: 100%;
        height: auto;
    }
    .image-button {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0;
        cursor: pointer;
        border: none;
        background: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 計算資料夾總頁數
total_folder_pages = (len(folders) - 1) // folders_per_page + 1

# 初始化頁面索引
if 'folder_page_index' not in st.session_state:
    st.session_state.folder_page_index = 0

# 獲取當前頁的資料夾
folder_start_index = st.session_state.folder_page_index * folders_per_page
folder_end_index = folder_start_index + folders_per_page
current_folders = folders[folder_start_index:folder_end_index]

# 顯示資料夾
for i in range(0, len(current_folders), folders_per_row):
    cols = st.columns(folders_per_row)
    for j, folder in enumerate(current_folders[i:i+folders_per_row]):
        folder_path = os.path.join(IMAGE_ROOT, folder)
        result = display_folder(folder_path)
        if result:
            first_image_path, images = result
            img_base64 = image_to_base64(first_image_path)
            with cols[j]:
                if st.button(f"Select {folder}", key=f"folder_{folder}"):
                    st.session_state.selected_folder = folder
                    st.session_state.images = images
                    st.session_state.image_page_index = 0  # Reset image page index when a new folder is selected
                st.markdown(
                    f"""
                    <div class="image-button-container">
                        <img src="data:image/jpeg;base64,{img_base64}" alt="{folder}">
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# 分頁按鈕
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
with col2:
    if st.button('Previous Folders'):
        if st.session_state.folder_page_index > 0:
            st.session_state.folder_page_index -= 1
            st.experimental_rerun()
with col3:
    st.write(f'Page {st.session_state.folder_page_index + 1} of {total_folder_pages}')
with col4:
    if st.button('Next Folders'):
        if st.session_state.folder_page_index < total_folder_pages - 1:
            st.session_state.folder_page_index += 1
            st.experimental_rerun()

# 顯示選中的資料夾內的圖片
if 'selected_folder' in st.session_state and 'images' in st.session_state:
    selected_folder = st.session_state.selected_folder
    images = st.session_state.images
    st.write(f'### {selected_folder}')
    
    # 計算圖片總頁數
    total_image_pages = (len(images) - 1) // images_per_page + 1
    
    # 初始化圖片頁面索引
    if 'image_page_index' not in st.session_state:
        st.session_state.image_page_index = 0
    
    # 獲取當前頁的圖片
    image_start_index = st.session_state.image_page_index * images_per_page
    image_end_index = image_start_index + images_per_page
    current_images = images[image_start_index:image_end_index]
    
    for i in range(0, len(current_images), images_per_row):
        cols = st.columns(images_per_row)
        for j, img in enumerate(current_images[i:i+images_per_row]):
            img_path = os.path.join(IMAGE_ROOT, selected_folder, img)
            img_base64 = image_to_base64(img_path)
            img_name, _ = os.path.splitext(img)  # 只顯示文件名，不包括擴展名
            with cols[j]:
                if st.button(f"Select {img_name}", key=f"image_{img}"):
                    st.session_state.selected_image = img_name
                st.markdown(
                    f"""
                    <div class="image-button-container">
                        <img src="data:image/jpeg;base64,{img_base64}" alt="{img}">
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # 圖片分頁按鈕
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col2:
        if st.button('Previous Images'):
            if st.session_state.image_page_index > 0:
                st.session_state.image_page_index -= 1
                st.experimental_rerun()
    with col3:
        st.write(f'Images Page {st.session_state.image_page_index + 1} of {total_image_pages}')
    with col4:
        if st.button('Next Images'):
            if st.session_state.image_page_index < total_image_pages - 1:
                st.session_state.image_page_index += 1
                st.experimental_rerun()

# 顯示選中的圖片名稱
if 'selected_image' in st.session_state:
    st.write(f'選擇的圖片名稱是: {st.session_state.selected_image}')
