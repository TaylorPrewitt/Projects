
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

![unnamed-chunk-18-1](https://user-images.githubusercontent.com/80305894/152270630-0a1051a5-47f1-42be-abfd-18a38b10ac81.png)
<center><sup><i>Above is the county level Mortality Rate vs PM2.5 Concentration <b>(Black)</b> and a non-linear trendline <b>(Blue)</b>. </i></sup></center>

<br>

Time invariant data showed a stronger linear relationship. Still retains trend seen in yearly models around 9 micrograms per cubic meter where there is an increase in mortality. 

<br>

![unnamed-chunk-19-1](https://user-images.githubusercontent.com/80305894/152268940-550a0f00-2306-407f-bdab-c83ccb783ae0.png)

<center><sup><i>Above is the county level Mortality Rate vs PM2.5 Concentration <b>(Black)</b>, linear regression model <b><span style="color: red"> (Red) </span></b>, and the distribution residuals <b><span style="color: magenta"> (Magenta) </span></b>.</i></sup></center> 


# Discussion

Using all overlapping data from both sets to examine the potential relationship between airborne PM2.5 concentrations and mortality rates due to health complications which have been previously linked to its inhalation, a linear model was created and visualized in Figure 8. 


**Equation 1:** <br>
<i>MR = (58.8 +/- 0.682) + (3.37 +/- 0.0684)p</i>

Equation 1 states that the Mortality Rate (MR) increases by approximately 3.37 per 100,000 population (p) for each integer increase of PM2.5 concentration measured in micrograms per cubic meter, and as seen in Figure 8 fits the trend data fairly well. This is an one variable approximation of a complex system, and as such it is not expected to get an exceptionally high R<sup>2</sup> value. The observed value was 0.2067 R<sup>2</sup> which supports the concept that mortality from these health conditions has other deterministic factors outside of PM2.5 presence in the air. However, the p-value: < 2.2e<sup>-16</sup> signifies that the observed relationship between increased PM2.5 pollution and increased mortality due to the linked health complications is very unlikely to be a random occurrence.  

Looking at the residuals, there around 9 micrograms per cubic meter there is a break from being normally distributed about the trend line. This was also observed in the single year models and is where an increase in morality rate occurs and is not accurately described by a linear fit.  

Moving forward, any investigation should include: <br>
- Other airborne pollutants linked to the health conditions. <br>
  - Specifically, any co-occurring pollutants present at higher PM2.5 concentrations and not low concentrations. <br>
- Further research in PM2.5 toxicity threshold <br>
- Deeper investigation into relationships between PM2.5 and specific causes of death, not all linked causes. <br>
