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

def parse_bbox(bbox_str: str):
    return [float(value) for value in bbox_str.strip().split(' ')[1:]]


def load_true_objects_v1(loader, total_label_map, include_boat=True, download_images=True):
    '''
    definite objects from pack2 both sides + 3 images of boat
    '''
    def filter_out_images(removed_stems, subsetted_stems_to_bbox_index, packlike):
        paths = [Path('/content', packlike, 'images', f'{stem}.JPG') for stem in sorted(total_label_map[packlike].keys()) if stem not in removed_stems]
        bboxes = []
        for p in paths:
            if p.stem not in removed_stems:
                bboxes.append([
                        parse_bbox(box) for i, box in enumerate(total_label_map[packlike][p.stem])
                            if (p.stem not in subsetted_stems_to_bbox_index) or (i in subsetted_stems_to_bbox_index[p.stem])
                        ])
        return paths, bboxes
    # pack2 leftside
    leftside_paths, leftside_boxes = filter_out_images(
        removed_stems=set(['G0017774', 'G0017775', 'G0017776', 'G0017777', 'G0017983', 'G0017987']),
        subsetted_stems_to_bbox_index={'G0017328': [0]},
        packlike='pack2/leftside'
        )
    # pack2 rightside
    rightside_paths, rightside_boxes = filter_out_images(
        removed_stems=set(['G0022019', 'G0022020', 'G0022021', 'G0022022', 'G0022023', 'G0022024', 'G0022025', 'G0022026', 'G0022027',
                        'G0022028', 'G0022181', 'G0022182', 'G0022183', 'G0022215', 'G0022216', 'G0022217', 'G0022218', 'G0032586',
                        'G0032587', 'G0032587', 'G0032589', 'G0032590', 'G0032591', 'G0032592', 'G0032593', 'G0032594', 'G0032595',
                        'G0032596', 'G0032597', 'G0032598', 'G0032599', 'G0032600', 'G0032601', 'G0032602', 'G0032627', 'G0032628',
                        'G0032629', 'G0032630', 'G0032631', 'G0032632']),
        subsetted_stems_to_bbox_index={},
        packlike='pack2/rightside'
    )

    paths = leftside_paths + rightside_paths
    bboxes = leftside_boxes + rightside_boxes

    # boat (pack1 rightside)
    if include_boat:
        stems_boat = ['G0022000', 'G0022089', 'G0022484']
        boat_paths = [Path('/content', 'pack1/rightside', 'images', f'{stem}.JPG') for stem in stems_boat]
        boat_boxes = [[parse_bbox(box) for box in total_label_map['pack1/rightside'][stem]] for stem in stems_boat]
        paths += boat_paths
        bboxes += boat_boxes
    
    if download_images:
        image_keys = [str(path.relative_to('/content')) for path in paths]
        loader.load_by_paths_threaded(image_keys)
    return paths, bboxes
