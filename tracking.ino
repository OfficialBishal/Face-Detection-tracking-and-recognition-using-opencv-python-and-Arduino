//by Bishal Shrestha
//header...call function library
#include <Servo.h> 

Servo servo;
Servo servoy;

// User input for servo and position
int UserIn[3];    // raw input from serial buffer, 3 bytes
int ini_byt;       // start byte, begin reading input//initial byte
int servo_num;           // which servo to pulse?
int pos;             // servo angle 0-180
int i;               // iterator
int t=90;    //variable to move to according angle
int u=120;
 

// Common servo setup values
int mini_Pul = 600;   // minimum servo position, us (microseconds)
int maxi_Pul = 2400;  // maximum servo position, us



void setup() 
{   
  servo.attach(9, mini_Pul, maxi_Pul); // Attach each Servo object to a digital pin
  servoy.attach(10, mini_Pul, maxi_Pul); // Attach each Servo object to a digital pin
  Serial.begin(9600); // Open the serial connection, 9600 baud

  servoy.write(u);
  servo.write(t);
} 



void loop() 
{ 
  if (Serial.available() > 0) // Wait for serial input (min 3 bytes in buffer)
    {                 //Serial.println("Inside");

  
      pos = Serial.read();// Read the first byte
     
//      if (ini_byt == 58) // If it's really the startbyte (25
//                UserIn[i] = Serial.read();
//              }
//          servo_num = UserIn[0];// First byte = servo to move?          
//          pos = UserIn[1];// Second byte = which position?          
//          if (pos == 255) // Packet error checking and recovery
//              { 
//                servo_num = 255; 
//                Serial.println("Moving0");
//              }
    // ----------X-axis--------------
          if (pos==49 || pos==1)//1=49
            {
              t=t+3;
              servo.write(t); 
            }
         else if (pos==50)//2=50
           {
             t=t-3;
             
             servo.write(t);
           }  
           else if (pos==48)
          {
            servo.write(t);
          }
      // ----------Y-axis--------------
           else if (pos==51)//3=51
           {
             u=u-5;
             servoy.write(u);
           } 
           else if (pos==52)//4=52
           {
             u=u+5;
             servoy.write(u);
           } 
           else if (pos==53)//5=53
           {
             servoy.write(u);
           } 
           
         
           Serial.flush();
//        }
    }
}
