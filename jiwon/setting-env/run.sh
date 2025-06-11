sudo podman run --rm -it --privileged \
  --security-opt label=type:unconfined_t \
  -v $(pwd)/output:/output \
  -v $(pwd)/config.toml:/config.toml:ro \
  -v /var/lib/containers/storage:/var/lib/containers/storage \
  quay.io/centos-bootc/bootc-image-builder:latest \
  --type iso \
  --config /config.toml \
  --local \
  localhost/bootc:v1