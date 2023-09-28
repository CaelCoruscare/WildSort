from ultralytics import YOLO


# Load a model
model = YOLO('yolov8n.pt')  # pretrained YOLOv8n model

# Run batched inference on a list of images
results = model(
    ['/Users/3rd/Desktop/Photos for Initial Testing of Yolo/Dogs/IMG_0122_Not Setup or Takedown_Any Trigger_Human Elements_Humans on Foot_Domestic Animals_Domestic Dogs.JPG',
      '/Users/3rd/Desktop/Photos for Initial Testing of Yolo/Humans/IMG_0117_Not Setup or Takedown_Any Trigger_Human Elements_Humans on Foot.JPG',
      '/Users/3rd/Desktop/Photos for Initial Testing of Yolo/Humans/IMG_0175_Not Setup or Takedown_Any Trigger_Human Elements_Humans on Foot_Domestic Animals_Shoats.JPG',
      '/Users/3rd/Desktop/Photos for Initial Testing of Yolo/Shoats/IMG_0134_Not Setup or Takedown_Any Trigger_Domestic Animals_Shoats.JPG'
      ], save=True)  # return a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    print(probs)






# # Create a new YOLO model from scratch
# model = YOLO('yolov8n.yaml')

# # Load a pretrained YOLO model (recommended for training)
# model = YOLO('yolov8n.pt')

# # Train the model using the 'coco128.yaml' dataset for 3 epochs
# results = model.train(data='coco128.yaml', epochs=3)

# # Evaluate the model's performance on the validation set
# results = model.val()

# # Perform object detection on an image using the model
# results = model('https://ultralytics.com/images/bus.jpg')

# # Export the model to ONNX format
# success = model.export(format='onnx')

# print(success)







# import random

# prizes = ['trophy','stuffed animal','money','candy','vacation']
# print()
# prize = random.sample(prizes,1) 
# print(f'Your prize is {prize}')


#>>>Your prize is {}




# print('What is your first name?')
# firstName = input()

# print('What is your last name?')
# lastName = input()

# print()

#print(f'Your fullname is {lastName} Poopybutt {lastName}')
















# print('hello')
# print('my name is Inigo Montoya')
# print('What is your name?')
# name = input()
# print("Hello " + name)





























# from dataclasses import dataclass

# @dataclass
# class ReportParts():
#     headers: []
#     columns: [[]]

#     def add(self, newParts): #Why does declaring type, ie: "newParts: reportParts" not work?
#         if ReportParts != type(newParts):
#              raise TypeError
#         self.headers.extend(newParts.headers)
#         self.columns.extend(newParts.columns)

# petNames = ReportParts(['cat','dog'], [['Gato','Sabrina','Meow'],['Spot','Cerberus','Argos']])

# bunnnyNames = ReportParts(['bunny'], [['Hopper','Flopsy','Snowball']])

# petNames.add(bunnnyNames)

# #Pretty Print
# for animal, names in zip(petNames.headers, petNames.columns):
#         print (animal + ': ' + str(names))


# print(a.headers)
# print('---------')
# print(a.columns)





######Generators
# dataColumn = [0,1,0,0,1,-1,-1,1]

# cleaned = [0 if (data == -1) else data for data in dataColumn]

# print(cleaned)




######ZIP
# listOfList = [['col A', 'a1',2,3],['col B', 'b4',5,6],['col C', 'c7',8,9]]


# zippedList = zip(*listOfList)

# reversedList =  zip(*reversed(listOfList))

# for list in listOfList:
#     print(list)

# print('(----------)')

# for list in zippedList:
#     print(list)

# print('((----------))')

# for list in reversedList:
#     print(list)


# print('((----------))')
# print(listOfList)

# print('((----------))')
# print(*listOfList)