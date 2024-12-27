from pathlib import Path
# from threaded_loader import ThreadedLoader


def parse_bbox(bbox_str: str):
    return [float(value) for value in bbox_str.strip().split(' ')[1:]]


def load_pack2_all_labelled(loader, total_label_map):
    image_paths = []
    bboxes_per_image = []
    for packlike in ['pack2/leftside', 'pack2/rightside']:
        map_keys = total_label_map[packlike].keys()
        image_keys = [f'{packlike}/images/{stem}.JPG' for stem in map_keys]
        loader.load_by_paths_threaded(image_keys)
        bboxes = []
        for key in map_keys:
            bboxes.append([parse_bbox(bbox_str) for bbox_str in total_label_map[packlike][key]])
        image_paths += [Path('/content', key) for key in image_keys]
        bboxes_per_image += bboxes
    return image_paths, bboxes_per_image
