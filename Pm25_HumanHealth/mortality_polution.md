PM2.5 Concentration and Human Health
================
Taylor Prewitt
2/1/2022

# Introduction

PM2.5 inhalation has been linked to health complications, ([Negative
PM2.5
Impacts](%22#https://www.health.ny.gov/environmental/indoors/air/pmq_a.htm#:~:text=Exposure%20to%20fine%20particles%20can,as%20asthma%20and%20heart%20disease.%22)).
Looking at county level death and their causes along with county level
PM2.5 particle concentration, I will investigate a potential
relationship between the two.

    ## -- Attaching packages -------------------------------------------------------------------------- tidyverse 1.3.0 --

    ## v ggplot2 3.3.2     v purrr   0.3.4
    ## v tibble  3.0.3     v dplyr   1.0.2
    ## v tidyr   1.1.2     v stringr 1.4.0
    ## v readr   1.3.1     v forcats 0.5.0

    ## -- Conflicts ----------------------------------------------------------------------------- tidyverse_conflicts() --
    ## x dplyr::filter() masks stats::filter()
    ## x dplyr::lag()    masks stats::lag()

    ## 
    ## Attaching package: 'MASS'

    ## The following object is masked from 'package:dplyr':
    ## 
    ##     select

    ## Warning: package 'gridExtra' was built under R version 4.0.5

    ## 
    ## Attaching package: 'gridExtra'

    ## The following object is masked from 'package:dplyr':
    ## 
    ##     combine

    ## Warning: package 'olsrr' was built under R version 4.0.5

    ## 
    ## Attaching package: 'olsrr'

    ## The following object is masked from 'package:MASS':
    ## 
    ##     cement

    ## The following object is masked from 'package:datasets':
    ## 
    ##     rivers

``` r
# loading in the data, county level mortality
mort_data = read.csv("mort.csv",
                  header=TRUE)

# loading in the data, county level PM2.5 concentrations  
p25_data = read.csv("Daily_PM2.5_Concentrations_All_County__2001-2016.csv",
                  header=TRUE)
```

``` r
# data examples
head(mort_data)
```

    ##                  Location FIPS           Category Mortality.Rate..1980.
    ## 1           United States  NaN Neonatal disorders                  9.18
    ## 2                 Alabama    1 Neonatal disorders                 11.03
    ## 3 Autauga County, Alabama 1001 Neonatal disorders                  9.58
    ## 4 Baldwin County, Alabama 1003 Neonatal disorders                  8.75
    ## 5 Barbour County, Alabama 1005 Neonatal disorders                 12.30
    ## 6    Bibb County, Alabama 1007 Neonatal disorders                 11.28
    ##   Mortality.Rate..1980...Min. Mortality.Rate..1980...Max. Mortality.Rate..1985.
    ## 1                        8.83                        9.93                  6.91
    ## 2                       10.57                       12.00                  8.51
    ## 3                        8.37                       11.02                  7.50
    ## 4                        7.86                        9.81                  6.54
    ## 5                       10.64                       14.15                  9.26
    ## 6                        9.63                       13.14                  8.88
    ##   Mortality.Rate..1985...Min. Mortality.Rate..1985...Max. Mortality.Rate..1990.
    ## 1                        6.73                        7.36                  6.09
    ## 2                        8.25                        9.12                  7.52
    ## 3                        6.56                        8.58                  6.76
    ## 4                        5.88                        7.27                  5.76
    ## 5                        8.13                       10.60                  8.12
    ## 6                        7.57                       10.27                  7.92
    ##   Mortality.Rate..1990...Min. Mortality.Rate..1990...Max. Mortality.Rate..1995.
    ## 1                        5.94                        6.44                  4.71
    ## 2                        7.28                        7.95                  6.08
    ## 3                        5.93                        7.71                  5.24
    ## 4                        5.15                        6.45                  4.65
    ## 5                        7.08                        9.28                  6.60
    ## 6                        6.82                        9.11                  6.44
    ##   Mortality.Rate..1995...Min. Mortality.Rate..1995...Max. Mortality.Rate..2000.
    ## 1                        4.60                        4.84                  4.50
    ## 2                        5.89                        6.29                  6.21
    ## 3                        4.59                        5.94                  5.26
    ## 4                        4.15                        5.14                  4.56
    ## 5                        5.77                        7.49                  6.65
    ## 6                        5.58                        7.39                  6.59
    ##   Mortality.Rate..2000...Min. Mortality.Rate..2000...Max. Mortality.Rate..2005.
    ## 1                        4.29                        4.61                  4.44
    ## 2                        5.92                        6.40                  6.32
    ## 3                        4.61                        5.93                  5.55
    ## 4                        4.09                        5.00                  4.55
    ## 5                        5.83                        7.53                  6.90
    ## 6                        5.66                        7.57                  7.14
    ##   Mortality.Rate..2005...Min. Mortality.Rate..2005...Max. Mortality.Rate..2010.
    ## 1                        4.18                        4.55                  3.75
    ## 2                        5.96                        6.52                  5.58
    ## 3                        4.83                        6.30                  4.83
    ## 4                        4.09                        5.03                  4.02
    ## 5                        6.01                        7.89                  5.99
    ## 6                        6.13                        8.26                  6.29
    ##   Mortality.Rate..2010...Min. Mortality.Rate..2010...Max. Mortality.Rate..2014.
    ## 1                        3.43                        3.85                  3.32
    ## 2                        5.16                        5.78                  5.10
    ## 3                        4.19                        5.49                  4.56
    ## 4                        3.53                        4.48                  3.68
    ## 5                        5.16                        6.84                  5.43
    ## 6                        5.32                        7.27                  5.89
    ##   Mortality.Rate..2014...Min. Mortality.Rate..2014...Max.
    ## 1                        3.02                        3.45
    ## 2                        4.67                        5.32
    ## 3                        3.96                        5.21
    ## 4                        3.25                        4.08
    ## 5                        4.63                        6.24
    ## 6                        4.98                        6.85
    ##   X..Change.in.Mortality.Rate..1980.2014
    ## 1                                 -63.85
    ## 2                                 -53.82
    ## 3                                 -52.43
    ## 4                                 -57.97
    ## 5                                 -55.86
    ## 6                                 -47.76
    ##   X..Change.in.Mortality.Rate..1980.2014..Min.
    ## 1                                       -68.95
    ## 2                                       -60.08
    ## 3                                       -60.01
    ## 4                                       -64.96
    ## 5                                       -62.49
    ## 6                                       -56.13
    ##   X..Change.in.Mortality.Rate..1980.2014..Max.
    ## 1                                       -61.55
    ## 2                                       -50.77
    ## 3                                       -46.16
    ## 4                                       -52.87
    ## 5                                       -50.32
    ## 6                                       -40.11

``` r
head(p25_data)
```

    ##   year      date statefips countyfips PM25_max_pred PM25_med_pred
    ## 1 2001 01JAN2001         1          1     10.664367     10.264546
    ## 2 2001 01JAN2001         1          3      9.803209      8.739505
    ## 3 2001 01JAN2001         1          5     12.087599     11.809159
    ## 4 2001 01JAN2001         1          7      8.579425      8.435394
    ## 5 2001 01JAN2001         1          9     14.399446     13.577741
    ## 6 2001 01JAN2001         1         11     11.853907     11.824247
    ##   PM25_mean_pred PM25_pop_pred
    ## 1      10.137631     10.188703
    ## 2       8.743748      8.811486
    ## 3      11.812775     11.802062
    ## 4       8.458118      8.448871
    ## 5      13.300528     13.231461
    ## 6      11.728350     11.774401

# Data Descriptions and Sources:

## Mortality Rates

|     **Parameter**     |                      **Description**                       |
| :-------------------: | :--------------------------------------------------------: |
|       Location        |                 County and State of record                 |
|         FIPS          |    Federal Information Processing Standard county code     |
|       Category        |                       Cause of death                       |
| Mortality.Rate.xx.Min | Minimum deaths per 100,000 population during the year ‘xx’ |
| Mortality.Rate.xx.Max | Maximum deaths per 100,000 population during the year ‘xx’ |
|  Mortality.Rate.xx.   |   Mean deaths per 100,000 population over the year ‘xx’    |

[Mortality
Dataset](%22https://www.kaggle.com/IHME/us-countylevel-mortality/version/2%22)

## PM2.5 Concentration Rates

|  **Parameter**   |                                      **Description**                                      |
| :--------------: | :---------------------------------------------------------------------------------------: |
|       year       |                                    Year of prediction                                     |
|       date       |                            Date (day-month-year) of prediction                            |
|    statefips     |                                      State FIPS code                                      |
|    countyfips    |                                     County FIPS code                                      |
| PM25\_max\_pred  |       Maximum estimated 24-hour average PM2.5 concentration in μg/m3 for the county       |
| PM25\_med\_pred  |       Median estimated 24-hour average PM2.5 concentration in μg/m3 for the county        |
| PM25\_mean\_pred |        Mean estimated 24-hour average PM2.5 concentration in μg/m3 for the county         |
| PM25\_pop\_pred  | Population-weighted estimated 24-hour average PM2.5 concentration in μg/m3 for the county |

[PM2.5
Dataset](%22https://data.cdc.gov/Environmental-Health-Toxicology/Daily-PM2-5-Concentrations-All-County-2001-2016/7vdq-ztk9%22)

    ## 'data.frame':    67074 obs. of  30 variables:
    ##  $ Location                                    : chr  "United States" "Alabama" "Autauga County, Alabama" "Baldwin County, Alabama" ...
    ##  $ FIPS                                        : num  NaN 1 1001 1003 1005 ...
    ##  $ Category                                    : chr  "Neonatal disorders" "Neonatal disorders" "Neonatal disorders" "Neonatal disorders" ...
    ##  $ Mortality.Rate..1980.                       : num  9.18 11.03 9.58 8.75 12.3 ...
    ##  $ Mortality.Rate..1980...Min.                 : num  8.83 10.57 8.37 7.86 10.64 ...
    ##  $ Mortality.Rate..1980...Max.                 : num  9.93 12 11.02 9.81 14.15 ...
    ##  $ Mortality.Rate..1985.                       : num  6.91 8.51 7.5 6.54 9.26 8.88 4.8 12.5 8.92 7.37 ...
    ##  $ Mortality.Rate..1985...Min.                 : num  6.73 8.25 6.56 5.88 8.13 ...
    ##  $ Mortality.Rate..1985...Max.                 : num  7.36 9.12 8.58 7.27 10.6 ...
    ##  $ Mortality.Rate..1990.                       : num  6.09 7.52 6.76 5.76 8.12 ...
    ##  $ Mortality.Rate..1990...Min.                 : num  5.94 7.28 5.93 5.15 7.08 6.82 3.87 9.44 6.9 6.32 ...
    ##  $ Mortality.Rate..1990...Max.                 : num  6.44 7.95 7.71 6.45 9.28 ...
    ##  $ Mortality.Rate..1995.                       : num  4.71 6.08 5.24 4.65 6.6 6.44 3.68 8.94 6.32 5.74 ...
    ##  $ Mortality.Rate..1995...Min.                 : num  4.6 5.89 4.59 4.15 5.77 5.58 3.22 7.7 5.41 5.2 ...
    ##  $ Mortality.Rate..1995...Max.                 : num  4.84 6.29 5.94 5.14 7.49 ...
    ##  $ Mortality.Rate..2000.                       : num  4.5 6.21 5.26 4.56 6.65 6.59 3.78 8.94 6.45 5.97 ...
    ##  $ Mortality.Rate..2000...Min.                 : num  4.29 5.92 4.61 4.09 5.83 5.66 3.31 7.67 5.56 5.4 ...
    ##  $ Mortality.Rate..2000...Max.                 : num  4.61 6.4 5.93 5 7.53 7.57 4.29 10.4 7.42 6.6 ...
    ##  $ Mortality.Rate..2005.                       : num  4.44 6.32 5.55 4.55 6.9 7.14 4.06 9.37 6.87 6.43 ...
    ##  $ Mortality.Rate..2005...Min.                 : num  4.18 5.96 4.83 4.09 6.01 6.13 3.52 7.89 5.88 5.78 ...
    ##  $ Mortality.Rate..2005...Max.                 : num  4.55 6.52 6.3 5.03 7.89 8.26 4.6 11 7.96 7.08 ...
    ##  $ Mortality.Rate..2010.                       : num  3.75 5.58 4.83 4.02 5.99 6.29 3.7 8.03 5.97 5.9 ...
    ##  $ Mortality.Rate..2010...Min.                 : num  3.43 5.16 4.19 3.53 5.16 5.32 3.16 6.78 5.03 5.23 ...
    ##  $ Mortality.Rate..2010...Max.                 : num  3.85 5.78 5.49 4.48 6.84 7.27 4.23 9.49 6.89 6.53 ...
    ##  $ Mortality.Rate..2014.                       : num  3.32 5.1 4.56 3.68 5.43 5.89 3.52 7 5.53 5.37 ...
    ##  $ Mortality.Rate..2014...Min.                 : num  3.02 4.67 3.96 3.25 4.63 4.98 2.99 5.85 4.61 4.76 ...
    ##  $ Mortality.Rate..2014...Max.                 : num  3.45 5.32 5.21 4.08 6.24 6.85 4.06 8.3 6.43 5.93 ...
    ##  $ X..Change.in.Mortality.Rate..1980.2014      : num  -63.9 -53.8 -52.4 -58 -55.9 ...
    ##  $ X..Change.in.Mortality.Rate..1980.2014..Min.: num  -69 -60.1 -60 -65 -62.5 ...
    ##  $ X..Change.in.Mortality.Rate..1980.2014..Max.: num  -61.5 -50.8 -46.2 -52.9 -50.3 ...

    ## 'data.frame':    18168996 obs. of  8 variables:
    ##  $ year          : int  2001 2001 2001 2001 2001 2001 2001 2001 2001 2001 ...
    ##  $ date          : chr  "01JAN2001" "01JAN2001" "01JAN2001" "01JAN2001" ...
    ##  $ statefips     : int  1 1 1 1 1 1 1 1 1 1 ...
    ##  $ countyfips    : int  1 3 5 7 9 11 13 15 17 19 ...
    ##  $ PM25_max_pred : num  10.66 9.8 12.09 8.58 14.4 ...
    ##  $ PM25_med_pred : num  10.26 8.74 11.81 8.44 13.58 ...
    ##  $ PM25_mean_pred: num  10.14 8.74 11.81 8.46 13.3 ...
    ##  $ PM25_pop_pred : num  10.19 8.81 11.8 8.45 13.23 ...

``` r
# general inspection of data

dim(mort_data)
```

    ## [1] 67074    30

``` r
names(mort_data)
```

    ##  [1] "Location"                                    
    ##  [2] "FIPS"                                        
    ##  [3] "Category"                                    
    ##  [4] "Mortality.Rate..1980."                       
    ##  [5] "Mortality.Rate..1980...Min."                 
    ##  [6] "Mortality.Rate..1980...Max."                 
    ##  [7] "Mortality.Rate..1985."                       
    ##  [8] "Mortality.Rate..1985...Min."                 
    ##  [9] "Mortality.Rate..1985...Max."                 
    ## [10] "Mortality.Rate..1990."                       
    ## [11] "Mortality.Rate..1990...Min."                 
    ## [12] "Mortality.Rate..1990...Max."                 
    ## [13] "Mortality.Rate..1995."                       
    ## [14] "Mortality.Rate..1995...Min."                 
    ## [15] "Mortality.Rate..1995...Max."                 
    ## [16] "Mortality.Rate..2000."                       
    ## [17] "Mortality.Rate..2000...Min."                 
    ## [18] "Mortality.Rate..2000...Max."                 
    ## [19] "Mortality.Rate..2005."                       
    ## [20] "Mortality.Rate..2005...Min."                 
    ## [21] "Mortality.Rate..2005...Max."                 
    ## [22] "Mortality.Rate..2010."                       
    ## [23] "Mortality.Rate..2010...Min."                 
    ## [24] "Mortality.Rate..2010...Max."                 
    ## [25] "Mortality.Rate..2014."                       
    ## [26] "Mortality.Rate..2014...Min."                 
    ## [27] "Mortality.Rate..2014...Max."                 
    ## [28] "X..Change.in.Mortality.Rate..1980.2014"      
    ## [29] "X..Change.in.Mortality.Rate..1980.2014..Min."
    ## [30] "X..Change.in.Mortality.Rate..1980.2014..Max."

``` r
dim(p25_data)
```

    ## [1] 18168996        8

``` r
names(p25_data)
```

    ## [1] "year"           "date"           "statefips"      "countyfips"    
    ## [5] "PM25_max_pred"  "PM25_med_pred"  "PM25_mean_pred" "PM25_pop_pred"

Looking at the date ranges, the Mortality Rate data set covers the years
1980-2014 and the PM2.5 data set is for the years 2001-2016. Further
more, the the years covered by the Mortality set are not consecutive,
having records approximately every 5 years. Due to this the only years
in common are 2005, 2010, and 2014.

The PM2.5 set includes both the median and the mean observations over
the duration of data collection. For this investigation the mean value
will be used operating with a first order assumption that PM2.5
concentration is uniform over each county.

``` r
# getting causes of death
unique(mort_data$Category)
```

    ##  [1] "Neonatal disorders"                                               
    ##  [2] "HIV/AIDS and tuberculosis"                                        
    ##  [3] "Musculoskeletal disorders"                                        
    ##  [4] "Diabetes, urogenital, blood, and endocrine diseases"              
    ##  [5] "Digestive diseases"                                               
    ##  [6] "Chronic respiratory diseases"                                     
    ##  [7] "Neurological disorders"                                           
    ##  [8] "Cirrhosis and other chronic liver diseases"                       
    ##  [9] "Mental and substance use disorders"                               
    ## [10] "Forces of nature, war, and legal intervention"                    
    ## [11] "Unintentional injuries"                                           
    ## [12] "Nutritional deficiencies"                                         
    ## [13] "Other communicable, maternal, neonatal, and nutritional diseases" 
    ## [14] "Cardiovascular diseases"                                          
    ## [15] "Diarrhea, lower respiratory, and other common infectious diseases"
    ## [16] "Maternal disorders"                                               
    ## [17] "Other non-communicable diseases"                                  
    ## [18] "Self-harm and interpersonal violence"                             
    ## [19] "Neoplasms"                                                        
    ## [20] "Transport injuries"                                               
    ## [21] "Neglected tropical diseases and malaria"

As explained in [Negative PM2.5
Impacts](%22#https://www.health.ny.gov/environmental/indoors/air/pmq_a.htm#:~:text=Exposure%20to%20fine%20particles%20can,as%20asthma%20and%20heart%20disease.%22),
PM2.5 has not been shown to significantly impact all of these causes of
death, for example, “Transport injuries”. Excluding any causes of death
not previously shown to have a correlation to PM2.5 respective health
complication, the only causes of death considered are: “Chronic
respiratory diseases”, “Cardiovascular diseases”, “Neonatal disorders”,
and “Other non-communicable diseases”.

``` r
# creating function to count any missing values in data
count_missing_vals = function(df) 
  {missing_vals = c(0)
  dataset = df
  for (col in 1:ncol(dataset))
    {missing_vals = append(missing_vals, sum(is.na(dataset[,col])))}
  missing_vals = missing_vals[1:length(dataset)]
  missing_vals_df = data.frame(Variable = c(colnames(dataset)),
                                NumMissing = missing_vals)
  return(missing_vals_df)}
```

``` r
# searching for missing values
count_missing_vals(mort_data)
```

    ##                                        Variable NumMissing
    ## 1                                      Location          0
    ## 2                                          FIPS          0
    ## 3                                      Category         21
    ## 4                         Mortality.Rate..1980.          0
    ## 5                   Mortality.Rate..1980...Min.          0
    ## 6                   Mortality.Rate..1980...Max.          0
    ## 7                         Mortality.Rate..1985.          0
    ## 8                   Mortality.Rate..1985...Min.          0
    ## 9                   Mortality.Rate..1985...Max.          0
    ## 10                        Mortality.Rate..1990.          0
    ## 11                  Mortality.Rate..1990...Min.          0
    ## 12                  Mortality.Rate..1990...Max.          0
    ## 13                        Mortality.Rate..1995.          0
    ## 14                  Mortality.Rate..1995...Min.          0
    ## 15                  Mortality.Rate..1995...Max.          0
    ## 16                        Mortality.Rate..2000.          0
    ## 17                  Mortality.Rate..2000...Min.          0
    ## 18                  Mortality.Rate..2000...Max.          0
    ## 19                        Mortality.Rate..2005.          0
    ## 20                  Mortality.Rate..2005...Min.          0
    ## 21                  Mortality.Rate..2005...Max.          0
    ## 22                        Mortality.Rate..2010.          0
    ## 23                  Mortality.Rate..2010...Min.          0
    ## 24                  Mortality.Rate..2010...Max.          0
    ## 25                        Mortality.Rate..2014.          0
    ## 26                  Mortality.Rate..2014...Min.          0
    ## 27                  Mortality.Rate..2014...Max.          0
    ## 28       X..Change.in.Mortality.Rate..1980.2014          0
    ## 29 X..Change.in.Mortality.Rate..1980.2014..Min.          0
    ## 30 X..Change.in.Mortality.Rate..1980.2014..Max.          0

``` r
count_missing_vals(p25_data)
```

    ##         Variable NumMissing
    ## 1           year          0
    ## 2           date          0
    ## 3      statefips          0
    ## 4     countyfips          0
    ## 5  PM25_max_pred          0
    ## 6  PM25_med_pred          0
    ## 7 PM25_mean_pred          0
    ## 8  PM25_pop_pred          0

``` r
# find NA values from count
which(is.na(mort_data))
```

    ##  [1]  67075  70269  73463  76657  79851  83045  86239  89433  92627  95821
    ## [11]  99015 102209 105403 108597 111791 114985 118179 121373 124567 127761
    ## [21] 130955

``` r
# inspect data at/around these df cell values

# cell 67075 is index 1 of column 2
mort_data[1,]
```

    ##        Location FIPS           Category Mortality.Rate..1980.
    ## 1 United States  NaN Neonatal disorders                  9.18
    ##   Mortality.Rate..1980...Min. Mortality.Rate..1980...Max. Mortality.Rate..1985.
    ## 1                        8.83                        9.93                  6.91
    ##   Mortality.Rate..1985...Min. Mortality.Rate..1985...Max. Mortality.Rate..1990.
    ## 1                        6.73                        7.36                  6.09
    ##   Mortality.Rate..1990...Min. Mortality.Rate..1990...Max. Mortality.Rate..1995.
    ## 1                        5.94                        6.44                  4.71
    ##   Mortality.Rate..1995...Min. Mortality.Rate..1995...Max. Mortality.Rate..2000.
    ## 1                         4.6                        4.84                   4.5
    ##   Mortality.Rate..2000...Min. Mortality.Rate..2000...Max. Mortality.Rate..2005.
    ## 1                        4.29                        4.61                  4.44
    ##   Mortality.Rate..2005...Min. Mortality.Rate..2005...Max. Mortality.Rate..2010.
    ## 1                        4.18                        4.55                  3.75
    ##   Mortality.Rate..2010...Min. Mortality.Rate..2010...Max. Mortality.Rate..2014.
    ## 1                        3.43                        3.85                  3.32
    ##   Mortality.Rate..2014...Min. Mortality.Rate..2014...Max.
    ## 1                        3.02                        3.45
    ##   X..Change.in.Mortality.Rate..1980.2014
    ## 1                                 -63.85
    ##   X..Change.in.Mortality.Rate..1980.2014..Min.
    ## 1                                       -68.95
    ##   X..Change.in.Mortality.Rate..1980.2014..Max.
    ## 1                                       -61.55

``` r
mort_data[(70269-67074),]
```

    ##           Location FIPS                  Category Mortality.Rate..1980.
    ## 3195 United States  NaN HIV/AIDS and tuberculosis                  1.52
    ##      Mortality.Rate..1980...Min. Mortality.Rate..1980...Max.
    ## 3195                        1.44                        1.61
    ##      Mortality.Rate..1985. Mortality.Rate..1985...Min.
    ## 3195                  3.16                        3.11
    ##      Mortality.Rate..1985...Max. Mortality.Rate..1990.
    ## 3195                        3.22                 11.45
    ##      Mortality.Rate..1990...Min. Mortality.Rate..1990...Max.
    ## 3195                       11.34                       11.56
    ##      Mortality.Rate..1995. Mortality.Rate..1995...Min.
    ## 3195                 16.61                       16.48
    ##      Mortality.Rate..1995...Max. Mortality.Rate..2000.
    ## 3195                       16.74                  5.97
    ##      Mortality.Rate..2000...Min. Mortality.Rate..2000...Max.
    ## 3195                        5.92                        6.02
    ##      Mortality.Rate..2005. Mortality.Rate..2005...Min.
    ## 3195                  4.87                        4.83
    ##      Mortality.Rate..2005...Max. Mortality.Rate..2010.
    ## 3195                        4.91                   3.2
    ##      Mortality.Rate..2010...Min. Mortality.Rate..2010...Max.
    ## 3195                        3.17                        3.22
    ##      Mortality.Rate..2014. Mortality.Rate..2014...Min.
    ## 3195                  2.66                        2.63
    ##      Mortality.Rate..2014...Max. X..Change.in.Mortality.Rate..1980.2014
    ## 3195                        2.69                                  74.35
    ##      X..Change.in.Mortality.Rate..1980.2014..Min.
    ## 3195                                        64.77
    ##      X..Change.in.Mortality.Rate..1980.2014..Max.
    ## 3195                                        84.14

``` r
mort_data[(70269-67072):(70269-67076),]
```

    ##                      Location  FIPS                  Category
    ## 3197  Autauga County, Alabama  1001 HIV/AIDS and tuberculosis
    ## 3196                  Alabama     1 HIV/AIDS and tuberculosis
    ## 3195            United States   NaN HIV/AIDS and tuberculosis
    ## 3194   Weston County, Wyoming 56045        Neonatal disorders
    ## 3193 Washakie County, Wyoming 56043        Neonatal disorders
    ##      Mortality.Rate..1980. Mortality.Rate..1980...Min.
    ## 3197                  0.95                        0.68
    ## 3196                  1.46                        1.33
    ## 3195                  1.52                        1.44
    ## 3194                  8.49                        6.97
    ## 3193                  7.56                        6.29
    ##      Mortality.Rate..1980...Max. Mortality.Rate..1985.
    ## 3197                        1.29                  1.44
    ## 3196                        1.59                  2.15
    ## 3195                        1.61                  3.16
    ## 3194                       10.19                  6.11
    ## 3193                        9.14                  5.74
    ##      Mortality.Rate..1985...Min. Mortality.Rate..1985...Max.
    ## 3197                        1.12                        1.86
    ## 3196                        2.03                        2.27
    ## 3195                        3.11                        3.22
    ## 3194                        5.03                        7.25
    ## 3193                        4.75                        6.92
    ##      Mortality.Rate..1990. Mortality.Rate..1990...Min.
    ## 3197                  6.57                        5.49
    ## 3196                  8.03                        7.79
    ## 3195                 11.45                       11.34
    ## 3194                  5.07                        4.28
    ## 3193                  4.83                        4.02
    ##      Mortality.Rate..1990...Max. Mortality.Rate..1995.
    ## 3197                        7.84                 10.75
    ## 3196                        8.25                 14.10
    ## 3195                       11.56                 16.61
    ## 3194                        6.03                  3.92
    ## 3193                        5.80                  3.79
    ##      Mortality.Rate..1995...Min. Mortality.Rate..1995...Max.
    ## 3197                        9.18                       12.50
    ## 3196                       13.76                       14.43
    ## 3195                       16.48                       16.74
    ## 3194                        3.26                        4.65
    ## 3193                        3.17                        4.55
    ##      Mortality.Rate..2000. Mortality.Rate..2000...Min.
    ## 3197                  3.62                        2.94
    ## 3196                  5.47                        5.30
    ## 3195                  5.97                        5.92
    ## 3194                  3.79                        3.15
    ## 3193                  3.79                        3.15
    ##      Mortality.Rate..2000...Max. Mortality.Rate..2005.
    ## 3197                        4.37                  3.32
    ## 3196                        5.65                  4.67
    ## 3195                        6.02                  4.87
    ## 3194                        4.55                  3.77
    ## 3193                        4.57                  3.69
    ##      Mortality.Rate..2005...Min. Mortality.Rate..2005...Max.
    ## 3197                        2.66                        4.14
    ## 3196                        4.51                        4.83
    ## 3195                        4.83                        4.91
    ## 3194                        3.13                        4.52
    ## 3193                        3.09                        4.42
    ##      Mortality.Rate..2010. Mortality.Rate..2010...Min.
    ## 3197                  2.37                        1.82
    ## 3196                  3.35                        3.21
    ## 3195                  3.20                        3.17
    ## 3194                  3.07                        2.53
    ## 3193                  3.13                        2.60
    ##      Mortality.Rate..2010...Max. Mortality.Rate..2014.
    ## 3197                        3.07                  2.30
    ## 3196                        3.50                  2.94
    ## 3195                        3.22                  2.66
    ## 3194                        3.69                  2.75
    ## 3193                        3.76                  2.78
    ##      Mortality.Rate..2014...Min. Mortality.Rate..2014...Max.
    ## 3197                        1.68                        2.96
    ## 3196                        2.80                        3.08
    ## 3195                        2.63                        2.69
    ## 3194                        2.23                        3.37
    ## 3193                        2.30                        3.37
    ##      X..Change.in.Mortality.Rate..1980.2014
    ## 3197                                 143.15
    ## 3196                                 101.52
    ## 3195                                  74.35
    ## 3194                                 -67.63
    ## 3193                                 -63.24
    ##      X..Change.in.Mortality.Rate..1980.2014..Min.
    ## 3197                                        65.10
    ## 3196                                        82.33
    ## 3195                                        64.77
    ## 3194                                       -73.44
    ## 3193                                       -69.91
    ##      X..Change.in.Mortality.Rate..1980.2014..Max.
    ## 3197                                       245.14
    ## 3196                                       124.12
    ## 3195                                        84.14
    ## 3194                                       -61.73
    ## 3193                                       -57.42

``` r
# removing bad data
mort_data = subset(mort_data, mort_data$FIPS > 1000 | is.na(mort_data$FIPS) == FALSE)
```

The dataset contained some bad values. The cells which had NaN values
were in the FIPS column and weren’t associated with any single county.
These were aggregated United States mortality rates for a given cause of
death. There are 21 NaN since there are 21 unique causes of death in the
Mortality dataset. Furthermore, this happened on the state level too.
This did not create NaN in the FIPS column, but did generate non-county
specific data. Both of these types of values were removed from
consideration.

# Data Processing

``` r
# condense p25_data to year value from daily. with only common years


# making df with for model with no index values as variable
p25_df = p25_data %>% 
  group_by(year, statefips, countyfips) %>%
  filter(year %in% c(2005, 2010, 2014)) %>% 
  summarise(PM25_mean = mean(PM25_mean_pred))
```

    ## `summarise()` regrouping output by 'year', 'statefips' (override with `.groups` argument)

``` r
# get yearly average PM2.5 value
p25_df = aggregate(p25_df[, 2:4], list(p25_df$year, p25_df$statefips, p25_df$countyfips), mean)

# keep only needed columns and rename
p25_df = p25_df %>% 
  dplyr::select(Group.1, Group.2, Group.3, PM25_mean)
colnames(p25_df) = c('year','statefips', 'countyfips', 'PM25_mean')


head(p25_df)
```

    ##   year statefips countyfips PM25_mean
    ## 1 2005         1          1 13.071456
    ## 2 2010         1          1 10.720234
    ## 3 2014         1          1 11.196810
    ## 4 2005         4          1  6.265535
    ## 5 2010         4          1  5.080875
    ## 6 2014         4          1  4.521123

``` r
# keep data with common years for linked health issues
mort_df = mort_data %>% 
  group_by(Category) %>% 
  filter(Category %in% c("Chronic respiratory diseases", 
                         "Cardiovascular diseases",
                         "Neonatal disorders", 
                         "Other non-communicable diseases")) %>% 
  dplyr::select(Location, 
                FIPS, 
                Mortality.Rate..2005., 
                Mortality.Rate..2010., 
                Mortality.Rate..2014., 
                Category)


# mean mortality for all selected causes per county
mort_df = mort_df %>% 
  group_by(Location, FIPS) %>% 
  summarise(MR_2005 = mean(Mortality.Rate..2005.), 
            MR_2010 = mean(Mortality.Rate..2010.), 
            MR_2014 = mean(Mortality.Rate..2014.))
```

    ## `summarise()` regrouping output by 'Location' (override with `.groups` argument)

``` r
head(mort_df)
```

    ## # A tibble: 6 x 5
    ## # Groups:   Location [6]
    ##   Location                          FIPS MR_2005 MR_2010 MR_2014
    ##   <chr>                            <dbl>   <dbl>   <dbl>   <dbl>
    ## 1 Abbeville County, South Carolina 45001    87.0    81.4    81.2
    ## 2 Acadia Parish, Louisiana         22001   118.    106.    108. 
    ## 3 Accomack County, Virginia        51001    97.1    86.9    86.3
    ## 4 Ada County, Idaho                16001    77.9    66.3    68.4
    ## 5 Adair County, Iowa               19001    88.1    82.3    81.4
    ## 6 Adair County, Kentucky           21001   112.    103.    104.

``` r
# transpose year data into columns for FIPS joining 
p25_df = pivot_wider(p25_df, 
                         id_cols = c("statefips","countyfips"),
                         names_from = "year", 
                         values_from = "PM25_mean")


head(p25_df)
```

    ## # A tibble: 6 x 5
    ##   statefips countyfips `2005` `2010` `2014`
    ##       <int>      <int>  <dbl>  <dbl>  <dbl>
    ## 1         1          1  13.1   10.7   11.2 
    ## 2         4          1   6.27   5.08   4.52
    ## 3         5          1  13.4   11.1    9.81
    ## 4         6          1  10.0    9.30   8.97
    ## 5         8          1   9.32   8.04   8.51
    ## 6         9          1  12.2    8.53   8.92

``` r
# recast as characters to create compound FIPS
p25_df$countyfips =  as.character(p25_df$countyfips)
p25_df$statefips =  as.character(p25_df$statefips)

# creating descriptive FIPS with both state and county
p25_df = p25_df %>%
  mutate(coded_countyFIPS = case_when(nchar(countyfips) == 1 ~ paste0("00", countyfips),
                      nchar(countyfips) == 2 ~ paste0("0", countyfips),
                      nchar(countyfips) == 3 ~ countyfips)) %>% 
  mutate(coded_stateFIPS = case_when(nchar(statefips) == 1 ~ paste0("0", statefips),
                    nchar(statefips) == 2 ~ statefips)) %>% 
  mutate(FIPS = paste0(coded_stateFIPS, coded_countyFIPS)) %>% 
  dplyr::select(-countyfips, -statefips, -coded_countyFIPS, -coded_stateFIPS) %>% 
  drop_na()

# rename columns
colnames(p25_df) = c('PM25_mean2005','PM25_mean2010', 'PM25_mean2014', 'FIPS')
```

``` r
# wrangled data example (pre-join)

# Reverting FIPS dtype to match mort_df now that compound FIPS has been made
p25_df$FIPS =  as.double(p25_df$FIPS)

head(mort_df)
```

    ## # A tibble: 6 x 5
    ## # Groups:   Location [6]
    ##   Location                          FIPS MR_2005 MR_2010 MR_2014
    ##   <chr>                            <dbl>   <dbl>   <dbl>   <dbl>
    ## 1 Abbeville County, South Carolina 45001    87.0    81.4    81.2
    ## 2 Acadia Parish, Louisiana         22001   118.    106.    108. 
    ## 3 Accomack County, Virginia        51001    97.1    86.9    86.3
    ## 4 Ada County, Idaho                16001    77.9    66.3    68.4
    ## 5 Adair County, Iowa               19001    88.1    82.3    81.4
    ## 6 Adair County, Kentucky           21001   112.    103.    104.

``` r
head(p25_df)
```

    ## # A tibble: 6 x 4
    ##   PM25_mean2005 PM25_mean2010 PM25_mean2014  FIPS
    ##           <dbl>         <dbl>         <dbl> <dbl>
    ## 1         13.1          10.7          11.2   1001
    ## 2          6.27          5.08          4.52  4001
    ## 3         13.4          11.1           9.81  5001
    ## 4         10.0           9.30          8.97  6001
    ## 5          9.32          8.04          8.51  8001
    ## 6         12.2           8.53          8.92  9001

``` r
# Joined data on FIPS.
data = inner_join(p25_df, mort_df, by="FIPS")


head(data)
```

    ## # A tibble: 6 x 8
    ##   PM25_mean2005 PM25_mean2010 PM25_mean2014  FIPS Location MR_2005 MR_2010
    ##           <dbl>         <dbl>         <dbl> <dbl> <chr>      <dbl>   <dbl>
    ## 1         13.1          10.7          11.2   1001 Autauga~   115.    102. 
    ## 2          6.27          5.08          4.52  4001 Apache ~    73.0    67.4
    ## 3         13.4          11.1           9.81  5001 Arkansa~   135.    124. 
    ## 4         10.0           9.30          8.97  6001 Alameda~    77.8    64.1
    ## 5          9.32          8.04          8.51  8001 Adams C~    78.2    67.7
    ## 6         12.2           8.53          8.92  9001 Fairfie~    75.2    62.8
    ## # ... with 1 more variable: MR_2014 <dbl>

# Experiment and Results

``` r
# exploratory plotting to find an appropriate models

# 2005
plot_2005 = ggplot() +
  # data
  geom_point(mapping = aes(x = PM25_mean2005, y = MR_2005), 
             data = data, 
             shape = 1) +
  # gamma best fit
  geom_smooth(data= data, mapping = aes(x = PM25_mean2005,y = MR_2005)) +
  # plot aesthetics
  theme_light() +
  xlab(expression(paste(PM2.5, phantom(x), (mu*g/m^3)))) +
  ylab("Mortality Rate (Death per 100,000)") +
  ggtitle("2005") +
  ylim(0, 200) +
  xlim(0, 19)
 

# 2010
plot_2010 = ggplot(data = data) +
  # data
  geom_point(mapping = aes(x = PM25_mean2010, 
                           y = MR_2010), 
                           shape = 1) +
  # gamma best fit
  geom_smooth(data= data, mapping = aes(x = PM25_mean2010,y = MR_2010)) + 
  # plot aesthetics
  theme_light() +
  xlab(expression(paste(PM2.5, phantom(x), (mu*g/m^3)))) +
  ylab("Mortality Rate (Death per 100,000)") +
  ggtitle("2010") +
  ylim(0, 200) +
  xlim(0, 19)


# 2014
plot_2014 = ggplot(data = data) +
  # data
  geom_point(mapping = aes(x = PM25_mean2014, 
                           y = MR_2014), 
                           shape = 1) +
  # gamma best fit
  geom_smooth(data= data, 
              mapping = aes(x = PM25_mean2014,y = MR_2014)) +
  # plot aesthetics  
  theme_light() +
  xlab(expression(paste(PM2.5, phantom(x), (mu*g/m^3)))) +
  ylab("Mortality Rate (Death per 100,000)") +
  ggtitle("2014") +
  ylim(0, 200) +
  xlim(0, 19)


# multi plot of all 3 exploratory plots/fits
grid.arrange(plot_2005, plot_2010, plot_2014, nrow = 1,
             top = textGrob("Figure 1: Mortality Rate vs PM2.5 Concentration with Fit", 
                            gp=gpar(fontsize=16)))
```

    ## `geom_smooth()` using method = 'gam' and formula 'y ~ s(x, bs = "cs")'
    ## `geom_smooth()` using method = 'gam' and formula 'y ~ s(x, bs = "cs")'
    ## `geom_smooth()` using method = 'gam' and formula 'y ~ s(x, bs = "cs")'

![](mortality_polution_files/figure-gfm/unnamed-chunk-17-1.png)<!-- -->

<center>

<sup><i>Figure 1: Is the county level Mortality Rate vs PM2.5
Concentration <b>(Black)</b> and a smooth gamma fit
<b><span style="color: blue"> (Blue) </span></b> for each year: 2005,
2010, and 2014 .</i></sup>

</center>

``` r
# Linear models for each year.

model_2005 = lm(MR_2005 ~  PM25_mean2005, data = data)
summary(model_2005)
```

    ## 
    ## Call:
    ## lm(formula = MR_2005 ~ PM25_mean2005, data = data)
    ## 
    ## Residuals:
    ##     Min      1Q  Median      3Q     Max 
    ## -50.303 -10.994  -1.402  10.149  88.790 
    ## 
    ## Coefficients:
    ##               Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)    70.0552     1.2232   57.27   <2e-16 ***
    ## PM25_mean2005   2.5126     0.1071   23.46   <2e-16 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 15.95 on 3105 degrees of freedom
    ## Multiple R-squared:  0.1506, Adjusted R-squared:  0.1503 
    ## F-statistic: 550.5 on 1 and 3105 DF,  p-value: < 2.2e-16

``` r
model_2010 = lm(MR_2010 ~  PM25_mean2010, data = data)
summary(model_2010)
```

    ## 
    ## Call:
    ## lm(formula = MR_2010 ~ PM25_mean2010, data = data)
    ## 
    ## Residuals:
    ##     Min      1Q  Median      3Q     Max 
    ## -46.917 -10.825  -1.037   9.681  82.469 
    ## 
    ## Coefficients:
    ##               Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)    54.7529     1.3435   40.76   <2e-16 ***
    ## PM25_mean2010   3.6069     0.1429   25.25   <2e-16 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 15.47 on 3105 degrees of freedom
    ## Multiple R-squared:  0.1703, Adjusted R-squared:  0.1701 
    ## F-statistic: 637.5 on 1 and 3105 DF,  p-value: < 2.2e-16

``` r
model_2014 = lm(MR_2014 ~  PM25_mean2014, data = data)
summary(model_2014)
```

    ## 
    ## Call:
    ## lm(formula = MR_2014 ~ PM25_mean2014, data = data)
    ## 
    ## Residuals:
    ##     Min      1Q  Median      3Q     Max 
    ## -44.749 -11.425  -1.413  10.272  81.446 
    ## 
    ## Coefficients:
    ##               Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)    54.2432     1.3751   39.45   <2e-16 ***
    ## PM25_mean2014   3.9021     0.1547   25.22   <2e-16 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 16.43 on 3105 degrees of freedom
    ## Multiple R-squared:   0.17,  Adjusted R-squared:  0.1697 
    ## F-statistic: 635.9 on 1 and 3105 DF,  p-value: < 2.2e-16

Being unlikely that populations respond differently to PM2.5 between the
years 2005 and 2014, all years of data are combined to get a first order
approximation of any relationship between PM2.5 concentration and human
morality rates.

``` r
# creating time invariant dataset using all three years
time_invar_data = data.frame(data$Location, data$FIPS, 
                       c(data$PM25_mean2005, data$PM25_mean2010, data$PM25_mean2014),
                       c(data$MR_2005, data$MR_2010, data$MR_2014))
colnames(time_invar_data) = c("Location", "FIPS", "PM25_mean", "MR")
```

``` r
# time invariant data exploration

# All Years
ggplot() +
  # data
  geom_point(mapping = aes(x = PM25_mean, y = MR), 
             data = time_invar_data, 
             shape = 1) +
  # gamma best fit
  geom_smooth(data= time_invar_data, mapping = aes(x = PM25_mean, y = MR)) +
  # plot aesthetics
  theme_light() +
  xlab(expression(paste(PM2.5, phantom(x), (mu*g/m^3)))) +
  ylab("Mortality Rate (Death per 100,000)") +
  ggtitle("Figure 2: Mortality Rate vs PM2.5 Concentration, All Years") +
  ylim(0, 200) +
  xlim(0, 19) +
  theme(plot.title = element_text(size = 16)) 
```

    ## `geom_smooth()` using method = 'gam' and formula 'y ~ s(x, bs = "cs")'

![](mortality_polution_files/figure-gfm/unnamed-chunk-20-1.png)<!-- -->

<center>

<sup><i>Above is the county level Mortality Rate vs PM2.5 Concentration
<b>(Black)</b> and a smooth gamma fit <b><span style="color: blue">
(Blue) </span></b>.</i></sup>

</center>

Time invariant data shows a stronger linear relationship. Still retains
trend seen in yearly models around 9 micrograms per cubic meter where
there is an increase in mortality.

``` r
# making a linear model with data from all three years
model = lm(MR ~  PM25_mean, data = time_invar_data)
coef(model)
```

    ## (Intercept)   PM25_mean 
    ##   58.771763    3.370418

``` r
summary(model)
```

    ## 
    ## Call:
    ## lm(formula = MR ~ PM25_mean, data = time_invar_data)
    ## 
    ## Residuals:
    ##     Min      1Q  Median      3Q     Max 
    ## -49.776 -11.372  -1.301  10.238  93.516 
    ## 
    ## Coefficients:
    ##             Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)  58.7718     0.6816   86.23   <2e-16 ***
    ## PM25_mean     3.3704     0.0684   49.27   <2e-16 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 16.09 on 9319 degrees of freedom
    ## Multiple R-squared:  0.2067, Adjusted R-squared:  0.2066 
    ## F-statistic:  2428 on 1 and 9319 DF,  p-value: < 2.2e-16

``` r
# plotting time invariant data, best fit, and residuals
ggplot(data = time_invar_data) +
  #data
  geom_point(mapping = aes(x = PM25_mean, 
                           y = MR), 
               shape = 1,
               col="black") +
  # residuals
  geom_segment(aes(x=PM25_mean, 
                 y= MR ,
                 xend = PM25_mean, 
                 yend = model$fitted.values), 
             alpha = 0.07,
             col='magenta') + 
  # linear best fit
  geom_function(fun = function(x) coef(model)[1] + coef(model)[2]*x, 
              col='red', 
              size = 1.1,) + 
  # plot aesthetics
  xlab(expression(paste(PM2.5, phantom(x), (mu*g/m^3)))) +
  ylab("Mortality Rate (Death per 100,000)") +
  ggtitle("Figure 3: Mortality Rate vs PM2.5 Concentration with Best Fit and Residuals, All Years") +
  ylim(0, 200) +
  xlim(0, 19) +
  theme_light() +
  theme(plot.title = element_text(size = 16)) 
```

![](mortality_polution_files/figure-gfm/unnamed-chunk-21-1.png)<!-- -->

<center>

<sup><i>Above is the county level Mortality Rate vs PM2.5 Concentration
<b>(Black)</b>, linear regression model <b><span style="color: red">
(Red) </span></b>, and the residuals <b><span style="color: magenta">
(Magenta) </span></b>.</i></sup>

</center>

``` r
# residuals vs fitted
rfitt = ggplot(mapping = aes(x=fitted(model), y=resid(model))) +
  geom_point(shape = 1,
              col="black") +
  geom_hline(yintercept=0, 
             linetype="dashed", 
             col="cyan",size = 1) +
  theme_light() +
  geom_smooth(col='red') + 
  xlab("Fitted Values") +
  ylab("Residuals") +
  ggtitle("Residuals vs. Fitted")

# Normal Q-Q
nqq = ggplot(data = model, aes(sample = rstandard(model))) +
  stat_qq(shape = 1,
          col="black") +
  stat_qq_line(linetype="dashed",
               col="cyan",
               size = 1) +
  theme_light() +
  xlab("Theoretical Quantiles") +
  ylab("Standardized Residuals") +
  ggtitle("Normal Q-Q")

# Side by side plots
grid.arrange(rfitt, nqq, nrow = 1,
             top = textGrob("Figure 4: Statistical Plots", 
                            gp=gpar(fontsize=16)))
```

    ## `geom_smooth()` using method = 'gam' and formula 'y ~ s(x, bs = "cs")'

![](mortality_polution_files/figure-gfm/unnamed-chunk-22-1.png)<!-- -->

``` r
# compute 95% prediction confidence 
confint(model, level=0.95)
```

    ##                 2.5 %    97.5 %
    ## (Intercept) 57.435687 60.107840
    ## PM25_mean    3.236339  3.504497

``` r
# test homoscedasticity 
ols_test_breusch_pagan(model)
```

    ## 
    ##  Breusch Pagan Test for Heteroskedasticity
    ##  -----------------------------------------
    ##  Ho: the variance is constant            
    ##  Ha: the variance is not constant        
    ## 
    ##              Data              
    ##  ------------------------------
    ##  Response : MR 
    ##  Variables: fitted values of MR 
    ## 
    ##          Test Summary           
    ##  -------------------------------
    ##  DF            =    1 
    ##  Chi2          =    25.82274 
    ##  Prob > Chi2   =    3.742532e-07

# Discussion

By using data from all sets to examine the potential relationship
between airborne PM2.5 concentrations and mortality rates due to health
complications which have been previously linked to its inhalation, a
linear model was created and visualized in *Figure 3*.

**Equation 1: Linear Regression Best Fit** <br> *MR = (58.8 +/- 1.36) +
(3.37 +/- 0.137)p*

*Equation 1* states that the Mortality Rate (MR) increases by
approximately 3.37 deaths per 100,000 population (p) for each integer
increase in micrograms of PM2.5 per cubic meter. This is an one variable
approximation of a complex system, and as such it is not expected to get
an exceptionally high R<sup>2</sup> value. The observed value was 0.2067
R<sup>2</sup> which supports the concept that mortality from these
health conditions has other deterministic factors outside of PM2.5
presence in the air. However, the p-value: \< 2.2e<sup>-16</sup>
signifies that the observed relationship between increased PM2.5
pollution and increased mortality due to the linked health complications
is very unlikely to be a random occurrence.

Looking at *Figure 1* and *Figure 3*, at approximately 9 micrograms
PM2.5 per cubic meter there an unknown event. This is seen in *Figure 1*
as a break from linearity and in *Figure 3* as a location where a
deviation from homoscedasticity takes place. Both of these were also
observed when investigating single year models. This is where an
increase in morality rate occurs and is not accurately described by a
linear fit.

**Residuals vs Fitted:** <br> This suggests that the relationship
between PM2.5 concentration and mortality rate is reasonable to be
described by a linear approximation. Observations supporting this from
*Figure 4* are that the residuals are mostly evenly distributed about
the 0 line, and the fit of the two approximately follows the 0 line as
well. There is a break from linearity seen for extreme values of
morality.

**Q-Q:** <br> Similar to the *Residual vs Fitted* plot in *Figure 4*,
this supports the linear description of the relationship between PM2.5
concentration and Mortality due to health conditions linked to PM2.5
exposure. The linear relationship is able to describe the data, but as
the quantiles become more extreme, deviation from this behavior occurs.

**Breusch Pagan** <br> Seeing a break from homoscedasticity in
exploratory plots, the Breusch Pagan test was used to verify that
variances were not homogeneous. This produced a test statistic that
strongly rejected the hypothesis that variances are produced similarly
across all observations.

Being a one parameter simplification, it was expected that no model
would be perfect as there are many known causes to the selected health
conditions. While *Equation 1* can be used to get an approximation of
the death rate in each county based on pollution levels, other
parameters need to be considered.

## Moving Forward

Any investigation should include:

  - Other airborne pollutants linked to the health conditions.
    Specifically, any co-occurring pollutants present at higher PM2.5
    concentrations and not low concentrations.
  - Include other known causes to the chosen health conditions in future
    models.
  - Inspect PM2.5’s relationship to morality rates for individual causes
    of death.
  - Further research into PM2.5 toxicity thresholds and human capacity
    to metabolize.
  - Deeper investigation into the event around 9 micrograms of PM2.5 per
    cubic meter.
