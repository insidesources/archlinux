import os
import subprocess

def run_command(command):
    """Run a shell command."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f"Command failed: {stderr.decode().strip()}")
    return stdout.decode().strip()

def run_command_interactive(command):
    """Run a shell command with interaction."""
    subprocess.run(command, shell=True)

def install_yay():
    """Clone yay and install it, allowing for interactive prompts."""
    print("Installing yay...")
    run_command_interactive("git clone https://aur.archlinux.org/yay.git")
    os.chdir("yay")
    run_command_interactive("makepkg -si")
    os.chdir("..")
    run_command("rm -rf yay")
    print("yay installed successfully.")

def install_blackarch():
    """Install BlackArch."""
    print("Installing BlackArch...")
    run_command("curl -O https://blackarch.org/strap.sh")
    run_command("echo 3f121404fd02216a053f7394b8dab67f105228e3 strap.sh | sha1sum -c")
    run_command("chmod +x strap.sh")
    run_command_interactive("sudo ./strap.sh")
    run_command("rm strap.sh")
    print("BlackArch installed successfully.")

def install_packages(category, packages):
    """Install packages from a given category."""
    response = input(f"Do you want to install {category} packages? (yes/no): ").lower()
    if response.startswith('y'):
        for package in packages:
            print(f"Installing {package}...")
            run_command(f"yay -S {package}")
    elif response.startswith('n'):
        print(f"Skipping installation of {category} packages.")
            
def clone_and_copy_repo():
    """Clone a GitHub repository and copy its contents to the home directory interactively."""
    print("Cloning GitHub repository...")
    run_command("git clone https://github.com/insidesources/archlinux.git")
    os.chdir("archlinux")
    print("Copying files to the home directory...")
    run_command_interactive("sudo cp -ri . ~/")

def main():
    try:
        install_yay()
        install_blackarch()

        # Package lists
        core_packages = ["linux-zen-headers", "sxiv", "firefox", "bitwarden", "krusader", "alacritty", "kvantum", "qt5ct", "qt6ct", "ttf-nerd-fonts-symbols-mono",
                        "noto-fonts-emoji", "arc-gtk-theme", "arc-icon-theme", "discord", "betterdiscord-installer-bin", "brave-bin", "debtap", "dunst", "easyeffects",
                        "glances", "mc", "google-chrome", "gotop", "ledger-live-bin", "lxappearance", "lynx", "mysql-workbench", "neofetch",
                        "neovim", "nitrogen", "noisetorch", "notepadqq", "notion-app-enhanced", "nvidia-settings", "nvtop", "obs-studio", "obsidian", "onlyoffice-bin",
                        "openrgb", "openvpn", "pavucontrol", "picom", "postman-bin", "powershell-bin", "protonmail-bridge-bin", "protonvpn", "proxychains-ng", "qbittorrent",
                        "qflipper", "qtile-extras", "qutebrowser", "rofi", "rofi-power-menu-git", "rpi-imager", "scrot", "solaar", "spicetify-cli", "spotify",
                        "streamdeck-ui", "tailscale", "teamviewer", "telegram-desktop", "termius", "thunderbird", "tmux", "tor", "torbrowser-launcher", "tradingview",
                        "unicode-character-database", "unicode-emoji", "visual-studio-code-bin", "vlc", "vmware-workstation", "weechat", "xorg-xrandr", "xreader", "zerotier-one", "zoom",
                        "zsh", "man"]
        
        cybersecurity_tools = ["dnsrecon", "exploitdb", "hydra", "metasploit", "ngrok", "nmap", "phonesploit", "punter", "recon-ng", "set",
                        "sublist3r", "thefatrat", "theharvester", "wireshark-qt", "wpscan"]
        
        games = ["steam", "lutris", "curseforge", "strongbox", "proton-ge-custom-bin"]

        install_packages("core packages", core_packages)
        install_packages("cybersecurity tools", cybersecurity_tools)
        install_packages("games", games)
        
        clone_and_copy_repo()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()