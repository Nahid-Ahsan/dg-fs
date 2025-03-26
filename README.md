

# Face Swap Tool (Image & Multi-Video Support)

This project provides a web-based interface for swapping faces in images and videos. It uses a custom face-swapping model and supports both image-to-image and image-to-multi-video modes. The app is fully containerized with Docker Compose for easy setup.

---

## 🚀 Features

- Swap a face from a source image onto:
  - A single target image
  - Multiple target videos
- Optional face enhancement for higher-quality results
- web interface for easy use
- Dockerized for portability and quick setup

---

## 🐳 Getting Started with Docker Compose

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/face-swap-tool.git
cd face-swap-tool
```

### 2. Build and Run with Docker Compose

```bash
docker-compose up --build
```

This command will:

- Build the Docker image
- Start the `faceswap` container
- Expose the app on [http://localhost:7860](http://localhost:7860)

### 3. Using the App

Once the container is running, open your browser and go to:

```
http://localhost:7860
```

Upload a source face image and either:

- A target image (for face-to-image swap)
- Multiple videos (for face-to-video swap)

Click **"Run Face Swap 🚀"** and view the results in the gallery!

---

## 📁 Output Files

The output (swapped images/videos) will be saved to:

```
./output_folder/
```

This is mounted inside the Docker container via a volume for persistent storage.

---

## 🛠 Project Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── ui.py
├── output_folder/      # Outputs are saved here (mounted as a volume)
└── README.md
```

---

## 🧼 Stopping and Cleaning Up

To stop the app:

```bash
docker-compose down
```

To remove all containers, networks, and volumes:

```bash
docker system prune -a --volumes
```

---

---
