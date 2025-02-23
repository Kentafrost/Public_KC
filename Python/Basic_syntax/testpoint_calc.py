def calc(name, point):
    if point >= 90:
        grade = "A"
    elif point >= 80:
        grade = "B"
    elif point >= 70:
        grade = "C"
    elif point >= 60:
        grade = "D"
    else:
        grade = "F"
    MSG = "Students name: " + name + " your point: " + str(point) + " your grade: " + grade
    
    return MSG