\begin{verbatim}
paradox<- function(graphType) {
  # Graphical analysis of the friendship paradox
  # input is either:
  # 1 - the friend_count associated with a Facebook account  
  # 2 - the followers count associated with a Twitter account
  # 3 - the following (friend) count associated with a Twitter

setwd("C:/Users/Corren/Documents/My R Scripts")
# Ignore the header line
switch(graphType,
      G1 = {data<-read.csv("paradox.txt", head=TRUE)
            what<-"friend(s)"},
      G2 = {data<-read.csv("followersFile.txt", head=TRUE)
            what<-"followers"},
      G3 = {data<-read.csv("friendsFile.txt", head=TRUE)
            what<-"following"},
      stop("valid graph types are: (1) Facebook (2) Followers (3) Following")
       
)

# coerce to numeric. column 2 is the FRIEND.COUNT
data[,2] <- as.numeric(data[,2])

# sort by the number of friends. 
sortedData<- data[order(data[,2]),]
# mean
meanData<-round(mean(data[,2], na.rm=TRUE), digits=0)
print(paste("Mean = ", meanData))

# standard deviation
sdData<-round(sd(data$COUNT, na.rm=TRUE), digits=0)
print(paste("Standard Deviation = ", sdData))

# how many records in the file (i.e., friends, followers, following)
myDataCount <- nrow(data)

# median
medianData<-median(data[,2], na.rm=TRUE)
print(paste("Median = ", medianData))

# Trim off excess margin space (bottom, left, top, right)
#par(mar=c(0.2, 0.2, 0.2, 0.2), bg="grey")
par(bg="ghostwhite")

labelMean<-paste("Mean = ", meanData )
labelMedian<-paste("Median = ", medianData )
labelSD<-paste("Standard Deviation = ", sdData )

# Put calculations in the footer of the graph
footer<- paste(paste(labelMean, labelMedian, sep=" ~ "), labelSD, sep= " ~ ")

plot(sortedData$COUNT, sortedData$ID, 
     main="Friendship Paradox",
     sub=footer,
     ylab=paste("My ",what),
     xlab=paste(paste("Their ",what), " Count\n"),
     pch=19, 
     col="blue"
     )

# add a vertical line for my count
#abline (v=myDataCount, col="purple", lwd="2")
textloc <- myDataCount
textlabel <- paste(paste(paste("  My ", what), " count is"), myDataCount, sep=" ")
# use the value of myFriendCOunt to determine where to print the text
text(textloc+20, textloc-5, textlabel, col = "purple", adj = c(0, -.1), font=4)
points(textloc+20, textloc-5, pch=18, cex=2,col="purple")
        
# add a vertical line for my count
#abline (v=medianData, col="red", lwd="2")
textloc <- medianData
textlabel <- paste(paste(paste("  The median ", what)," count is"), medianData, sep=" ")
# use the value of median to determine where to print the text
text(textloc + 70, myDataCount -50, textlabel, col = "red", adj = c(0, -.1), font=4)
points(textloc+70, myDataCount -50, pch=18, cex=2,col="red")

legend("topright", 
legend=c('My Count', 'Median Count', 'Their Count'), 
col=c('purple', 'red', 'blue'), lwd=1, lty=c(1,1,1))

}
\end{verbatim}