import os
import urllib.request


def download_zip(url: str, output_path: os.PathLike):
    """Download a zip file from a URL to the specified output path."""
    if os.path.exists(output_path):
        raise ValueError(f"Output path {output_path} exists and is not a file.")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    urllib.request.urlretrieve(url, output_path)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Download a file from a URL.")
    parser.add_argument("url", help="URL of the file to download.")
    parser.add_argument("output", help="Path to save the file to.")
    args = parser.parse_args()

    print(f"Downloading {args.url} file into {args.output}...", end="")
    download_zip(args.url, args.output)
    print("Done.")
