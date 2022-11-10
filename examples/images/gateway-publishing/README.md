# [larsid/soft-iot-base:1.1.3-start](https://hub.docker.com/layers/larsid/soft-iot-base/1.1.3-start/images/sha256-1997ca6939ea88d6cb7c8cb7ebdc9c55cdcb735b7741acf73459dcb575cfa712?context=repo)

## Build image

1. With the terminal in the images directory, run:
   ```powershell
   docker build -t larsid/soft-iot-base:1.1.3-start . 
   ```
   
## Create and run docker image
   
```powershell
docker run -i -t -p 1883:1883 -p 8181:8181 -p 1099:1099 -p 8101:8101 -p 61616:61616 -p 44444:44444 larsid/soft-iot-base:1.1.3-start
```
