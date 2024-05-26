from pathlib import Path

# Get the current directory path
current_path = Path(__file__).parent.resolve()

# Define the new SBERT directory path
sbert_path = current_path / "SBERT_data"

# Create the SBERT directory
sbert_path.mkdir(parents=True, exist_ok=True)

print(f"SBERT directory created at: {sbert_path}")
