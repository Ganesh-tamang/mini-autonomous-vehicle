# small-autonomous-vehicle
This is a prototype for small autonomous vehicle.

<div>
  <p>
    <a align="center" href="https://github.com/Ganesh-tamang/small-autonomous-vehicle" target="_blank">
  </p>

<br>

<div>


# Install

Clone repo and install requirements.txt

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

# Future Enchancement:
1. Use Gps module to exactly know your location instead of using ip address
2. Use directions value to take turns at prescribed locations. 
 
    TIP: Take location value from Gps module and match it with location list,then turn left or right according to direction value

3. Calculate velocity of others cars in a road
4. Use more advanced tools like Radar, Lidar,Gps module etc 
