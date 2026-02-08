from pathlib import Path
import pandas as pd
import kagglehub

# Download latest version
dataset_path = kagglehub.dataset_download("ralle360/historic-tour-de-france-dataset")
INPUT_CSV = Path(dataset_path) / "stages_TDF.csv"
OUTPUT_TEXT = Path("data/raw_locations.txt")

def main():
    df = pd.read_csv(INPUT_CSV)

    raw = pd.concat([df["Origin"], df["Destination"]],ignore_index=True)
    raw.dropna().astype(str)

    #Normalize
    raw = raw.map(lambda s: s.strip())
    raw = raw[raw != ""]

    unique = sorted(set(raw.tolist()))

    #Write new file with the cities
    OUTPUT_TEXT.parent.mkdir(parents = True, exist_ok = True)
    OUTPUT_TEXT.write_text("\n".join(unique), encoding = "utf-8")
    print(f"Extracted {len(unique)} location: {OUTPUT_TEXT}")

if __name__ == "__main__":
    main()