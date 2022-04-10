import cv2
import imutils
import numpy as np



# Param
max_size = 5000
min_size = 900

# Load image
img = cv2.imread('bien-so-xe-9999.jpg', cv2.IMREAD_COLOR)

# Resize image
img = cv2.resize(img, (620, 480))

#Phát hiện cạnh
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Chuyển đổi về ảnh xám
Gray = cv2.bilateralFilter(gray, 11, 17, 17)  # bộ lọc làm mịn phi tuyến tính, bảo toàn cạnh và giảm nhiễu cho hình ảnh
edged = cv2.Canny(Gray, 30, 200)  # Phát hiện cạnh


# Tìm đường viền chỉ giữ lại cái lớn nhất
cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)# Tính Contours của ảnh
# cv2.CHAIN_APPROX_SIMPLE:loại bỏ tất cả các điểm thừa và viền do đó ở đây ta xét 4 điểm
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)#SAwawso xếp các contours giảm dần
#là một danh sách tất cả các đường viền trong ảnh
#mỗi đường bao riêng lẻ là một mảng numpy tọa độc (x,y) các điểm biên của đối tượng
screenCnt = None

# loop over our contours
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)#hàm tính chu vi của đường viền,True là đường viền này khép kín

    approx = cv2.approxPolyDP(c, 0.05 * peri, True)#hàm tính xấp xỉ đường viền

    #giá trị coutours trong khoảng giá trị max min thì chọn
    if len(approx) == 4 and max_size > cv2.contourArea(c) > min_size:
        screenCnt = approx
        break#nếu thỏa mãn thì thoát khỏi vòng for

if screenCnt is None:
    detected = 0
    print ("Không tìm thấy biển số xe nào")
else:
    detected = 1

if detected == 1:#nếu tìm được contours thích hợp thì tiến hành cắt
    cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)#dùng để vẽ đường viền theo chu vi
    #vẽ màu xanh bao quanh là biển số được chọn

    # Che phần không phải biển số
    mask = np.zeros(gray.shape, np.uint8)#tạo 1 mảng số nguyên 8 bit gồm các số 0
    new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )#vẽ hình màu trắng lên cái mask đã tạo
    new_image = cv2.bitwise_and(img, img, mask=mask)#toán tử and và giá trị đường biên để tạo ra khung phát hiện biển số


    # Now crop
    (x, y) = np.where(mask == 255)#tìm tất cả các vị trí hàng và cột trong mảng khớp với cột điều kiện
    (topx, topy) = (np.min(x), np.min(y))#tìm giá trị min max của contour để cắt
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]#Cắt ảnh mức xám và lưu vào ảnh Cropped

    # Display image
    cv2.imshow('anh xe', img)
    cv2.imshow('anh xam',gray)
    cv2.imshow('anh loc min',Gray)
    cv2.imshow('phat hien canh',edged)
    cv2.imshow('bien so xe', Cropped)

    cv2.waitKey(0)
    cv2.destroyAllWindows()