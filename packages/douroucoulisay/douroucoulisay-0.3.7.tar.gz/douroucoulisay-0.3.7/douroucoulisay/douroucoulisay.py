import os
import argparse
import random
import textwrap

def get_douroucouli_art(name):
    """Fetch the ASCII art for the specified douroucouli."""
    current_dir = os.path.dirname(__file__)
    asset_path = os.path.join(current_dir, 'assets', f'{name}.txt')
    if not os.path.exists(asset_path):
        raise FileNotFoundError(f"Asset file '{asset_path}' not found.")
    with open(asset_path, 'r') as file:
        return file.read()

def wrap_text(message, width=40):
    """Wrap the text to the specified width."""
    return textwrap.fill(message, width=width)

def create_speech_bubble(message, width=40):
    """Create a speech bubble around the message."""
    wrapped_message = wrap_text(message, width)
    lines = wrapped_message.splitlines()
    max_width = max(len(line) for line in lines)
    border = '-' * (max_width + 2)
    
    bubble = f"  {border}\n"
    for line in lines:
        bubble += f" < {line.ljust(max_width)} >\n"
    bubble += f"  {border}"
    
    return bubble

def get_random_douroucouli():
    """Randomly select a douroucouli ASCII art file from the assets directory."""
    current_dir = os.path.dirname(__file__)
    assets_dir = os.path.join(current_dir, 'assets')
    files = [f for f in os.listdir(assets_dir) if f.endswith('.txt')]
    if not files:
        raise FileNotFoundError("No douroucouli files found in assets directory.")
    random_file = random.choice(files)
    return os.path.splitext(random_file)[0]

def douroucoulisay(message, douroucouli=None, width=40):
    """Print the message with the selected or randomized douroucouli ASCII art."""
    if douroucouli is None:
        douroucouli = get_random_douroucouli()
    
    try:
        douroucouli_art = get_douroucouli_art(douroucouli)
    except FileNotFoundError:
        raise ValueError(f"Douroucouli '{douroucouli}' not found.")
    
    bubble = create_speech_bubble(message, width)
    print(f"\n{bubble}\n\n{douroucouli_art}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print a message with douroucouli ASCII art.")
    parser.add_argument("message", type=str, help="The message to display.")
    parser.add_argument("-d", "--douroucouli", type=str, help="The douroucouli to use. If not specified, a random one will be chosen.")
    parser.add_argument("-w", "--width", type=int, default=40, help="The width to wrap the text (default: 40).")
    
    args = parser.parse_args()
    douroucoulisay(args.message, args.douroucouli, args.width)
