#Thurs May 18, 2017
#This code runs Elastic Net regression on the features extracted from the satellite images using the CNN
#

#X_lacity_fc7_vggf_z18.txt - feature file
#y_lacity_fc7_vggf_z18.txt - obesity prevalence from 500 cities project
#X_lacity_poi.txt - points of interest data from Google 


rm(list = ls())

library(MASS)
library(glmnet)


#set random seed
set.seed(1768)


#Read the data
datx <- read.table("~/Dropbox/obesity/Los Angeles/X_lacity_fc7_vggf_z18.txt", stringsAsFactors = FALSE) 
daty <- read.table("~/Dropbox/obesity/Los Angeles/y_lacity_fc7_vggf_z18.txt", stringsAsFactors = FALSE)

datx <- as.matrix(datx) #n=4096 features
daty <- as.matrix(daty) #n=993 census tracts
length(daty)

#10-fold cross validation for each alpha value (try different alpha values and compare model fit)
fit.elnet.cv <- cv.glmnet(datx, daty, type.measure="mse", family="gaussian", nfolds=5, alpha=0.5, standardize.response=TRUE) 


yhat <- predict(fit.elnet.cv, s=fit.elnet.cv$lambda.min, newx=datx)
plot(yhat, daty, xlab="predicted obesity prevalence", ylab="obesity prevalence", bty="l")
print(cor(yhat, daty))

out <- data.frame(cbind(yhat, daty))
colnames(out) <- c("predict", "true")
write.table(out, "~/Dropbox/obesity/Los Angeles/predicted_features.txt", row.names=FALSE, col.names=TRUE, quote=FALSE)

##########################################################################################
##########################################################################################
#Point of interest data

#Read the data
datx <- read.table("~/Dropbox/obesity/Los Angeles/X_lacity_poi.txt", stringsAsFactors = FALSE)
daty <- read.table("~/Dropbox/obesity/Los Angeles/y_lacity_fc7_vggf_z18.txt", stringsAsFactors = FALSE)

datx <- as.matrix(datx)
daty <- as.matrix(daty)

#5-fold cross validation for each alpha (try different alpha values and compare model fit)
fit.elnet.cv <- cv.glmnet(datx, daty, type.measure="mse", family="gaussian", nfolds=5, alpha=0.5, standardize.response=TRUE) 

yhat <- predict(fit.elnet.cv, s=fit.elnet.cv$lambda.min, newx=datx)

#visualize and compute correlation 
plot(yhat, daty, xlab="predicted obesity prevalence", ylab="obesity prevalence", bty="l")
print(cor(yhat, daty)) 

#write predictions to file 
out <- data.frame(cbind(yhat, daty))
colnames(out) <- c("predict", "true")
write.table(out, "~/Dropbox/obesity/Los Angeles/predicted_poi.txt", row.names=FALSE, col.names=TRUE, quote=FALSE)

