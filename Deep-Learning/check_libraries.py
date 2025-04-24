import subprocess

# Danh sách các thư viện cần kiểm tra
libraries = {
    'numpy': 'numpy',
    'pandas': 'pandas',
    'opencv-python': 'cv2',
    'tensorflow': 'tensorflow',
    'matplotlib': 'matplotlib',
    'scikit-learn': 'sklearn',
    'kaggle': 'kagglehub',
    'Pillow': 'PIL',
   
    'h5py': 'h5py'
}


# Kiểm tra các thư viện Python
for lib_name, module_name in libraries.items():
    try:
        __import__(module_name)
        print(f"{lib_name} đã được cài đặt.")
    except ImportError:
        print(f"{lib_name} chưa được cài đặt.")

# Kiểm tra công cụ dòng lệnh tensorflowjs_converter
print("\nKiểm tra công cụ dòng lệnh:")
try:
    result = subprocess.run(['tensorflowjs_converter', '--version'], capture_output=True, text=True, check=True)
    print(f"tensorflowjs_converter đã được cài đặt: {result.stdout.strip()}")
except FileNotFoundError:
    print("tensorflowjs_converter chưa được cài đặt.")
except subprocess.CalledProcessError as e:
    print(f"Đã xảy ra lỗi khi kiểm tra tensorflowjs_converter: {e}")
