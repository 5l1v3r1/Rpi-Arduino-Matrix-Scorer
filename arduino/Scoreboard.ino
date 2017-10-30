/*
Scoreboard sketch for arduino

v0.0.5: v0.0.4 failed and turned to shit, now using String instead of char* to avoid memory corruption
- added a working Split() function that returns a specified element from a list. YUUS.

v0.0.6: attempts to implement a timer, and removed the Serial communication for now until it 
is tested that the memory no longer overflows.

v0.1.0: add serial communication and some position tweaks, still on 3x2 layout

v0.1.2: 
- Now moving onto 3x3, and attempts to implement a new function to check for the validity of
the different data before putting it on the display.

- Founm that the timer is too slow and inaccurate, due to the execution time of the code before. I will try
to put it as far up the loop() as possible.

v1.2.1:
- 1.2 implemented a lot of good "safety filters" for the inputted data, however this proved that the 
data is not reliable at all now that they are checked.
- so 1.2.1 is a "redo" from 1.1 putting it into 3x3 for a start.

v0.1.3
- read the code from http://buildyourownscoreboard.wordpress.com/downloads and found that they
have used a reliable serial comms libary !! called cmdMessenger!! grabbed it and it should solve the 
serial communications issue. *PHeeeeeeeeeeeeeeeeeew*
- redo the code with char arrays to save RAM

v0.2.0
- 1.3 kinda failed, rewriting from the properly timed out Example code of CmdMessenger
- Now Serial communications is working, but havn't added in the DMD displays yet.
- also changed the SVN system so that every version is now a "minor" version, since none of
them properly function yet... haha

v0.2.1
- turns out that CmdMessenger doesn't work when the Arduino is driving the scoreboards at the same time..
Uggh.. Saw the post http://forum.freetronics.com/viewtopic.php?t=5685#p13155 and now going to try with
a lower baud rate to see what happens.
- Serial communications now stable with 2400 baud rate. Just one more issue to solve -- the (in)accuracy of the timer.

0.2.2
- Serial communication now stable, so I will get rid of the spare bits of code from the example
of CmdMessenger.
- Also tries to test what could be delaying the timer by commenting out the pause/resume management code.
- added mathmetical model for accurate timing, altho it "skips" time. This will do for now.

0.3.0:
- Now testing for a new solution for the clock: to implement it on the Raspberry Pi side and update the time
via serial input
- Removed taking the pause variable from the serial input as it is no longer needed.
- Commented out uneccesarry serial comms to make the program run faster
- Made m a buffer of [4] because minutes can go up to 3 digits.
- removed the TwoDigits() function as it will be handled on the Raspberry Pi side, and
plus the String operations take more memory and processing so it might make the program run slower.
- Changed timestr to a char array to save memory, and now storing it as a local variable in loop()

0.3.1: adjusting different settings to make the program more robust.
- 

author: Haoxi Tan
*/

// This example demonstrates CmdMessenger's callback  & attach methods
// For Arduino Uno and Arduino Duemilanove board (may work with other)

// Download these into your Sketches/libraries/ folder...

// CmdMessenger library available from https://github.com/dreamcat4/cmdmessenger
#include <CmdMessenger.h>

// Base64 library available from https://github.com/adamvr/arduino-base64
#include <Base64.h>

// Streaming4 library available from http://arduiniana.org/libraries/streaming/
#include <Streaming.h>


//components of the DMD library and the stopwatch
#include <StopWatch.h>
#include <DMD2.h>
#include <SPI.h>
//fonts to display
#include <fonts/SystemFont5x7.h>
#include <fonts/Droid_Sans_16.h>
#include <fonts/Droid_Sans_24.h>


// Mustnt conflict / collide with our message payload data. Fine if we use base64 library ^^ above
char field_separator = ',';
char command_separator = ';';

// Attach a new CmdMessenger object to the default Serial port
CmdMessenger cmdMessenger = CmdMessenger(Serial, field_separator, command_separator);
SoftDMD dmd(3,3); //DMD controls the entire displaySoftDMD dmd(3,3); //DMD controls the entire display
StopWatch timer(StopWatch::SECONDS); //initiates stopwatch in seconds

//variables
char team1[4],team2[4],score1[3],score2[3],m[4],s[3];  //use char arrays with limited size to save memory.

// ------------------ C M D  L I S T I N G ( T X / R X ) ---------------------

// We can define up to a default of 50 cmds total, including both directions (send + recieve)
// and including also the first 4 default command codes for the generic error handling.
// If you run out of message slots, then just increase the value of MAXCALLBACKS in CmdMessenger.h

// Commands we send from the Arduino to be received on the PC
enum
{
  kCOMM_ERROR    = 000, // Lets Arduino report serial port comm error back to the PC (only works for some comm errors)
  kACK           = 001, // Arduino acknowledges cmd was received
  kARDUINO_READY = 002, // After opening the comm port, send this cmd 02 from PC to check arduino is ready
  kERR           = 003, // Arduino reports badly formatted cmd, or cmd not recognised

  // Now we can define many more 'send' commands, coming from the arduino -> the PC, eg
  // kICE_CREAM_READY,
  // kICE_CREAM_PRICE,
  // For the above commands, we just call cmdMessenger.sendCmd() anywhere we want in our Arduino program.

  kSEND_CMDS_END, // Mustnt delete this line
};

// Commands we send from the PC and want to recieve on the Arduino.
// We must define a callback function in our Arduino program for each entry in the list below vv.
// They start at the address kSEND_CMDS_END defined ^^ above as 004
messengerCallbackFunction messengerCallbacks[] = 
{
  updateInfo, //004
  updateTime, //005
  NULL
};
// Its also possible (above ^^) to implement some symetric commands, when both the Arduino and
// PC / host are using each other's same command numbers. However we recommend only to do this if you
// really have the exact same messages going in both directions. Then specify the integers (with '=')


// ------------------ C A L L B A C K  M E T H O D S -------------------------


void updateInfo()
{
  /*
  uses the CmdMessenger class to receive and update data for the scoreboard.
  Basically everytime data is sent from the computer/serial server it loops over the data by
  each field separator, until the command separator is found. If copyString() is only called once, 
  it copies all data into the buffer. However, if it is called 2 times, it splits the data by the first field separator. So by calling it
  5 times, it loops over the data string of (<command number>,<team1>,<team2>,<score1>,<score2>,<pause> perfectly
  and store the data into respective variables.
  
  the use of a local buffer buf[4] here limits the buffer size and saves memory, as a String object has no size limit therefore takes up
  more memory.
  */
  
  ;
  // Message data is any ASCII bytes (0-255 value). But can't contain the field
  // separator, command separator chars you decide (eg ',' and ';')
  cmdMessenger.sendCmd(kACK,"updateInfo cmd recieved");
  while ( cmdMessenger.available() )
  {
    static char buf[4] = {'\0'};
    
    //team1
   cmdMessenger.copyString(buf, 4);
   strcpy(team1,buf);
   //cmdMessenger.sendCmd(kACK, team1);
   
   //team2 
   memset(buf, '\0', 4);  //memset resets the buffer
   cmdMessenger.copyString(buf,4);
   strcpy(team2,buf); 
   //cmdMessenger.sendCmd(kACK, team2);
   
   //score1
   memset(buf, '\0', 3); //3 to prevent numbers from going to 2 (+1 for trailing nullbyte)
   cmdMessenger.copyString(buf,3);
   strcpy(score1,buf);
   //cmdMessenger.sendCmd(kACK, score1);
   
   //score2
   memset(buf, '\0', 3);
   cmdMessenger.copyString(buf,3);
   strcpy(score2,buf);
   //cmdMessenger.sendCmd(kACK, score2);
   
   //refresh the display for clearing out extra dots
   dmd.clearScreen();
  }
}
  
  
void updateTime()
{ /*
  updates the time on the board by retrieving it from the serial port
  every second. Works the same way as updateInfo(), however it doesn't 
  refresh the screen as the font for the timer doesn't leave 'residues' (it's monospace)
  */  
  
  static char buf[4] = {'\0'};  //size is string length +1
  
  //minutes
  cmdMessenger.copyString(buf, 4);
  strcpy(m,buf);
  //cmdMessenger.sendCmd(kACK,m);
  
  //seconds
  memset(buf,'\0',3);
  cmdMessenger.copyString(buf,3);
  strcpy(s,buf);
  //cmdMessenger.sendCmd(kACK,s);
  
}
  
// ------------------ D E F A U L T  C A L L B A C K S -----------------------

void arduino_ready()
{
  // In response to ping. We just send a throw-away Acknowledgement to say "im alive"
  cmdMessenger.sendCmd(kACK,"Arduino ready");
}

void unknownCmd()
{
  // Default response for unknown commands and corrupt messages
  cmdMessenger.sendCmd(kERR,"Unknown command");
  
}

// ------------------ E N D  C A L L B A C K  M E T H O D S ------------------



// ------------------ S E T U P ----------------------------------------------

void attach_callbacks(messengerCallbackFunction* callbacks)
{
  int i = 0;
  int offset = kSEND_CMDS_END;
  while(callbacks[i])
  {
    cmdMessenger.attach(offset+i, callbacks[i]);
    i++;
  }
}


void setup() 
{
  
  timer.start();
  dmd.selectFont(SystemFont5x7); //set this font to default
  dmd.setBrightness(255); //max out brightness
  dmd.begin(); //begin dmd display
  
  // Listen on serial connection for messages from the pc
  Serial.begin(1200); 

  // cmdMessenger.discard_LF_CR(); // Useful if your terminal appends CR/LF, and you wish to remove them
  cmdMessenger.print_LF_CR();   // Make output more readable whilst debugging in Arduino Serial Monitor
  
  // Attach default / generic callback methods
  cmdMessenger.attach(kARDUINO_READY, arduino_ready);
  cmdMessenger.attach(unknownCmd);

  // Attach my application's user-defined callback methods
  attach_callbacks(messengerCallbacks);

  arduino_ready();

  // blink
  pinMode(13, OUTPUT);
  
  //copies 00 into both minutes and seconds buffer to initialize the timer
  strcpy(m,"00");
  strcpy(s,"00");
}


// ------------------ M A I N ( ) --------------------------------------------

// Timeout handling
long timeoutInterval = 400; // in milliseconds
long previousMillis = 0;
int counter = 0;

void timeout()
{
  // blink
  if (counter % 2)
    digitalWrite(13, HIGH);
  else
    digitalWrite(13, LOW);
  counter ++;
}  

void loop() 
{
  static char timestr[7]={'\0'}; //for displaying time
  
  // Process incoming serial data, if any
  cmdMessenger.feedinSerialData();
  strcpy(timestr,m); //the time is read instead from the serial input
  strcat(timestr,":");
  strcat(timestr,s);
  
  //Serial.println(timestr);
  //Serial.println(millis()/1000);
  
  dmd.selectFont(SystemFont5x7);
  dmd.drawString(33,2,timestr);
  dmd.selectFont(Droid_Sans_16);
  dmd.drawString(14,11,team1);
  dmd.drawString(56,11,team2);
  
  
  //dmd.drawString(45,9,"--"); //team separator using the same look as score separator
  int coords[2][6];
  for (int i = 0;i<6;i++)
  {
   dmd.setPixel(44+i,18);
   dmd.setPixel(44+i,19);
  }
  
  dmd.selectFont(Droid_Sans_24); //a bigger font for the score
  dmd.drawString(13,26,score1);
  dmd.drawString(44,24,"-");
  dmd.drawString(57,26,score2);
  
   if (  millis() - previousMillis > timeoutInterval )
  {
    timeout();
    previousMillis = millis();
  }

}

