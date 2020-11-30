# Script for running two-tailed IWT
#
# This script should be run from the command line using:
#    Rscript run_iwt_two_tailed.R {seed} {n.iter} {file_data} {file_results} 
#
# Optional command line arguments are:
#
#    {seed}         = (integer, default=0) random number generator seed
#
#    {n.iter}       = (integer, default = 1000) number of iterations for the IWT function call 
#
#    {n.groupA}     = (integer, default = floor( n/2 )) number of observations (data file rows) for Group A
#                     the first n.groupA rows of {file_data} will be assigned to Group A
#                     default: floor( n/2 )   where n is the total number of rows
#
#    {file_data}    = (file path, default = 'data.csv' in this script's directory)  full path to a CSV data file containing multiple functional responses (rows: responses, columns: domain nodes)
#
#    {file_results} = (file path, default = 'iwt.csv' in this script's directory)  full path to the CSV data file into which results will be written (single row of adjusted p values);  previous results will be overwritten
#
# Example:
#
#    Rscript run_iwt_two_tailed.R 1 1000 5 data.csv iwt.csv
#
# Note:
#
#    An example data file "data.csv" and expected results "iwt.csv" are included in this script's directory
#    for testing purposes


rm( list = ls() )


# get the path of this script
args              <- commandArgs( trailingOnly=FALSE )
path.script       <- unlist( strsplit(args[4], "=") )[2]
dir.script        <- dirname( path.script )


# set defaults:
seed              <- 0
n.iter            <- 1000
n.groupA          <- -1
fname.data        <- file.path(dir.script, 'data.csv')
fname.results     <- file.path(dir.script, 'iwt.csv')
# override defaults with command line arguments:
if (length(args)>4){
    seed          <- strtoi( args[6] )
}
if (length(args)>6){
    n.iter        <- strtoi( args[7] )
}
if (length(args)>7){
    n.groupA      <- strtoi( args[8] )
}
if (length(args)>8){
    fname.data    <- args[9]
}
if (length(args)>9){
    fname.results <- args[10]
}


# source the IWT functions:
fname.module      <- file.path(dir.script, 'iwt.R')
source(fname.module)


# load CSV data file:
y   <- read.csv(fname.data, header=FALSE)
y   <- as.matrix( y )
n   <- dim(y)[1]
if (n.groupA == -1){
    n.groupA <- floor( n/2 )
}
y0  <- y[1:(n.groupA),]    # first group
y1  <- y[(n.groupA+1):n,]  # second group


# run IWT (two-tailed):
set.seed(seed)
x   <- IWT2(y1, y0, B=n.iter, alternative="two.sided")$adjusted_pval
write.table( matrix(x, nrow=1), file=fname.results, col.names=FALSE, row.names=FALSE , sep=",", quote=FALSE)
