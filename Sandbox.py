

# import random
# prizes = ['trophy','stuffed animal','money','candy','vacation']
# print(random.sample(prizes,2))









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