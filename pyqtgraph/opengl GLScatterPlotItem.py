'''
http://www.pyqtgraph.org/documentation/3dgraphics/glscatterplotitem.html
    
Docs » API Reference » PyQtGraph’s 3D Graphics System » GLScatterPlotItemView page source
GLScatterPlotItem

class pyqtgraph.opengl.GLScatterPlotItem(**kwds)[source]
    Draws points at a list of 3D positions.

    __init__(**kwds)[source]
    setData(**kwds)[source]
        Update the data displayed by this item. All arguments are optional;
        for example it is allowed to update spot positions while leaving colors unchanged, etc.

    Arguments:	 
        pos	(N,3) array of floats specifying point locations.
        color	(N,4) array of floats (0.0-1.0) specifying spot colors OR a tuple of floats specifying a single color for all spots.
        size	(N,) array of floats specifying spot sizes or a single value to apply to all spots.
        pxMode	If True, spot sizes are expressed in pixels. Otherwise, they are expressed in item coordinates.

'''