# coding=utf-8
# The nui package provides interactions with the Kinect cameras including skeleton tracking,
# video camera, as well as the depth camera. [1]
import pygame
from pykinect import nui
# JointId provides skeleton information for us to manipulate them for our needs.
from pykinect.nui import JointId
# itertools are used in the “draw_skeleton_data” method. “itertool.islice” selectively prints the
# values mentioned in its iterable container passed as an argument.
import itertools
# Required for skeleton coloring
from pygame.color import THECOLORS
import sys
from pygame import mixer

# Skeleton Start
from Item import Item

# Screen
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

isCurled = False

SKELETON_COLORS = [THECOLORS["red"],
                   THECOLORS["blue"],
                   THECOLORS["green"],
                   THECOLORS["orange"],
                   THECOLORS["purple"],
                   THECOLORS["violet"]]

LEFT_ARM = (JointId.ShoulderCenter,
            JointId.ShoulderLeft,
            JointId.ElbowLeft,
            JointId.WristLeft,
            JointId.HandLeft)
RIGHT_ARM = (JointId.ShoulderCenter,
             JointId.ShoulderRight,
             JointId.ElbowRight,
             JointId.WristRight,
             JointId.HandRight)
LEFT_LEG = (JointId.HipCenter,
            JointId.HipLeft,
            JointId.KneeLeft,
            JointId.AnkleLeft,
            JointId.FootLeft)
RIGHT_LEG = (JointId.HipCenter,
             JointId.HipRight,
             JointId.KneeRight,
             JointId.AnkleRight,
             JointId.FootRight)
SPINE = (JointId.HipCenter,
         JointId.Spine,
         JointId.ShoulderCenter,
         JointId.Head)

skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image


def draw_skeleton_data(pSkelton, index, positions, width=4):
    start = pSkelton.SkeletonPositions[positions[0]]

    for position in itertools.islice(positions, 1, None):
        next = pSkelton.SkeletonPositions[position.value]

        curstart = skeleton_to_depth_image(start, window_size[0], window_size[1])
        curend = skeleton_to_depth_image(next, window_size[0], window_size[1])

        pygame.draw.line(window, SKELETON_COLORS[index], curstart, curend, width)

        start = next


def draw_skeletons(skeletons):
    distance_min = 1000000
    index = -1
    for i, data in enumerate(skeletons):
        hip = data.SkeletonPositions[JointId.HipCenter]
        distance = (hip.x * hip.x) + (hip.y * hip.y) + (hip.z * hip.z)
        if (distance > 0) and (distance < distance_min):
            distance_min = distance
            index = i

    if index >= 0:
        data = skeletons[index]
        # draw the Head
        HeadPos = skeleton_to_depth_image(data.SkeletonPositions[JointId.Head], window_size[0], window_size[1])
        draw_skeleton_data(data, index, SPINE, 10)
        pygame.draw.circle(window, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)

        # drawing the limbs
        draw_skeleton_data(data, index, LEFT_ARM)
        draw_skeleton_data(data, index, RIGHT_ARM)
        draw_skeleton_data(data, index, LEFT_LEG)
        draw_skeleton_data(data, index, RIGHT_LEG)


def video_frame_ready(frame):
    frame.image.copy_bits(window._pixels_address)
    draw_skeletons(skeletons)
    pygame.display.update()


def post_frame(frame):
    try:
        pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons=frame.SkeletonData))
    except:
        # event queue full
        pass


# Skeleton End
def takeObjectWithRightHandOnCollision(item, rightHandCoords):
    if item.isCollidingOnCoords(rightHandCoords):
        item.setIsHolding(True)


def isDumbbellCurled(rightHandCoords, rightShoulderCoords):
    # when the player's right hand is above player's shoulders, it is in curled position
    if rightHandCoords[1] < rightShoulderCoords[1]:
        return True
    else:
        return False


def showScore(x, y):
    score = scoreFont.render("Total Volume :" + str(scoreVal), True, (0, 0, 0))
    window.blit(score, (x, y))


if __name__ == '__main__':

    # Screen Settings
    window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    window = pygame.display.set_mode(window_size)
    KINECTEVENT = pygame.USEREVENT

    skeletons = []

    # some other methods

    pygame.init()

    mixer.init()

    #Provided to YouTube by TuneCore
    #
    # Curl Muthafucka · Kali Muscle
    #
    # Money & Muscle
    #
    # ℗ 2015 Sounds So Digital LLC
    #
    # Released on: 2015-07-03
    #Creator : https://www.youtube.com/watch?v=B0Ld-kGI1_E

    #I DO NOT OWN THIS SONG. THIS PROJECT IS NOT MONETIZED.
    #YOU CAN CONTACT ME VIA contact@muratkirlioglu.com IF YOU HAVE ANY REQUEST.
    mixer.music.load('Music/CurlMuthafucka.wav')
    mixer.music.set_volume(1)
    mixer.music.play(-1)

    clock = pygame.time.Clock()

    # Score
    scoreVal = 0
    isScoreAdded = False
    scoreFont = pygame.font.Font('freesansbold.ttf', 32)
    scoreTextX = 0
    scoreTextY = 10

    # Dumbbell object
    dumbbell = Item('Objects/dumbbell.png', 100, 500)

    # Game loop start
    with nui.Runtime() as kinect:

        # standard initialization for kinect
        kinect.skeleton_engine.enabled = True
        kinect.video_frame_ready += video_frame_ready
        kinect.skeleton_frame_ready += post_frame

        window.fill((250, 250, 250))
        pygame.display.update()


        # game loop
        while True:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # enters when kinect detects the player
                elif event.type == KINECTEVENT:
                    skeletons = event.skeletons
                    window.fill((250, 250, 250))

                    # DRAW GAME OBJECTS HERE
                    # draws the skeletons
                    draw_skeletons(skeletons)
                    for skeleton in skeletons:
                        if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:
                            # holds the player’s joint data.
                            leftHand = skeleton.SkeletonPositions[JointId.HandLeft]
                            rightHand = skeleton.SkeletonPositions[JointId.HandRight]
                            rightWrist = skeleton.SkeletonPositions[JointId.WristRight]
                            head = skeleton.SkeletonPositions[JointId.Head]
                            rightElbow = skeleton.SkeletonPositions[JointId.ElbowRight]
                            rightShoulder = skeleton.SkeletonPositions[JointId.ShoulderRight]

                            # these are the coordinates you need to use instead of mouse/keyboard movements.
                            leftHandCoords = skeleton_to_depth_image(leftHand, window_size[0], window_size[1])
                            rightHandCoords = skeleton_to_depth_image(rightHand, window_size[0], window_size[1])
                            rightWristCoords = skeleton_to_depth_image(rightWrist, window_size[0], window_size[1])
                            headCoords = skeleton_to_depth_image(head, window_size[0], window_size[1])
                            rightElbowCoords = skeleton_to_depth_image(rightElbow, window_size[0], window_size[1])
                            rightShoulderCoords = skeleton_to_depth_image(rightShoulder, window_size[0], window_size[1])

                            # OTHER METHODS/FUNCTIONS

                            takeObjectWithRightHandOnCollision(dumbbell, rightHandCoords)

                            if (dumbbell.isHolding):
                                dumbbell.setPosition(rightHandCoords[0] - 60, rightHandCoords[1] - 40)

                            isCurled = isDumbbellCurled(rightHandCoords, rightShoulderCoords)
                            if not isScoreAdded and isCurled:
                                scoreVal += 100
                                isScoreAdded = True
                            if not isCurled:
                                isScoreAdded = False

            showScore(scoreTextX, scoreTextY)
            window.blit(dumbbell.getImage(), dumbbell.getRect())
            pygame.display.update()

# Game loop end
