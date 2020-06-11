
# Render Experiments
![Overview](img/render/overview.png)
**Figure 1:** Some results obtained with different techniques 
## Overview

The main goal of this assignment is to learn more about rendering, creating different types of effects in Unity and testing the different tools that are provided to the developer, extending the scene from the previous assignment with new visual features.
<br/>
In this project, the Universal Render Pipeline(URP) was used to take advantage of optimizations on lightweight platforms like WebGL, as well as try out the ShaderGraph feature. The experiments were made exploring three main areas: Post-Effects, ShaderGraph and commom CG shaders, for each of these, different visual effects were created, exploring the particularities of each tool.

## Post-Effects

Taking advantage of the particle system created in the previous assignment, I decided to implement a system that make just the areas that are emmiting particles glow, so the shine effect will start from the bottom and progress to the top.
<br/> 
To achieve this, I create a material with the same texture as the tree, but the Emission Map field of it was filled with a intense red color, then I create a GameObject with this material, without a mesh associated to it. 
To get the glow, the post-processessing effect bloom was added to the scene with a high treshold to make sure that the effect will be applied just in the intense red color of the material and not in undesirable places.
<br/> 
Each iteraction, when new triangles are added to the custom mesh created via C# script, the "mesh" property of the GameObject is filled with an updated value, creating a progressive illumination effect, which can be seen below:

![Overview](img/render/glow.gif)
<br/>
**Figure 2:** Bloom effect in my particle emmiter model.

## Shader Graph 

With Shader Graph it's very simple to get incredible visual results. Instead of writing code for the shader, you can create nodes in a graph network and connecting them to get, in real time, the desireable result.
<br /> 
For this experiment, I create a simple hologram effect and applied to my tree model, creating some sort of cyberpunk dissolving. The modelling is simple and straightfoward, both of the simple graph network and final result can be seen above:
![Overview](img/render/shadergraph.png)
<br/>
**Figure 3:** Shader Graph network.
<br/>
![Overview](img/render/hologram.gif)
<br/>
**Figure 4:** Final result.

## CG Shader Code

Although Shader Graph is a great tool for creating shaders, Unity has the tools to creating shader codes the old fashion way using HLSL CG, in cases when a low-level programming is required to achieve the desired effect.
<br />
Two effects were made, a stained glass transpent effect and a heat distortion effect.

* **Stained Glass**
The core that this shader uses is the _CameraOpaqueTexture parameter to take what has already been rendered on the screen. The part where the distortion takes place is in the Pixel Shader. Here, a normal map is unpacked and used to offset the UV data of the grab texture.
![Overview](img/render/moon.gif)
<br/>
**Figure 5:** Moon seen through the glass.

* **Heat distortion**

The distortion effect is achieved by appling a shader to a plane that will billboard that and draw it on top of everything, then grab the camera rendered texture through the _CameraOpaqueTexture parameter, distort the texture sample position and use the distorted position to sample and draw the camera texture.
![Overview](img/render/fire.gif)
<br/>
**Figure 5:** Campfire with the distortion effect.



















