# Don't use this!!
# It successfully moves the window position 
# of the given figure BUT it locks up the app.

# requires 'brew install pyqt' and 'pip intall PyQt5'
# brew install pyqt
# pip install PyQt5

import matplotlib
matplotlib.use("Qt5Agg") 

def set_window_position(fig, x, y):
    win = fig.canvas.manager.window if fig is not None else None
    if win is not None:
        old_geom = win.geometry()
        (old_x,old_y,dx,dy) = old_geom.getRect()
        print("old window geometry:", old_geom)
        win.setGeometry(x,y,dx,dy)
        print("new window geometry:", win.geometry().getRect() )
    else:
        print("window not available")
    sys.stdout.flush()
