import sys
import json
import os
import PIL.Image


IMAGE_MIME = {
    'JPEG': 'image/jpeg',
    'PNG': 'image/png',
    'GIF': 'image/gif',
    'BMP': 'image/bmp',
}


# Get target directory from command line arguments
target_dirs = []
target_dirs = sys.argv[1:]

print('Target dirs: {0}'.format(target_dirs))

# Find all images in the target directory
images = []
for target_dir in target_dirs:
    for (dirpath, dirnames, filenames) in os.walk(target_dir):
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            if ext.lower() in ['.gif', '.jpg', 'jpeg', '.png', '.bmp']:
                real_path = os.path.realpath(os.path.join(dirpath, filename))
                images.append(real_path)

# Find unique images
images_tmp = []
for i in images:
    if i not in images_tmp:
        images_tmp.append(i)
images = images_tmp

print('Images found: {0}'.format(len(images)))

# Exit if none images found
if len(images) == 0:
    exit()

# Get directories' paths
script_dir = os.path.dirname(os.path.realpath(__file__))
upload_dir = os.path.join(script_dir, '..', 'dev', 'upload_fakes')
images_dir = os.path.join(upload_dir, 'images')
thumbs_dir = os.path.join(upload_dir, 'thumbs')

# Create images dirs
os.makedirs(images_dir, exist_ok=True)
os.makedirs(thumbs_dir, exist_ok=True)

images_data = []
# Create thumbs and symlinks, get image data
for image_path in images:
    image_pil_object = PIL.Image.open(image_path)
    image_filename = os.path.basename(image_path)
    image_name, image_ext = os.path.splitext(image_filename)

    thumbnail_pil_object = image_pil_object.copy()
    thumbnail_pil_object.thumbnail((200, 200))
    thumbnail_path = os.path.join(thumbs_dir, image_name)
    thumbnail_pil_object.save(thumbnail_path, "PNG")

    # Create image symlink
    image_symlink_path = os.path.join(images_dir, image_filename)
    try:
        os.symlink(image_path, image_symlink_path)
    except FileExistsError:
        os.remove(image_symlink_path)
        os.symlink(image_path, image_symlink_path)

    # Save image data
    images_data.append({
        "original_name": image_filename,
        "mimetype": IMAGE_MIME[image_pil_object.format],
        "size": os.path.getsize(image_path),
        "width": image_pil_object.width,
        "height": image_pil_object.height,
        "thumb_width": thumbnail_pil_object.width,
        "thumb_height": thumbnail_pil_object.height,
        "base_name": image_name,
        "extension": image_ext.lower()[1:],
    })

# Save images list
with open(os.path.join(upload_dir, 'images.json'), mode='w', encoding='utf8') as images_json:
    json.dump(images_data, images_json, indent=4, ensure_ascii=False)