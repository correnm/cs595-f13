\begin{verbatim}
library("igraph")
xlist<-read.table("graph.txt")
xlist<-graph.data.frame(xlist)
plot(xlist)
box()
# Trim off excess margin space (bottom, left, top, right)
par(mar=c(0.2, 0.2, 0.2, 0.2))
\end{verbatim}