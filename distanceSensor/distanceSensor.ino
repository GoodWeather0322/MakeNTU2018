#include <Ultrasonic.h> //　使用超音波的程式庫
#include <Servo.h>
#define TRIGGER_PIN 12 //　定義模組triger端為數位接腳12
#define ECHO_PIN 11 //　定義模組echo端為數位接腳11
Servo myservo;  // 建立一個 servo 物件，最多可建立 12個 servo
Servo myservo2;  // 建立一個 servo 物件，最多可建立 12個 servo
int pos = 0;    // 設定 Servo 位置的變數*
int LED=7;
Ultrasonic ultrasonic(TRIGGER_PIN, ECHO_PIN); //設定HC-SR04初始化參數
void setup()
{
Serial.begin(9600);

myservo.attach(9);  // 將 servo 物件連接到 pin 9
myservo2.attach(8);  // 將 servo 物件連接到 pin 9
}

void loop()
{
float cmMsec; //　定義浮動數
long microsec = ultrasonic.timing(); //　 測距，返回的是一個時間單位(microsec)

cmMsec = ultrasonic.convert(microsec,Ultrasonic::CM); //將測得的時間單位計算為距離單位
//Serial.print(" CM: ");
//Serial.println(cmMsec);
     pos = 90;
    myservo.write(pos);               // 告訴 servo 走到 'pos' 的位置
    myservo2.write(180);               // 告訴 servo 走到 'pos' 的位置
    //delay(15); 
if(cmMsec<20){
    pos = 180;
    myservo.write(pos);               // 告訴 servo 走到 'pos' 的位置
    myservo2.write(90);               // 告訴 servo 走到 'pos' 的位置
    Serial.println('y');
    delay(3000);                        // 等待 15ms 讓 servo 走到指定位
}
else{
     pos = 90;
    myservo.write(pos);               // 告訴 servo 走到 'pos' 的位置
    myservo2.write(180);               // 告訴 servo 走到 'pos' 的位置
    //Serial.println(cmMsec);
    //delay(15);  
}

    if (Serial.read()=='H') {digitalWrite(LED, HIGH);
    delay(3000);  
    
    }
    else {digitalWrite(LED, LOW);}

}
