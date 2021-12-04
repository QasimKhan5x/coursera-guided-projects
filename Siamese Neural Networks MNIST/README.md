# Siamese Network with Triplet Loss in Keras

Implementation of a Siamese Network using MNIST dataset in Keras.

## Architecture
1. Provide anchor/input image, positive image (same label as anchor), negative image (label is different from anchor's)
2. Pass each example to the **same** linear layer separately
3. Concatenate the embeddings and return them

## Loss
- Calculate difference between embeddings of anchor and image using RMSE
- Minimize difference between anchor and positive image
- Maximize difference between anchor and negative image
- In other words, `pos_loss - neg_loss <= 0`
- Add noise to make the loss non-trivial
- `Asymptotically, max(loss, 0) should always be 0`
