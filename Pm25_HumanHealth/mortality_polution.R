# loading in libraries for investigation 

library(tidyverse)
library(ggplot2)
library(MASS)

# loading in the data, county level mortality
mort_data = read.csv("mort.csv",
                     header=TRUE)

# loading in the data, county level PM2.5 concentrations  
p25_data = read.csv("Daily_PM2.5_Concentrations_All_County__2001-2016.csv",
                    header=TRUE)


# data examples
head(mort_data)
head(p25_data)

# inspecting data types
str(mort_data)
str(p25_data)

# general inspection of data
dim(mort_data)
names(mort_data)
dim(p25_data)
names(p25_data)



# getting causes of death
unique(mort_data$Category)

# creating function to count any missing values in data
count_missing_vals = function(df) {
  missing_vals = c(0)
  dataset = df
  for (col in 1:ncol(dataset))
  {
    missing_vals = append(missing_vals, sum(is.na(dataset[,col])))
  }
  missing_vals = missing_vals[1:length(dataset)]
  missing_vals_df = data.frame(Variable = c(colnames(dataset)),
                               NumMissing = missing_vals)
  return(missing_vals_df)
}


# searching for missing values
count_missing_vals(mort_data)
count_missing_vals(p25_data)


# condense p25_data to year value from daily. with only common years


# making df with for model with no index values as variable
p25_df = p25_data %>% 
  group_by(year, statefips, countyfips) %>%
  filter(year %in% c(2005, 2010, 2014)) %>% 
  summarise(PM25_mean = mean(PM25_mean_pred))


# get yearly average PM2.5 value
p25_df = aggregate(p25_df[, 2:4], list(p25_df$year, p25_df$statefips, p25_df$countyfips), mean)

# keep only needed columns and rename
p25_df = p25_df %>% 
  dplyr::select(Group.1, Group.2, Group.3, PM25_mean)
colnames(p25_df) = c('year','statefips', 'countyfips', 'PM25_mean')


head(p25_df)


# keep data with common years for linked health issues
mort_df = mort_data %>% 
  group_by(Category) %>% 
  filter(Category %in% c("Chronic respiratory diseases", "Cardiovascular diseases",
                         "Neonatal disorders", "Other non-communicable diseases")) %>% 
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

head(mort_df)



# transpose year data into columns for FIPS joining 
p25_df = pivot_wider(p25_df, 
                     id_cols = c("statefips","countyfips"),
                     names_from = "year", 
                     values_from = "PM25_mean")


head(p25_df)


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

# wrangled data example (pre-join)

# Reverting FIPS dtype to match mort_df now that compound FIPS has been made
p25_df$FIPS =  as.double(p25_df$FIPS)

head(mort_df)
head(p25_df)

# Joined data on FIPS.

data = inner_join(p25_df, mort_df, by="FIPS")


head(data)



# exploratory plotting to find an appropriate models

# 2005
ggplot() +
  geom_point(mapping = aes(x = PM25_mean2005, y = MR_2005), 
             data = data, 
             shape = 1) +
  theme_light() +
  xlab(expression(paste(PM2.5, phantom(x), (mu*g/m^3)))) +
  ylab("Mortality Rate (Death per 100,000)") +
  ggtitle("Figure 1: Mortality Rate vs PM2.5 Concentration with Residuals, 2005") +
  ylim(0, 200) +
  xlim(0, 19) +
  geom_smooth(data= data, mapping = aes(x = PM25_mean2005,y = MR_2005))

# 2010
ggplot(data = data) +
  geom_point(mapping = aes(x = PM25_mean2010, 
                           y = MR_2010), 
             shape = 1) +
  theme_light() +
  xlab(expression(paste(PM2.5, phantom(x), (mu*g/m^3)))) +
  ylab("Mortality Rate (Death per 100,000)") +
  ggtitle("Figure 2: Mortality Rate vs PM2.5 Concentration with Residuals, 2010") +
  ylim(0, 200) +
  xlim(0, 19)+ 
  geom_smooth(data= data, mapping = aes(x = PM25_mean2010,y = MR_2010))

# 2014
ggplot(data = data) +
  geom_point(mapping = aes(x = PM25_mean2014, 
                           y = MR_2014), 
             shape = 1) +
  theme_light() +
  xlab(expression(paste(PM2.5, phantom(x), (mu*g/m^3)))) +
  ylab("Mortality Rate (Death per 100,000)") +
  ggtitle("Figure 3: Mortality Rate vs PM2.5 Concentration with Residuals, 2014") +
  ylim(0, 200) +
  xlim(0, 19) +
  geom_smooth(data= data, 
              mapping = aes(x = PM25_mean2014,y = MR_2014))



# Linear models for each year.

model_2005 = lm(MR_2005 ~  PM25_mean2005, data = data)
summary(model_2005)

model_2010 = lm(MR_2010 ~  PM25_mean2010, data = data)
summary(model_2010)

model_2014 = lm(MR_2014 ~  PM25_mean2014, data = data)
summary(model_2014)


# Plot of data, best fit line, and model residuals for 2005
ggplot() +
  geom_point(mapping = aes(x = PM25_mean2005, y = MR_2005), 
             data = data, 
             shape = 1) +
  theme_light() +
  xlab(expression(paste(PM2.5, phantom(x), (mu*g/m^3)))) +
  ylab("Mortality Rate (Death per 100,000)") +
  ggtitle("Figure 4: Mortality Rate vs PM2.5 Concentration with Residuals, 2005") +
  ylim(0, 200) +
  xlim(0, 19) +
  geom_function(fun = function(x) coef(model_2005)[1] + coef(model_2005)[2]*x, 
                col='red', 
                size = 1.1) +
  geom_segment(aes(x=data$PM25_mean2005, 
                   y= data$MR_2014 ,
                   xend = data$PM25_mean2005, 
                   yend = model_2005$fitted.values), 
               alpha = 0.07,
               col='magenta')               


# Plot of data, best fit line, and model residuals for 2010
ggplot(data = data) +
  geom_point(mapping = aes(x = PM25_mean2010, 
                           y = MR_2010), 
             shape = 1) +
  theme_light() +
  xlab(expression(paste(PM2.5, phantom(x), (mu*g/m^3)))) +
  ylab("Mortality Rate (Death per 100,000)") +
  ggtitle("Figure 5: Mortality Rate vs PM2.5 Concentration with Residuals, 2010") +
  ylim(0, 200) +
  xlim(0, 19)+ 
  geom_function(fun = function(x) coef(model_2010)[1] + coef(model_2010)[2]*x, 
                col='red', 
                size = 1.1) +
  geom_segment(aes(x=PM25_mean2010, 
                   y= MR_2010 ,
                   xend = PM25_mean2010, 
                   yend = model_2010$fitted.values), 
               alpha = 0.07,
               col='magenta')


# Plot of data, best fit line, and model residuals for 2014
ggplot(data = data) +
  geom_point(mapping = aes(x = PM25_mean2014, 
                           y = MR_2014), 
             shape = 1) +
  theme_light() +
  xlab(expression(paste(PM2.5, phantom(x), (mu*g/m^3)))) +
  ylab("Mortality Rate (Death per 100,000)") +
  ggtitle("Figure 6: Mortality Rate vs PM2.5 Concentration with Residuals, 2014") +
  ylim(0, 200) +
  xlim(0, 19) +
  geom_function(fun = function(x) coef(model_2014)[1] + coef(model_2014)[2]*x, 
                col='red', 
                size = 1.1) +
  geom_segment(aes(x=PM25_mean2014, 
                   y= MR_2014 ,
                   xend = PM25_mean2014, 
                   yend = model_2014$fitted.values), 
               alpha = 0.07,
               col='magenta') 


# creating time invariant dataset using all three years
time_invar_data = data.frame(data$Location, data$FIPS, 
                             c(data$PM25_mean2005, data$PM25_mean2010, data$PM25_mean2014),
                             c(data$MR_2005, data$MR_2010, data$MR_2014))
colnames(time_invar_data) = c("Location", "FIPS", "PM25_mean", "MR")


# time invariant data exploration

# All Years
ggplot() +
  geom_point(mapping = aes(x = PM25_mean, y = MR), 
             data = time_invar_data, 
             shape = 1) +
  theme_light() +
  xlab(expression(paste(PM2.5, phantom(x), (mu*g/m^3)))) +
  ylab("Mortality Rate (Death per 100,000)") +
  ggtitle("Figure 7: Mortality Rate vs PM2.5 Concentration, All Years") +
  ylim(0, 200) +
  xlim(0, 19) +
  geom_smooth(data= time_invar_data, mapping = aes(x = PM25_mean,y = MR))


# making a linear model with data from all three years
model = lm(MR ~  PM25_mean, data = time_invar_data)
coef(model)
summary(model)

# plotting time invariant data, best fit, and residuals
ggplot(data = time_invar_data) +
  geom_point(mapping = aes(x = PM25_mean, 
                           y = MR), 
             shape = 1,
             col="black") +
  xlab(expression(paste(PM2.5, phantom(x), (mu*g/m^3)))) +
  ylab("Mortality Rate (Death per 100,000)") +
  ggtitle("Figure 8: Mortality Rate vs PM2.5 Concentration with Residuals, All Years") +
  ylim(0, 200) +
  xlim(0, 19) +
  geom_segment(aes(x=PM25_mean, 
                   y= MR ,
                   xend = PM25_mean, 
                   yend = model$fitted.values), 
               alpha = 0.05,
               col='magenta') + 
  
  geom_function(fun = function(x) coef(model)[1] + coef(model)[2]*x, 
                col='red', 
                size = 1.1,) +
  theme_light()



