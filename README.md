Đây là file Readme của License Detect module
Tác giả : giang lê, duy, quốc

Nội dung : 
    - Hướng dẫn sử dụng
    - Mô tả hoạt động
    - Một số kinh nghiệm
    - FAQ
 
 
I, Hướng dẫn sử dụng
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


IV, Quá trình phát triển
---------------------------
	- Hai phương án đề xuất ban đầu: 	
		+ Tạo training data để nhận diện chữ cái
		+ Nhận diện trực tiếp bằng font chữ ENG có sẵn, chất lượng detect sẽ kém hơn đôi chút.
			Một vài chữ cái sẽ nhận diện sai và khó( như Z và 2, 1. và L, O và 0, ...)
	- Phương án tạo training data:
		+ Khó tìm được bộ data tốt do mỗi ảnh chỉ có khoảng 7 chữ cái lẫn số. Các chữ số 
			thì nhiều và chữ cái thì ít, bộ training sẽ không hợp lí( không đảm bảo lượng ).
			Chưa kể việc cắt box cũng tốn thời gian. Và vẫn phải tiền xử lí kha khá công đoạn.
			Trong khi đó, ảnh tiền xử lí, sau khi ném vào Tesseract nhận diện được kết quả có độ
			chính xác khá ổn, nhất là nếu bộ ảnh input tốt
			=> Tập trung vào việc tiền xử lí tốt và kiếm data tốt sẽ hợp lí hơn
	- Trong quá trình nâng cấp phần tiền xử lí:
		+ Chất lượng đầu vào không tốt. Nhiều ảnh nhòe, bị bóng, biển số Việt Nam có đinh quá to,
			viền cũng quá dày. Viền lại có nhiều kí tự hoa văn nhập nhằng
		=> Xóa bỏ hết phần viền ảnh, chỉ lấy dữ liệu bên trong. Sử dụng Adaptive ThreshHolding 
			để xử lí phần bị nhòe, bị bóng. Equalize Histogram giúp làm ảnh rõ nét hơn. 
		+ Tuy nhiên, các Module sử dụng đều được lựa chọn thông số cho phù hợp nhất với bộ data, 
			cho nên nó có thể chạy không tốt với một số bộ data khác
		+ Sử dụng threshHold cơ bản sẽ detect được nhiều số hơn, trong khi đó Adaptive ThreshHold 
			thì nhận diện số rõ nét hơn -> dùng ThreshHold thường để nhận diện số cơ bản, và sử dụng
			Adaptive ThreshHold để nhận diện số rõ hơn. Nếu Adaptive nhận diện được số nào thì sẽ 
			chắc chắn sử dụng chữ số đó, còn những số nào mà ThreshHold thường nhận diện được mà
			Adaptive không nhận diện được sẽ sử dụng chữ số của ThreshHold nhận diện
		+ Kết quả nhận diện khá tốt, với một bộ dữ liệu kém, song đã nhận diện đúng 100% cho khoảng 10% 
			bộ data, đúng >= 50% cho phần lớn bộ dữ liệu. Nếu với bộ dữ liệu đẹp thì ước lượng đúng >= 80% 
			cho tất cả các ảnh