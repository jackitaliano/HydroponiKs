# HydroponiKs
__Goal:__ <br/>

OSU Engineering 1182 Design Project to produce a prototype for a project after doing market research, determining user needs, and evaluating how our idea meets those requirements. <br/>

<br />

__Awards:__ <br />

Chosen to represent our class at the OSU design showcase.

<br/>

__Components:__  <br/>

<ul>
  <li>Tkinter GUI </li>
  <li>Pyfirmata python library and Firmata Arduino firmware to connect GUI to hardware</li>
  <li>Data/schedule is stored and easily accessible </li>
  <li>JSON files contain all plant information and education modules for easy access to add or remove plants/modules </li>
  <li>MVC design pattern to easily change GUI view or have alternate forms of data collection </li>
</ul>

<br/>

__Overview:__ <br/>

 <ul> 
  <li><i>Scheduling</i>
    <ul>
      <li>Custom schedules for watering</li>
      <li>Load default schedules for selected plant types</li>
      <li>Toggle buttons on schedule allow for adding/removing times from schedule</li>
      <li>Manual controls for turning on and off watering</li>
    </ul>
  </li>
  <li><i>Plant Information</i>
    <ul>
      <li>Select plant type from drop down menu</li>
      <li>Selected plant type determines information displayed on screen inclduing a description of the plant, its watering needs, and its nutrients needs</li>
    </ul>
  </li>
  <li><i>Education Modules</li>
    <ul>
      <li>Display education modules including an overview of STEM, the applications of STEM, and how you can impact your community with STEM</li>
    </ul>
  </li>
  <li><i>Arduino</li>
    <ul>
     <li>Turns water pump on and off based on current active schedule </li>
     <li>Gets water level of hydroponics reservoir, sends alert if water is low and prevents pump from turning on</li>
     <li>Protection against arduino disconnection</li>
    </ul>
  </li>
 </ul>
 
 __How to use:__ <br/>
 <ol>
  <li>Run "pip install /your_path/config/requirements.txt" in command line</li>
  <li>Ensure config/arduino_config "active" set to FALSE (unless proper Arduino is connected)</li>
  <li>Run app.py</li>
 </ol>
 
 __Screenshots:__ <br/>
 
<img width="1012" alt="schedule_img" src="https://user-images.githubusercontent.com/93797825/164543920-d3c7174d-5e55-4e72-8fb3-967aa71e5b4e.png"> 
 
<img width="1012" alt="selection_img" src="https://user-images.githubusercontent.com/93797825/164543736-dbf8141a-62ea-4bf5-817e-3437abc73246.png">

<img width="1012" alt="education_img" src="https://user-images.githubusercontent.com/93797825/164543744-cc15d842-cffb-4443-add7-071271d0439a.png">
