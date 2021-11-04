cube = ["WWWWWWWWW","OOOOOOOOO","GGGGGGGGG","RRRRRRRRR","BBBBBBBBB","YYYYYYYYY"]

def rotate(face):
    tempcorner = face[6]
    tempedge = face[3]
    face = face[:6] + face[8] + face[7:]
    face = face[:3] + face[7] + face[4:] 
    face = face[:8] + face[2] + face[9:]
    face = face[:7] + face[5] + face[8:]
    face = face[:2] + face[0] + face[3:]
    face = face[:5] + face[1] + face[6:]
    face = face[:0] + tempcorner + face[1:]
    face = face[:1] + tempedge + face[2:]
     
    return face                 

def move(turn):
    print("Doing turn: " + turn)
    #U FACE
    if turn == "U" or turn == "U2" or turn == "U'":
        
        if turn == "U":
            num = 1
        elif turn == "U2":
            num = 2
        else:
            num = 3

        for i in range(num):

            temp = cube[1][0] + cube[1][1] + cube[1][2]

            for i in range(1,4):
                cube[i] = cube[i][:0] + cube[i+1][0] + cube[i][1:]
                cube[i] = cube[i][:1] + cube[i+1][1] + cube[i][2:]
                cube[i] = cube[i][:2] + cube[i+1][2] + cube[i][3:]

            cube[4] = cube[4][:0] + temp[0] + cube[4][1:]
            cube[4] = cube[4][:1] + temp[1] + cube[4][2:]
            cube[4] = cube[4][:2] + temp[2] + cube[4][3:]
    
            cube[0] = rotate(cube[0])

    #F FACE
    if turn == "F" or turn == "F2" or turn == "F'":
        
        if turn == "F":
            num = 1
        elif turn == "F2":
            num = 2
        else:
            num = 3

        for i in range(num):

            temp = cube[0][6] + cube[0][7] + cube[0][8]
            
            #white
            cube[0] = cube[0][:6] + cube[1][8] + cube[0][7:]
            cube[0] = cube[0][:7] + cube[1][5] + cube[0][8:]
            cube[0] = cube[0][:8] + cube[1][2] + cube[0][9:]

            #orange
            cube[1] = cube[1][:2] + cube[5][0] + cube[1][3:]
            cube[1] = cube[1][:5] + cube[5][1] + cube[1][6:]
            cube[1] = cube[1][:8] + cube[5][2] + cube[1][9:]
    
            #yellow
            cube[5] = cube[5][:0] + cube[3][6] + cube[5][1:]
            cube[5] = cube[5][:1] + cube[3][3] + cube[5][2:]
            cube[5] = cube[5][:2] + cube[3][0] + cube[5][3:]
    
            #red
            cube[3] = cube[3][:0] + temp[0] + cube[3][1:]
            cube[3] = cube[3][:3] + temp[1] + cube[3][4:]
            cube[3] = cube[3][:6] + temp[2] + cube[3][7:]
            
            cube[2] = rotate(cube[2])





def draw(cube):
    textimage = [[ " ", " ", " ", cube[0][0], cube[0][1], cube[0][2], " ", " ", " ", " ", " ", " "], \
                 [ " ", " ", " ", cube[0][3], cube[0][4], cube[0][5], " ", " ", " ", " ", " ", " "], \
                 [ " ", " ", " ", cube[0][6], cube[0][7], cube[0][8], " ", " ", " ", " ", " ", " "], \
                 [ cube[1][0], cube[1][1], cube[1][2], cube[2][0], cube[2][1], cube[2][2],cube[3][0], cube[3][1], cube[3][2],cube[4][0], cube[4][1], cube[4][2]], \
                 [ cube[1][3], cube[1][4], cube[1][5], cube[2][3], cube[2][4], cube[2][5],cube[3][3], cube[3][4], cube[3][5],cube[4][3], cube[4][4], cube[4][5]], \
                 [ cube[1][6], cube[1][7], cube[1][8], cube[2][6], cube[2][7], cube[2][8],cube[3][6], cube[3][7], cube[3][8],cube[4][6], cube[4][7], cube[4][8]], \
                 [ " ", " ", " ", cube[5][0], cube[5][1], cube[5][2], " ", " ", " ", " ", " ", " "], \
                 [ " ", " ", " ", cube[5][3], cube[5][4], cube[5][5], " ", " ", " ", " ", " ", " "], \
                 [ " ", " ", " ", cube[5][6], cube[5][7], cube[5][8], " ", " ", " ", " ", " ", " "]]
    for i in range(9):
        print(textimage[i])

scramble = "" 

draw(cube)
move("U'")
draw(cube)
move("F")
draw(cube)
move("U'")
draw(cube)
move("F'")
draw(cube)
move("U2")
draw(cube)
