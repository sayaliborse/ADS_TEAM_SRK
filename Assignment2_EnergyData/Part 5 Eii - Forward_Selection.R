library(ISLR)
library(leaps)
library(tidyverse)
library(caret)

regfit.fwd=regsubsets(Energy_consumed~.,data=Revised_Data,nvmax=34,method = "forward")
B=summary(regfit.fwd)
names(B)
B
B$rss
B$adjr2
coef(regfit.fwd,34)


     