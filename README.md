# Image Cryptography .txt less version

[dannyi96's repository](https://github.com/dannyi96/Image-Cryptography)の改変

## 環境設定

```
pip install pipenv
pipenv sync
```

## 起動方法

1. To encrypt an image, first place that image in the ```input/``` folder  
2. Then run  
``` python encrypt.py <image_name> ```  
The encrypted image can be found at the ```encrypted_images/``` folder.       
The keys generated during encryption is stored in the ```keys.txt``` file.  
(Note: The number of iterations of encryption to be performed can be adjusted by changing the ```ITER_MAX``` value in the ```encrypt.py``` file. Larger values will make encryption more secure but it is more time consuming)

3. To decrypt the image, run  
``` python decrypt.py <image_name> ```  
And Then enter the value of the Keys (Kr, Kc and ITER_MAX)  
The decrypted image can be found at the ```decrypted_images/``` folder.     

## Example

1. To encrypt the image ```pic3.png``` stored in the ```input``` folder

![](https://github.com/danny311296/Image-Cryptography/blob/master/input/pic3.png)

Run
``` python encrypt.py pic3.png ```  

The encrypted Picture can be found at ```encrypted_images/pic3.png```

![](https://github.com/danny311296/Image-Cryptography/blob/master/encrypted_images/pic3.png)

The keys are stored in ```keys.txt ```

2. To decrypt the image

Run
``` python decrypt.py pic3.png ``` 

and enter the key values (Kr, Kc and ITER_MAX)  

The decrypted Picture can be found at ```decrypted_images/pic3.png```

![](https://github.com/danny311296/Image-Cryptography/blob/master/decrypted_images/pic3.png)


