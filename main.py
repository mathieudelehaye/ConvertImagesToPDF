import sys
import os
import glob
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

def parse_size(size_arg):
    try:
        w, h = map(int, size_arg.lower().split('x'))
        return w, h
    except:
        raise ValueError("Invalid size format. Use WIDTHxHEIGHT (e.g., 1512x2016).")

def adapt_size(im, target_size):
    w, h = im.size
    tw, th = target_size
    if (w >= h and tw < th) or (w < h and tw > th):
        return (th, tw)
    else:
        return (tw, th)

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py WIDTHxHEIGHT pattern1 [pattern2 ...]")
        sys.exit(1)

    target_size = parse_size(sys.argv[1])
    patterns = sys.argv[2:]

    thumbnails = []

    for pattern in patterns:
        files = glob.glob(pattern)
        files.sort()

        for infile in files:
            dirpath = os.path.dirname(infile) or '.'
            base, ext = os.path.splitext(os.path.basename(infile))
            thumb_file = os.path.join(dirpath, base + ".thumbnail.png")

            try:
                with Image.open(infile) as im:
                    adapted_size = adapt_size(im, target_size)
                    im.thumbnail(adapted_size, Image.Resampling.LANCZOS)
                    im.save(thumb_file, "PNG")
                    thumbnails.append(thumb_file)
                    print(f"Thumbnail created: {thumb_file} ({im.size[0]}x{im.size[1]})")
            except Exception as e:
                print(f"Failed to process '{infile}': {e}")

    if thumbnails:
        pdf_dir = os.path.dirname(os.path.abspath(thumbnails[0])) or '.'
        pdf_path = os.path.join(pdf_dir, "thumbnails.pdf")

        images = []
        try:
            for thumb in thumbnails:
                im = Image.open(thumb)
                images.append(im.convert('RGB'))

            images[0].save(pdf_path, "PDF", resolution=100.0,
                           save_all=True, append_images=images[1:])
            print(f"PDF created successfully at '{pdf_path}'")
        except Exception as e:
            print(f"Failed to create PDF: {e}")
        finally:
            # Explicitly close all images
            for im in images:
                im.close()
    else:
        print("No thumbnails created, PDF generation skipped.")

if __name__ == "__main__":
    main()
