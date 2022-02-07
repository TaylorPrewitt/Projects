# Introduction
This script queries the NASA to gather information available about Near Earth Objects (NEO). The goal of this is to provide information about the NEO and a potential impact with Earth. 

# Methods
* Gather data from NASA on all NEO which have their closest proximity to Earth within a week of a date of interest.
* Select all NEO which NASA has tagged as an upcoming potential hazard. 
* Select the NEO from any returned which will come closest Earth.
* Using the max and min diameters, approximate volume with an assumed shape of an ellipsoid.
  * Third semi-axis is approximated as the average of the min and max radii. 
* Find kinetic energy of object and covert to human understandable values.  
  

# Example I/O

### Input 
```2022-05-05```

### Output
During the week of ```2022-05-05``` to ```2022-05-12``` the biggest NEO danger is on ```2022-05-09```. <br>
Impact energy is equivalent to: 
* ```4206.44``` megatons of TNT. <br>
* ```22.16``` simultaneous 9.0 Earthquakes. <br>
* ```17.6``` billion lightning bolts. <br>

Get more information on this NEO at [https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=2416801](https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=2416801) <br>
