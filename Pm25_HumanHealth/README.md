
# Introduction

PM2.5 inhalation has been linked to health complications, ([Negative PM2.5 Impacts](https://www.health.ny.gov/environmental/indoors/air/pmq_a.htm#:~:text=Exposure%20to%20fine%20particles%20can,as%20asthma%20and%20heart%20disease)). Looking at county level death and their causes along with county level PM2.5 particle concentration, I will investigate a potential relationship between the two. 


# Data Descriptions and Sources

## Mortality Rates
| **Parameter**  | **Description**  | 
| :----------: | :----------: |
| Location  | County and State of record |
| FIPS | Federal Information Processing Standard county code |
| Category | Cause of death | 
| Mortality.Rate.xx.Min | Minimum deaths per 100,000 population during the year 'xx' | 
| Mortality.Rate.xx.Max | Maximum deaths per 100,000 population during the year 'xx' | 
| Mortality.Rate.xx. | Mean deaths per 100,000 population over the year 'xx' |  

[Mortality Dataset](https://www.kaggle.com/IHME/us-countylevel-mortality/version/2)




## PM2.5 Concentration Rates
| **Parameter**  | **Description**  | 
| :----------: | :----------: |
| year  | Year of prediction |
| date | Date (day-month-year) of prediction |
| statefips | State FIPS code | 
| countyfips | County FIPS code | 
| PM25_max_pred | Maximum estimated 24-hour average PM2.5 concentration in μg/m3 for the county | 
| PM25_med_pred | 	Median estimated 24-hour average PM2.5 concentration in μg/m3 for the county | 
| PM25_mean_pred |Mean estimated 24-hour average PM2.5 concentration in μg/m3 for the county | 
| PM25_pop_pred |Population-weighted estimated 24-hour average PM2.5 concentration in μg/m3 for the county | 

[PM2.5 Dataset](https://data.cdc.gov/Environmental-Health-Toxicology/Daily-PM2-5-Concentrations-All-County-2001-2016/7vdq-ztk9)

Inspecting the date ranges, the Mortality Rate data set covers the years 1980-2014 and the PM2.5 data set is for the years 2001-2016.  Further more, the the years covered by the Mortality set are not consecutive, having records approximately every 5 years.  Due to this the only years in common are 2005, 2010, and 2014.  

As explained in [Negative PM2.5 Impacts](https://www.health.ny.gov/environmental/indoors/air/pmq_a.htm#:~:text=Exposure%20to%20fine%20particles%20can,as%20asthma%20and%20heart%20disease.), PM2.5 has not been shown to significantly impact all of the causes of death included in the Mortality dataset, for example, "Transport injuries". Excluding any causes of death not previously shown to have a correlation to PM2.5 respective health complication, the only causes of death considered are: "Chronic respiratory diseases", "Cardiovascular diseases", "Neonatal disorders", and "Other non-communicable diseases".


The PM2.5 set includes both the median and the mean observations over the duration of data collection.  For this investigation the mean value will be used operating with a first order assumption that PM2.5 concentration is uniform over each county.


# Results

![unnamed-chunk-17-1](https://user-images.githubusercontent.com/80305894/153100009-d30fdf3c-6a2e-49fd-84e9-18a0a4b6228e.png)
<center><sup><i>Figure 1 is the county level Mortality Rate vs PM2.5 Concentration <b>(Black)</b> and a smooth gamma fit <b><span style="color: blue"> (Blue) </span></b> for each year: 2005, 2010, and 2014 .</i></sup></center> 

Being unlikely that populations respond differently to PM2.5 between the years 2005 and 2014, all years of data are combined to get a first order approximation of any relationship between PM2.5 concentration and human morality rates.

<br><br>

![unnamed-chunk-20-1](https://user-images.githubusercontent.com/80305894/153099772-26752aa3-081d-49b4-a0bc-b3ad03f2507b.png)
<center><sup><i>Figure 2 is the county level Mortality Rate vs PM2.5 Concentration <b>(Black)</b> and a non-linear trendline <b>(Blue)</b>. </i></sup></center>

<br>
Time invariant data showed a stronger linear relationship. Still retains trend seen in yearly models around 9 micrograms per cubic meter where there is an increase in mortality. 

<br><br>

![unnamed-chunk-21-1](https://user-images.githubusercontent.com/80305894/153099829-22e3b432-ed2b-481a-9e43-e1a4fee7451a.png)

<center><sup><i>Figure 3 is the county level Mortality Rate vs PM2.5 Concentration <b>(Black)</b>, linear regression model <b><span style="color: red"> (Red) </span></b>, and the distribution residuals <b><span style="color: magenta"> (Magenta) </span></b>.</i></sup></center> 


<br><br>

![unnamed-chunk-22-1](https://user-images.githubusercontent.com/80305894/153099626-a946c10d-92b1-402f-8156-06da65724f44.png)





# Discussion


By using data from all sets to examine the potential relationship between airborne PM2.5 concentrations and mortality rates due to health complications which have been previously linked to its inhalation, a linear model was created and visualized in *Figure 3*. 


**Equation 1: Linear Regression Best Fit** <br>
*MR = (58.8 +/- 1.36) + (3.37 +/- 0.137)p*


*Equation 1* states that the Mortality Rate (MR) increases by approximately 3.37 deaths per 100,000 population (p) for each integer increase in micrograms of PM2.5 per cubic meter. This is an one variable approximation of a complex system, and as such it is not expected to get an exceptionally high R<sup>2</sup> value. The observed value was 0.2067 R<sup>2</sup> which supports the concept that mortality from these health conditions has other deterministic factors outside of PM2.5 presence in the air. However, the p-value: < 2.2e<sup>-16</sup> signifies that the observed relationship between increased PM2.5 pollution and increased mortality due to the linked health complications is very unlikely to be a random occurrence. 

Looking at *Figure 1* and *Figure 3*, at approximately 9 micrograms PM2.5 per cubic meter there an unknown event.  This is seen in *Figure 1* as a break from linearity and in *Figure 3* as a location where a deviation from homoscedasticity takes place. Both of these were also observed when investigating single year models.  This is where an increase in morality rate occurs and is not accurately described by a linear fit.  



**Residuals vs Fitted:**  <br>
This suggests that the relationship between PM2.5 concentration and mortality rate is reasonable to be described by a linear approximation. Observations supporting this from *Figure 4* are that the residuals are mostly evenly distributed about the 0 line, and the fit of the two approximately follows the 0 line as well. There is a break from linearity seen for extreme values of morality.     

**Q-Q:** <br>
Similar to the *Residual vs Fitted* plot in *Figure 4*, this supports the linear description of the relationship between PM2.5 concentration and Mortality due to health conditions linked to PM2.5 exposure.  The linear relationship is able to describe the data, but as the quantiles become more extreme, deviation from this behavior occurs.  

**Breusch Pagan** <br>
Seeing a break from homoscedasticity in exploratory plots, the Breusch Pagan test was used to verify that variances were not homogeneous. This produced a test statistic that strongly rejected the hypothesis that variances are produced similarly across all observations.   
 

Being a one parameter simplification, it was expected that no model would be perfect as there are many known causes to the selected health conditions. While *Equation 1* can be used to get an approximation of the death rate in each county based on pollution levels, other parameters need to be considered.     


# Moving Forward 

Any investigation should include:

* Other airborne pollutants linked to the health conditions. Specifically, any co-occurring pollutants present at higher PM2.5 concentrations and not low concentrations.
* Include other known causes to the chosen health conditions in future models.
* Inspect PM2.5's relationship to morality rates for individual causes of death. 
* Further research into PM2.5 toxicity thresholds and human capacity to metabolize.
* Deeper investigation into the event around 9 micrograms of PM2.5 per cubic meter.






