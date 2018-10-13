import vispy as vp 
import numpy as np
from vispy import app
from vispy import gloo

c = app.Canvas(keys="interactive")
vertex = """
attribute vec2 a_position;
void main (void) 
{
    gl_Position = vec4(a_position, 0.0, 1.0);
}
"""

fragement = """
void main (void)
{
    gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
}
"""

program = gloo.Program(vertex, fragement)

program["a_position"] = np.c_[
        [x for x in range(100)],
        [math.sin(x) for x in range(100)]].astype(np.float32)
        
@c.connect
def on_resize(event):
    gloo.set_viewport(0,0,*event.size)


@c.connect
def on_draw(event):
    gloo.clear((1,1,1,1))
    program.draw('line_strip')    

c.show()
app.run()