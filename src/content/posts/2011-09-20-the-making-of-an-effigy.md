---
title: "The Making of an Effigy (Kinect + Architecture + Fire = Fun!)"
date: 2011-09-20 12:00:00 +0000
---

*Originally published on [craneium.net](https://web.archive.org/web/20160315095018/http://craneium.net/)*

## I know what you are here for, so lets start with some porno for pyros:

![The burn](/images/craneium/kinect-effigy/bridge-starter.jpg)

Photo credit Derrick (Donut) Peterson

February 11 was my first introduction to the [Burning Flipside](https://web.archive.org/web/20160319063733/http://burningflipside.com/ "Burning Flipside") community. Thanks to the suggestion of a good friend (you know who you are!), I found myself huddled by a tiny wood stove in a freezing cold warehouse staring at a some diagrams that looked something like the following:

![Sketch](/images/craneium/kinect-effigy/sketch.jpg)

Credit to Dotti Spearman (Pretend)

I had never been privy to a large build like this before; I had some idea the amount of work that was in store for us, but not a clear idea of exactly what I had to add. During the initial planning weeks, I spent a good amount of time talking to Dotti (Pretend), our rock-star architect and DaFT lead, and had a fun idea. . .

In parallel to this project, I had been playing with the [Microsoft Kinect](https://web.archive.org/web/20160319063733/http://en.wikipedia.org/wiki/Kinect "Kinect Wiki"), a device designed to sit atop a television set, and sense the movement and gestures of game players for XBOX. Right around this time, [libfreenect](https://web.archive.org/web/20160319063733/http://openkinect.org/wiki/Main_Page "Link to the open Kinect project") and supporting Python/cython code was hot off the presses and extremely glitchy. I had been prototyping code to map caves in the Austin area, most significantly [Airman's cave](https://web.archive.org/web/20160319063733/http://tynan.com/exploring-airmans-cave "Airmans Cave in Austin"), but in my testing it did a reasonable job on convex objects as well. I suggested, that we might be able to use the Kinect to scan an actual model, thusly incorporate a true human form into the design. She was ecstatic, and over the next week, I got my code on . . . hard . . .

1. I wrangled down the libfreenect Python/cython drivers as well as the python wrappers to vlfeat
2. I wrote code to co-register the depth and image cameras ([fundamental matrix](https://web.archive.org/web/20160319063733/http://en.wikipedia.org/wiki/Fundamental_matrix_(computer_vision) "Wikipedia: Fundamental Matrix") estimation)
3. Coded up a capture routine to record the depth and image camera information at about 15 frames per second, and dump them to disk via [pytables](https://web.archive.org/web/20160319063733/http://www.pytables.org/moin). (I Added a post-process compression later)
4. Wrangled the depth camera information into .ply based meshes, (including depth culling, quality pruning, and aberrational correction)
5. Incorporated a SIFT based keypoint detector (from the [vlfeat library](https://web.archive.org/web/20160319063733/http://www.vlfeat.org/ "VLFeat Computer Vision Library")) to estimate camera pose changes, and transform the output meshes accordingly.

Additionally, I threw together an extremely ghetto steady camera stand from parts found on the hack-shelf in the [Austin Hackerspace](https://web.archive.org/web/20160319063733/http://www.atxhackerspace.org/index.php/Main_Page "Austin Hackerspace"), including a monster transformer as counter-weight, a metal spoon handle, and a sheet-metal laptop tray. [The lovely and talented KT](https://web.archive.org/web/20160319063733/http://www.purekt.com/ "Link to KT Pure") served as the model for our scan, and posed extremely patiently during the whole process. Here is myself and KT (also at the hacker space):

![Scanning KT](/images/craneium/kinect-effigy/scanning-kt.jpg)

Photo credit to Dotti (Pretend)

Here is a shot through the eyes of the Kinect (Depth is false colored on the right, and visual image on the left):

![Kinect depth projection](/images/craneium/kinect-effigy/kt-projection.png)

Below is the computed mesh that came from that image above on the left:

![Kinect mesh](/images/craneium/kinect-effigy/kt-mesh.png)

We did three scans, each taking about 3 minutes, and generating ~1.5 GB of uncompressed data. The second scan turned out the best (I missed a significant section of her back on the third), and the post-processing fun began. I algorithmically estimated the camera's position throughout time in each subsequent frame, then transformed and outputted ~150 .ply mesh files. Based on these I selected, hand-cleaned, smoothed, and aligned about 30 of these using [Meshlab](https://web.archive.org/web/20160319063733/http://meshlab.sourceforge.net/ "Meshlab mesh manipulation tool"), a tool which had a much fast global [ICP algorithm](https://web.archive.org/web/20160319063733/http://en.wikipedia.org/wiki/Iterative_Closest_Point "Iterative Closest Point"). Coloring all the overlapping meshes differently gives a feel for the complexity of the assembly:

![Multi-colored mesh assembly](/images/craneium/kinect-effigy/mesh-y.png)

(~20 Million polygons when finished)

The meshes were merged and imported into sketchup. These went through a couple geometric operations, and were augmented with hands and feet (features which were below the attainable resolution of the Kinect) and sliced into ~200 sections per form. From the sketchup design, these cross-sections and a half-ton of salvaged plywood were fed into a CNC router (a [ShopBot](https://web.archive.org/web/20160319063733/http://www.shopbottools.com/ "Shopbot") - graciously hosted by [Dave Umlas and Marrilee Ratcliff](https://web.archive.org/web/20160319063733/http://communityartmakers.com/ "Dave and Community Art Makers") of the [epic "Fire of Fires" Temple](https://web.archive.org/web/20160319063733/http://digi10ve.com/wp-content/uploads/2010/08/burning-man.jpeg "Lotus Temple Image"))

The output was several trucks full of scrap, >100 pounds of saw-dust, and ~400 pieces of wood which we came to affectionately refer to as "the lady bits." The collation, transport, and assembly of these pieces presented a unique hoard of challenges. I can not emphasize enough the efforts of more than two dozen people in their assembly, but the end effect was simply stunning. Here you see our charming model next to her 5.5 times larger wooden embodiment.

![KT next to her effigy](/images/craneium/kinect-effigy/kt-pose1.jpg)

Photo credit Derrick (Donut) Peterson

In keeping with the nature of burn events, the true beauty of this structure was born out in the flames.

![Sol burning](/images/craneium/kinect-effigy/sol-burn.jpg)

![Luna burning](/images/craneium/kinect-effigy/luna-burn.jpg)

Photo credit Derrick (Donut) Peterson

There is really nothing like seeing thousands of hours of human effort vested in the conception, design, and fabrication of something so ephemeral.

![Center burn](/images/craneium/kinect-effigy/center-burn.jpg)

Photo credit Derrick (Donut) Peterson

In closing, I want to say thank you to everyone involved. As all our work was reduced to ash and cinders, I felt more connected to the Austin community than I ever did before.

I have heard the Sirens call of effigy design, and I know it will be my turn soon. When that time comes, I hope I can create something even half as beautiful and moving as Dotti did for us! Happy burn and thanks again!

## More Links:

[Like DaFT on facebook](https://web.archive.org/web/20160319063733/http://www.facebook.com/pages/DaFT-2011/190416520983619 "DaFT on Facebook")

[Watch It Burn!](https://web.archive.org/web/20160319063733/http://www.facebook.com/video/video.php?v=2057390910190 "Yay BURN!") (make sure to select the "HD" option)
