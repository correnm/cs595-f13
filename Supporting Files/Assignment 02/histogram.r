\begin{verbatim}
w1 <- read.csv(file="histogram.txt",sep=",",head=TRUE)
names(w1)
m<-mean(w1$mementos)
std<-sqrt(var(w1$mementos))
hist(w1$mementos,
col="lightgreen",
main="URIs vs Number of Mementos",
xlab="Number of Mementos",
ylab="URIs",
labels=TRUE)
curve(dnorm(x, mean=m, sd=std), add=TRUE)
\end{verbatim}