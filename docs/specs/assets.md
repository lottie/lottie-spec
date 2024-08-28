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
