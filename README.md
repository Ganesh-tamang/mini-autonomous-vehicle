# small-autonomous-vehicle
This is a prototype for small autonomous vehicle.

Run: 
Run the main.py 

<div>
  <p>
    <a align="center" href="https://github.com/Ganesh-tamang/small-autonomous-vehicle" target="_blank">
  </p>

<br>

<div>


# Install

Clone repo and install [requirements.txt](https://github.com/Ganesh-tamang/small-autonomous-vehicle/requirements.txt)

```bash
https://github.com/Ganesh-tamang/small-autonomous-vehicle.git
cd small-autonomous-vehicle
pip install -r requirements.txt  # install
```

# STEPS TODO:
1. Camera calibration: Take 20 pictures of chess board from your camera and place the images in images folder. Then, Run camera_calibrate.ipynd as saved camera matrix
2. Copy camera matrix to main/camera.py
3. Plaxe your camera to suitable position such that it shows your lane properly 
4. Take 4 points of your lane and copy it in src and dst matrix in camera.py perspective transform function
5. run main.py
