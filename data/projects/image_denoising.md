# Project : IMAGE DENOISING

## INtroduction
Date: July 16 2025 - July 25 2025 ( with a great beak at one point)

Data: The data used in this project is MNIST dataset. We could find it using the modul datasets of torchvision and then call the function MNIST. It contains 60,000 images of 28x28.

Description : In this second project , we will try to build a model able to remove the nose of an image and give the most clear image possible. Otherwise here it will be only number. So the data set will be MNIST and we will see Auto-Encoder.

## Model used
FCAutoEncoder() -- fully connected auto encoder
ConvAutoEncoder -- convolutional auto encoder
VAE -- variational auto encoder

## Conclusion
Regarding the different reconstruction made by the models, we can say that:

    The Full connected Auto encoder manage to re-build the original image with much precision. We could have a little problem with the letter 4 because it could seems like a 9 but it is still a satisfying 4. So we did a great full connected auto encoder with only 3 layers. This model only aims to reduce the MSE between the noisy image and the real one, it has only one task to do and could sometimes memorize the patterns that why it has so good result. Concerning the time, we can clearly see that this model was by far the fastest of all of them.

    The Convolutional Auto Encoder is also a good but not better than the first one. We can notice that the generated images are not totally clear and have in some places white parts (like the 7, 4 and 1). We use, for this model only 2 convolutions layers and 2 maxpooling layers, maybe with more convolution layers we could have a better model. This model take more time to run than the full connected one, it is 3 times longer. Which is logical because here we work in a 2 dimentional space instead of 1 dimentional for the full connected.

    The Variational Auto Encoder is by far the worst model and is not able to re-build correctly an image. This problem could have many reasons. Firstly, we could change our loss function to use binary cross-entropy instead of MSE because our image are binary; also the dimension of the latent space is maybe too short to cath the diversity of the image or too big;... Concerning the runing time, it last approximatly as long as the convolution auto encoder.

The goal of this project is not to correct every problem faced by the models but to have a first experience in the implementation of an AE. Let's find our to resolve some problem meet here in another project or maybe after.