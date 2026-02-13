# HectorCastelli Packs

This is a [monorepo](https://monorepo.tools/) with multiple DataPacks and ResourcePacks developed by me, for myself.

## Structure

- [`packs/`](./packs/): All of the packs (DataPacks and ResourcePacks) are located in the  directory.
  - `<packName>/`: Files relating to one pack (named `packName`), which may require both a DataPack and a ResourcePack to function in-game.
    - `pack.mcmeta`: An extended `pack.mcmeta` file, with internal metadata used for versioning and building.
- [`scripts/`](./scripts/): Tooling for the repository.
- [`dist/`](./dist/): The location where the final distribution files are saved into.

## Versioning

This repository uses a dual-versioning policy to ensure clarity for players and developers.

Each pack has two versioning components:

1. The supported Minecraft version
1. The pack [Semantical Versioning](https://semver.org/) version

These versions are stored on each pack separately, in the `pack.mcmeta` file as follows:

```jsonc
{
  // ...
  "metadata": {
    "version": "1.1.0", // The pack version
    "minecraft_version": "1.21.11", // The Minecraft version
    // ...
  }
}
```

New features, changes and updates to packs will **not** be applied retroactively. This means that new versions (even fixes) will only be available if you are updating your game version to match the supported Minecraft version of the pack.

When new Minecraft versions are released, the packs will be updated individually over time. There is no estimated time-range for this effort.

## Contributions

While contributions are welcome, there is no expectancy of timeliness for their review and no guarantee of integration.

Bugs and issues reported will be investigated on a best-effort basis, and depending on the versions involved may not be fixed.

Ideas and suggestions should be submitted as issues, and will be implemented only if they match with my personal goals for the pack. In these cases, feel free to fork the repository and implement the changes you'd like yourself.

Pull Requests will be reviewed and feedback will be shared. There are no guarantees that they will be merged, as the same standards for ideas and suggestions apply.

## Disclaimers

This is a personal project maintained by an individual on their free time.

This is:

- NOT AN OFFICIAL MINECRAFT PRODUCT.
- NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT.

Some assets are heavily based on or modified from assets that ship with Minecraft. This repository claims no ownership of those original assets, and is utilizing them according to fair-use guidelines of copyright law.

All other contents (scripts, data logic, and original textures) are released under the terms described in the attached [LICENSE](./LICENSE) file. 