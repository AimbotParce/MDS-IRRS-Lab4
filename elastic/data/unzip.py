import os
import zipfile


def unzip_file(zip_path: os.PathLike, extract_to: os.PathLike):
    """Unzip a zip file to the specified directory."""
    if not os.path.exists(zip_path):
        raise ValueError(f"Zip path {zip_path} does not exist.")
    if not os.path.isfile(zip_path):
        raise ValueError(f"Zip path {zip_path} is not a file.")
    if os.path.exists(extract_to):
        if not os.path.isdir(extract_to):
            raise ValueError(f"Extract to path {extract_to} exists and is not a directory.")
        if len(os.listdir(extract_to)) > 0:
            raise ValueError(f"Extract to directory {extract_to} is not empty.")
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


if __name__ == "__main__":
    """Download and unzip the arXiv dataset."""
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Unzip a file and store its contents in a directory.")
    parser.add_argument("input_file", help="Path to the zip file to unzip.")
    parser.add_argument("output_dir", help="Directory in which to save the contents of the zip file.")
    args = parser.parse_args()

    print(f"Unzipping {args.input_file} dataset to {args.output_dir}...", end="")
    unzip_file(args.input_file, args.output_dir)
    print("Done.")
