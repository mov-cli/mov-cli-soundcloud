<div align="center">

  # mov-cli-soundcloud
  <sub>A mov-cli v4 plugin for playing soundcloud.</sub>

</div>

## Installation 🛠️
Here's how to install and add the plugin to mov-cli.

1. Install the package.
### PIP
```sh
pip install mov-cli-soundcloud
```

### AUR
```
yay -S python-mov-cli-soundcloud
```
2. Then add the plugin to your mov-cli config.
```sh
mov-cli -e
```
```toml
[mov-cli.plugins]
soundcloud = "mov-cli-soundcloud"
```

## Usage 🖱️
```sh
mov-cli -s soundcloud sakuro
```
