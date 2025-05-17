import cv2, os, struct
ROW_BYTES = 4
OUTPUT_BIN = True
def binary_2_output(binary_img):
    frame_arr = []
    for row in binary_img:
        i = 0
        for bit in row:
            i = i << 1 | (bit >> 7)
        frame_arr.append(i)
    return struct.pack(f"{len(frame_arr)}H", *frame_arr) if OUTPUT_BIN else (str.join("", [f"{row:0{ROW_BYTES}X}" for row in frame_arr]) + '\n')

def gray_resize_binary(file_name:str, grid_size:tuple):
    cap = cv2.VideoCapture(file_name)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_delay = int(1000/cap.get(cv2.CAP_PROP_FPS))
    frame_cnt = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_cnt += 1
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_frame = cv2.resize(frame, grid_size)
        _, bin_frame = cv2.threshold(resized_frame, 127, 256, cv2.THRESH_BINARY)
        yield bin_frame, frame_cnt, total_frames, frame_delay
    cap.release()
def path_walker(videoname:str=None):
    if videoname is None:
        for root, _, files in os.walk("src"):
            for file in files:
                yield os.path.join(root, file), *os.path.splitext(file)
    else:
        yield os.path.join("src", videoname), *os.path.splitext(videoname)
def video_to_led_grid_fmt(videoname:str=None, grid_size:tuple[int, int]=(12, 9), fpsdiv:int = 1):
    global ROW_BYTES, OUTPUT_BIN
    ROW_BYTES = grid_size[0] >> 2 + (1 if grid_size[0] & 0x07 else 0)
    for full_path, name, ext in path_walker(videoname):
        out_ext, out_type = "bin" if OUTPUT_BIN else "txt", "wb" if OUTPUT_BIN else "w"
        out_name = os.path.join("output", f"{name}.{out_ext}")
        print(f"process: {full_path} => {out_name}")
        with open(out_name, out_type) as f:
            for frame, cnt, total, delay in gray_resize_binary(full_path, grid_size):
                if (cnt - 1) % fpsdiv == 0:
                    f.write(binary_2_output(frame))
                print(f"\rprocess: {name + ext} {(cnt / total) * 100:.02f} % [{cnt}/{total:.0f}]", end="", flush=True)
            print(f"\nprocess success, {full_path} => {out_name}")
        print(f"\nFinished.")