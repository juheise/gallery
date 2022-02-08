from fs.osfs import OSFS
import click

from ..ingestion.ingest import import_image


PREFIX = "GALLERY"

@click.command()
@click.option("--thumb-size", type=int, default=128)
@click.option("--thumb-dir", envvar=f"{PREFIX}_THUMB_DIR")
@click.option("--filter", "-f", multiple=True, default=["*.jpg", "*.jpeg"])
@click.argument("path")
def ingest(path, filter, thumb_dir, thumb_size):
    
    source_fs = OSFS(path)
    thumb_fs = OSFS(thumb_dir)

    for path in source_fs.walk.files(filter=filter):
        try:
            print(f"ingesting {path}...")
            import_image(source_fs, path, thumb_fs, thumb_size)
        except Exception as e:
            print(f"ERROR {e.__class__.__name__}: {e!s}")


if __name__ == "__main__":
    ingest()
