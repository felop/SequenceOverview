import pygame, math
from pygame import gfxdraw

def init():
    screen.fill(colors[th]["bg"])

    pygame.draw.line(screen, colors[th]["bissec"], (input_size[0],0), (0,input_size[1]))
    for dist in range(1,thickness["bissec"]+1):
        pygame.draw.line(screen, colors[th]["bissec"], (input_size[0]-1*dist,0), (0,input_size[1]-1*dist))
        pygame.draw.line(screen, colors[th]["bissec"], (input_size[0],dist), (0,input_size[1]+1*dist))

    for LineX in range(input_scale[0]+1):
        pygame.draw.line(screen, colors[th]["grid"], (LineX*(input_size[0]/input_scale[0]),0), (LineX*(input_size[0]/input_scale[0]),input_size[1]))
        if LineX <= input_scale[0]:
            val_x = text_font.render(str(int(LineX-input_scale[0]/2)), True, colors[th]["text"])
            screen.blit(val_x, (LineX*(input_size[0]/input_scale[0]) -12,input_size[1]/2 +5))

    for LineY in range(input_scale[1]+1):
        pygame.draw.line(screen, colors[th]["grid"], (0,LineY*(input_size[1]/input_scale[1])), (input_size[0],LineY*(input_size[1]/input_scale[1])))
        if LineY <= input_scale[1]:
            val_y = text_font.render(str(-int(LineY-input_scale[1]/2)), True, colors[th]["text"])
            screen.blit(val_y, (input_size[0]/2 -12, LineY*(input_size[1]/input_scale[1]) +5))

    pygame.draw.line(screen, colors[th]["axes"], (input_size[0]/2,0), (input_size[0]/2,input_size[1]))
    pygame.draw.line(screen, colors[th]["axes"], (0,input_size[1]/2), (input_size[0],input_size[1]/2))

    #### OUTPUT ####
    graph = pygame.Rect(input_size[0]+border_size[0], border_size[1], output_size[0], output_size[1])
    pygame.draw.rect(screen, colors[th]["rect"], graph)

def update():
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = min(input_size[1],mouse_pos[0]),min(input_size[1],mouse_pos[1])
    if fixed_U0:
        mouse_pos = fixed_U0

    global func
    def func(x):
        f = lambda x: 9/(6-x)#-1.1*x-2
        try:
            value = f(x)#-f(0)
            defined = True
        except ZeroDivisionError:
            value = None
            defined = False
        except ValueError:
            value = None
            defined = False
        return defined, value

    for val_x in range(input_size[0]):
        defined, val_y = func(val_x/input_size[0]*input_scale[0]-input_scale[0]/2)
        if defined:
            pygame.gfxdraw.pixel(screen, val_x, int((-val_y+input_scale[0]/2)*input_size[0]/input_scale[0]), colors[th]["func"])
            for dist in range(1,thickness["func"]+1):
                pygame.gfxdraw.pixel(screen, val_x, int((-val_y+input_scale[0]/2)*input_size[0]/input_scale[0])-1*dist, colors[th]["func"])
                pygame.gfxdraw.pixel(screen, val_x, int((-val_y+input_scale[0]/2)*input_size[0]/input_scale[0])+1*dist, colors[th]["func"])

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
            pygame.draw.line(screen, colors[th]["u1_line"], (int(image[0]),int(image[1])), (int(mirrored[0]),int(mirrored[1])))
            prev_mirrored = mirrored
            if i == 0:
                pygame.draw.line(screen, colors[th]["pointer"], (image[0]-3,image[1]), (image[0]+3,image[1]))
                pygame.draw.line(screen, colors[th]["pointer"], (image[0],image[1]-3), (image[0],image[1]+3))
            i += 1
            image, mirrored,_ = step(prev_mirrored[0])

    pygame.draw.line(screen, colors[th]["pointer"], (mouse_pos[0]-5,mouse_pos[1]), (mouse_pos[0]+5,mouse_pos[1]))
    pygame.draw.line(screen, colors[th]["pointer"], (mouse_pos[0],mouse_pos[1]-5), (mouse_pos[0],mouse_pos[1]+5))

    #### OUTPUT ####

    first_images = [mouse_pos[0]/input_size[0]*input_scale[0]-input_scale[0]/2]
    for _ in range(1,15+1):
        defined, funcResult = func(first_images[-1])
        if not defined:
            break
        first_images.append(funcResult)
    if defined:
        output_scale = [max(first_images),min(first_images)]
        if output_scale[0] != output_scale[1]:
            for i in range(len(first_images)):
                x, y = input_size[0]+border_size[0]+int(output_size[0]/15*i), border_size[1]+output_size[1]-(first_images[i]-output_scale[1])/(output_scale[0]-output_scale[1])*output_size[1]
                pygame.draw.line(screen, colors[th]["u1_line"], (x-5, y), (x+5, y))
                pygame.draw.line(screen, colors[th]["u1_line"], (x, y-5), (x, y+5))
                u_text = text_font.render("U"+str(i), True, colors[th]["u0_line"])
                screen.blit(u_text, (x-17,y+2))
                u_text = text_font.render(str(round(first_images[i],3)), True, colors[th]["outputText"])
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
            mirrored = (min(input_size[0]/2 + input_size[1]/2-image[1], input_size[0]),image[1])
            return image, mirrored, True
        else:
            return None, None, False

func = lambda x: x
size = (1300,501)
input_size = (500,500)
input_scale = (8,8)
border_size = (20,30)
output_size = (size[0]-input_size[0]-2*border_size[0], size[1]-2*border_size[1])
fixed_U0 = [None, (lambda x,y : [input_size[0]/input_scale[0]*(x+input_scale[0]/2),input_size[1]/input_scale[1]*(-y+input_scale[1]/2)])(-1,-2)][1]
thickness = {
    "func" : 0,
    "bissec" : 1,
}
th = ["light","dark"][1]

colors = {
    "light" : {
        "bg" : (255,255,255),
        "axes" : (0,150,0),
        "bissec" : (20,190,20),
        "grid" : (150,150,150),
        "text" : (0,0,0),
        "rect" : (230,230,230),
        "func" : (0,200,200),
        "u0_line" : (255,150,50),
        "u1_line" : (200,60,60),
        "pointer" : (0,0,0),
        "outputText" : (50,50,50)
    },
    "dark" : {
        "bg" : (0,0,0),
        "axes" : (100,255,0),
        "bissec" : (40,130,0),
        "grid" : (50,50,50),
        "text" : (150,150,150),
        "rect" : (50,50,50),
        "func" : (100,255,255),
        "u0_line" : (255,150,50),
        "u1_line" : (255,100,100),
        "pointer" : (255,255,255),
        "outputText" : (200,200,200)
    }
}

screen = pygame.display.set_mode(size)
pygame.display.set_caption('(Un ; Un+1)')
pygame.font.init()
text_font = pygame.font.SysFont(None, 20)

running = True
while running:
    init()
    update()

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
