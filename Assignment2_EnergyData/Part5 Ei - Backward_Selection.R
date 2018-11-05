library(ISLR)
library(leaps)
library(tidyverse)
library(caret)

regfit.bwd=regsubsets(Energy_consumed~.,data=Revised_Data,nvmax=34,method = "backward")
B=summary(regfit.bwd)
names(B)
B
B$rss
B$adjr2
coef(regfit.bwd,34)




