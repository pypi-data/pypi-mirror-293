import os
import argparse

def get_douroucouli_art(name):
    """Fetch the ASCII art for the specified douroucouli."""
    current_dir = os.path.dirname(__file__)
    asset_path = os.path.join(current_dir, 'assets', f'{name}.txt')
    with open(asset_path, 'r') as file:
        return file.read()

def create_speech_bubble(message):
    """Create a speech bubble around the message."""
    lines = message.splitlines()
    width = max(len(line) for line in lines)
    border = '-' * (width + 2)
    
    bubble = f"  {border}\n"
    for line in lines:
        bubble += f" < {line.ljust(width)} >\n"
    bubble += f"  {border}"
    
    return bubble

def douroucoulisay(message, douroucouli='douroucouli1'):
    """Print the message with the selected douroucouli ASCII art."""
    try:
        douroucouli_art = get_douroucouli_art(douroucouli)
    except FileNotFoundError:
        raise ValueError(f"Douroucouli '{douroucouli}' not found.")
    
    bubble = create_speech_bubble(message)
    print(f"\n{bubble}\n\n{douroucouli_art}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="douroucoulisay: Print a message with douroucouli ASCII art.")
    parser.add_argument("message", type=str, help="The message to display.")
    parser.add_argument("-d", "--douroucouli", type=str, default="douroucouli1", help="The douroucouli to use (default: douroucouli1).")
    
    args = parser.parse_args()
    douroucoulisay(args.message, args.douroucouli)
