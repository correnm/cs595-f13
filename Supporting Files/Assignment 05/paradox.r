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
            what<-"Friends"},
      G2 = {data<-read.csv("followersFile.txt", head=TRUE)
            what<-"Followers"},
      G3 = {data<-read.csv("friendsFile.txt", head=TRUE)
            what<-"Following"},
      stop("valid graph types are: (1) Facebook (2) Followers (3) Following")
       
)

# coerce to numeric. column 2 is the FRIEND.COUNT
data[,2] <- as.numeric(data[,2])

# sort by the number of friends, followers, following
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
medianData<-round(median(data[,2], na.rm=TRUE), digits=0)
print(paste("Median = ", medianData))

# Trim off excess margin space (bottom, left, top, right)
#par(mar=c(0.2, 0.2, 0.2, 0.2), bg="grey")
par(bg="ghostwhite")

labelMean<-paste("Mean = ", meanData )
labelMedian<-paste("Median = ", medianData )
labelSD<-paste("Standard Deviation = ", sdData )

# Put calculations in the footer of the graph
footer<- paste(paste(labelMean, labelMedian, sep=" ~ "), labelSD, sep= " ~ ")

barplot(sortedData$COUNT, width=3,space=1.5,
      main="Friendship Paradox",
      sub=footer,
      ylab="",
      xlab=paste(what,"\n"),
      col="blue"
     )

#abline (v=myDataCount, col="purple", lwd="2")
textloc <- myDataCount
textlabel <- paste(paste(paste(". . .Dr. Nelson's ", what), " ="), myDataCount, sep=" ")
# use the value of the "count" to determine where to print the text
text(textloc, textloc+(max(sortedData$COUNT) / 3), textlabel, col = "purple", srt=90, font=4)
points(textloc, textloc, pch=18, cex=2,col="purple")
   

# add a vertical line for my count
#abline (v=medianData, col="red", lwd="2")
textloc <- medianData
textlabel <- paste(paste(paste(". . .The median ", what)," ="), medianData, sep=" ")
# use the value of median to determine where to print the text
text(textloc, textloc + (max(sortedData$COUNT) / 3), textlabel, col = "red", srt=90, font=4)
points(textloc, textloc, pch=18, cex=2,col="red")

legend("topleft", 
legend=c('Dr. Nelson', 'Median', what), 
col=c('purple', 'red', 'blue'), lwd=2, lty=c(1,1,1))

}
\end{verbatim}