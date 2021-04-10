#IMPORT HERE..
import cv2 
import numpy as np

#DEFINE CONSTANTS HERE..
FONT = None
BOOKMARK_ICON = None

def render_button(question_num, marked_for_review, bg_color, font_color):
    define_constants()
    image = np.zeros((83,112,3), dtype = np.uint8)
    for i in range(len(image)):
        for j in range(len(image[i])):
            image[i][j] = np.array(list(bg_color), dtype = int)
    text = "Q." + str(question_num)
    text_size = cv2.getTextSize(text, FONT, 1, 2)[0]
    coordinates = ((image.shape[1] - text_size[0])//2, (image.shape[0] + text_size[1])//2-3)
    image = cv2.putText(img = image, text = text, org =  coordinates, fontFace= FONT, fontScale = 1, color = font_color, thickness = 2, lineType= cv2.LINE_AA)

    if marked_for_review == True:
        for i in range(len(BOOKMARK_ICON)):
            for j in range(len(BOOKMARK_ICON[i])):
                if sum(BOOKMARK_ICON[i][j]) <= 600 :
                    image[i][j+87] = BOOKMARK_ICON[i][j]
    if __name__ == "__main__":
        print(BOOKMARK_ICON.shape)
        print(image.shape)
        cv2.imshow("image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    image = cv2.resize(image, (0, 0), fx = 0.8, fy = 0.8)
    return image

    #cv2.imwrite("UI_Images/button.jpg", image)

def define_constants():
    global FONT, BOOKMARK_ICON
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    BOOKMARK_ICON = cv2.imread(r"UI_Images\bookmark.png")

if __name__ == '__main__':
    render_button(15, True, bg_color = (128, 0, 128), font_color = (255, 255, 255))
    
