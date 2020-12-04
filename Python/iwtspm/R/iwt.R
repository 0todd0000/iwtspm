# Interval-wise testing (IWT)


suppressMessages( library(fda) )



# The "IWT2" function is redistributed under a GPL license.
# It was downloaded on 2020-11-30 from Alessia Pini's "fdatest" repository:
# https://github.com/alessiapini/fdatest


IWT2 <- function(data1,data2,mu=0,B=1000,paired=FALSE,dx=NULL,recycle=TRUE,alternative="two.sided"){
  pval.correct <- function(pval.matrix){
    matrice_pval_2_2x <- cbind(pval.matrix,pval.matrix)
    p <- dim(pval.matrix)[2]
    matrice_pval_2_2x <- matrice_pval_2_2x[,(2*p):1]
    corrected.pval <- numeric(p)
    corrected.pval.matrix <- matrix(nrow=p,ncol=p)
    corrected.pval.matrix[p,] <- pval.matrix[p,p:1]
    for(var in 1:p){
      pval_var <- matrice_pval_2_2x[p,var]
      inizio <- var
      fine <- var #inizio fisso, fine aumenta salendo nelle righe
      for(riga in (p-1):1){
        fine <- fine + 1
        pval_cono <- matrice_pval_2_2x[riga,inizio:fine]
        pval_var <- max(pval_var,pval_cono,na.rm=TRUE)
        corrected.pval.matrix[riga,var] <- pval_var
      }
      corrected.pval[var] <- pval_var
    }
    corrected.pval <- corrected.pval[p:1]
    corrected.pval.matrix <- corrected.pval.matrix[,p:1]
    return(corrected.pval.matrix)
  }

  possible_alternatives <- c("two.sided", "less", "greater")
  if(!(alternative %in% possible_alternatives)){
    stop(paste0('Possible alternatives are ',paste0(possible_alternatives,collapse=', ')))
  }

  # data preprocessing
  if(is.fd(data1)){ # data1 is a functional data object
    rangeval1 <- data1$basis$rangeval
    rangeval2 <- data2$basis$rangeval
    if(is.null(dx)){
      dx <- (rangeval1[2]-rangeval1[1])*0.01
    }
    if(sum(rangeval1 == rangeval2)!=2){
      stop("rangeval of data1 and data2 must coincide.")
    }
    abscissa <- seq(rangeval1[1],rangeval1[2],by=dx)
    coeff1 <- t(eval.fd(fdobj=data1,evalarg=abscissa))
    coeff2 <- t(eval.fd(fdobj=data2,evalarg=abscissa))

  }else if(is.matrix(data1)){
    coeff1 <- data1
    coeff2 <- data2
  }else{
    stop("First argument must be either a functional data object or a matrix.")
  }

  if (is.fd(mu)){ # mu is a functional data
    rangeval.mu <- mu$basis$rangeval
    if(sum(rangeval.mu == rangeval1)!=2){
      stop("rangeval of mu must be the same as rangeval of data.")
    }
    if(is.null(dx)){
      dx <- (rangeval.mu[2]-rangeval.mu[1])*0.01
    }
    abscissa <- seq(rangeval.mu[1],rangeval.mu[2],by=dx)
    mu.eval <- t(eval.fd(fdobj=mu,evalarg=abscissa))
  }else if(is.vector(mu)){
    mu.eval <- mu
  }else{
    stop("Second argument must be either a functional data object or a numeric vector.")
  }

  n1 <- dim(coeff1)[1]
  n2 <- dim(coeff2)[1]
  p <- dim(coeff1)[2]
  n <- n1+n2
  etichetta_ord <- c(rep(1,n1),rep(2,n2))
  coeff1 <- coeff1 - matrix(data=mu,nrow=n1,ncol=p)

  #print('First step: basis expansion')
  #splines coefficients:
  eval <- coeff <- rbind(coeff1,coeff2)

  data.eval <- eval
  data.eval[1:n1,] <- data.eval[1:n1,] + matrix(data=mu,nrow=n1,ncol=p)

  # print('Point-wise tests')
  #univariate permutations
  meandiff <- colMeans(coeff[1:n1,,drop=FALSE],na.rm=TRUE) - colMeans(coeff[(n1+1):n,,drop=FALSE],na.rm=TRUE)
  sign.diff <- sign(meandiff)
  sign.diff[which(sign.diff==-1)] <- 0
  T0 <- switch(alternative,
               two.sided =  (meandiff)^2,
               greater   =  (meandiff*sign.diff)^2,
               less      =  (meandiff*(sign.diff-1))^2)

  T_coeff <- matrix(ncol=p,nrow=B)
  for (perm in 1:B){
    if(paired){
      if.perm <- rbinom(n1,1,0.5)
      coeff_perm <- coeff
      for(couple in 1:n1){
        if(if.perm[couple]==1){
          coeff_perm[c(couple,n1+couple),] <- coeff[c(n1+couple,couple),]
        }
      }
    }else{
      permutazioni <- sample(n)
      coeff_perm <- coeff[permutazioni,]
    }
    meandiff <- colMeans(coeff_perm[1:n1,,drop=FALSE],na.rm=TRUE) - colMeans(coeff_perm[(n1+1):n,,drop=FALSE],na.rm=TRUE)
    sign.diff <- sign(meandiff)
    sign.diff[which(sign.diff==-1)] <- 0
    T_coeff[perm,] <- switch(alternative,
                             two.sided =  (meandiff)^2,
                             greater   =  (meandiff*sign.diff)^2,
                             less      =  (meandiff*(sign.diff-1))^2)
  }
  pval <- numeric(p)
  for(i in 1:p){
    pval[i] <- sum(T_coeff[,i]>=T0[i])/B
  }

  #combination
  # print('Interval-wise tests')

  #asymmetric combination matrix:
  matrice_pval_asymm <- matrix(nrow=p,ncol=p)
  matrice_pval_asymm[p,] <- pval[1:p]
  T0_2x <- c(T0,T0)
  T_coeff_2x <- cbind(T_coeff,T_coeff)

  maxrow <- 1
  # con parametro scale
  #maxrow <- p-scale+1

  if(recycle==TRUE){
    for(i in (p-1):maxrow){ # rows
      for(j in 1:p){ # columns
        inf <- j
        sup <- (p-i)+j
        T0_temp <- sum(T0_2x[inf:sup])
        T_temp <- rowSums(T_coeff_2x[,inf:sup])
        pval_temp <- sum(T_temp>=T0_temp)/B
        matrice_pval_asymm[i,j] <- pval_temp
      }
      # print(paste('creating the p-value matrix: end of row ',as.character(p-i+1),' out of ',as.character(p),sep=''))
    }
  }else{ # without recycling
    for(i in (p-1):maxrow){ # rows
      for(j in 1:i){ # columns
        inf <- j
        sup <- (p-i)+j
        T0_temp <- sum(T0_2x[inf:sup])
        T_temp <- rowSums(T_coeff_2x[,inf:sup])
        pval_temp <- sum(T_temp>=T0_temp)/B
        matrice_pval_asymm[i,j] <- pval_temp
      }
      # print(paste('creating the p-value matrix: end of row ',as.character(p-i+1),' out of ',as.character(p),sep=''))
    }
  }

  corrected.pval.matrix <- pval.correct(matrice_pval_asymm)
  corrected.pval <- corrected.pval.matrix[1,]

  # print('Interval-Wise Testing completed')
  IWT.result <- list(
    test = '2pop', mu = mu.eval,
    adjusted_pval = corrected.pval,
    unadjusted_pval = pval,
    pval_matrix = matrice_pval_asymm,
    data.eval=data.eval,
    ord_labels = etichetta_ord)
  class(IWT.result) = 'IWT2'
  return(IWT.result)
}







