from PIL import Image, ImageColor

cube = [["W","W","W","W","W","W","W","W","W"],\
        ["O","O","O","O","O","O","O","O","O"],\
        ["G","G","G","G","G","G","G","G","G"],\
        ["R","R","R","R","R","R","R","R","R"],\
        ["B","B","B","B","B","B","B","B","B"],\
        ["Y","Y","Y","Y","Y","Y","Y","Y","Y"]]

     
def rotate(face):
    
    tempcorner = face[6]
    tempedge = face[3]
    
    face[6] = face[8]
    face[3] = face[7]
    face[8] = face[2] 
    face[7] = face[5] 
    face[2] = face[0] 
    face[5] = face[1] 
    
    face[0] = tempcorner 
    face[1] = tempedge 
     
    return face                 

def move(turn):

    #print("Doing turn: " + turn)

    #U FACE
    if turn == "U" or turn == "U2" or turn == "U'":
        
        if turn == "U":
            num = 1
        elif turn == "U2":
            num = 2
        else:
            num = 3

        for i in range(num):

            temp = [cube[1][0],cube[1][1],cube[1][2]]

            cube[1][0] = cube[2][0]
            cube[1][1] = cube[2][1] 
            cube[1][2] = cube[2][2]
 
            cube[2][0] = cube[3][0]
            cube[2][1] = cube[3][1] 
            cube[2][2] = cube[3][2]
            
            cube[3][0] = cube[4][0]
            cube[3][1] = cube[4][1] 
            cube[3][2] = cube[4][2]

            cube[4][0] = temp[0]
            cube[4][1] = temp[1]
            cube[4][2] = temp[2]
    
            #rotate white
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

            temp = [cube[0][6],cube[0][7],cube[0][8]]
            
            #white
            cube[0][6] = cube[1][8]
            cube[0][7] = cube[1][5]
            cube[0][8] = cube[1][2]

            #orange
            cube[1][2] = cube[5][0]
            cube[1][5] = cube[5][1]
            cube[1][8] = cube[5][2]
    
            #yellow
            cube[5][0] = cube[3][6]
            cube[5][1] = cube[3][3]
            cube[5][2] = cube[3][0]
    
            #red
            cube[3][0] = temp[0]
            cube[3][3] = temp[1]
            cube[3][6] = temp[2]
            
            #rotate green
            cube[2] = rotate(cube[2])

    #D FACE
    if turn == "D" or turn == "D2" or turn == "D'":
        
        if turn == "D":
            num = 1
        elif turn == "D2":
            num = 2
        else:
            num = 3

        for i in range(num):

            temp = [cube[1][6],cube[1][7], cube[1][8]]

            #orange
            cube[1][6] = cube[4][6] 
            cube[1][7] = cube[4][7]
            cube[1][8] = cube[4][8]

            #orange
            cube[4][6] = cube[3][6] 
            cube[4][7] = cube[3][7]
            cube[4][8] = cube[3][8]

            cube[3][6] = cube[2][6]
            cube[3][7] = cube[2][7]
            cube[3][8] = cube[2][8]

            cube[2][6] = temp[0]
            cube[2][7] = temp[1]
            cube[2][8] = temp[2]
            
            #rotate yellow 
            cube[5] = rotate(cube[5])

    #B FACE
    if turn == "B" or turn == "B2" or turn == "B'":
        
        if turn == "B":
            num = 1
        elif turn == "B2":
            num = 2
        else:
            num = 3

        for i in range(num):

            temp = [cube[0][0],cube[0][1],cube[0][2]]
            
            #white
            cube[0][0] = cube[3][2]
            cube[0][1] = cube[3][5]
            cube[0][2] = cube[3][8]
        
            #red
            cube[3][2] = cube[5][8]
            cube[3][5] = cube[5][7]
            cube[3][8] = cube[5][6]

            #yellow
            cube[5][6] = cube[1][0]
            cube[5][7] = cube[1][3]
            cube[5][8] = cube[1][6]
        
            #orange
            cube[1][0] = temp[2]
            cube[1][3] = temp[1]
            cube[1][6] = temp[0]
            
            #rotate blue
            cube[4] = rotate(cube[4])
    
    #L FACE
    if turn == "L" or turn == "L2" or turn == "L'":
        
        if turn == "L":
            num = 1
        elif turn == "L2":
            num = 2
        else:
            num = 3

        for i in range(num):

            temp = [cube[5][0],cube[5][3], cube[5][6]]

            #yellow
            cube[5][0] = cube[2][0]
            cube[5][3] = cube[2][3]
            cube[5][6] = cube[2][6]

            #green
            cube[2][0] = cube[0][0]
            cube[2][3] = cube[0][3]
            cube[2][6] = cube[0][6]
    
            #white
            cube[0][0] = cube[4][8]
            cube[0][3] = cube[4][5]
            cube[0][6] = cube[4][2]
    
            #blue
            cube[4][2] = temp[2]
            cube[4][5] = temp[1]
            cube[4][8] = temp[0]
           
            #rotate red 
            cube[1] = rotate(cube[1])
    
    #R FACE
    if turn == "R" or turn == "R2" or turn == "R'":
        
        if turn == "R":
            num = 1
        elif turn == "R2":
            num = 2
        else:
            num = 3

        for i in range(num):

            temp = [cube[0][2],cube[0][5], cube[0][8]]

            #white
            cube[0][2] = cube[2][2]
            cube[0][5] = cube[2][5]
            cube[0][8] = cube[2][8]

            #green
            cube[2][2] = cube[5][2]
            cube[2][5] = cube[5][5]
            cube[2][8] = cube[5][8]
    
            #yellow
            cube[5][2] = cube[4][6]
            cube[5][5] = cube[4][3]
            cube[5][8] = cube[4][0]
    
            #blue
            cube[4][6] = temp[0]
            cube[4][3] = temp[1]
            cube[4][0] = temp[2]
           
            #rotate red 
            cube[3] = rotate(cube[3])

def draw(cube):
    
    img2 = Image.new('RGB', (120,90), color = 'black')

    textimage = [[ " ", " ", " ", cube[0][0], cube[0][1], cube[0][2], " ", " ", " ", " ", " ", " "], \
                 [ " ", " ", " ", cube[0][3], cube[0][4], cube[0][5], " ", " ", " ", " ", " ", " "], \
                 [ " ", " ", " ", cube[0][6], cube[0][7], cube[0][8], " ", " ", " ", " ", " ", " "], \
                 [ cube[1][0], cube[1][1], cube[1][2], cube[2][0], cube[2][1], cube[2][2],cube[3][0], cube[3][1], cube[3][2],cube[4][0], cube[4][1], cube[4][2]], \
                 [ cube[1][3], cube[1][4], cube[1][5], cube[2][3], cube[2][4], cube[2][5],cube[3][3], cube[3][4], cube[3][5],cube[4][3], cube[4][4], cube[4][5]], \
                 [ cube[1][6], cube[1][7], cube[1][8], cube[2][6], cube[2][7], cube[2][8],cube[3][6], cube[3][7], cube[3][8],cube[4][6], cube[4][7], cube[4][8]], \
                 [ " ", " ", " ", cube[5][0], cube[5][1], cube[5][2], " ", " ", " ", " ", " ", " "], \
                 [ " ", " ", " ", cube[5][3], cube[5][4], cube[5][5], " ", " ", " ", " ", " ", " "], \
                 [ " ", " ", " ", cube[5][6], cube[5][7], cube[5][8], " ", " ", " ", " ", " ", " "]]
    for i in range(1,10):
        for j in range(1,13):
            if textimage[i-1][j-1] == "W":
                color = ImageColor.getrgb("white")
                print(str(j) + ":" + str(i))
                for k in range(10):
                    for l in range(10):
                        img2.putpixel((((j*10)-10)+k,((i*10)-10)+l), color) 
            if textimage[i-1][j-1] == "Y":
                color = ImageColor.getrgb("yellow")
                for k in range(10): 
                     for l in range(10):
                        img2.putpixel((((j*10)-10)+k,((i*10)-10)+l), color)
            if textimage[i-1][j-1] == "R":
                color = ImageColor.getrgb("red")
                for k in range(10):
                     for l in range(10):
                        img2.putpixel((((j*10)-10)+k,((i*10)-10)+l), color)
            if textimage[i-1][j-1] == "O":
                color = ImageColor.getrgb("orange")
                for k in range(10):              
                     for l in range(10):
                        img2.putpixel((((j*10)-10)+k,((i*10)-10)+l), color)
            if textimage[i-1][j-1] == "B":
                color = ImageColor.getrgb("blue")
                for k in range(10):
                     for l in range(10):
                        img2.putpixel((((j*10)-10)+k,((i*10)-10)+l), color)
            if textimage[i-1][j-1] == "G":
                color = ImageColor.getrgb("green")
                for k in range(10):
                     for l in range(10):
                        img2.putpixel((((j*10)-10)+k,((i*10)-10)+l), color)
    
    img2.save('cubelarge.gif')


#scramble = "R2 U R' U2 B' L F2 L' B2 F' R D2 U2 R2 B2 R2 B2 L' D' U L' B U2 R' U F' L B' R' U2"
#scramble = "R B' R2 F D L' R F U R U2 R D' U L R2 D B2 F D' R2 B' F U B2 F2 D2 R' U L"


scramble = input("Enter your scramble:") 

splitScramble = scramble.split()

for i in range(len(splitScramble)):
    move(splitScramble[i])
    draw(cube)

print("Scrambled image saved in \"cube.gif\"")
