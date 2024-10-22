# Python Scene Renderer

This project supports rendering 3D objects from Wavefront .OBJ files. It is largely based on 
[einarf's scene module of moderngl_window](https://github.com/moderngl/moderngl-window/tree/master/moderngl_window/scene). 
There are couple differences, though. Firstly, it uses [wavefront parser](https://test.pypi.org/project/wavefront/0.0.1/). 
Also, it allows somewhat higher flexibility. 
Project uses [moderngl_window](https://github.com/moderngl/moderngl-window) for rendering and [pyglm](https://pypi.org/project/PyGLM/) for computations. 

You can see a usage example at `example` folder. It can be invoked with:

```
python ./example/render.py ./example/resources/monkey.obj
```

# How to build

```
pip install -i https://test.pypi.org/simple/ scene==0.0.1
```
