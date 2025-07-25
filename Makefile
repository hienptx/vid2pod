# Name of the Docker image
IMAGE_NAME=yt-pipeline

# Docker build (with cache)
build:
	docker build -t $(IMAGE_NAME) -f api/Dockerfile api

# Force rebuild (no cache)
rebuild:
	docker build --no-cache -t $(IMAGE_NAME) -f api/Dockerfile api

# Run downloader.py inside the container
run-downloader:
	docker run --rm \
		-v $(PWD)/storage:/app/storage \
		$(IMAGE_NAME) \
		python pipeline/downloader.py

# Run transcriber.py inside container
run-transcriber:
	docker run --rm \
		-v $(PWD)/storage:/app/storage \
		-v $(PWD)/models:/app/models \
		$(IMAGE_NAME) \
		python pipeline/transcriber.py

# Run uvicorn app normally
run-api:
	docker run --rm -p 8000:8000 \
		-v $(PWD)/storage:/app/storage \
		$(IMAGE_NAME)

# Clean unused Docker images (optional)
clean-docker:
	docker system prune -f

# Help
help:
	@echo "Makefile targets:"
	@echo "  build           - Build Docker image with cache"
	@echo "  rebuild         - Build Docker image without cache"
	@echo "  run-downloader  - Run downloader.py script inside container"
	@echo "  run-api         - Run FastAPI app with uvicorn"
	@echo "  clean-docker    - Prune unused Docker images"
