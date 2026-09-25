from pathlib import Path

CHUNK_ROOT = Path("agent_data")
DATASET_ROOT = Path("dataset")

for chunk_dir in sorted(CHUNK_ROOT.rglob("*")):

    if not chunk_dir.is_dir():
        continue

    parts = sorted(chunk_dir.glob("part-*.tsvpart"))

    if not parts:
        continue

    # Convert:
    # agent_data/train/train_source1
    # into:
    # dataset/train/train_source1.tsv

    relative = chunk_dir.relative_to(CHUNK_ROOT)
    output_file = DATASET_ROOT / relative.with_suffix(".tsv")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    print(f"Rebuilding {output_file}")

    with output_file.open("wb") as out:

        for index, part in enumerate(parts):

            with part.open("rb") as f:

                # Every chunk contains the header.
                # Only keep the header from the first chunk.
                if index > 0:
                    f.readline()

                while True:
                    data = f.read(1024 * 1024)

                    if not data:
                        break

                    out.write(data)

print("\nDataset reconstruction complete.")