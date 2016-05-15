Đây là file Readme của License Detect module
Tác giả : giang lê, duy, quốc

Nội dung : 
    - Hướng dẫn sử dụng
    - Mô tả hoạt động
    - Một số kinh nghiệm
    - FAQ
 
 
I, HƯỚNG DẪN SỬ DỤNG 
---------------------
    0, Cài đặt
		- Module được viết bằng ngôn ngữ Python, cần cài Python 2.7
			https://www.python.org/download/releases/2.7/
       
		- Module này sử dùng OpenCV, cách cài đặt OpenCV  
            http://docs.opencv.org/3.1.0/d5/de5/tutorial_py_setup_in_windows.html
            
        - Tesseract 3.02, sử dụng Windows Installer 
            https://sourceforge.net/projects/tesseract-ocr-alt/files/
       
		- Chạy được trên windows( chưa test trên Linux và MacOS)
    
    1, Chuẩn bị ảnh input
        - Các ảnh phải được chụp vuông góc, có cỡ fullHD, càng ít hình tạp càng tốt         
        - Chất lượng hình phải tốt, không nhòe, không bóng, nếu không chất lượng output sẽ bị giảm    
        - Vị trí các chữ, số phải đặt ở giữa của ảnh, các số/chữ bị đặt sát lề sẽ không được tính                   
    
    2, Các bước tiến hành       
        - Chạy python tesseract.py -h để hiện hỗ trợ
        - Với mỗi ảnh, output sẽ là: 
				+ File ảnh tiền xử lí
				+ Output ra Command Line kết quả đọc được của từng ảnh                               

II, Mô tả hoạt động 
-----------

    Module sử dụng : 
        - ThreshHold để phần số nổi lên 
        - Contour để lấy các phần nổi lên
        - Equalize Histogram đề phòng trường hợp ảnh bị tối, không rõ
        - Contrast để làm rõ hình ảnh, phục vụ ThreshHold
		- Tesseract OCR để đọc biển số
        

III, Một số kinh nghiệm
-------------------------


IV, FAQ
---------------------------
