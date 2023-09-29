from ultralytics import YOLO

def yoloPhotos(photoURLs: list[str]) -> list[str]:

    # Load a model
    model = YOLO('yolov8n.pt')  # pretrained YOLOv8n model

    # Run batched inference on a list of images
    results = model(
        photoURLs
        , save=True)  # return a list of Results objects
    
    saveDirectory = results[0].save_dir
    yoloPhotoURLs = []

    for result in results:
        url = result.save_dir + '/' + result.path.split('/')[-1]
        yoloPhotoURLs.append(url)

    return yoloPhotoURLs

    # # Process results list
    # for result in results:
    #     boxes = result.boxes  # Boxes object for bbox outputs
    #     masks = result.masks  # Masks object for segmentation masks outputs
    #     keypoints = result.keypoints  # Keypoints object for pose outputs
    #     probs = result.probs  # Probs object for classification outputs
        
    #     print()
    #     print('confidences: ')
    #     for box in boxes:
    #         print(model.names[int(box.cls)])
    #         print(box.conf.numpy()[0])
    #     print()