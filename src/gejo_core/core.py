import pathlib
import tomllib

from pystac import (
    Collection,
    Catalog,
    CatalogType,
)


def build_without_stacitems() -> None:
    """Create a STAC skeleton from the TOML config."""
    config = load_config(name="geo-joinery.toml")
    for item in config["project"]["catalogs"]:
        catalog = create_catalog(item)
        catalog.normalize_hrefs(str(pathlib.Path("docs", "stac", catalog.id)))
        catalog.save(catalog_type=CatalogType.SELF_CONTAINED)


def create_catalog(id: str) -> Catalog:
    config = load_config(parents=("catalogs", id))
    catalog = Catalog(
        id=id,
        description=config.get("description"),
        title=config.get("title"),
    )
    for item in config["collections"]:
        collection = create_collection(item)
        catalog.add_child(collection)
    return catalog


def create_collection(config: dict) -> Collection:
    href = config.get("href")
    kwargs = {}
    if href is not None:
        collection = Collection.from_file(href)
        kwargs["id"] = collection.id
        kwargs["description"] = collection.description
        kwargs["extent"] = collection.extent
    else:
        kwargs["id"] = config["id"]
    collection = Collection(**kwargs)
    return collection


def load_config(name: str = "catalog.toml", parents: tuple = ()) -> dict:
    path = pathlib.Path(*parents, name)
    with path.open("rb") as fh:
        config = tomllib.load(fh)
    return config
