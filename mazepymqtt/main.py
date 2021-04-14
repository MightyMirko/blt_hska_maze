
from mazelib import *
from mazelib.generate.Prims import Prims
from mazelib.generate.HuntAndKill import HuntAndKill
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt



class Player():
    x = 0
    y = 0
    lastPos =[]
    pos =[]
    def __init__(self,start):
        self.y = start[0]
        self.x = start[1]
        plpos= [self.x,self.y]
    #
    # def walk(self,k):
    #     self.lastPos=[self.x, self.y]
    #     if k == "u":
    #         self.y -= 1
    #     if k == "d":
    #         self.y += 1
    #     if k == "l":
    #         self.x -= 1
    #     if k == "r":
    #         self.x += 1
    #     self.pos= [self.x, self.y]
    #
    # def forbidden_actions(self,grid):
    #     if grid[self.x, self.y - 1 ] == 1:
    #
    #
    #     if k == "d":
    #         self.y += 1
    #     if k == "l":
    #         self.x -= 1
    #     if k == "r":
    #         self.x += 1




def plotXKCD(grid):
    """ Generate an XKCD-styled line-drawn image of the maze. """
    H = len(grid)
    W = len(grid[0])
    h = (H - 1) // 2
    w = (W - 1) // 2

    with plt.xkcd():
        fig = plt.figure()
        ax = fig.add_subplot(111)

        vertices = []
        codes = []

        # loop over horizontals
        for r,rr in enumerate(range(1, H, 2)):
            run = []
            for c,cc in enumerate(range(1, W, 2)):
                if grid[rr-1,cc]:
                    if not run:
                        run = [(r,c)]
                    run += [(r,c+1)]
                else:
                    use_run(codes, vertices, run)
                    run = []
            use_run(codes, vertices, run)

        # grab bottom side of last row
        run = []
        for c,cc in enumerate(range(1, W, 2)):
            if grid[H-1,cc]:
                if not run:
                    run = [(H//2,c)]
                run += [(H//2,c+1)]
            else:
                use_run(codes, vertices, run)
                run = []
            use_run(codes, vertices, run)

        # loop over verticles
        for c,cc in enumerate(range(1, W, 2)):
            run = []
            for r,rr in enumerate(range(1, H, 2)):
                if grid[rr,cc-1]:
                    if not run:
                        run = [(r,c)]
                    run += [(r+1,c)]
                else:
                    use_run(codes, vertices, run)
                    run = []
            use_run(codes, vertices, run)

        # grab far right column
        run = []
        for r,rr in enumerate(range(1, H, 2)):
            if grid[rr,W-1]:
                if not run:
                    run = [(r,W//2)]
                run += [(r+1,W//2)]
            else:
                use_run(codes, vertices, run)
                run = []
            use_run(codes, vertices, run)

        vertices = np.array(vertices, float)
        path = Path(vertices, codes)

        # for a line maze
        pathpatch = PathPatch(path, facecolor='None', edgecolor='black', lw=2)
        ax.add_patch(pathpatch)

        # hide axis and labels
        ax.axis('off')
        ax.set_title('XKCD Maze')
        ax.dataLim.update_from_data_xy([(-0.1,-0.1), (h + 0.1, w + 0.1)])
        ax.autoscale_view()

        plt.show()

def use_run(codes, vertices, run):
    """Helper method for plotXKCD. Updates path with newest run."""
    if run:
        codes += [Path.MOVETO] + [Path.LINETO] * (len(run) - 1)
        vertices += run

def showPNG(grid):
    """Generate a simple image of the maze."""
    plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.show()

def toHTML(grid, start, end, cell_size=10):
    row_max = grid.height
    col_max = grid.width

    html = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"' + \
           '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">' + \
           '<html xmlns="http://www.w3.org/1999/xhtml"><head>' + \
           '<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />' + \
           '<style type="text/css" media="screen">' + \
           '#maze {width: ' + str(cell_size * col_max) + 'px;height: ' + \
           str(cell_size * row_max) + 'px;border: 3px solid grey;}' + \
           'div.maze_row div{width: ' + str(cell_size) + 'px;height: ' + str(cell_size) + 'px;}' + \
           'div.maze_row div.bl{background-color: black;}' + \
           'div.maze_row div.wh{background-color: white;}' + \
           'div.maze_row div.rd{background-color: red;}' + \
           'div.maze_row div.gr{background-color: green;}' + \
           'div.maze_row div{float: left;}' + \
           'div.maze_row:after{content: ".";height: 0;visibility: hidden;display: block;clear: both;}' + \
           '</style></head><body>' + \
           '<div id="maze">'

    for row in range(row_max):
        html += '<div class="maze_row">'
        for col in range(col_max):
            if (row, col) == start:
                html += '<div class="gr"></div>'
            elif (row, col) == end:
                html += '<div class="rd"></div>'
            elif grid[row][col]:
                html += '<div class="bl"></div>'
            else:
                html += '<div class="wh"></div>'
        html += '</div>'
    html += '</div></body></html>'

    return html

# class MazeKnoedel():
#
#     def __init__(self):
#         m = Maze()
#         m.generator = HuntAndKill(10, 10)
#         m.generate()
#         m.solver = BacktrackingSolver()
#         m.generate_entrances()

def checkpos(p1pos, grid):
    print("non me gusta") if grid[p1pos] == 1 else print("wd")

def check_if_key_valid(self, key):
    valid_keys = ["w", "a", "s", "d"]
    if key in valid_keys and self.forbidden_actions[self.snake_heading] != key:
        return True
    else:
        return False

def key_input(self, event):
    if not self.crashed:
        key_pressed = event.keysym
        # Check if the pressed key is a valid key
        if self.check_if_key_valid(key_pressed):
            # print(key_pressed)
            self.begin = True
            self.last_key = key_pressed

if __name__ == "__main__":

    m = Maze()
    m.generator = HuntAndKill(75, 75)
    m.generate()
    m.solver = BacktrackingSolver()
    m.generate_entrances()
    print(m.tostring(True, True))  # print walls and entrances
    plotXKCD(m.grid)
    p1 = Player(m.start)
    # while p1.x != m.end[1] and p1.y!= m.end[0]:
    #     user_guess =str(input("Guess: \n"))
    #     checkInput(user_guess)
    #     p1.walk(user_guess.lower())
    #     checkpos(p1.pos,m.grid)


    #while True:



    #
    #showPNG(m.grid)

    #
    # m = Maze()
    # m.generator = Prims(10, 10)
    # m.generate()

    #
    #
    # m.solver = BacktrackingSolver()
    # m.generate_entrances()
    # m.solve()
    # print("\n\n\n\n")
    # print(m)

