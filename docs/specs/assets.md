# Assets

<h2 id="asset">Asset</h2>

{schema_string:assets/asset/description}

{schema_object:assets/asset}


<h2 id="precomposition">Precomposition</h2>

{schema_string:assets/precomposition/description}

{schema_object:assets/precomposition}

<h2 id="image">Image</h2>

{schema_string:assets/image/description}

Image formats supported vary depending on the player. Some commonly supported formats are JPEG, GIF, PNG and SVG. 

{schema_object:assets/image}

If the dimensions of the image asset does not match the size given by `w` and `h`,
renderers MUST ensure image layers referencing that asset do not have any visuals
exceeding the `w`-`h` size. It's RECOMMENDED they scale the image maintaining
its aspect ratio and they center it within the $(0, 0)$, $(w, h)$ box.

Even if an image asset does not have any intrinsic size, its contents MUST
still stay within the `w`-`h` bounds when rendered.

Authoring tools SHOULD export files where `w` and `h` match the physical size of the assets.

<h2 id="video">Video</h2>

{schema_string:assets/video/description}

Video formats supported vary depending on the player. Some commonly supported formats are MP4, WebM, and MOV.

{schema_object:assets/video}

Video assets define the source video content that can be referenced by video frame assets.
This enables the use of video compression techniques to reduce the overall animation size, when working with raster-based animations.

Players MUST support extracting individual frames from video assets at specified timestamps when initializing animations.

<h2 id="video-frame">Video Frame</h2>

{schema_string:assets/video-frame/description}

{schema_object:assets/video-frame}

Video frame assets reference a video asset by ID and specify a timestamp to extract a specific frame. Players MUST extract the frame at the exact timestamp specified, or the closest available frame if the exact timestamp is not available. The extracted frame should be treated as a static image for rendering purposes.

