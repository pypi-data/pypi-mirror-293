# tjwmd

## Installation

```shell
pip install tjwmd
```

## Quick Start

```python
import cv2
from tjwmd import TJWMD
from ultralytics import YOLO

image = cv2.imread('image.jpg')

wmc = YOLO(
    'wmc_model.pt'
)
wmd = YOLO(
    'wmd_model.pt'
)
tjwmd = TJWMD(
    wmc,
    wmc.names.values(),
    wmd
)

r = tjwmd.predict(
    frame_=image,
    num_of_digits=6,
    angle=0,
    wm_counter_conf=0.4,
    wm_digits_conf=0.1
)

if r:
    results, result_img = r
    print(result_img)
    cv2.imwrite('result.jpg', result_img)

```