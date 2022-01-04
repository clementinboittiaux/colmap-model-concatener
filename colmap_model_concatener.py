import os
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path1', required=True, help='path to first COLMAP model in TXT format')
    parser.add_argument('--input_path2', required=True, help='path to second COLMAP model in TXT format')
    parser.add_argument('--output_path', required=True, help='path to output directory for concatenated COLMAP model')
    parser.add_argument(
        '--RGB1', type=int, nargs=3, metavar=('R1', 'G1', 'B1'),
        help='RBG colors (0-255) for the fist model, useful for debug'
    )
    parser.add_argument(
        '--RGB2', type=int, nargs=3, metavar=('R2', 'G2', 'B2'),
        help='RBG colors (0-255) for the second model, useful for debug'
    )
    args = parser.parse_args()

    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    IMAGE_IDs = []
    CAMERA_IDs = []
    POINT3D_IDs = []

    # Read images.txt file and copies it while getting IMAGE_ID offset for second model
    with open(os.path.join(args.input_path1, 'images.txt'), mode='r') as reader, \
         open(os.path.join(args.output_path, 'images.txt'), mode='w') as writer:
        for _ in range(4):
            reader.readline()
        writer.write('# Image list with two lines of data per image:\n')
        writer.write('#   IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME\n')
        writer.write('#   POINTS2D[] as (X, Y, POINT3D_ID)\n')
        writer.write('# Number of images: X, mean observations per image: Y\n')
        for i, line in enumerate(reader):
            line = line.strip().split(' ')
            if i % 2 == 0:
                IMAGE_IDs.append(int(line[0]))
            writer.write(' '.join(line) + '\n')

    # Read cameras.txt file and copies it while getting CAMERA_ID offset for second model
    with open(os.path.join(args.input_path1, 'cameras.txt'), mode='r') as reader, \
         open(os.path.join(args.output_path, 'cameras.txt'), mode='w') as writer:
        for _ in range(3):
            reader.readline()
        writer.write('# Camera list with one line of data per camera:\n')
        writer.write('#   CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]\n')
        writer.write('# Number of cameras: X\n')
        for line in reader:
            line = line.strip().split(' ')
            CAMERA_IDs.append(int(line[0]))
            writer.write(' '.join(line) + '\n')

    # Read points3D.txt file and copies it while getting POINT3D_ID offset for second model
    with open(os.path.join(args.input_path1, 'points3D.txt'), mode='r') as reader, \
         open(os.path.join(args.output_path, 'points3D.txt'), mode='w') as writer:
        for _ in range(3):
            reader.readline()
        writer.write('# 3D point list with one line of data per point:\n')
        writer.write('#   POINT3D_ID, X, Y, Z, R, G, B, ERROR, TRACK[] as (IMAGE_ID, POINT2D_IDX)\n')
        writer.write('# Number of points: X, mean track length: Y\n')
        for line in reader:
            line = line.strip().split(' ')
            POINT3D_IDs.append(int(line[0]))
            if args.RGB1 is not None:
                line[4:7] = map(str, args.RGB1)
            writer.write(' '.join(line) + '\n')

    # The second model will be concatenated to the first while shifting IMAGE_ID, CAMERA_ID and POINT3D_ID by an offset
    IMAGE_ID_offset = max(IMAGE_IDs) + 1
    CAMERA_ID_offset = max(CAMERA_IDs) + 1
    POINT3D_ID_offset = max(POINT3D_IDs) + 1

    # Concatenate images.txt of the second model to the first model
    with open(os.path.join(args.input_path2, 'images.txt'), mode='r') as reader, \
         open(os.path.join(args.output_path, 'images.txt'), mode='a') as writer:
        for _ in range(4):
            reader.readline()
        for i, line in enumerate(reader):
            line = line.strip().split(' ')
            if i % 2 == 0:
                IMAGE_ID = int(line[0])
                CAMERA_ID = int(line[8])
                line[0] = str(IMAGE_ID + IMAGE_ID_offset)
                line[8] = str(CAMERA_ID + CAMERA_ID_offset)
            else:
                POINT3D_ID = map(lambda x: str(int(x) + POINT3D_ID_offset) if x != '-1' else x, line[2::3])
                line[2::3] = POINT3D_ID
            writer.write(' '.join(line) + '\n')

    # Concatenate cameras.txt of the second model to the first model
    with open(os.path.join(args.input_path2, 'cameras.txt'), mode='r') as reader, \
         open(os.path.join(args.output_path, 'cameras.txt'), mode='a') as writer:
        for _ in range(3):
            reader.readline()
        for line in reader:
            line = line.strip().split(' ')
            CAMERA_ID = int(line[0])
            line[0] = str(CAMERA_ID + CAMERA_ID_offset)
            writer.write(' '.join(line) + '\n')

    # Concatenate points3D.txt of the second model to the first model
    with open(os.path.join(args.input_path2, 'points3D.txt'), mode='r') as reader, \
         open(os.path.join(args.output_path, 'points3D.txt'), mode='a') as writer:
        for _ in range(3):
            reader.readline()
        for line in reader:
            line = line.strip().split(' ')
            POINT3D_ID = int(line[0])
            line[0] = str(POINT3D_ID + POINT3D_ID_offset)
            IMAGE_ID = map(lambda x: str(int(x) + IMAGE_ID_offset), line[8::2])
            line[8::2] = IMAGE_ID
            if args.RGB2 is not None:
                line[4:7] = map(str, args.RGB2)
            writer.write(' '.join(line) + '\n')
