# Setting the sizes for the environment
pixels = 20   # pixels
env_height = 50  # grid height
env_width = 50  # grid width
maxIndex = min(env_height,env_width) 
# ratio must be max 1  
randomPixelRatio = 0.3
# Global variable for dictionary with coordinates for the final route
a = {}
# episodeAmount 
episodeAmount =1000
startPageTitle ='Home Page'
startPageResolation="450x300" 
XCBOptions=tuple(range(env_width))
YCBOptions = tuple(range(env_height))
