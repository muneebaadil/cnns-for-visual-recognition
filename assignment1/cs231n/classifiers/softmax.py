import numpy as np
from random import shuffle
import math

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  num_train = X.shape[0]
  num_classes = W.shape[1]

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  
  for i in xrange(num_train): 
    toadd = np.zeros(W.shape) 
    numerator = math.exp(W[:, y[i]].dot(X[i, :]))
    denominator = 0.0 
    for j in xrange(num_classes): 
        denominator += math.exp(W[:, j].dot(X[i, :]))
    for j in xrange(num_classes): 
        toadd[:, j] = (-1 * math.exp(W[:, j].dot(X[i, :])) / denominator) * X[i, :]
    toadd[:, y[i]] = toadd[:, y[i]] + X[i, :] 
    toadd = -1 * toadd 
    dW = dW + toadd 
    loss -= math.log(numerator / denominator)

  loss /= num_train
  loss += 0.5 * reg * np.sum(W * W)
    
  dW = dW / num_train
  dW = dW + 2 * W
    
  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  num_classes = W.shape[1]
  num_train = X.shape[0]

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  scoresMatrix = np.exp(X.dot(W))
  alpha = np.log(np.sum(scoresMatrix, axis = 1))
  beta = np.log(scoresMatrix[np.arange(0, num_train), y])
  loss = (np.sum(alpha - beta)) / num_train
  loss += 0.5 * reg * np.sum(W * W)
    
  temp = np.diag(1 / np.sum(scoresMatrix, axis = 1))
  temp = temp.dot(scoresMatrix) 
  dW = X.transpose().dot(temp) 
  
  binarylabels = np.zeros((num_train, num_classes))
  binarylabels[np.arange(0, num_train), y] = 1
  #temp2 = X.transpose().dot(binarylabels)
  dW = dW - X.transpose().dot(binarylabels)
  
  dW = dW / num_train
  dW = dW + 2 * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

