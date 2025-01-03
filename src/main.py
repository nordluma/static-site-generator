import os
import shutil

PUBLIC_DIR = "./public"
STATIC_DIR = "./static"


def main():
    print("Deleting public directory...")
    if os.path.exists(PUBLIC_DIR):
        shutil.rmtree(PUBLIC_DIR)

    print("Copying static files to public directory...")
    copy_files(STATIC_DIR, PUBLIC_DIR)


def copy_files(src_dir: str, dst_dir: str):
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    for entry in os.listdir(src_dir):
        src_path = os.path.join(src_dir, entry)
        dst_path = os.path.join(dst_dir, entry)

        print(f" * {src_path} -> {dst_path}")
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            copy_files(src_path, dst_path)


if __name__ == "__main__":
    main()
