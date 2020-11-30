# Script for running two-tailed IWT analysis
# This script is meant to be run from the command line using:
#    Rscript run_iwt_two_tailed.R {seed} {n.iter} {file_data} {file_results} 
#
# where optional command line arguments are:
#
#    {seed}         = (integer, default=0) random number generator seed
#
#    {n.iter}       = (integer, default = 1000) number of iterations for the IWT function call 
#
#    {file_data}    = (file path, default = 'data.csv' in this script's directory)  full path to a CSV data file containing multiple functional responses (rows: responses, columns: domain nodes)
#   The first column must contain integer labels representing the two groups (e.g. "0"s and "1"s)
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
    fname.data    <- args[8]
}
if (length(args)>8){
    fname.results <- args[9]
}


# source the IWT2 function:
fname.module      <- file.path(dir.script, 'iwt.R')
source(fname.module)


# load CSV data file:
a     <- read.csv(fname.data, header=FALSE)
a     <- as.matrix( a )
group <- a[,1]
y     <- a[,2:ncol(a)]
u     <- unique(group)
y1    <- y[group==u[1] , ]   # first group
y2    <- y[group==u[2] , ]   # second group


# run IWT (two-tailed)
set.seed(seed)
x     <- IWT2(y1, y2, B=n.iter, alternative="two.sided")$adjusted_pval
write.table( matrix(x, nrow=1), file=fname.results, col.names=FALSE, row.names=FALSE , sep=",", quote=FALSE)
