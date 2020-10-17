# FaceRecognitionATK
- For original author's code, see [this](https://github.com/krasserm/face-recognition).

## Setup
### Environment
* Python 3.8
* MacOS or Linux

### Steps
* Recommend setting up a virtual environment. (Old version of Keras & Tensorflow to install.)
```bash
pip install virtualenv

virtualenv FaceRecognition

source ./FaceRecognition/bin/activate
```
* Install packages in **requirements.txt**.
```bash
pip install -r requirements.txt
```

## Usage
### Parameters
* **data**: Data path, e.g. './data/humanface'
* **n**: Image index to attack.
* **-i, --inten**: Added signals intensity. R(red) channel. Automatically cropped to 0-255.
* **-r, --ratio**: Decay ratio. B(blue) & G(green) channels. (0.0~1.0)
* **-a**: Starting polluting pixel in x axis (top-left).
* **-b**: Ending polluting pixel in x axis (bottom-left).
* **-c**: Starting polluting pixel in y axis (top-right).
* **-d**: Ending polluting pixel in y axis (bottom-right).

### Example
```bash
python util.py './data/humanface' 9 -i 60 -r 0.4 -a 75 -b 175 -c 75 -d 175
```
For this example, you are running an attack with:
* Attacking the tenth image. (n=9)
* Place a 100\*100 Pattern position in the middle. (\[-a,-b,-c,-d]=\[75,175,75,175] in a 250\*250 image)
* R adds 60. (-i=60)
* GB decay to 40%. (-r=0.4)

![](Figure_1.png)

### Comments
- Images in **humanface** are all 250\*250. You can apply to new images (.jpg/ .jpeg) at any time. But pay attention to pattern position in different image sizes.
- If the program returns None and raises an error, this means alignment fails (attack succeeds).
- For very big images (e.g. 1500\*1000), better crop to proper size first.

## Reference
* Afifi M, Brown M S. [What else can fool deep learning? Addressing color constancy errors on deep neural network performance](https://openaccess.thecvf.com/content_ICCV_2019/papers/Afifi_What_Else_Can_Fool_Deep_Learning_Addressing_Color_Constancy_Errors_ICCV_2019_paper.pdf). ICCV. 2019: 243-252.
* Afifi M, Brown M S. [Deep White-Balance Editing](https://openaccess.thecvf.com/content_CVPR_2020/papers/Afifi_Deep_White-Balance_Editing_CVPR_2020_paper.pdf). CVPR. 2020: 1397-1406.
* Zhou Z, Tang D, Wang X, et al. [Invisible mask: Practical attacks on face recognition with infrared](https://arxiv.org/pdf/1803.04683.pdf). arXiv preprint arXiv:1803.04683, 2018.
* Nguyen D L, Arora S S, Wu Y, et al. [Adversarial Light Projection Attacks on Face Recognition Systems: A Feasibility Study](https://openaccess.thecvf.com/content_CVPRW_2020/papers/w48/Nguyen_Adversarial_Light_Projection_Attacks_on_Face_Recognition_Systems_A_Feasibility_CVPRW_2020_paper.pdf). CVPR. 2020: 814-815.

## Schedule
- [x] Theoretical attack for face alignments.
  - [x] Exposure.
  - [x] White-Balance.
  - [x] Cheating with T-shirts.
- [ ] Theoretical model for lens tolerance and adjustment.
- [ ] Real parameters measurement and attacks.
- [ ] Theoretical attack for face recognition (identity misclassification).
- [ ] Real face recognition attacks.
