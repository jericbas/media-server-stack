# Media Server Stack

> **Note:** This project is created for personal use only. It is not intended for commercial deployment or redistribution.

A Docker Compose setup for a home media server, featuring qBittorrent for torrenting, Jellyfin for media streaming, and a custom monitoring dashboard to display system stats (disk space) and quick links to the services. The dashboard features a dynamic nature-themed background slideshow.

## Features

- **qBittorrent**: Web-based torrent client for downloading media.
- **Jellyfin**: Open-source media server for streaming movies, TV shows, and music.
- **Monitor Dashboard**:
  - Displays free disk space for `C:/Docker`.
  - Placeholder for PC temperature (requires host integration).
  - Quick links to qBittorrent and Jellyfin using the host's WLAN IP.
  - Random nature background images that slide every 5 seconds.
- **Docker Compose**: Easy deployment with a single configuration file.
- **Custom Network**: Isolated `media_network` for service communication.

## Prerequisites

- **Docker Desktop**: Installed and running on Windows (with WSL 2 or Hyper-V enabled).
- **Disk Space**: At least 10 GB free on `C:` for Docker volumes.
- **Network**: Access to the host's WLAN IP (e.g., `192.168.1.100`).
- **Permissions**: User with `PUID=1000` and `PGID=1000` (or adjust environment variables).

## Directory Structure

```text
media-server-stack/
├── docker-compose.yml
└── monitor/
    ├── Dockerfile
    ├── nginx.conf
    ├── app/
    │   └── app.py
    └── usr/share/nginx/html/
        └── index.html
```

## Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/jericbas/media-server-stack.git
   cd media-server-stack
   ```

2. **Create Docker Volumes Directory**:
   - Create `C:/Docker` on your Windows host.
   - Ensure subdirectories exist: `qbittorrent/config`, `qbittorrent/downloads`, `jellyfin/config`, `jellyfin/cache`, `jellyfin/media`.

   ```bash
   mkdir -p C:/Docker/qbittorrent/config C:/Docker/qbittorrent/downloads C:/Docker/jellyfin/config C:/Docker/jellyfin/cache C:/Docker/jellyfin/media
   ```

3. **Configure WLAN IP** (Optional):
   - Edit `docker-compose.yml` and set the `WLAN_IP` environment variable in the `monitor` service to your host's IP (e.g., `192.168.1.100`).
   - If unset, the dashboard will attempt to detect the IP dynamically (fallback: `192.168.1.100`).

4. **Run Docker Compose**:

   ```bash
   docker-compose up -d --build
   ```

5. **Access Services**:
   - **Monitor Dashboard**: `http://192.168.1.100`
   - **Jellyfin**: `http://192.168.1.100:8096`
   - **qBittorrent**: `http://192.168.1.100:8080`

## How to Run

1. Ensure Docker Desktop is installed and running on Windows.
2. Create the required directories:
   - C:/Docker/qbittorrent/config
   - C:/Docker/qbittorrent/downloads
   - C:/Docker/jellyfin/config
   - C:/Docker/jellyfin/cache
   - C:/Docker/jellyfin/media
3. (Optional) Edit `docker-compose.yml` to set your WLAN_IP if needed.
4. Open PowerShell in the project directory and run:

   ```powershell
   docker-compose up -d --build
   ```

5. Access the services in your browser:
   - Monitor Dashboard: http://[WLAN_IP]
   - Jellyfin: http://[WLAN_IP]:8096
   - qBittorrent: http://[WLAN_IP]:8080

> **Note:** For qBittorrent, the initial password is randomly generated. Check the container logs with:
>
> ```powershell
> docker-compose logs qbittorrent
> ```
>
> Look for a line like `INFO - qBittorrent password is: ...`.

## Usage

- **Monitor Dashboard**:
  - View free disk space for `C:/Docker`.
  - Click quick links to access Jellyfin or qBittorrent.
  - Toggle between light and dark themes.
  - Background images (nature-themed) change every 5 seconds.
- **Jellyfin**:
  - Configure media libraries to point to `/media` (maps to `C:/Docker/jellyfin/media`.
  - Access via the web interface to stream media.
- **qBittorrent**:
  - Download torrents to `/downloads` (maps to `C:/Docker/qbittorrent/downloads`.
  - Move completed media to `/media` for Jellyfin to access.

## Troubleshooting

- **Service Not Starting**:
  - Check logs: `docker-compose logs <service>` (e.g., `monitor`, `jellyfin`).
  - Ensure `C:/Docker` exists and is accessible.
- **Dashboard Links Not Working**:
  - Verify `WLAN_IP` in `docker-compose.yml` or update the fallback IP in `monitor/usr/share/nginx/html/index.html`.
- **Permission Issues**:
  - Adjust `PUID` and `PGID` in `docker-compose.yml` to match your user (run `id` on Linux or check Windows user SID).

## Security Notes

- The monitor dashboard is publicly accessible on port 80. For production, add authentication (e.g., Nginx basic auth).
- Ensure `C:/Docker` has appropriate permissions (owned by `PUID=1000`, `PGID=1000` or equivalent).
- Consider a reverse proxy with SSL for external access.

## Extending the Setup

- **Temperature Monitoring**:
  - Implement host-side temperature monitoring (e.g., Open Hardware Monitor on Windows) and mount data into the `monitor` container.
- **Additional Services**:
  - Add services like Radarr or Sonarr for automated media management.
- **Backup**:
  - Regularly back up `C:/Docker` to prevent data loss.

## API Endpoints

The Monitor Dashboard exposes the following API endpoints (served by the Flask app in `monitor/app/app.py`):

- `GET /api/disk` — Returns free disk space for `C:/Docker` in JSON format.
- `GET /api/temp` — Returns PC temperature (currently a placeholder; requires host integration).
- `GET /api/links` — Returns quick links to qBittorrent and Jellyfin using the configured WLAN IP.

> Note: Endpoints may be extended or changed as you customize the dashboard. See `monitor/app/app.py` for implementation details.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## Acknowledgments

- [LinuxServer.io](https://www.linuxserver.io/) for the qBittorrent image.
- [Jellyfin](https://jellyfin.org/) for the media server.
- [Unsplash](https://unsplash.com/) for royalty-free nature images.
