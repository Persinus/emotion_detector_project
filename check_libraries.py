# check_libraries.py

libraries = ['numpy', 'pandas', 'cv2', 'tensorflow', 'matplotlib', 'sklearn']  # Sử dụng 'sklearn' cho scikit-learn

for lib in libraries:
    try:
        __import__(lib)
        print(f"{lib} đã được cài đặt.")
    except ImportError:
        print(f"{lib} chưa được cài đặt.")