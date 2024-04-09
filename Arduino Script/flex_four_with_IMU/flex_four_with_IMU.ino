#include <Adafruit_MPU6050.h>

#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

int flexpin0 = A0; // index
int flexpin1 = A1; // middle
int flexpin2 = A2; // ring
int flexpin3 = A3; // pinky

void setup() {
  Serial.begin(9600);
  Serial.println("Initialize MPU6050");

  // Initialize MPU6050
  while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G))
  {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }

  // Calibrate gyroscope. The calibration must be at rest.
  mpu.calibrateGyro();

  // Check settings for both accelerometer and gyroscope
  checkAccelSettings();
  checkGyroSettings();
}

void checkAccelSettings()
{
  Serial.println();
  
  Serial.print(" * Sleep Mode:            ");
  Serial.println(mpu.getSleepEnabled() ? "Enabled" : "Disabled");
  
  Serial.print(" * Clock Source:          ");
  switch(mpu.getClockSource())
  {
    case MPU6050_CLOCK_KEEP_RESET:     Serial.println("Stops the clock and keeps the timing generator in reset"); break;
    case MPU6050_CLOCK_EXTERNAL_19MHZ: Serial.println("PLL with external 19.2MHz reference"); break;
    case MPU6050_CLOCK_EXTERNAL_32KHZ: Serial.println("PLL with external 32.768kHz reference"); break;
    case MPU6050_CLOCK_PLL_ZGYRO:      Serial.println("PLL with Z axis gyroscope reference"); break;
    case MPU6050_CLOCK_PLL_YGYRO:      Serial.println("PLL with Y axis gyroscope reference"); break;
    case MPU6050_CLOCK_PLL_XGYRO:      Serial.println("PLL with X axis gyroscope reference"); break;
    case MPU6050_CLOCK_INTERNAL_8MHZ:  Serial.println("Internal 8MHz oscillator"); break;
  }
  
  Serial.print(" * Accelerometer:         ");
  switch(mpu.getRange())
  {
    case MPU6050_RANGE_16G:            Serial.println("+/- 16 g"); break;
    case MPU6050_RANGE_8G:             Serial.println("+/- 8 g"); break;
    case MPU6050_RANGE_4G:             Serial.println("+/- 4 g"); break;
    case MPU6050_RANGE_2G:             Serial.println("+/- 2 g"); break;
  }  

  Serial.print(" * Accelerometer offsets: ");
  Serial.print(mpu.getAccelOffsetX());
  Serial.print(" / ");
  Serial.print(mpu.getAccelOffsetY());
  Serial.print(" / ");
  Serial.println(mpu.getAccelOffsetZ());
  
  Serial.println();
}

void checkGyroSettings()
{
  Serial.println();
  
  Serial.print(" * Sleep Mode:        ");
  Serial.println(mpu.getSleepEnabled() ? "Enabled" : "Disabled");
  
  Serial.print(" * Clock Source:      ");
  switch(mpu.getClockSource())
  {
    case MPU6050_CLOCK_KEEP_RESET:     Serial.println("Stops the clock and keeps the timing generator in reset"); break;
    case MPU6050_CLOCK_EXTERNAL_19MHZ: Serial.println("PLL with external 19.2MHz reference"); break;
    case MPU6050_CLOCK_EXTERNAL_32KHZ: Serial.println("PLL with external 32.768kHz reference"); break;
    case MPU6050_CLOCK_PLL_ZGYRO:      Serial.println("PLL with Z axis gyroscope reference"); break;
    case MPU6050_CLOCK_PLL_YGYRO:      Serial.println("PLL with Y axis gyroscope reference"); break;
    case MPU6050_CLOCK_PLL_XGYRO:      Serial.println("PLL with X axis gyroscope reference"); break;
    case MPU6050_CLOCK_INTERNAL_8MHZ:  Serial.println("Internal 8MHz oscillator"); break;
  }
  
  Serial.print(" * Gyroscope:         ");
  switch(mpu.getScale())
  {
    case MPU6050_SCALE_2000DPS:        Serial.println("2000 dps"); break;
    case MPU6050_SCALE_1000DPS:        Serial.println("1000 dps"); break;
    case MPU6050_SCALE_500DPS:         Serial.println("500 dps"); break;
    case MPU6050_SCALE_250DPS:         Serial.println("250 dps"); break;
  } 
  
  Serial.print(" * Gyroscope offsets: ");
  Serial.print(mpu.getGyroOffsetX());
  Serial.print(" / ");
  Serial.print(mpu.getGyroOffsetY());
  Serial.print(" / ");
  Serial.println(mpu.getGyroOffsetZ());
  
  Serial.println();
}

void loop() {
  // Declearing variables
  int index; // A0
  int middle; // A1
  int ring; // A2
  int pinky; // A3

  // Getting analog ping value and storing it in variables
  index = analogRead(flexpin0);
  middle = analogRead(flexpin1);
  ring = analogRead(flexpin2);
  pinky = analogRead(flexpin3);

  // Reading MPU6050 data
  Vector rawAccel = mpu.readRawAccel();
  Vector normAccel = mpu.readNormalizeAccel();
  Vector rawGyro = mpu.readRawGyro();
  Vector normGyro = mpu.readNormalizeGyro();

  // Print flex sensor readings
  // Serial.println("Flex Sensor Readings:");
  //==========================================================================
  // Serial.print("Index: ");
  Serial.print(index);
  Serial.print(",");
  // Serial.print(" Middle: ");
  Serial.print(middle);
  Serial.print(",");
  // Serial.print(" Ring: ");
  Serial.print(ring);
  Serial.print(",");
  // Serial.print(" Pinky: ");
  Serial.print(pinky);
  Serial.print(",");

  // Print accelerometer data
  // Serial.println("Accelerometer Data:");
  // Serial.print(" Accelerometer Xraw = ");
  Serial.print(rawAccel.XAxis);
  Serial.print(",");
  // Serial.print(" Accelerometer Yraw = ");
  Serial.print(rawAccel.YAxis);
  Serial.print(",");
  // Serial.print(" Accelerometer Zraw = ");
  Serial.print(rawAccel.ZAxis);
  Serial.print(",");
  //=====================================
  // Serial.print(" Accelerometer Xnorm = ");
  Serial.print(normAccel.XAxis);
  Serial.print(",");
  // Serial.print(" Accelerometer Ynorm = ");
  Serial.print(normAccel.YAxis);
  Serial.print(",");
  // Serial.print(" Accelerometer Znorm = ");
  Serial.print(normAccel.ZAxis);
  Serial.print(",");
  
  // Print gyroscope data
  // Serial.println("Gyroscope Data:");
  // Serial.print(" Gyroscope Xraw = ");
  Serial.print(rawGyro.XAxis);
  Serial.print(",");
  // Serial.print(" Gyroscope Yraw = ");
  Serial.print(rawGyro.YAxis);
  Serial.print(",");
  // Serial.print(" Gyroscope Zraw = ");
  Serial.print(rawGyro.ZAxis);
  Serial.print(",");
  //=====================================
  // Serial.print(" Gyroscope Xnorm = ");
  Serial.print(normGyro.XAxis);
  Serial.print(",");
  // Serial.print(" Gyroscope Ynorm = ");
  Serial.print(normGyro.YAxis);
  Serial.print(",");
  // Serial.print(" Gyroscope Znorm = ");
  Serial.print(normGyro.ZAxis);
  Serial.println();

  delay(1000);
}
