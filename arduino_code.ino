'''
Things that happens in arduino are
1. run ultrasonic to detect obstacles
2. read steering and throtle signal from raspberry pi
Types of message send from raspberry pi 
1. "s" for stop
2. "g" for go
3. "w" for move
4. "a" for left steering 
5. "d" for right steering
'''






#define rear_pwm_pin1 11 // left rear wheel pwm pin
#define rear_pwm_pin2 10 // right rear wheel pwm pin
#define front_leftpwm_pin 5
#define front_rightpwm_pin 6

#define decrease_rate 20;
const int triggerPin = 2; // Trigger Pin of Ultrasonic Sensor
const int echoPin = 3; // Echo Pin of Ultrasonic Sensor
long duration, inches, cm;

//initial move_pwm value 
//-----change pwm value as you want 
int move_pwm = 150;
int steer_pwm = 130;
//flags
bool isStop = false;

bool ultra_stop = false; // is car stop due to ultrasonic
char raspberry_value; // value save from raspberry pi
int pwm_value;

void setup() {
  Serial.begin(115200);
  while(!Serial){}
  pinMode(triggerPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(rear_pwm_pin1, OUTPUT) ;
  pinMode(rear_pwm_pin2, OUTPUT) ;  
  pinMode(front_leftpwm_pin, OUTPUT) ;
  pinMode(front_rightpwm_pin, OUTPUT) ;
}//setup end
void loop() {
  //run ultrasonic
  ultra_sonic();
  // read input from pi
  if(Serial.available() > 0){
    raspberry_value = char(Serial.read());
    } 
  
  if ((isStop== false) && ( raspberry_value== char('s') )) {  // raspberry pi send 's' to stop the car
      isStop =  true;
      stop();   
  }
  if(!ultra_stop){ //run only when no obstacle is present 
    if (raspberry_value==char('g')){     // accelerate only when car is in stop position
        isStop =  false;
        move_pwm = 150;
        move(move_pwm);
      } 
    if ((isStop== false) && ( raspberry_value== char('u') )) {
        move_pwm = 100;
        move(move_pwm);
      }
    if ((isStop== false) && ( raspberry_value== char('w') )) {   
        move(move_pwm);
      }
      if ((isStop== false) &&(raspberry_value==char('a'))){
        left_steering(steer_pwm);
      } 
      if ((isStop== false) &&(raspberry_value==char('d'))){
        right_steering(steer_pwm);
      } 
  }//end of not ultra_stop 
}//loop end

//calculate the distance of obstacle from the car in cm
long microsecondsToCentimeters(long microseconds) {
   return microseconds / 29 / 2;
}

//left steering function
void left_steering(int left_pwm){ 
  //send pwm only to left rear and front motor
  analogWrite(front_leftpwm_pin, 0);
  analogWrite(front_rightpwm_pin, left_pwm);
   
  analogWrite(rear_pwm_pin1, 80);
  analogWrite(rear_pwm_pin2, left_pwm);
  
}// left steering end

void right_steering(int right_pwm){
  //send pwm only to right rear and front motor
  analogWrite(front_leftpwm_pin, right_pwm);
  analogWrite(front_rightpwm_pin, 20);
  analogWrite(rear_pwm_pin2, 0);
  analogWrite(rear_pwm_pin1, right_pwm);
  
}

void stop(){
   // send 0 pwm value to all motors
  analogWrite(rear_pwm_pin1, 0);
  analogWrite(rear_pwm_pin2, 0);
  analogWrite(front_leftpwm_pin, 0);
  analogWrite(front_rightpwm_pin, 0);
  
 }

void move(int pwm){
  // send pwm values only to the rear motors
  analogWrite(rear_pwm_pin1, pwm);
  analogWrite(rear_pwm_pin2, pwm);
  analogWrite(front_leftpwm_pin, 0);
  analogWrite(front_rightpwm_pin, 0);
}
void ultra_sonic(){
  // stop the car only when the obstacle is with in 30 cm 
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  cm = microsecondsToCentimeters(duration);
  if(cm >0){
    if(cm< 30 ) {
         stop(); 
         ultra_stop = true; 
         Serial.println("cm = {cm}");
         Serial.println(cm);
       }
     else {
        if(ultra_stop){
          ultra_stop = false;
          }
       }
  }
}
