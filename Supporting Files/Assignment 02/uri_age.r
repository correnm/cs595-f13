\begin{verbatim}
# Scatter plot
w1 <- read.csv(file="uri_age.txt",sep=",",head=TRUE)
attach(w1)
age=w1$Age
mementos=w1$Mementos
plot(age, mementos, col="green",
main="Age vs. Number of Mementos",
xlab="Age in Days",
ylab="Mementos",
pch=19
)
# Add fit lines
abline(lm(mementos~age), col="blue") # regression line (y~x) 
\end{verbatim}