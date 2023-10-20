import pygame, math, os
from pygame import gfxdraw
from pytexit import py2tex
import webbrowser

def init():
    #### INPUT ####
    screen.fill(colors[th]["bg"])
    drawBissec(thickness["bissec"])
    xAxisOff = (input_origin[1] if abs(input_origin[1]) <= input_scale[1]/2 else None)
    yAxisOff = (input_origin[0] if abs(input_origin[0]) <= input_scale[0]/2 else None)
    #print(xAxisOff, yAxisOff)
    drawGrid(xAxisOff, yAxisOff)
    drawAxis(xAxisOff, yAxisOff)

    #### OUTPUT ####
    graph = pygame.Rect(input_size[0] + border_size[0], border_size[1], output_size[0], output_size[1])
    pygame.draw.rect(screen, colors[th]["rect"], graph)

def drawBissec(width):
    width = math.floor(width/2)
    for val_x in range(input_size[0]):
        x = val_x/input_size[0]*input_scale[0]-input_scale[0]/2+input_origin[0]
        val_y = x+input_origin[0]-input_origin[1]
        val_y = (val_y-input_origin[0]+input_scale[0]/2)/input_scale[0]*input_size[0]
        pygame.draw.line(screen, colors[th]["bissec"], (val_x, input_size[1]-val_y-1*width),(val_x, input_size[1]-val_y+1*(width+1)))

def drawGrid(xOff,yOff):
    for LineX in range(input_scale[0]+1):
        pygame.draw.line(screen, colors[th]["grid"], (LineX*(input_size[0]/input_scale[0]),0), (LineX*(input_size[0]/input_scale[0]),input_size[1]))
        val_x = text_font.render(str(int(LineX - input_scale[0] / 2 + input_origin[0])), True, colors[th]["text"])
        if xOff is not None:
            screen.blit(val_x, (LineX*(input_size[0]/input_scale[0]) -12,input_size[1]/2+xOff*input_size[1]/input_scale[1] +5))
        else:
            if input_origin[1] > input_scale[1]/2:
                screen.blit(val_x, (LineX*(input_size[0]/input_scale[0]) -12, input_size[1] -15))
            else:
                screen.blit(val_x, (LineX*(input_size[0]/input_scale[0]) -12, 5))

    for LineY in range(input_scale[1]+1):
        pygame.draw.line(screen, colors[th]["grid"], (0,LineY*(input_size[1]/input_scale[1])), (input_size[0],LineY*(input_size[1]/input_scale[1])))
        val_y = text_font.render(str(-int(LineY - input_scale[1] / 2 - input_origin[1])), True, colors[th]["text"])
        if yOff is not None:
            screen.blit(val_y, (input_size[0]/2-yOff*input_size[0]/input_scale[0] -12, LineY*(input_size[1]/input_scale[1]) +5))
        else:
            if input_origin[0] > input_scale[0]/2: #CH A GAUCHE
                screen.blit(val_y, (5, LineY*(input_size[1]/input_scale[1]) +5))
            else:
                screen.blit(val_y, (input_size[0]-12, LineY*(input_size[1]/input_scale[1]) +5))

def drawAxis(xOff,yOff):
    if xOff is not None:
        pygame.draw.line(screen, colors[th]["axes"], (0,input_size[1]/2+xOff*input_size[1]/input_scale[1]), (input_size[0],input_size[1]/2+xOff*input_size[1]/input_scale[1]))
    if yOff is not None:
        pygame.draw.line(screen, colors[th]["axes"], (input_size[0]/2-yOff*input_size[0]/input_scale[0],0), (input_size[0]/2-yOff*input_size[0]/input_scale[0],input_size[1]))

def update():
    #### INPUT ####
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = min(input_size[1],mouse_pos[0]),min(input_size[1],mouse_pos[1])

    global func, f, U0
    if fixed_U0:
        mouse_pos = fixed_U0
    else:
        U0 = (mouse_pos[0]/input_size[0]*input_scale[0]-input_scale[0]/2, -(mouse_pos[1]/input_size[1]*input_scale[1]-input_scale[1]/2))

    def func(x):
        try:
            value = f(x)
            defined = True
        except ZeroDivisionError:
            value = None
            defined = False
        except ValueError:
            value = None
            defined = False
        return defined, value

    imagesFunc = {}
    for val_x in range(input_size[0]):
        defined, val_y = func(val_x/input_size[0]*input_scale[0]-input_scale[0]/2)
        if defined and abs(val_y) <= input_scale[0]:
            imagesFunc[val_x] = int((-val_y+input_scale[0]/2)*input_size[0]/input_scale[0])
    keys = list(imagesFunc.keys())
    for i in range(len(imagesFunc)-1):
        if keys[i+1] - keys[i] == 1:
            pygame.draw.line(screen, colors[th]["func"], (keys[i],imagesFunc[keys[i]]), (keys[i+1],imagesFunc[keys[i+1]]))
            for dist in range(1,thickness["func"]+1):
                pygame.draw.line(screen, colors[th]["func"], (keys[i],imagesFunc[keys[i]]-1*dist), (keys[i+1],imagesFunc[keys[i+1]]-1*dist))
                pygame.draw.line(screen, colors[th]["func"], (keys[i],imagesFunc[keys[i]]+1*dist), (keys[i+1],imagesFunc[keys[i+1]]+1*dist))
                pygame.draw.line(screen, colors[th]["func"], (keys[i]-1*dist,imagesFunc[keys[i]]), (keys[i+1]-1*dist,imagesFunc[keys[i+1]]))
                pygame.draw.line(screen, colors[th]["func"], (keys[i]+1*dist,imagesFunc[keys[i]]), (keys[i+1]+1*dist,imagesFunc[keys[i+1]]))

    pygame.draw.line(screen, colors[th]["u0_line"], mouse_pos, (mouse_pos[0],input_size[1]/2))
    u0_text = text_font.render("U0", True, colors[th]["u0_line"])
    screen.blit(u0_text, (mouse_pos[0]-17,input_size[1]/2-13))

    prev_mirrored = (mouse_pos[0], input_size[1]/2)
    image, mirrored, defined = step(prev_mirrored[0])
    boundaries = lambda x: x[0] >= 0 and x[1] >= 0 and x[0] <= input_size[0] and x[1] <= input_size[1]
    i = 0
    if defined:
        while math.sqrt((image[0]-mirrored[0])**2+ (image[1]-mirrored[1])**2) > 3 and boundaries(image) and boundaries(mirrored):
            pygame.draw.line(screen, colors[th]["u1_line"], (int(prev_mirrored[0]),int(prev_mirrored[1])), (int(image[0]),int(image[1])))
            for dist in range(1,thickness["u1_line"]+1):
                pygame.draw.line(screen, colors[th]["u1_line"], (int(prev_mirrored[0])-1*dist,int(prev_mirrored[1])), (int(image[0])-1*dist,int(image[1])))
                pygame.draw.line(screen, colors[th]["u1_line"], (int(prev_mirrored[0])+1*dist,int(prev_mirrored[1])), (int(image[0])+1*dist,int(image[1])))

            pygame.draw.line(screen, colors[th]["u1_line"], (int(image[0]),int(image[1])), (int(mirrored[0]),int(mirrored[1])))
            for dist in range(1,thickness["u1_line"]+1):
                pygame.draw.line(screen, colors[th]["u1_line"], (int(image[0]),int(image[1])-1*dist), (int(mirrored[0]),int(mirrored[1])-1*dist))
                pygame.draw.line(screen, colors[th]["u1_line"], (int(image[0]),int(image[1])+1*dist), (int(mirrored[0]),int(mirrored[1])+1*dist))

            prev_mirrored = mirrored
            if i%input_pointerFreq == 0:
                pygame.draw.line(screen, colors[th]["pointer"], (image[0]-3,image[1]), (image[0]+3,image[1]))
                pygame.draw.line(screen, colors[th]["pointer"], (image[0],image[1]-3), (image[0],image[1]+3))
            i += 1
            image, mirrored,_ = step(prev_mirrored[0])

    pygame.draw.line(screen, colors[th]["pointer"], (mouse_pos[0]-5,mouse_pos[1]), (mouse_pos[0]+5,mouse_pos[1]))
    pygame.draw.line(screen, colors[th]["pointer"], (mouse_pos[0],mouse_pos[1]-5), (mouse_pos[0],mouse_pos[1]+5))

    #### OUTPUT ####
    first_y = [mouse_pos[0]/input_size[0]*input_scale[0]-input_scale[0]/2+input_origin[0]]
    for _ in range(1,15+1):
        defined, funcResult = func(first_y[-1]-input_origin[0])
        if not defined:
            break
        first_y.append(funcResult+input_origin[1])
    if defined:
        output_scale = [max(first_y),min(first_y)]
        if output_scale[0] != output_scale[1]:
            for i in range(len(first_y)):
                x, y = input_size[0]+border_size[0]+int(output_size[0]/15*i), border_size[1]+output_size[1]-(first_y[i]-output_scale[1])/(output_scale[0]-output_scale[1])*output_size[1]
                pygame.draw.line(screen, colors[th]["u1_line"], (x-5, y), (x+5, y))
                pygame.draw.line(screen, colors[th]["u1_line"], (x, y-5), (x, y+5))
                u_text = text_font.render("U"+str(i), True, colors[th]["u0_line"])
                screen.blit(u_text, (x-17,y+2))
                u_text = text_font.render(str(round(first_y[i],3)), True, colors[th]["outputText"])
                screen.blit(u_text, (x-10,y+13))

def step(pos):
    global func, input_size, input_scale
    if pos > input_size[0]:
        print("error")
        return (pos,pos)
    else:
        defined, funcResult = func(pos/input_size[0]*input_scale[0]-input_scale[0]/2)
        if defined:
            image = (pos,(-funcResult+input_scale[0]/2)*input_size[0]/input_scale[0])
            mirrored = (min(input_size[0]/2+input_size[1]/2-image[1], input_size[0]) -input_origin[0]*(input_size[0]/input_scale[0]), image[1])
            return image, mirrored, True
        else:
            return None, None, False

func = lambda x: x
stringF = "1/8*(x+2)*(11-2*x)" #"x/math.sqrt(x+4) +2"
fEval = lambda x: eval(stringF)
f = lambda x: fEval(x+input_origin[0])-input_origin[1]
size = (1300,501)
input_size = (500,500)
input_scale = (8, 8)
input_origin = (0, 0)
input_pointerFreq = 1 # number of skipped crosses  (1 is min)
border_size = (20,30)
output_size = (size[0]-input_size[0]-2*border_size[0], size[1]-2*border_size[1])
U0 = (-34/10, -31/10)

fixed_U0 = [None, (lambda x,y : [input_size[0]/input_scale[0]*(x+input_scale[0]/2-input_origin[0]),input_size[1]/input_scale[1]*(-y+input_scale[1]/2+input_origin[1])])(U0[0],U0[1])][0]
thickness = {
    "func" : 1,
    "bissec" : 1,
    "u1_line" : 1,
}
th = ["light","dark"][1]

colors = {
    "light" : {
        "bg" : (255,255,255),
        "axes" : (50,50,50),
        "bissec" : (118,120,237),
        "grid" : (150,150,150),
        "text" : (0,0,0),
        "rect" : (230,230,230),
        "func" : (243,91,4),
        "u0_line" : (243,91,4),
        "u1_line" : (241,152,41),
        "pointer" : (0,0,0),
        "outputText" : (50,50,50)
    },
    "dark" : {
        "bg" : (0,0,0),
        "axes" : (100,100,100),
        "bissec" : (118,120,237),
        "grid" : (50,50,50),
        "text" : (150,150,150),
        "rect" : (50,50,50),
        "func" : (243,91,4),
        "u0_line" : (243,91,4),
        "u1_line" : (241,135,1),
        "pointer" : (255,255,255),
        "outputText" : (200,200,200)
    }
}

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Un+1 = f(Un)')
pygame.font.init()
text_font = pygame.font.SysFont(None, 20)

if input_scale[0]%2 == 1 or input_scale[1]%2 == 1:
    input_scale_oldRef = input_scale
    input_scale = (input_scale[0] + input_scale[0] % 2, input_scale[1] + input_scale[1] % 2)
    print(f'WARNING : input scale {input_scale_oldRef} -> {input_scale}')

running = True
while running:
    init()
    update()

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    KeysPressed = pygame.key.get_pressed()
    if KeysPressed[pygame.K_p] == 1:
        th = ["light","dark"][0]
        init();update()
        pygame.image.save(screen, "image.jpg")
        running = False
        with open("index.html","r") as htmlPage:
            lines = htmlPage.readlines()
            lines[17] = "      f(x) = "+ py2tex(stringF,print_formula=False,print_latex=False)[2:-2] +" \;\;\; u_{n+1} = f(u_n) \;\;\; u_0 = "+ str(round(U0[0],2)) +" \n"
        with open("index.html","w+") as htmlPage:
            htmlPage.write("".join(lines))
        webbrowser.open_new_tab("file://"+os.path.realpath("index.html"))