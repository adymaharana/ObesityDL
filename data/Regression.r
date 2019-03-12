#Thurs May 18, 2017
#Land use and crime correlated. See publications.


rm(list = ls())

#Read data and model it
library(MASS)
library(glmnet)
###Convert response to log scale

#set random seed
set.seed(1768)


#Read the data
#Seattle-Tacoma-Bellevue
datx <- read.table("~/Dropbox/obesity/Seattle-Tacoma-Bellevue/X_sea-tac-bel_z16.txt", stringsAsFactors = FALSE)
daty <- read.table("~/Dropbox/obesity/Seattle-Tacoma-Bellevue/obesity_sea-tac-bel_z16.txt", stringsAsFactors = FALSE)

#Los Angeles
datx <- read.table("~/Dropbox/obesity/Los Angeles/X_lacity_z18.txt", stringsAsFactors = FALSE)
daty <- read.table("~/Dropbox/obesity/Los Angeles/obesity_lacity_z18.txt", stringsAsFactors = FALSE)


datx <- as.matrix(datx)
#daty <- log(as.matrix(daty))
daty <- as.matrix(daty)

#10-fold cross validation for each alpha (try different alpha values)
fit.elnet.cv <- cv.glmnet(datx, daty, type.measure="mse", family="gaussian", alpha=0.5, standardize.response=TRUE) #standardize.response


yhat <- predict(fit.elnet.cv, s=fit.elnet.cv$lambda.min, newx=datx)
plot(yhat, daty, xlab="predicted", ylab="true value", bty="l")
#plot(exp(yhat), exp(daty))
cor(yhat, daty) #0.8734496

#out <- cbind(exp(yhat), exp(daty))
out <- data.frame(cbind(yhat, daty))
colnames(out) <- c("predict_all", "true_all")



#Remove outliers and rerun

