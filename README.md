# floydsteinberg.pythonanywhere.com

This repository holds the source of <https://floydsteinberg.pythonanywhere.com>.


## About

<https://floydsteinberg.pythonanywhere.com> provides a simple API that performs Floyd-Steinberg dithering algorithm.

Everyday at 05:20:00 UTC, images uploaded within the previous 24 hours get deleted.

## API Guide

### Upload Image

Endpoint:

```
https://floydsteinberg.pythonanywhere.com/upload
```

Request body:

- form-data
  - image            : file (the image to upload)
  - width (optional) : Integer (target width)
  - height (optional) : Integer (target height)

Response (json):

```
{
    "filename": <String>
}
```

### Get Image

Endpoint:

```
https://floydsteinberg.pythonanywhere.com/static/:filename
```

where `filename` is the filename received in [Upload Image](#upload-image) plus file extension. There are two extensions available: `.png` and `.ppm`.

## Workflow

1. Upload a color image through [Upload Image](#upload-image)
2. If the response has a status code of 200, save `filename` from the response body (e.g. `"af29e4ca-232a-46db-b27c-2fc2531804a6"`)
3. Now, the dithered image in `png` format is available at <https://floydsteinberg.pythonanywhere.com/static/af29e4ca-232a-46db-b27c-2fc2531804a6.png>
4. The dithered image in `ppm` format is available at <https://floydsteinberg.pythonanywhere.com/static/af29e4ca-232a-46db-b27c-2fc2531804a6.ppm>

