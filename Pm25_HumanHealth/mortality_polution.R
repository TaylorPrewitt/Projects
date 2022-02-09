# loading in libraries for investigation 
library(tidyverse)
library(ggplot2)
library(MASS)
library(gridExtra)
library(grid)
library(olsrr)


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
count_missing_vals = function(df) 
  {missing_vals = c(0)
  dataset = df
  for (col in 1:ncol(dataset))
    {missing_vals = append(missing_vals, sum(is.na(dataset[,col])))}
  missing_vals = missing_vals[1:length(dataset)]
  missing_vals_df = data.frame(Variable = c(colnames(dataset)),
                               NumMissing = missing_vals)
  return(missing_vals_df)}

# searching for missing values
count_missing_vals(mort_data)
count_missing_vals(p25_data)

# find NA values from count
which(is.na(mort_data))

# inspect data at/around these df cell values
# cell 67075 is index 1 of column 2
mort_data[1,]
mort_data[(70269-67074),]
mort_data[(70269-67072):(70269-67076),]

# removing bad data
mort_data = subset(mort_data, mort_data$FIPS > 1000 | is.na(mort_data$FIPS) == FALSE)

# condense p25_data to year value from daily. with only common years
# making df with for model with no index values as variable
p25_df = p25_data %>% 
  group_by(year, statefips, countyfips) %>%
  filter(year %in% c(2005, 2010, 2014)) %>% 
  summarise(PM25_mean = mean(PM25_mean_pred))

# get yearly average PM2.5 value
p25_df = aggregate(p25_df[, 2:4], list(p25_df$year, 
                                       p25_df$statefips, 
                                       p25_df$countyfips), mean)

# keep only needed columns and rename
p25_df = p25_df %>% 
  dplyr::select(Group.1, Group.2, Group.3, PM25_mean)
colnames(p25_df) = c('year','statefips', 'countyfips', 'PM25_mean')

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

# transpose year data into columns for FIPS joining 
p25_df = pivot_wider(p25_df, 
                     id_cols = c("statefips","countyfips"),
                     names_from = "year", 
                     values_from = "PM25_mean")

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

# Joined data on FIPS.
data = inner_join(p25_df, mort_df, by="FIPS")

# exploratory plotting to find an appropriate models

# 2005
plot_2005 = ggplot() +
  # data
  geom_point(mapping = aes(x = PM25_mean2005, 
                           y = MR_2005), 
             data = data, 
             shape = 1) +
  # gamma best fit
  geom_smooth(data= data, mapping = aes(x = PM25_mean2005,
                                        y = MR_2005)) +
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
  geom_smooth(data= data, mapping = aes(x = PM25_mean2010,
                                        y = MR_2010)) + 
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
              mapping = aes(x = PM25_mean2014, 
                            y = MR_2014)) +
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

# Linear models for each year.

model_2005 = lm(MR_2005 ~  PM25_mean2005, data = data)
summary(model_2005)

model_2010 = lm(MR_2010 ~  PM25_mean2010, data = data)
summary(model_2010)

model_2014 = lm(MR_2014 ~  PM25_mean2014, data = data)
summary(model_2014)

# creating time invariant dataset using all three years
time_invar_data = data.frame(data$Location, data$FIPS, 
                             c(data$PM25_mean2005, data$PM25_mean2010, data$PM25_mean2014),
                             c(data$MR_2005, data$MR_2010, data$MR_2014))
colnames(time_invar_data) = c("Location", "FIPS", "PM25_mean", "MR")


# time invariant data exploration

# All Years
ggplot() +
  # data
  geom_point(mapping = aes(x = PM25_mean, 
                           y = MR), 
             data = time_invar_data, 
             shape = 1) +
  # gamma best fit
  geom_smooth(data= time_invar_data, 
              mapping = aes(x = PM25_mean, 
                            y = MR)) +
  # plot aesthetics
  theme_light() +
  xlab(expression(paste(PM2.5, phantom(x), (mu*g/m^3)))) +
  ylab("Mortality Rate (Death per 100,000)") +
  ggtitle("Figure 2: Mortality Rate vs PM2.5 Concentration, All Years") +
  ylim(0, 200) +
  xlim(0, 19) +
  theme(plot.title = element_text(size = 16)) 

# making a linear model with data from all three years
model = lm(MR ~  PM25_mean, data = time_invar_data)
coef(model)
summary(model)

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

# residuals vs fitted
rfitt = ggplot(mapping = aes(x=fitted(model), 
                             y=resid(model))) +
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
nqq = ggplot(data = model, 
             aes(sample = rstandard(model))) +
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

# compute 95% prediction confidence 
confint(model, level=0.95)

# test homoscedasticity 
ols_test_breusch_pagan(model)



