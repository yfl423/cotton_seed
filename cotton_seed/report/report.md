## Report
### Data Acquisition
A script within 80 lines, only dependent on python standard library and open-cv was developed to generate image data. 
Specifically, it first parsed xml files to acquire coordinate data and image labels for following segmentation and classification. 
The segmented images were defined as training data and testing data by inputting a specified proportion parameter; each image was located under a subfolder named with its class.
Then these processed data was directly applied with deep learning model. 
### Model Design
Convolutional Neural Network is widely applied in pattern recognition and image classification, which is a good fit for this project.
Considering dataset size, I did not take overly complex model into account, only designed a classical, simple CNN model and mainly focused on some optimization tricks including data augmentation and parameter tuning. 
As for the model, Conv1 consists of 32 filters, both kernel size and stride of which are 1 by 1, Relu is applied as activation function. 
Conv2 is similar to Conv1, while kernel size is enlarged into 3 by 3, a max-pooling layer with 2 by 2 is connected after convolution layer for subsampling. 
Conv3 and Conv4 reduce filter size to 16, 8 with kernel size 3 by 3 and 5 by 5, respectively. Both two layer consider Relu as activation function, and Conv4 is connected with max-pooling layer.
A fully connected layer follows convolution layer with 128 unit output, eventually four class values will be output by another fully connected layer with softmax function. 
BN (Batch Normalization) layer and dropout function are applied in convolution layer and fully connected layer for avoiding overfitting.
### Experimental Process
Google Colab is an ideal environment which allows me hire free GPU; Jupyter Notebook offers better visualization. 
The experimental data after segmentation and labeling via python script was uploaded to my Google Drive.
Then model in colab will be able to access data by mounting the cloud drive thanks to Google community.
Data augmentation was a significant step before applying data into model.
After many times retries, the CNN model can benefit a lot from factors including rescale=1./255, featurewise_center=True, featurewise_std_normalization=True, shear_range=0.2, zoom_range=0.2, zca_whitening=True.
Whereas, rotation, flipping make model's performance worse, one speculation is that the definition of mechanic injury of cotton seed depends on the direction and angle of the crack, random rotation or flipping may confuse the model.
Some other hyperparameters such as batch size, dropout proportion also greatly affected the performance of model; In particular, batch size has a significant impact on convergence rate, it can usually be faster convergent with a relatively smaller batch size.
it is close to optimal regrading this model when batch size = 8 or 16. 
During the process of training model, I took categorical_crossentropy as loss function and Adam worked as optimizer. 
After experiencing 30 rounds' epochs, the model performed on testing data with loss = 0.8542 and accuracy = 0.7520.
### Further Consideration
From the plotting charts, overwriting still exists to some extent in spite of some normalization measurements, which should be a possible direction of further optimization.
More domain knowledge is required, which can applied in data preprocessing and image augmentation, because it is also hard to recognize and classify raw images even involved with eyes, this might be one reason why the performance is not that adorable. 
Eventually, constrained by current expertise's level and time, I did not use any customized APIs, if possible in future, a case-by-case implementation is expected to be conducted on some a topic.
### Declaration
As promised, I keep all experimental data private, and all codes, analysis were 100% conducted personally, beyond google search.