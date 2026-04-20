# My Dotfiles
These are my dotfiles, they're nothing special. They are specifically tailored for my personal system, so make sure to correctly change it to work for yours. The install instructions are also just made to help me remember how to reinstall everything for my system when I reinstall arch

# Install Guide
## Step 1: Grub
Move the "grub" file to /etc/default. Replace the old file.
## Step 2: mkinitcpio.conf
Edit /etc/mkinitcpio.conf.
Find the modules line, and change it to this:
'''
MODULES=(nvidia nvidia_modeset nvidia_uvm nvidia_drm)
'''
Next, run '''sudo mkinitcpio -P''' and '''sudo grub-mkconfig -o /boot/grub/grub.cfg'''
## Step 3: Install Packages
-Make sure you have yay installed
run '''yay -S --needed - < aur-pkglist.txt'''
run '''sudo pacman -S --needed - < pkglist.txt'''
## Step 4: Set Up System
Move the kitty, nvim, rofi, waybar, and hypr folders, as well as starship.toml to the ~/.config folder. Accept any replacements.
Make a ~/pics directory, and then make a subdirectory called ss. Also, move wallpaper folder into the ~/pics directory.
move the tools folder into ~
## Step 5: Install Extras
For photoshop: https://www.youtube.com/watch?v=aaTvRDsdy0s
More extras to come
