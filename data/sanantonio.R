rm(list = ls())

#Read data and model it
library(MASS)
library(glmnet)

#set random seed
set.seed(100)


#Read the data
datx <- read.table("~/Dropbox/obesity/San Antonio/X_san-antonio_fc7_vggf_z18.txt", stringsAsFactors = FALSE) #4096
daty <- read.table("~/Dropbox/obesity/San Antonio/y_san-antonio_fc7_vggf_z18.txt", stringsAsFactors = FALSE)

datx <- as.matrix(datx) #4096 features
daty <- as.matrix(daty) #n=311
length(daty)

#10-fold cross validation for each alpha (try different alpha values)
fit.elnet.cv <- cv.glmnet(datx, daty, type.measure="mse", family="gaussian", nfolds=5, alpha=0.5, standardize.response=TRUE) #standardize.response


yhat <- predict(fit.elnet.cv, s=fit.elnet.cv$lambda.min, newx=datx)
plot(yhat, daty, xlab="predicted", ylab="true value", bty="l")
cor(yhat, daty) #0.9072027

out <- data.frame(cbind(yhat, daty))
colnames(out) <- c("predict_all", "true_all")
write.table(out, "~/Dropbox/obesity/San Antonio/predicted_features.txt", row.names=FALSE, col.names=TRUE, quote=FALSE)

#Extract and write out most significant coefficients to a file
temp1 <- coef(fit.elnet.cv, s="lambda.min")
temp2 <- row.names(temp1)
temp.dat <- data.frame(temp2, as.numeric(temp1[,1])); colnames(temp.dat) <- c("variables", "coefficients")
fin.coef <- temp.dat[order(temp.dat$coefficients, decreasing=TRUE),]
fin.coef <- subset(fin.coef, coefficients != 0)
write.table(fin.coef, "~/Dropbox/obesity/San Antonio/significant_coeffs_features.txt", row.names=FALSE)

##########################################################################################
##########################################################################################
#Analysis with point of interest
#Read the data
datx <- read.table("~/Dropbox/obesity/San Antonio/X_san-antonio_poi.txt", stringsAsFactors = FALSE) #101
daty <- read.table("~/Dropbox/obesity/San Antonio/y_san-antonio_fc7_vggf_z18.txt", stringsAsFactors = FALSE)

datx <- as.matrix(datx)
daty <- as.matrix(daty)

#10-fold cross validation for each alpha (try different alpha values)
fit.elnet.cv <- cv.glmnet(datx, daty, type.measure="mse", family="gaussian", nfolds=5, alpha=0.5, standardize.response=TRUE) #standardize.response


yhat <- predict(fit.elnet.cv, s=fit.elnet.cv$lambda.min, newx=datx)
plot(yhat, daty, xlab="predicted", ylab="true value", bty="l")
cor(yhat, daty) #0.7697753

out <- data.frame(cbind(yhat, daty))
colnames(out) <- c("predict_all", "true_all")
write.table(out, "~/Dropbox/obesity/San Antonio/predicted_poi.txt", row.names=FALSE, col.names=TRUE, quote=FALSE)

#Extract and write out most significant coefficients to a file
temp1 <- coef(fit.elnet.cv, s="lambda.min")
temp2 <- row.names(temp1)
temp.dat <- data.frame(temp2, as.numeric(temp1[,1])); colnames(temp.dat) <- c("variables", "coefficients")
fin.coef <- temp.dat[order(temp.dat$coefficients, decreasing=TRUE),]
fin.coef <- subset(fin.coef, coefficients != 0)
write.table(fin.coef, "~/Dropbox/obesity/San Antonio/significant_coeffs_poi.txt", row.names=FALSE)

##########################################################################################
##########################################################################################
#Analysis with combined point of interest and features data
#Read the data
datx1 <- read.table("~/Dropbox/obesity/San Antonio/X_san-antonio_poi.txt", stringsAsFactors = FALSE)
datx2 <- read.table("~/Dropbox/obesity/San Antonio/X_san-antonio_fc7_vggf_z18.txt", stringsAsFactors = FALSE) #4096
 datx <- cbind(datx1, datx2); dim(datx)
 daty <- read.table("~/Dropbox/obesity/San Antonio/y_san-antonio_fc7_vggf_z18.txt", stringsAsFactors = FALSE)#4197

datx <- as.matrix(datx)
daty <- as.matrix(daty)

#10-fold cross validation for each alpha (try different alpha values)
fit.elnet.cv <- cv.glmnet(datx, daty, type.measure="mse", family="gaussian", nfolds=5, alpha=0.5, standardize.response=TRUE) #standardize.response


yhat <- predict(fit.elnet.cv, s=fit.elnet.cv$lambda.min, newx=datx)
plot(yhat, daty, xlab="predicted", ylab="true value", bty="l")
cor(yhat, daty) #0.9186826

out <- data.frame(cbind(yhat, daty))
colnames(out) <- c("predict_all", "true_all")
write.table(out, "~/Dropbox/obesity/San Antonio/predicted_combined.txt", row.names=FALSE, col.names=TRUE, quote=FALSE)

#Extract and write out most significant coefficients to a file
temp1 <- coef(fit.elnet.cv, s="lambda.min")
temp2 <- row.names(temp1)
temp.dat <- data.frame(temp2, as.numeric(temp1[,1])); colnames(temp.dat) <- c("variables", "coefficients")
fin.coef <- temp.dat[order(temp.dat$coefficients, decreasing=TRUE),]
fin.coef <- subset(fin.coef, coefficients != 0)
write.table(fin.coef, "~/Dropbox/obesity/San Antonio/significant_coeffs_combined.txt", row.names=FALSE)

##########################################################################################
##########################################################################
##Perform principal components analysis

#Read the data
dat <- read.table("~/Dropbox/obesity/San Antonio/X_san-antonio_fc7_vggf_z18.txt", stringsAsFactors = FALSE) #4096
daty <- read.table("~/Dropbox/obesity/San Antonio/y_san-antonio_fc7_vggf_z18.txt", stringsAsFactors = FALSE)

out <- prcomp(t(dat))

#get variance explained
summary(out) #90% variance explained at component 2

#get principal components for regression
datx <- as.matrix(cbind(out$rotation)[,1:9])
daty <- as.matrix(daty) #n=311
dim(datx)

#10-fold cross validation for each alpha (try different alpha values)
fit.elnet.cv <- cv.glmnet(datx, daty, type.measure="mse", family="gaussian", nfolds=5, alpha=0.5, standardize.response=TRUE) #standardize.response


yhat <- predict(fit.elnet.cv, s=fit.elnet.cv$lambda.min, newx=datx)
plot(yhat, daty, xlab="predicted", ylab="true value", bty="l")
cor(yhat, daty) #0.8402634



##########################################################################################
##########################################################################
##Split data and make predictions

#Read the data
datx <- read.table("~/Dropbox/obesity/Memphis/X_memphis_poi.txt", stringsAsFactors = FALSE)
daty <- read.table("~/Dropbox/obesity/Memphis/y_memphis_fc7_vggf_z18.txt", stringsAsFactors = FALSE)

datx <- as.matrix(datx)
daty <- as.matrix(daty)

loc <- sample(1:length(daty), 100)
daty.train <- daty[loc]
datx.train <- datx[loc,]


#10-fold cross validation for each alpha (try different alpha values)
fit.elnet.cv <- cv.glmnet(datx.train, daty.train, type.measure="mse", family="gaussian", alpha=0.5, nfolds=3, standardize.response=TRUE) #standardize.response

daty.test <- daty[-c(loc)]
datx.test <- datx[-c(loc),]


yhat <- predict(fit.elnet.cv, s=fit.elnet.cv$lambda.min, newx=datx.test)


plot(yhat, daty.test, xlab="predicted", ylab="true value", bty="l")
cor(yhat, daty.test) #0.6829677

out <- data.frame(cbind(yhat, daty.test))
colnames(out) <- c("predict_all", "true_all")
write.table(out, "~/Dropbox/obesity/Memphis/predicted_outsample.txt", row.names=FALSE, col.names=TRUE, quote=FALSE)

#Analysis with point of interest
#Read the data
datx <- read.table("~/Dropbox/obesity/Memphis/X_memphis_poi.txt", stringsAsFactors = FALSE)
daty <- read.table("~/Dropbox/obesity/Memphis/y_memphis_fc7_vggf_z18.txt", stringsAsFactors = FALSE)

datx <- as.matrix(datx)
daty <- as.matrix(daty)

loc <- sample(1:length(daty), 100)
daty.train <- daty[loc]
datx.train <- datx[loc,]


#10-fold cross validation for each alpha (try different alpha values)
fit.elnet.cv <- cv.glmnet(datx.train, daty.train, type.measure="mse", family="gaussian", alpha=0.5, nfolds=3,  standardize.response=TRUE) #standardize.response

daty.test <- daty[-c(loc)]
datx.test <- datx[-c(loc),]

yhat <- predict(fit.elnet.cv, s=fit.elnet.cv$lambda.min, newx=datx.test)

plot(yhat, daty.test, xlab="predicted", ylab="true value", bty="l")
cor(yhat, daty.test) #0.5630812

out <- data.frame(cbind(yhat, daty.test))
colnames(out) <- c("predict_all", "true_all")
write.table(out, "~/Dropbox/obesity/Memphis/predicted_poi_outsample.txt", row.names=FALSE, col.names=TRUE, quote=FALSE)



