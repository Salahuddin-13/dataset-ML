from pathlib import Path

MAX_BYTES = 20 * 1024 * 1024  # 20 MiB
SOURCE_ROOT = Path("dataset")
OUTPUT_ROOT = Path("agent_data")

for src in sorted(SOURCE_ROOT.rglob("*.tsv")):
    rel = src.relative_to(SOURCE_ROOT)

    # Example:
    # dataset/train/train_source1.tsv
    # becomes:
    # agent_data/train/train_source1/
    out_dir = OUTPUT_ROOT / rel.with_suffix("")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Remove old chunks if they exist
    for old in out_dir.glob("part-*.tsvpart"):
        old.unlink()

    with src.open("rb") as f:
        header = f.readline()

        if not header:
            continue

        part = 0
        out = None
        current_size = 0

        try:
            while True:
                line = f.readline()

                if not line:
                    break

                # Start a new chunk if this line would exceed the limit.
                # Every chunk gets the header so each chunk remains a valid TSV.
                if (
                    out is None
                    or current_size + len(line) > MAX_BYTES
                ):
                    if out is not None:
                        out.close()

                    part += 1
                    output_file = out_dir / f"part-{part:04d}.tsvpart"

                    out = output_file.open("wb")
                    out.write(header)
                    current_size = len(header)

                    print(f"Creating {output_file}")

                out.write(line)
                current_size += len(line)

        finally:
            if out is not None:
                out.close()

print("\nFinished splitting dataset.")