# MOVIE2GRID  
This project is used to convert videos into files for monochrome `LED Grid` using `openCV`.  
The output data consists of all `frames` or reduced `fps` according to the `fpsdiv` parameter.

### **Processing Workflow**
Original Frame → Grayscale → Scaling → Binarization  

**Recommended for materials like shadow art. Color videos are not suitable for direct conversion via binarization.**  

## **Behavior**
- When using Movie2Grid for the first time, it will create two folders: `src` (for storing videos) and `output` (for saving processed results).  

## **Function**
- `video_to_led_grid_fmt(videoname: str = None, grid_size: tuple[int, int] = (12, 9), fpsdiv: int = 1)`  
  - `videoname`: The video file name inside the `src` folder. For example, if the path is `./src/BadApple.mp4`, input `"BadApple.mp4"`. If left empty, all videos in the `src` folder will be converted (excluding subdirectories).  
  - `grid_size`: Format as `(x, y)`, e.g., for a 12x9 LED grid, set it as `(12, 9)`.  
  - `fpsdiv`: Determines how often a frame is output. The function works by outputting when `frm_cnt % fpsdiv == 0`. The default value is `1`, meaning every frame will be processed.

## **Settings**
- `OUTPUT_BIN`  
  - `True`: Output format is `struct.pack` with `"0{n}H"`, e.g., for a 16x9 grid, it produces `04H` per row.  
  - `False`: Output format is `str`, using uppercase `Hex` representation.  
  - Each row corresponds to one `Frame`. For example, in a 16x8 grid, there will be 8 sets of `HHHH` formatted data.  
  - The data is **not compressed**. When used on an MCU platform, it may require external Flash storage to avoid exceeding the PGM Flash limit.

## **Example**
- Code
```python
from Movie2Grid import methods
if __name__ == "__main__":
    methods.OUTPUT_BIN = False  # Set output format
    methods.video_to_led_grid_fmt(grid_size=(16, 8))
```
- CLI Output
```bash
process: src\BadApple.mp4 => output\BadApple.txt  # Auto traversal  
process: BadApple.mp4 100.00 % [13142/13142]  # Progress info  
process success, src\BadApple.mp4 => output\BadApple.txt  
```
- BadApple.txt
```
[...]
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000001000000000000
00000000000000010001000100000000
00010001000100010001000100000000
00010001000100010001000100000000
00010001000100010001000100000000
00000000000100030001000300000000
00000000000200030003000300010000
00000000000000020003000300010000
00000000000000000007000300010001
00000000000000000006000600030001
[...]
```