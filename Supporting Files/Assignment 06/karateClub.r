\begin{verbatim}
karateClub <- function(communities=2) {
  
  # Pass a parameter to identify the desired number of communities.
  # Default to 2 which is the initial split between club members.
  setwd("C:/Users/Corren/Documents/My R Scripts/Assignment 06")

  library(igraph)
  library(igraphdata)
  
  # The igraphdata package contains the karate club data set along with
  # the edge weights which identify the common activities between
  # club members.
  
  # Load the dataset into the "R" workspace.
  data("karate",package="igraphdata")
  # Save the package data as an igraph object.
  graphk <- karate
  
  # Alternative dataset from UCI repository
  #graphk<- read.graph("karate.paj", format="pajek")
    
  # How many vertices are in the graph? Use this number to 
  # control the iterations of the algorithm.
  vertices <- length(V(karate))

  # Using a force-based layout with a large number of iterations (recommended)
  l <- layout.kamada.kawai(graphk, niter=1000)
  #l <- layout.fruchterman.reingold(graphk, niter=1000)
  # Examine the shortest path between all edges
  ebc <- edge.betweenness.community(graphk, weights=E(graphk)$weight)
  
  # Set up the color palette for the plot (vertices)
  colbar  <- rainbow(6, start=.3, end=.7)
  # Set up the color palette for the calculations (EBC).
  # Display the first ones in color, remaining are black.
  colbar2 <- c(rainbow(3, start = 0.0, end = 0.66), rep("black", 31))
  
  # Trim off excess margin space (bottom, left, top, right)
  #par(mar=c(0.5, 0.5, 0.5, 0.5), bg="white")

  # Either iterate over all the vertices or
  # stop when we have the desired number of communities.
  numClusters <- no.clusters(graphk)
  i <- 1
  while (i <= vertices && numClusters != communities) {
    # Girvan-Newman: iteratively delete edges
    g2 <- delete.edges(graphk, ebc$removed.edges[seq(length=i-1)])
    # Recalculate the flow between edges
    eb <- edge.betweenness(g2)
  
    # Node membership in the clusters
    cl <- clusters(g2)$membership
    # Number of Clusters
    numClusters<- no.clusters(g2)
    # Debug:
    print (numClusters)
    
    q <- modularity(g2, cl)
  
    E(g2)$color <- "grey"
    # Sort the edges by betweenness. Highlight the top 3
    E(g2)[order(eb, decreasing=TRUE)[1:3] ]$color <- colbar2[1:3]
  
    # default edge width
    E(g2)$width <- 1
    # Emphasize the candidate edges we might delete
    E(g2)[ color != "grey" ]$width <- 2
  
    # Save each iteration to a file for our report
    png(sprintf("karateClub-community-%04d.png", i))
    
    plot(g2, layout=l, vertex.size=15,  vertex.label.font=2,
      edge.label.color="red", vertex.color=colbar[cl+2],
      edge.label.font=2)
    
    # Add a heading
    title(main=paste("Modularity = ", round(q,3)), font.main=1)
    
    # Vector for the Y coordinate
    yCoords <- seq(1,by=-strheight("1")*1.5, length=3)
    # Display the top EBC calculation. Color of text matches the
    # corresponding edge in the graph

    #text(-1.5, yCoords, adj=c(0,0.5), round(sort(eb, dec=TRUE)[1:3],2), col=colbar2,
    #  font=2)
    # Legend for the edge weights
    legend("bottomright", 
           legend=c(round(sort(eb, dec=TRUE)[1:3],2)), 
           col=c(colbar2), lwd=2, lty=c(1,1,1),
           title="Betweeness",
           horiz=FALSE
           )
    
    dev.off()
		# Pause so we can review each plot as it changes
    if (interactive()) Sys.sleep(4)
    # increment the loop counter
    i<- i + 1
  } # end of loop
} # end function
\end{verbatim}