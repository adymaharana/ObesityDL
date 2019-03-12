rm(list = ls())

#Read data and model it
library(MASS)
library(glmnet)

#set random seed
set.seed(100)


#Read the data
datx1 <- read.table("~/Dropbox/obesity/San Antonio/X_san-antonio_fc7_vggf_z18.txt", stringsAsFactors = FALSE) #4096
datx2 <- read.table("~/Dropbox/obesity/Memphis/X_memphis_fc7_vggf_z18.txt", stringsAsFactors = FALSE) #4096
datx3 <- read.table("~/Dropbox/obesity/Seattle-Tacoma-Bellevue/X_stb_fc7_vggf_z18.txt", stringsAsFactors = FALSE) 

datx <- rbind(datx1, datx2, datx3)

daty1 <- read.table("~/Dropbox/obesity/San Antonio/y_san-antonio_fc7_vggf_z18.txt", stringsAsFactors = FALSE)
daty2 <- read.table("~/Dropbox/obesity/Memphis/y_memphis_fc7_vggf_z18.txt", stringsAsFactors = FALSE)
daty3 <- read.table("~/Dropbox/obesity/Seattle-Tacoma-Bellevue/y_stb_fc7_vggf_z18.txt", stringsAsFactors = FALSE)

daty <- rbind(daty1, daty2, daty3)


datx <- as.matrix(datx) #4096 features
daty <- as.matrix(daty) #n=702
length(daty)

#10-fold cross validation for each alpha (try different alpha values)
fit.elnet.cv <- cv.glmnet(datx, daty, type.measure="mse", family="gaussian", nfolds=10, alpha=0.5, dfmax=70, standardize.response=TRUE) #standardize.response


yhat <- predict(fit.elnet.cv, s=fit.elnet.cv$lambda.min, newx=datx)
plot(yhat, daty, xlab="predicted", ylab="true value", bty="l")
cor(yhat, daty) #0.9072027

out <- data.frame(cbind(yhat, daty))
colnames(out) <- c("predict_all", "true_all")
write.table(out, "~/Dropbox/obesity/All Cities/predicted_features_allcities.txt", row.names=FALSE, col.names=TRUE, quote=FALSE)


#Extract and write out most significant coefficients to a file
temp1 <- coef(fit.elnet.cv, s="lambda.min")
temp2 <- row.names(temp1)
temp.dat <- data.frame(temp2, as.numeric(temp1[,1])); colnames(temp.dat) <- c("variables", "coefficients")
fin.coef <- temp.dat[order(temp.dat$coefficients, decreasing=TRUE),]
fin.coef <- subset(fin.coef, coefficients != 0) #63 variables selected
write.table(fin.coef, "~/Dropbox/obesity/All Cities/significant_coeffs_features_allcities.txt", row.names=FALSE)


##use ggplot2 to visualize
library(ggplot2)
out$location <- c(rep("SAN", length(daty1[,1])), rep("MEM", times=length(daty2[,1])), rep("SEA", times=length(daty3[,1])))

cbPalette <- c("bisque4", "darkolivegreen4", "aquamarine4", "seagreen4", "bisque2", "grey66", "black", "olivedrab1", "grey42", "slategrey", "bisque", "blue")


png("~/Dropbox/obesity/All Cities/crossvalided_est_allcities.png", width=11, height=8, units='in', res=400) 
ggplot(out, aes(x=true_all, y=predict_all, col=location)) + geom_point(size=4) + xlab("obesity prevalence") + ylab("model estimated obesity prevalence") + scale_colour_manual(values=cbPalette[c(3,7,12)], name="locations", breaks=c("SAN", "MEM", "SEA"), labels=c("San Antonio", "Memphis", "Seattle")) + theme_bw() + theme(panel.border = element_blank(),  panel.grid.minor = element_blank(), panel.grid.major= element_line(colour="grey70", size=0.2), text=element_text(size=20)) 
dev.off()

##########################################################################################
#Model predicted obesity prevalence

#Read the data
#length(daty.v)


locs <- sample(1:length(daty[,1]), 60*length(daty[,1])/100) 
datx.t <- datx[locs,]
datx.v <- datx[-c(locs),]

daty.t <- daty[locs,]
daty.v <- daty[-c(locs),]

#10-fold cross validation for each alpha (try different alpha values)
fit.elnet.cv <- glmnet(datx.t, daty.t, family="gaussian", alpha=0.5, standardize.response=TRUE) #standardize.response

fit.elnet.cv <- cv.glmnet(datx.t, daty.t, type.measure="mse", family="gaussian", nfolds=10, alpha=0.5, dfmax=70, standardize.response=TRUE) #standardize.response

#yhat <- predict(fit.elnet.cv, s=min(fit.elnet.cv$lambda), newx=datx.v)

yhat <- predict(fit.elnet.cv, s=fit.elnet.cv$lambda.min, newx=datx.v)

plot(yhat, daty.v, xlab="predicted", ylab="true value", bty="l")
cor(yhat, daty.v) 


out <- data.frame(cbind(yhat, daty.v))
colnames(out) <- c("predict_all", "true_all")


##use ggplot2 to visualize
library(ggplot2)
#out$location <- c(rep("SAN", length(daty1.v[,1])), rep("MEM", times=length(daty2.v[,1])), rep("SEA", times=length(daty3.v[,1])))

cbPalette <- c("bisque4", "darkolivegreen4", "aquamarine4", "seagreen4", "bisque2", "grey66", "black", "olivedrab1", "grey42", "slategrey", "bisque", "blue")


png("~/Dropbox/obesity/All Cities/outsample_predict_allcities.png", width=11, height=8, units='in', res=400) 
ggplot(out, aes(x=true_all, y=predict_all)) + geom_point(size=4) + xlab("obesity prevalence") + ylab("model predicted obesity prevalence") +  scale_colour_manual(values=cbPalette[c(2)]) + theme_bw() + theme(panel.border = element_blank(),  panel.grid.minor = element_blank(), panel.grid.major= element_line(colour="grey70", size=0.2), text=element_text(size=20), legend.position="none") 
dev.off()



##########################################################################################
##########################################################################################
#Analysis with point of interest
#Read the data

#Read the data
datx1 <- read.table("~/Dropbox/obesity/San Antonio/X_san-antonio_poi.txt", stringsAsFactors = FALSE) 
datx2 <- read.table("~/Dropbox/obesity/Memphis/X_memphis_poi.txt", stringsAsFactors = FALSE)
datx3 <- read.table("~/Dropbox/obesity/Seattle-Tacoma-Bellevue/X_stb_poi.txt", stringsAsFactors = FALSE) 

datx <- rbind(datx1, datx2, datx3)

daty1 <- read.table("~/Dropbox/obesity/San Antonio/y_san-antonio_fc7_vggf_z18.txt", stringsAsFactors = FALSE)
daty2 <- read.table("~/Dropbox/obesity/Memphis/y_memphis_fc7_vggf_z18.txt", stringsAsFactors = FALSE)
daty3 <- read.table("~/Dropbox/obesity/Seattle-Tacoma-Bellevue/y_stb_fc7_vggf_z18.txt", stringsAsFactors = FALSE)

daty <- rbind(daty1, daty2, daty3)


datx <- as.matrix(datx) #101 features
daty <- as.matrix(daty) #n=702
length(daty)



#10-fold cross validation for each alpha (try different alpha values)
fit.elnet.cv <- cv.glmnet(datx, daty, type.measure="mse", family="gaussian", nfolds=10, alpha=0.5, standardize.response=TRUE) #standardize.response


yhat <- predict(fit.elnet.cv, s=fit.elnet.cv$lambda.min, newx=datx)
plot(yhat, daty, xlab="predicted", ylab="true value", bty="l")
cor(yhat, daty) #0.7260205; r2=0.5271058


out <- data.frame(cbind(yhat, daty))
colnames(out) <- c("predict_all", "true_all")
write.table(out, "~/Dropbox/obesity/All Cities/predicted_poi.txt", row.names=FALSE, col.names=TRUE, quote=FALSE)

#Extract and write out most significant coefficients to a file
temp1 <- coef(fit.elnet.cv, s="lambda.min")
temp2 <- row.names(temp1)
temp.dat <- data.frame(temp2, as.numeric(temp1[,1])); colnames(temp.dat) <- c("variables", "coefficients")
fin.coef <- temp.dat[order(temp.dat$coefficients, decreasing=TRUE),]
fin.coef <- subset(fin.coef, coefficients != 0)
write.table(fin.coef, "~/Dropbox/obesity/All Cities/significant_coeffs_poi.txt", row.names=FALSE)



##use ggplot2 to visualize
library(ggplot2)
out$location <- c(rep("SAN", length(daty1[,1])), rep("MEM", times=length(daty2[,1])), rep("SEA", times=length(daty3[,1])))

cbPalette <- c("bisque4", "darkolivegreen4", "aquamarine4", "seagreen4", "bisque2", "grey66", "black", "olivedrab1", "grey42", "slategrey", "bisque", "blue")


png("~/Dropbox/obesity/All Cities/crossvalidated_poi_allcities.png", width=11, height=8, units='in', res=400) 
ggplot(out, aes(x=true_all, y=predict_all, col=location)) + geom_point(size=4) + xlab("obesity prevalence") + ylab("model estimated obesity prevalence") + scale_colour_manual(values=cbPalette[c(3,7,12)], name="locations", breaks=c("SAN", "MEM", "SEA"), labels=c("San Antonio", "Memphis", "Seattle")) + theme_bw() + theme(panel.border = element_blank(),  panel.grid.minor = element_blank(), panel.grid.major= element_line(colour="grey70", size=0.2), text=element_text(size=20)) 
dev.off()


##########################################################################################
#Model predicted obesity prevalence

#Read the data
#length(daty.v)


locs <- sample(1:length(daty[,1]), 60*length(daty[,1])/100) 
datx.t <- datx[locs,]
datx.v <- datx[-c(locs),]

daty.t <- daty[locs,]
daty.v <- daty[-c(locs),]

#10-fold cross validation for each alpha (try different alpha values)
#fit.elnet.cv <- glmnet(datx.t, daty.t, family="gaussian", alpha=0.5, standardize.response=TRUE) #standardize.response

fit.elnet.cv <- cv.glmnet(datx.t, daty.t, type.measure="mse", family="gaussian", nfolds=10, alpha=0.5, dfmax=70, standardize.response=TRUE) #standardize.response

#yhat <- predict(fit.elnet.cv, s=min(fit.elnet.cv$lambda), newx=datx.v)

yhat <- predict(fit.elnet.cv, s=fit.elnet.cv$lambda.min, newx=datx.v)

plot(yhat, daty.v, xlab="predicted", ylab="true value", bty="l")
cor(yhat, daty.v) #0.6850479

out <- data.frame(cbind(yhat, daty.v))
colnames(out) <- c("predict_all", "true_all")


##use ggplot2 to visualize
library(ggplot2)
#out$location <- c(rep("SAN", length(daty1.v[,1])), rep("MEM", times=length(daty2.v[,1])), rep("SEA", times=length(daty3.v[,1])))

cbPalette <- c("bisque4", "darkolivegreen4", "aquamarine4", "seagreen4", "bisque2", "grey66", "black", "olivedrab1", "grey42", "slategrey", "bisque", "blue")


png("~/Dropbox/obesity/All Cities/outsample_predict__poi_allcities.png", width=11, height=8, units='in', res=400) 
ggplot(out, aes(x=true_all, y=predict_all)) + geom_point(size=4) + xlab("obesity prevalence") + ylab("model predicted obesity prevalence") +  scale_colour_manual(values=cbPalette[c(2)]) + theme_bw() + theme(panel.border = element_blank(),  panel.grid.minor = element_blank(), panel.grid.major= element_line(colour="grey70", size=0.2), text=element_text(size=20), legend.position="none") 
dev.off()


