# from skimage.metrics import structural_similarity as ssim
from django.conf import settings
import json, cv2, os
import numpy as np
import itertools

def ssim(x, y, K1=0.01, K2=0.03, L=255, window_size=7):
    """
    Calculate the Structural Similarity Index (SSIM) between two images.
    """
    C1 = (K1 * L) ** 2
    C2 = (K2 * L) ** 2
    
    # Define a gaussian window for convolution
    window = np.outer(np.hanning(window_size), np.hanning(window_size))
    window /= np.sum(window)
    
    # Mean of x and y
    mu_x = np.convolve(x.ravel(), window.ravel(), mode='valid')[0]
    mu_y = np.convolve(y.ravel(), window.ravel(), mode='valid')[0]
    
    # Variance of x and y
    sigma_x = np.convolve(x.ravel()**2, window.ravel(), mode='valid')[0] - mu_x**2
    sigma_y = np.convolve(y.ravel()**2, window.ravel(), mode='valid')[0] - mu_y**2
    
    # Covariance between x and y
    sigma_xy = np.convolve(x.ravel()*y.ravel(), window.ravel(), mode='valid')[0] - mu_x*mu_y
    
    # Calculate SSIM
    numerator = (2 * mu_x * mu_y + C1) * (2 * sigma_xy + C2)
    denominator = (mu_x**2 + mu_y**2 + C1) * (sigma_x + sigma_y + C2)
    ssim = numerator / denominator
    
    return ssim

threshold = 160 
# ssim = cv2.quality.QualitySSIM_compute

def get_reference():
    ref = cv2.imread(os.path.join(settings.REFERENCE_ROOT, 'ballot_a3.jpg'), cv2.IMREAD_GRAYSCALE)
    shape = ref.shape
    
    bbox_data = json.load(open(os.path.join(settings.REFERENCE_ROOT, 'boxes_coor.json')))
    (x1, y1), (x2, y2) = bbox_data['Sign']['sign1']
    p, q, r, s = min(y1,y2), max(y1,y2), min(x1,x2), max(x1,x2)
    
    crop_ref = ref[p:q, r:s]
    _, bin_ref = cv2.threshold(ref, threshold, 255, cv2.THRESH_BINARY)

    return bbox_data, shape, crop_ref, bin_ref, (p, q, r, s)

def sort_points(points):
    centroid = np.mean(points, axis=0)
    angles = np.arctan2(points[:, 1] - centroid[1], points[:, 0] - centroid[0])
    sorted_indices = np.argsort(angles)
    sorted_points = points[sorted_indices]
    return sorted_points.astype(np.float32)
    
def find_max_quad(contour):
    max_area, max_quad = -1, None
    
    for quad_points in itertools.combinations(contour, 4):
        quad_points = np.array(quad_points)
        area = cv2.contourArea(quad_points)
        if area > max_area: 
            max_area, max_quad = area, quad_points
            
    if max_quad is not None and max_area > 2e6: return sort_points(max_quad.reshape(4, 2))
    return None

def get_contour(image):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = max(contours, key=cv2.contourArea)
    epsilon = 0.01 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    hull = cv2.convexHull(approx)
    max_quad = find_max_quad(hull)
    return max_quad

def wrap_image(image, max_quad):
    print("Here0")
    x, y, w, h = cv2.boundingRect(max_quad)
    tmp, incorrect = shape, False
    if w>h:
        tmp = (shape[1], shape[0])
        incorrect = True
    
    print("Here1")
    target_points = np.array([[0, 0], [tmp[1], 0], [tmp[1], tmp[0]], [0, tmp[0]]], dtype=np.float32)
    perspective_matrix = cv2.getPerspectiveTransform(max_quad, target_points)
    warped_image = cv2.warpPerspective(image, perspective_matrix, (tmp[1], tmp[0]))

    if incorrect:
        print("Here2")
        warped_image1 = cv2.rotate(warped_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        crop_wrp1 = warped_image1[p:q, r:s]
        ssim_score1 = ssim(crop_wrp1, crop_ref)

        warped_image2 = cv2.rotate(warped_image, cv2.ROTATE_90_CLOCKWISE)
        crop_wrp2 = warped_image2[p:q, r:s]
        ssim_score2 = ssim(crop_wrp2, crop_ref)
        
        warped_image = warped_image1 if ssim_score1 > ssim_score2 else warped_image2

    print("Here3")
    warped_image1 = warped_image
    crop_wrp1 = warped_image1[p:q, r:s]
    ssim_score1 = ssim(crop_wrp1, crop_ref)

    print("Here4")
    warped_image2 = cv2.rotate(cv2.rotate(warped_image, cv2.ROTATE_90_CLOCKWISE), cv2.ROTATE_90_CLOCKWISE)
    crop_wrp2 = warped_image2[p:q, r:s]
    ssim_score2 = ssim(crop_wrp2, crop_ref)
    
    print("Here5")
    warped_image = warped_image1 if ssim_score1 > ssim_score2 else warped_image2

    print("Here5.33")

    _, bin_img = cv2.threshold(warped_image, threshold, 255, cv2.THRESH_BINARY)
    
    print("Here5.66")

    sim = ssim(bin_img, bin_ref)

    print("Here6")

    mse = ((bin_img - bin_ref) ** 2).mean()
    psnr = cv2.PSNR(bin_img, bin_ref)

    print("Here7")

    score = sim/0.35 + psnr/5 - mse/0.3

    print("Here8")

    validity = True if score>0.8 else False

    print("Here9")
    return warped_image if validity else None

def check_valid(name):
    # print("Here0")
    ret = None
    try:
        # print("Here1")
        image = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
        # print("Here2")
        _, bin_img = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
        # print("Here3")
        max_quad = get_contour(bin_img)
        print("Here4")
        if max_quad is not None: ret = wrap_image(image, max_quad)
        print("Here5")
    except: pass
    # print("Here6")
    return ret

def get_member(image, sub_value):
    if image is not None and sub_value is not None:
        cropped_image = image[sub_value[0][1]:sub_value[1][1], sub_value[0][0]:sub_value[1][0]]
        _, binary_image = cv2.threshold(cropped_image, threshold, 255, cv2.THRESH_BINARY)
        if np.mean(binary_image == 0) > 0.3 : return True
    return False

def draw_bbox(image):
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    outliers, color = [], {}
    for key, values in bbox_data.items():
        for sub_key, sub_value in values.items():
            color = (0, 0, 0)
            if len(key) == 1:
                color = (0, 0, 255)
                if sub_key.isdigit():
                    color = (255, 0, 0)
                    if get_member(image, sub_value):
                        outliers.append(sub_key)
                        color = (0, 255, 0)
            cv2.rectangle(image, sub_value[0], sub_value[1], color, 5)
    
    return image, outliers

# def img_display(img, name='Image'):
#     cv2.namedWindow(name, cv2.WINDOW_NORMAL)
#     cv2.resizeWindow(name, (534, 756))
#     cv2.imshow(name, img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

bbox_data, shape, crop_ref, bin_ref, (p, q, r, s) = get_reference()

# if __name__ == '__main__':
#     file_name = 'ballot_a3.jpg' # 'ballot_3d9c889f0fc3ec64_20240415_235845.jpg'
#     image = check_valid(file_name)
#     if image is not None:
#         image, members = draw_bbox(image)
#         img_display(image, file_name)
#         print(members)