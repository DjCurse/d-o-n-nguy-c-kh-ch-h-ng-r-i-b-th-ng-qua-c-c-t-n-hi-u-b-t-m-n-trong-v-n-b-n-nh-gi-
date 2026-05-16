import subprocess
import os
import json
import pandas as pd
from google_play_scraper import Sort, reviews

# ==========================================
# HÀM 1: CÀO DỮ LIỆU TỪ GOOGLE PLAY
# ==========================================
def scrape_data(project_dir):
    print("\n[1/3] Đang cào dữ liệu Shopee từ Google Play...")
    app_id = 'com.shopee.vn'
    
    # Lấy 5000 đánh giá mới nhất và hữu ích nhất
    rvs, _ = reviews(
        app_id,
        lang='vi', 
        country='vn', 
        sort=Sort.MOST_RELEVANT, 
        count=5000
    )
    
    print(f"-> Đã cào thành công {len(rvs)} đánh giá.")
    
    df = pd.DataFrame(rvs)
    df = df[['content', 'score', 'at', 'thumbsUpCount']]
    df.columns = ['review_text', 'rating', 'review_date', 'thumbs_up']
    
    # Lưu vào thư mục raw
    save_dir = os.path.join(project_dir, 'data', 'raw')
    os.makedirs(save_dir, exist_ok=True)
    
    save_path = os.path.join(save_dir, 'Shopee_Reviews.csv')
    df.to_csv(save_path, index=False, encoding='utf-8-sig')
    print(f"✅ Xong! Dữ liệu thô đã được lưu tại: {save_path}")

# ==========================================
# HÀM 2: ĐỌC VÀ CHẠY FILE NOTEBOOK (.ipynb)
# ==========================================
def extract_and_run(ipynb_path, output_txt=None):
    if not os.path.exists(ipynb_path):
        print(f"❌ Lỗi: Không tìm thấy file {ipynb_path}")
        return False
        
    try:
        # Đọc ruột file Notebook
        with open(ipynb_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
            
        # Lấy code ra
        code_blocks = []
        for cell in notebook.get('cells', []):
            if cell.get('cell_type') == 'code':
                code_blocks.append("".join(cell.get('source', [])))
                
        # Tạo file .py tạm thời
        temp_py = ipynb_path.replace('.ipynb', '_temp.py')
        with open(temp_py, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(code_blocks))
            
        # Chạy file với chuẩn tiếng Việt (utf-8)
        if output_txt:
            with open(output_txt, 'w', encoding='utf-8') as out_f:
                subprocess.run(['python', '-X', 'utf8', temp_py], stdout=out_f, stderr=subprocess.STDOUT)
            print(f"📄 Kết quả đã in ra: {output_txt}")
        else:
            subprocess.run(['python', '-X', 'utf8', temp_py])
            
        # Xóa file tạm, bảo vệ file gốc
        if os.path.exists(temp_py):
            os.remove(temp_py)
            
        return True
        
    except Exception as e:
        print(f"❌ Có lỗi khi chạy file: {e}")
        return False

# ==========================================
# HÀM CHÍNH: ĐIỀU PHỐI TOÀN BỘ PROJECT
# ==========================================
def run_project():
    print("="*65)
    print("🚀 BẮT ĐẦU CHẠY PIPELINE TỰ ĐỘNG (END-TO-END) - NHÓM 18")
    print("="*65)
    
    # 1. Đường dẫn dự án
    project_dir = r"D:\NNLT_PYTHON\GroupPython\d-o-n-nguy-c-kh-ch-h-ng-r-i-b-th-ng-qua-c-c-t-n-hi-u-b-t-m-n-trong-v-n-b-n-nh-gi-\project"
    notebook_dir = os.path.join(project_dir, 'notebook')
    results_dir = os.path.join(project_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    khang_nb = os.path.join(notebook_dir, '1_Khang_EDA.ipynb')
    huy_nb = os.path.join(notebook_dir, '2_Huy_Preprocessing.ipynb')
    
    # 2. Thực thi Bước 1: Cào dữ liệu
    scrape_data(project_dir)
    
    # 3. Thực thi Bước 2: Gia Huy làm sạch & Chạy mô hình
    print("\n[2/3] Đang chạy file 2_Huy_Preprocessing.ipynb (Làm sạch & Train)...")
    output_txt = os.path.join(results_dir, 'ket_qua_Huy.txt')
    if extract_and_run(huy_nb, output_txt):
        print("✅ Hoàn tất quá trình tiền xử lý và học máy của Huy!")
        
    # 4. Thực thi Bước 3: Chí Khang vẽ biểu đồ
    print("\n[3/3] Đang chạy file 1_Khang_EDA.ipynb (Vẽ biểu đồ)...")
    if extract_and_run(khang_nb):
        print("✅ Hoàn tất vẽ biểu đồ của Khang! Các ảnh đã lưu trong thư mục results.")

    print("\n" + "="*65)
    print("🎉 HỆ THỐNG PIPELINE ĐÃ HOÀN THÀNH XUẤT SẮC!")
    print("="*65)

if __name__ == "__main__":
    run_project()