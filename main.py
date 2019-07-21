import pygame

# Supporting Classes


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_display(text, color, x, y, size):
    largeText = pygame.font.SysFont('arial', size)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = (x, y)
    dashDisplay.blit(TextSurf, TextRect)

class CoolantBar:
    def __init__(self, start_coolantSize, minV, maxV):
        self.coolantSize = start_coolantSize
        self.barWidth = start_coolantSize[2]-1.3*start_coolantSize[2]/20
        self.x = start_coolantSize[0] + start_coolantSize[2]/20
        self.y = start_coolantSize[1] +start_coolantSize[3]/40
        self.maxHeight = start_coolantSize[3] - 2*start_coolantSize[3]/20
        self.minV = minV
        self.maxV = maxV

    def draw(self, value):
        pygame.draw.rect(dashDisplay, coolantBackground, coolantSize)
        if value > self.maxV:
            value = self.maxV
        value = value - self.minV
        barHeight = value * self.maxHeight/self.maxV
        pygame.draw.rect(dashDisplay, (255, 0, 0), [self.x, self.y+self.maxHeight+5, self.barWidth, 5])
        pygame.draw.rect(dashDisplay, (255, 0, 0), [self.x, self.y*2-barHeight, self.barWidth, barHeight])

class RPMBar:
    def __init__(self, start_rpmSize):
        self.rpmSize = start_rpmSize
        self.maxRPMs = 10000
        # NEEDS to be even
        self.maxBoxes = 12
        self.boxes = []
        self.x = rpmSize[0] + rpmSize[2] / 48
        self.y = rpmSize[1] + rpmSize[3] / 14

        self.widths = rpmSize[2]/self.maxBoxes - rpmSize[2]/44
        self.heights = rpmSize[3] - 2*rpmSize[3]/14

        self.createBoxes()

    def createBoxes(self):
        nextX = self.x
        nextY = self.y
        green = 255
        red = 0
        yellow = False
        for i in range(self.maxBoxes):
            self.boxes.append(Box(nextX, nextY, self.widths, self.heights, (red, green, 0)))
            nextX += self.widths + self.x
            if red == 255:
                yellow = True
            if not yellow:
                red += (255/(self.maxBoxes/2))
            else:
                green -= (255/(self.maxBoxes/2))

    def draw(self, rpm):
        pygame.draw.rect(dashDisplay, rpmBackground, rpmSize)
        j = 1
        for element in self.boxes:
            rpm_compare = (self.maxRPMs/self.maxBoxes)*j
            if rpm >= rpm_compare:
                element.draw()
            j += 1


class Box:

    def __init__(self, start_x, start_y, start_width, start_height, start_color):
        self.x = start_x
        self.y = start_y
        self.width = start_width
        self.height = start_height
        self.color = start_color

    def draw(self):
        pygame.draw.rect(dashDisplay, self.color, [self.x, self.y, self.width, self.height])


# parameters

display_width = 480
display_height = 300

# colors
backgroundColor = (0, 0, 0)
rpmBackground = (255, 255, 255)
gearBackground = (255, 255, 255)
speedBackground = (0, 0, 0)
coolantBackground = (255, 255, 255)

# sizes
rpmSize = [0, 0, 480, 100]
coolantSize = [400, 140, 75, 150]

pygame.init()

# set up display
# dashDisplay = pygame.display.set_mode((display_width, display_height, 600), pygame.FULLSCREEN)
dashDisplay = pygame.display.set_mode((display_width, display_height))
dashDisplay.fill(backgroundColor)
pygame.display.set_caption('Dashboard UTR-25')
clock = pygame.time.Clock()

dRPMbar = RPMBar(rpmSize)
dCoolantBar = CoolantBar(coolantSize, 0, 10000)

mainLoop = True
rpm = 0
increase = True

while mainLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False

    # reDraw
    dashDisplay.fill(backgroundColor)
    if increase:
        rpm += 70
        if rpm > 13000:
            increase = False
    else:
        rpm -= 70
        if rpm < 50:
            increase = True
    dRPMbar.draw(rpm)
    dCoolantBar.draw(rpm)

    # test values
    rpm2 = str(rpm/1000)
    rpm2 = list(rpm2)
    rpm2 = rpm2[0] + rpm2[1] + rpm2[2]
    mph = int(rpm/100)
    gearTest = int(rpm*4/10000)
    # straight adds
    # RPM/MPH
    pygame.draw.rect(dashDisplay, (255, 255, 255), [10, 110, 135, 180])
    # Gear
    pygame.draw.rect(dashDisplay, (255, 255, 255), [170, 110, 125, 125])

    message_display('Gear', (0, 0, 0), 233, 125, 34)
    message_display('RPM:', (0, 0, 0,), 45, 130, 32)
    message_display('MPH:', (0, 0, 0,), 45, 210, 32)
    message_display(str(rpm), (0, 0, 0), 240, 50, 70)
    message_display(str(rpm2), (0, 0, 0), 100, 170, 55)
    message_display(str(mph), (0, 0, 0), 75, 260, 55)
    message_display(str(gearTest), (0, 0, 0), 233, 185, 105)
    pygame.display.update()
    clock.tick(30)


pygame.quit()
quit()
