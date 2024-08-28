# -*- coding: utf8 -*-
# Copyright (c) 2017-2021 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings

from tencentcloud.common.abstract_model import AbstractModel


class ChangeClothesRequest(AbstractModel):
    """ChangeClothes请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ModelUrl: 模特图片 Url。
图片限制：单边分辨率小于3000，且大于512，转成 Base64 字符串后小于 8MB。
输入要求：
1、建议上传正面模特图片，至少完整露出应穿着输入指定服装的身体部位（全身、上半身或下半身），无大角度身体偏转或异常姿势。
2、建议上传3:4比例的图片，生成效果更佳。
3、建议模特图片中的原始服装和更换后的服装类别一致，或原始服装在身体上的覆盖范围小于等于更换后的服装（例如需要给模特换上短裤，则原始模特图片中也建议穿短裤，不建议穿长裤），否则会影响人像生成效果。

        :type ModelUrl: str
        :param _ClothesUrl: 服装图片 Url。
图片限制：单边分辨率小于3000，大于512，转成 Base64 字符串后小于 8MB。
输入要求：
建议上传服装完整的正面平铺图片，仅包含1个服装主体，服装类型支持上衣、下装、连衣裙，三选一。算法将根据输入的图片，结合服装图片给模特换装。
        :type ClothesUrl: str
        :param _ClothesType: 服装类型，需要和服装图片保持一致。
取值：
Upper-body：上衣
Lower-body：下装
Dress：连衣裙
        :type ClothesType: str
        :param _LogoAdd: 为生成结果图添加标识的开关，默认为1。
1：添加标识。
0：不添加标识。
其他数值：默认按1处理。
建议您使用显著标识来提示结果图使用了 AI 绘画技术，是 AI 生成的图片。
        :type LogoAdd: int
        :param _LogoParam: 标识内容设置。
默认在生成结果图右下角添加“图片由 AI 生成”字样，您可根据自身需要替换为其他的标识图片。
        :type LogoParam: :class:`tencentcloud.aiart.v20221229.models.LogoParam`
        :param _RspImgType: 返回图像方式（base64 或 url) ，二选一，默认为 base64。url 有效期为1小时。
生成图分辨率较大时建议选择 url，使用 base64 可能因图片过大导致返回失败。
        :type RspImgType: str
        """
        self._ModelUrl = None
        self._ClothesUrl = None
        self._ClothesType = None
        self._LogoAdd = None
        self._LogoParam = None
        self._RspImgType = None

    @property
    def ModelUrl(self):
        return self._ModelUrl

    @ModelUrl.setter
    def ModelUrl(self, ModelUrl):
        self._ModelUrl = ModelUrl

    @property
    def ClothesUrl(self):
        return self._ClothesUrl

    @ClothesUrl.setter
    def ClothesUrl(self, ClothesUrl):
        self._ClothesUrl = ClothesUrl

    @property
    def ClothesType(self):
        return self._ClothesType

    @ClothesType.setter
    def ClothesType(self, ClothesType):
        self._ClothesType = ClothesType

    @property
    def LogoAdd(self):
        return self._LogoAdd

    @LogoAdd.setter
    def LogoAdd(self, LogoAdd):
        self._LogoAdd = LogoAdd

    @property
    def LogoParam(self):
        return self._LogoParam

    @LogoParam.setter
    def LogoParam(self, LogoParam):
        self._LogoParam = LogoParam

    @property
    def RspImgType(self):
        return self._RspImgType

    @RspImgType.setter
    def RspImgType(self, RspImgType):
        self._RspImgType = RspImgType


    def _deserialize(self, params):
        self._ModelUrl = params.get("ModelUrl")
        self._ClothesUrl = params.get("ClothesUrl")
        self._ClothesType = params.get("ClothesType")
        self._LogoAdd = params.get("LogoAdd")
        if params.get("LogoParam") is not None:
            self._LogoParam = LogoParam()
            self._LogoParam._deserialize(params.get("LogoParam"))
        self._RspImgType = params.get("RspImgType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ChangeClothesResponse(AbstractModel):
    """ChangeClothes返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ResultImage: 根据入参 RspImgType 填入不同，返回不同的内容。
如果传入 base64 则返回生成图 Base64 编码。
如果传入 url 则返回的生成图 URL , 有效期1小时，请及时保存。
        :type ResultImage: str
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ResultImage = None
        self._RequestId = None

    @property
    def ResultImage(self):
        return self._ResultImage

    @ResultImage.setter
    def ResultImage(self, ResultImage):
        self._ResultImage = ResultImage

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._ResultImage = params.get("ResultImage")
        self._RequestId = params.get("RequestId")


class Filter(AbstractModel):
    """训练图像质量过滤开关配置。
    支持开启或关闭对训练图像分辨率下限、脸部区域大小、脸部遮挡、脸部角度的过滤，默认开启以上过滤。
    如果训练图像内包含多人脸或无人脸、和 Base 人像不为同一人也将被过滤，不可关闭该过滤条件。
    建议：关闭以上过滤可能导致写真生成效果受损，建议使用单人、正脸、脸部清晰、无遮挡、无夸张表情、脸部区域占比较大的图像进行训练。

    """

    def __init__(self):
        r"""
        :param _Resolution: 过滤不满足分辨率下限的训练图像，默认开启过滤
开启后将过滤横边<512或竖边<720的图片，横、竖边上限均为2000，不支持调整

1：开启过滤
0：关闭过滤
        :type Resolution: int
        :param _Size: 过滤脸部区域过小的训练图像，默认开启过滤

1：开启过滤
0：关闭过滤
        :type Size: int
        :param _Occlusion: 过滤脸部存在明显遮挡、偏转角度过大等质量较差的训练图像，默认开启过滤

1：开启过滤
0：关闭过滤
        :type Occlusion: int
        """
        self._Resolution = None
        self._Size = None
        self._Occlusion = None

    @property
    def Resolution(self):
        return self._Resolution

    @Resolution.setter
    def Resolution(self, Resolution):
        self._Resolution = Resolution

    @property
    def Size(self):
        return self._Size

    @Size.setter
    def Size(self, Size):
        self._Size = Size

    @property
    def Occlusion(self):
        return self._Occlusion

    @Occlusion.setter
    def Occlusion(self, Occlusion):
        self._Occlusion = Occlusion


    def _deserialize(self, params):
        self._Resolution = params.get("Resolution")
        self._Size = params.get("Size")
        self._Occlusion = params.get("Occlusion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GenerateAvatarRequest(AbstractModel):
    """GenerateAvatar请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Style: 头像风格。
请在  [百变头像风格列表](https://cloud.tencent.com/document/product/1668/107741) 中选择期望的风格，必须传入风格编号。
        :type Style: str
        :param _InputImage: 输入图 Base64 数据。
Base64 和 Url 必须提供一个，如果都提供以 Url 为准。
图片限制：单边分辨率小于5000，转成 Base64 字符串后小于 6MB，格式支持 jpg、jpeg、png、bmp、tiff、webp。
        :type InputImage: str
        :param _InputUrl: 输入图 Url。
Base64 和 Url 必须提供一个，如果都提供以 Url 为准。
图片限制：单边分辨率小于5000，转成 Base64 字符串后小于 6MB，格式支持 jpg、jpeg、png、bmp、tiff、webp。
        :type InputUrl: str
        :param _Filter: 输入图像质量检测开关，默认开启。
1：开启
0：关闭
建议开启检测，可提升生成效果，关闭检测可能因输入图像质量较差导致生成效果受损。
开启后，将增强对输入图像的质量要求，如果输入图像单边分辨率<500、图像中人脸占比较小、存在多人、没有检测到人脸、人脸不完整、人脸遮挡等，将被拦截。
关闭后，将降低对输入图像的质量要求，如果图像中没有检测到人脸或人脸占比过小等，将被拦截。
        :type Filter: int
        :param _LogoAdd: 为生成结果图添加标识的开关，默认为1。
1：添加标识。
0：不添加标识。
其他数值：默认按1处理。
建议您使用显著标识来提示结果图是 AI 生成的图片。
        :type LogoAdd: int
        :param _LogoParam: 标识内容设置。
默认在生成结果图右下角添加“图片由 AI 生成”字样，您可根据自身需要替换为其他的标识图片。
        :type LogoParam: :class:`tencentcloud.aiart.v20221229.models.LogoParam`
        :param _RspImgType: 返回图像方式（base64 或 url) ，二选一，默认为 base64。url 有效期为1小时。
        :type RspImgType: str
        """
        self._Style = None
        self._InputImage = None
        self._InputUrl = None
        self._Filter = None
        self._LogoAdd = None
        self._LogoParam = None
        self._RspImgType = None

    @property
    def Style(self):
        return self._Style

    @Style.setter
    def Style(self, Style):
        self._Style = Style

    @property
    def InputImage(self):
        return self._InputImage

    @InputImage.setter
    def InputImage(self, InputImage):
        self._InputImage = InputImage

    @property
    def InputUrl(self):
        return self._InputUrl

    @InputUrl.setter
    def InputUrl(self, InputUrl):
        self._InputUrl = InputUrl

    @property
    def Filter(self):
        return self._Filter

    @Filter.setter
    def Filter(self, Filter):
        self._Filter = Filter

    @property
    def LogoAdd(self):
        return self._LogoAdd

    @LogoAdd.setter
    def LogoAdd(self, LogoAdd):
        self._LogoAdd = LogoAdd

    @property
    def LogoParam(self):
        return self._LogoParam

    @LogoParam.setter
    def LogoParam(self, LogoParam):
        self._LogoParam = LogoParam

    @property
    def RspImgType(self):
        return self._RspImgType

    @RspImgType.setter
    def RspImgType(self, RspImgType):
        self._RspImgType = RspImgType


    def _deserialize(self, params):
        self._Style = params.get("Style")
        self._InputImage = params.get("InputImage")
        self._InputUrl = params.get("InputUrl")
        self._Filter = params.get("Filter")
        self._LogoAdd = params.get("LogoAdd")
        if params.get("LogoParam") is not None:
            self._LogoParam = LogoParam()
            self._LogoParam._deserialize(params.get("LogoParam"))
        self._RspImgType = params.get("RspImgType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GenerateAvatarResponse(AbstractModel):
    """GenerateAvatar返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ResultImage: 根据入参 RspImgType 填入不同，返回不同的内容。
如果传入 base64 则返回生成图 Base64 编码。
如果传入 url 则返回的生成图 URL , 有效期1小时，请及时保存。
        :type ResultImage: str
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ResultImage = None
        self._RequestId = None

    @property
    def ResultImage(self):
        return self._ResultImage

    @ResultImage.setter
    def ResultImage(self, ResultImage):
        self._ResultImage = ResultImage

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._ResultImage = params.get("ResultImage")
        self._RequestId = params.get("RequestId")


class ImageToImageRequest(AbstractModel):
    """ImageToImage请求参数结构体

    """

    def __init__(self):
        r"""
        :param _InputImage: 输入图 Base64 数据。
算法将根据输入的图片，结合文本描述智能生成与之相关的图像。
Base64 和 Url 必须提供一个，如果都提供以 Url 为准。
图片限制：单边分辨率小于5000且大于50，转成 Base64 字符串后小于 8MB，格式支持 jpg、jpeg、png、bmp、tiff、webp。
        :type InputImage: str
        :param _InputUrl: 输入图 Url。
算法将根据输入的图片，结合文本描述智能生成与之相关的图像。
Base64 和 Url 必须提供一个，如果都提供以 Url 为准。
图片限制：单边分辨率小于5000且大于50，转成 Base64 字符串后小于 8MB，格式支持 jpg、jpeg、png、bmp、tiff、webp。
        :type InputUrl: str
        :param _Prompt: 文本描述。
用于在输入图的基础上引导生成图效果，增加生成结果中出现描述内容的可能。
推荐使用中文。最多支持256个 utf-8 字符。
        :type Prompt: str
        :param _NegativePrompt: 反向文本描述。
用于一定程度上从反面引导模型生成的走向，减少生成结果中出现描述内容的可能，但不能完全杜绝。
推荐使用中文。最多可传256个 utf-8 字符。
        :type NegativePrompt: str
        :param _Styles: 绘画风格。
请在  [图像风格化风格列表](https://cloud.tencent.com/document/product/1668/86250) 中选择期望的风格，传入风格编号。
推荐使用且只使用一种风格。不传默认使用201（日系动漫风格）。
        :type Styles: list of str
        :param _ResultConfig: 生成图结果的配置，包括输出图片分辨率和尺寸等。
支持生成以下分辨率的图片：origin（与输入图分辨率一致，长边最高为2000，超出将做等比例缩小）、768:768（1:1）、768:1024（3:4）、1024:768（4:3）。
不传默认使用origin。
        :type ResultConfig: :class:`tencentcloud.aiart.v20221229.models.ResultConfig`
        :param _LogoAdd: 为生成结果图添加标识的开关，默认为1。
1：添加标识。
0：不添加标识。
其他数值：默认按1处理。
建议您使用显著标识来提示结果图使用了 AI 绘画技术，是 AI 生成的图片。
        :type LogoAdd: int
        :param _LogoParam: 标识内容设置。
默认在生成结果图右下角添加“图片由 AI 生成”字样，您可根据自身需要替换为其他的标识图片。
        :type LogoParam: :class:`tencentcloud.aiart.v20221229.models.LogoParam`
        :param _Strength: 生成自由度。
Strength 值越小，生成图和原图越接近，取值范围(0, 1]，不传使用模型内置的默认值。
推荐的取值范围为0.6 - 0.8。
        :type Strength: float
        :param _RspImgType: 返回图像方式（base64 或 url) ，二选一，默认为 base64。url 有效期为1小时。
        :type RspImgType: str
        """
        self._InputImage = None
        self._InputUrl = None
        self._Prompt = None
        self._NegativePrompt = None
        self._Styles = None
        self._ResultConfig = None
        self._LogoAdd = None
        self._LogoParam = None
        self._Strength = None
        self._RspImgType = None

    @property
    def InputImage(self):
        return self._InputImage

    @InputImage.setter
    def InputImage(self, InputImage):
        self._InputImage = InputImage

    @property
    def InputUrl(self):
        return self._InputUrl

    @InputUrl.setter
    def InputUrl(self, InputUrl):
        self._InputUrl = InputUrl

    @property
    def Prompt(self):
        return self._Prompt

    @Prompt.setter
    def Prompt(self, Prompt):
        self._Prompt = Prompt

    @property
    def NegativePrompt(self):
        return self._NegativePrompt

    @NegativePrompt.setter
    def NegativePrompt(self, NegativePrompt):
        self._NegativePrompt = NegativePrompt

    @property
    def Styles(self):
        return self._Styles

    @Styles.setter
    def Styles(self, Styles):
        self._Styles = Styles

    @property
    def ResultConfig(self):
        return self._ResultConfig

    @ResultConfig.setter
    def ResultConfig(self, ResultConfig):
        self._ResultConfig = ResultConfig

    @property
    def LogoAdd(self):
        return self._LogoAdd

    @LogoAdd.setter
    def LogoAdd(self, LogoAdd):
        self._LogoAdd = LogoAdd

    @property
    def LogoParam(self):
        return self._LogoParam

    @LogoParam.setter
    def LogoParam(self, LogoParam):
        self._LogoParam = LogoParam

    @property
    def Strength(self):
        return self._Strength

    @Strength.setter
    def Strength(self, Strength):
        self._Strength = Strength

    @property
    def RspImgType(self):
        return self._RspImgType

    @RspImgType.setter
    def RspImgType(self, RspImgType):
        self._RspImgType = RspImgType


    def _deserialize(self, params):
        self._InputImage = params.get("InputImage")
        self._InputUrl = params.get("InputUrl")
        self._Prompt = params.get("Prompt")
        self._NegativePrompt = params.get("NegativePrompt")
        self._Styles = params.get("Styles")
        if params.get("ResultConfig") is not None:
            self._ResultConfig = ResultConfig()
            self._ResultConfig._deserialize(params.get("ResultConfig"))
        self._LogoAdd = params.get("LogoAdd")
        if params.get("LogoParam") is not None:
            self._LogoParam = LogoParam()
            self._LogoParam._deserialize(params.get("LogoParam"))
        self._Strength = params.get("Strength")
        self._RspImgType = params.get("RspImgType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ImageToImageResponse(AbstractModel):
    """ImageToImage返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ResultImage: 根据入参 RspImgType 填入不同，返回不同的内容。
如果传入 base64 则返回生成图 Base64 编码。
如果传入 url 则返回的生成图 URL , 有效期1小时，请及时保存。
        :type ResultImage: str
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ResultImage = None
        self._RequestId = None

    @property
    def ResultImage(self):
        return self._ResultImage

    @ResultImage.setter
    def ResultImage(self, ResultImage):
        self._ResultImage = ResultImage

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._ResultImage = params.get("ResultImage")
        self._RequestId = params.get("RequestId")


class LogoParam(AbstractModel):
    """logo参数

    """

    def __init__(self):
        r"""
        :param _LogoUrl: 水印 Url
        :type LogoUrl: str
        :param _LogoImage: 水印 Base64，Url 和 Base64 二选一传入，如果都提供以 Url 为准
        :type LogoImage: str
        :param _LogoRect: 水印图片位于生成结果图中的坐标，将按照坐标对标识图片进行位置和大小的拉伸匹配
        :type LogoRect: :class:`tencentcloud.aiart.v20221229.models.LogoRect`
        """
        self._LogoUrl = None
        self._LogoImage = None
        self._LogoRect = None

    @property
    def LogoUrl(self):
        return self._LogoUrl

    @LogoUrl.setter
    def LogoUrl(self, LogoUrl):
        self._LogoUrl = LogoUrl

    @property
    def LogoImage(self):
        return self._LogoImage

    @LogoImage.setter
    def LogoImage(self, LogoImage):
        self._LogoImage = LogoImage

    @property
    def LogoRect(self):
        return self._LogoRect

    @LogoRect.setter
    def LogoRect(self, LogoRect):
        self._LogoRect = LogoRect


    def _deserialize(self, params):
        self._LogoUrl = params.get("LogoUrl")
        self._LogoImage = params.get("LogoImage")
        if params.get("LogoRect") is not None:
            self._LogoRect = LogoRect()
            self._LogoRect._deserialize(params.get("LogoRect"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LogoRect(AbstractModel):
    """输入框

    """

    def __init__(self):
        r"""
        :param _X: 左上角X坐标
        :type X: int
        :param _Y: 左上角Y坐标
        :type Y: int
        :param _Width: 方框宽度
        :type Width: int
        :param _Height: 方框高度
        :type Height: int
        """
        self._X = None
        self._Y = None
        self._Width = None
        self._Height = None

    @property
    def X(self):
        return self._X

    @X.setter
    def X(self, X):
        self._X = X

    @property
    def Y(self):
        return self._Y

    @Y.setter
    def Y(self, Y):
        self._Y = Y

    @property
    def Width(self):
        return self._Width

    @Width.setter
    def Width(self, Width):
        self._Width = Width

    @property
    def Height(self):
        return self._Height

    @Height.setter
    def Height(self, Height):
        self._Height = Height


    def _deserialize(self, params):
        self._X = params.get("X")
        self._Y = params.get("Y")
        self._Width = params.get("Width")
        self._Height = params.get("Height")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryDrawPortraitJobRequest(AbstractModel):
    """QueryDrawPortraitJob请求参数结构体

    """

    def __init__(self):
        r"""
        :param _JobId: 查询生成写真图片任务 ID。
        :type JobId: str
        """
        self._JobId = None

    @property
    def JobId(self):
        return self._JobId

    @JobId.setter
    def JobId(self, JobId):
        self._JobId = JobId


    def _deserialize(self, params):
        self._JobId = params.get("JobId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryDrawPortraitJobResponse(AbstractModel):
    """QueryDrawPortraitJob返回参数结构体

    """

    def __init__(self):
        r"""
        :param _JobStatusCode: 任务状态码。
INIT: 初始化、WAIT：等待中、RUN：运行中、FAIL：处理失败、DONE：处理完成。
        :type JobStatusCode: str
        :param _JobStatusMsg: 任务状态信息。
        :type JobStatusMsg: str
        :param _JobErrorCode: 任务错误码。
        :type JobErrorCode: str
        :param _JobErrorMsg: 任务错误信息。
        :type JobErrorMsg: str
        :param _ResultUrls: 结果 URL 数组。
URL 有效期1小时，请及时保存。
        :type ResultUrls: list of str
        :param _ResultDetails: 结果描述数组。
        :type ResultDetails: list of str
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._JobStatusCode = None
        self._JobStatusMsg = None
        self._JobErrorCode = None
        self._JobErrorMsg = None
        self._ResultUrls = None
        self._ResultDetails = None
        self._RequestId = None

    @property
    def JobStatusCode(self):
        return self._JobStatusCode

    @JobStatusCode.setter
    def JobStatusCode(self, JobStatusCode):
        self._JobStatusCode = JobStatusCode

    @property
    def JobStatusMsg(self):
        return self._JobStatusMsg

    @JobStatusMsg.setter
    def JobStatusMsg(self, JobStatusMsg):
        self._JobStatusMsg = JobStatusMsg

    @property
    def JobErrorCode(self):
        return self._JobErrorCode

    @JobErrorCode.setter
    def JobErrorCode(self, JobErrorCode):
        self._JobErrorCode = JobErrorCode

    @property
    def JobErrorMsg(self):
        return self._JobErrorMsg

    @JobErrorMsg.setter
    def JobErrorMsg(self, JobErrorMsg):
        self._JobErrorMsg = JobErrorMsg

    @property
    def ResultUrls(self):
        return self._ResultUrls

    @ResultUrls.setter
    def ResultUrls(self, ResultUrls):
        self._ResultUrls = ResultUrls

    @property
    def ResultDetails(self):
        return self._ResultDetails

    @ResultDetails.setter
    def ResultDetails(self, ResultDetails):
        self._ResultDetails = ResultDetails

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._JobStatusCode = params.get("JobStatusCode")
        self._JobStatusMsg = params.get("JobStatusMsg")
        self._JobErrorCode = params.get("JobErrorCode")
        self._JobErrorMsg = params.get("JobErrorMsg")
        self._ResultUrls = params.get("ResultUrls")
        self._ResultDetails = params.get("ResultDetails")
        self._RequestId = params.get("RequestId")


class QueryTextToImageProJobRequest(AbstractModel):
    """QueryTextToImageProJob请求参数结构体

    """

    def __init__(self):
        r"""
        :param _JobId: 任务 ID。
        :type JobId: str
        """
        self._JobId = None

    @property
    def JobId(self):
        return self._JobId

    @JobId.setter
    def JobId(self, JobId):
        self._JobId = JobId


    def _deserialize(self, params):
        self._JobId = params.get("JobId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryTextToImageProJobResponse(AbstractModel):
    """QueryTextToImageProJob返回参数结构体

    """

    def __init__(self):
        r"""
        :param _JobStatusCode: 当前任务状态码：
1：等待中、2：运行中、4：处理失败、5：处理完成。
        :type JobStatusCode: str
        :param _JobStatusMsg: 当前任务状态：排队中、处理中、处理失败或者处理完成。

        :type JobStatusMsg: str
        :param _JobErrorCode: 任务处理失败错误码。

        :type JobErrorCode: str
        :param _JobErrorMsg: 任务处理失败错误信息。

        :type JobErrorMsg: str
        :param _ResultImage: 生成图 URL 列表，有效期1小时，请及时保存。

        :type ResultImage: list of str
        :param _ResultDetails: 结果 detail 数组，Success 代表成功。

        :type ResultDetails: list of str
        :param _RevisedPrompt: 对应 SubmitTextToImageProJob 接口中 Revise 参数。开启扩写时，返回扩写后的 prompt 文本。 如果关闭扩写，将直接返回原始输入的 prompt。
        :type RevisedPrompt: list of str
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._JobStatusCode = None
        self._JobStatusMsg = None
        self._JobErrorCode = None
        self._JobErrorMsg = None
        self._ResultImage = None
        self._ResultDetails = None
        self._RevisedPrompt = None
        self._RequestId = None

    @property
    def JobStatusCode(self):
        return self._JobStatusCode

    @JobStatusCode.setter
    def JobStatusCode(self, JobStatusCode):
        self._JobStatusCode = JobStatusCode

    @property
    def JobStatusMsg(self):
        return self._JobStatusMsg

    @JobStatusMsg.setter
    def JobStatusMsg(self, JobStatusMsg):
        self._JobStatusMsg = JobStatusMsg

    @property
    def JobErrorCode(self):
        return self._JobErrorCode

    @JobErrorCode.setter
    def JobErrorCode(self, JobErrorCode):
        self._JobErrorCode = JobErrorCode

    @property
    def JobErrorMsg(self):
        return self._JobErrorMsg

    @JobErrorMsg.setter
    def JobErrorMsg(self, JobErrorMsg):
        self._JobErrorMsg = JobErrorMsg

    @property
    def ResultImage(self):
        return self._ResultImage

    @ResultImage.setter
    def ResultImage(self, ResultImage):
        self._ResultImage = ResultImage

    @property
    def ResultDetails(self):
        return self._ResultDetails

    @ResultDetails.setter
    def ResultDetails(self, ResultDetails):
        self._ResultDetails = ResultDetails

    @property
    def RevisedPrompt(self):
        return self._RevisedPrompt

    @RevisedPrompt.setter
    def RevisedPrompt(self, RevisedPrompt):
        self._RevisedPrompt = RevisedPrompt

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._JobStatusCode = params.get("JobStatusCode")
        self._JobStatusMsg = params.get("JobStatusMsg")
        self._JobErrorCode = params.get("JobErrorCode")
        self._JobErrorMsg = params.get("JobErrorMsg")
        self._ResultImage = params.get("ResultImage")
        self._ResultDetails = params.get("ResultDetails")
        self._RevisedPrompt = params.get("RevisedPrompt")
        self._RequestId = params.get("RequestId")


class QueryTrainPortraitModelJobRequest(AbstractModel):
    """QueryTrainPortraitModelJob请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ModelId: 写真模型 ID。

        :type ModelId: str
        """
        self._ModelId = None

    @property
    def ModelId(self):
        return self._ModelId

    @ModelId.setter
    def ModelId(self, ModelId):
        self._ModelId = ModelId


    def _deserialize(self, params):
        self._ModelId = params.get("ModelId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QueryTrainPortraitModelJobResponse(AbstractModel):
    """QueryTrainPortraitModelJob返回参数结构体

    """

    def __init__(self):
        r"""
        :param _JobStatusCode: 任务状态码。
INIT: 初始化、WAIT：等待中、RUN：运行中、FAIL：处理失败、DONE：处理完成。
        :type JobStatusCode: str
        :param _JobStatusMsg: 任务状态信息。
        :type JobStatusMsg: str
        :param _JobErrorCode: 任务错误码。
        :type JobErrorCode: str
        :param _JobErrorMsg: 任务错误信息。
        :type JobErrorMsg: str
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._JobStatusCode = None
        self._JobStatusMsg = None
        self._JobErrorCode = None
        self._JobErrorMsg = None
        self._RequestId = None

    @property
    def JobStatusCode(self):
        return self._JobStatusCode

    @JobStatusCode.setter
    def JobStatusCode(self, JobStatusCode):
        self._JobStatusCode = JobStatusCode

    @property
    def JobStatusMsg(self):
        return self._JobStatusMsg

    @JobStatusMsg.setter
    def JobStatusMsg(self, JobStatusMsg):
        self._JobStatusMsg = JobStatusMsg

    @property
    def JobErrorCode(self):
        return self._JobErrorCode

    @JobErrorCode.setter
    def JobErrorCode(self, JobErrorCode):
        self._JobErrorCode = JobErrorCode

    @property
    def JobErrorMsg(self):
        return self._JobErrorMsg

    @JobErrorMsg.setter
    def JobErrorMsg(self, JobErrorMsg):
        self._JobErrorMsg = JobErrorMsg

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._JobStatusCode = params.get("JobStatusCode")
        self._JobStatusMsg = params.get("JobStatusMsg")
        self._JobErrorCode = params.get("JobErrorCode")
        self._JobErrorMsg = params.get("JobErrorMsg")
        self._RequestId = params.get("RequestId")


class ReplaceBackgroundRequest(AbstractModel):
    """ReplaceBackground请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ProductUrl: 商品原图 Url。
图片限制：单边分辨率小于4000，长宽比在2:5 ~ 5:2之间，转成 Base64 字符串后小于 6MB，格式支持 jpg、jpeg、png、bmp、tiff、webp。
        :type ProductUrl: str
        :param _Prompt: 对新背景的文本描述。
最多支持256个 utf-8 字符，支持中、英文。
        :type Prompt: str
        :param _Product: 商品图中的商品主体名称。
建议说明商品主体，否则影响生成效果。
        :type Product: str
        :param _MaskUrl: 商品 Mask 图 Url，要求背景透明，保留商品主体。
如果不传，将自动使用内置的商品分割算法得到 Mask。
支持自定义上传 Mask，如果该参数不为空，则以实际上传的数据为准。
图片限制：Mask 图必须和商品原图分辨率一致，转成 Base64 字符串后小于 6MB，格式仅支持 png。
        :type MaskUrl: str
        :param _Resolution: 替换背景后生成的商品图分辨率。
支持生成单边分辨率大于500且小于4000、长宽比在2:5 ~ 5:2之间的图片，不传默认生成1280:1280。
建议图片比例为1:1、9:16、16:9，生成效果更佳，使用其他比例的生成效果可能不如建议比例。
        :type Resolution: str
        :param _LogoAdd: 为生成结果图添加标识的开关，默认为1。
1：添加标识。
0：不添加标识。
其他数值：默认按1处理。
建议您使用显著标识来提示结果图是 AI 生成的图片。
        :type LogoAdd: int
        :param _LogoParam: 标识内容设置。
默认在生成结果图右下角添加“图片由 AI 生成”字样，您可根据自身需要替换为其他的标识图片。
        :type LogoParam: :class:`tencentcloud.aiart.v20221229.models.LogoParam`
        :param _RspImgType: 返回图像方式（base64 或 url) ，二选一，默认为 base64。url 有效期为1小时。
生成图分辨率较大时建议选择 url，使用 base64 可能因图片过大导致返回失败。
        :type RspImgType: str
        """
        self._ProductUrl = None
        self._Prompt = None
        self._Product = None
        self._MaskUrl = None
        self._Resolution = None
        self._LogoAdd = None
        self._LogoParam = None
        self._RspImgType = None

    @property
    def ProductUrl(self):
        return self._ProductUrl

    @ProductUrl.setter
    def ProductUrl(self, ProductUrl):
        self._ProductUrl = ProductUrl

    @property
    def Prompt(self):
        return self._Prompt

    @Prompt.setter
    def Prompt(self, Prompt):
        self._Prompt = Prompt

    @property
    def Product(self):
        return self._Product

    @Product.setter
    def Product(self, Product):
        self._Product = Product

    @property
    def MaskUrl(self):
        return self._MaskUrl

    @MaskUrl.setter
    def MaskUrl(self, MaskUrl):
        self._MaskUrl = MaskUrl

    @property
    def Resolution(self):
        return self._Resolution

    @Resolution.setter
    def Resolution(self, Resolution):
        self._Resolution = Resolution

    @property
    def LogoAdd(self):
        return self._LogoAdd

    @LogoAdd.setter
    def LogoAdd(self, LogoAdd):
        self._LogoAdd = LogoAdd

    @property
    def LogoParam(self):
        return self._LogoParam

    @LogoParam.setter
    def LogoParam(self, LogoParam):
        self._LogoParam = LogoParam

    @property
    def RspImgType(self):
        return self._RspImgType

    @RspImgType.setter
    def RspImgType(self, RspImgType):
        self._RspImgType = RspImgType


    def _deserialize(self, params):
        self._ProductUrl = params.get("ProductUrl")
        self._Prompt = params.get("Prompt")
        self._Product = params.get("Product")
        self._MaskUrl = params.get("MaskUrl")
        self._Resolution = params.get("Resolution")
        self._LogoAdd = params.get("LogoAdd")
        if params.get("LogoParam") is not None:
            self._LogoParam = LogoParam()
            self._LogoParam._deserialize(params.get("LogoParam"))
        self._RspImgType = params.get("RspImgType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ReplaceBackgroundResponse(AbstractModel):
    """ReplaceBackground返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ResultImage: 根据入参 RspImgType 填入不同，返回不同的内容。
如果传入 base64 则返回生成图 Base64 编码。
如果传入 url 则返回的生成图 URL , 有效期1小时，请及时保存。
        :type ResultImage: str
        :param _MaskImage: 如果 MaskUrl 未传，则返回使用内置商品分割算法得到的 Mask 结果。
        :type MaskImage: str
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ResultImage = None
        self._MaskImage = None
        self._RequestId = None

    @property
    def ResultImage(self):
        return self._ResultImage

    @ResultImage.setter
    def ResultImage(self, ResultImage):
        self._ResultImage = ResultImage

    @property
    def MaskImage(self):
        return self._MaskImage

    @MaskImage.setter
    def MaskImage(self, MaskImage):
        self._MaskImage = MaskImage

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._ResultImage = params.get("ResultImage")
        self._MaskImage = params.get("MaskImage")
        self._RequestId = params.get("RequestId")


class ResultConfig(AbstractModel):
    """返回结果配置

    """

    def __init__(self):
        r"""
        :param _Resolution: 生成图分辨率

图像风格化（图生图）支持生成以下分辨率的图片：origin（与输入图分辨率一致，长边最高为2000，超出将做等比例缩小）、768:768（1:1）、768:1024（3:4）、1024:768（4:3），不传默认使用origin，如果指定生成的长宽比与输入图长宽比差异过大可能导致图片内容被裁剪。
        :type Resolution: str
        """
        self._Resolution = None

    @property
    def Resolution(self):
        return self._Resolution

    @Resolution.setter
    def Resolution(self, Resolution):
        self._Resolution = Resolution


    def _deserialize(self, params):
        self._Resolution = params.get("Resolution")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubmitDrawPortraitJobRequest(AbstractModel):
    """SubmitDrawPortraitJob请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ModelId: 写真模型 ID。

        :type ModelId: str
        :param _StyleId: 写真风格模板。
请在[ AI 写真风格列表](https://cloud.tencent.com/document/product/1668/105740) 中选择期望的风格，传入风格编号。
        :type StyleId: str
        :param _ImageNum: 本次生成的图片数量，取值范围[1,4]
        :type ImageNum: int
        :param _LogoAdd: 为生成结果图添加标识的开关，默认为1。 
1：添加标识。
 0：不添加标识。 
其他数值：默认按1处理。 
建议您使用显著标识来提示结果图是 AI 生成的图片。
        :type LogoAdd: int
        :param _LogoParam: 标识内容设置。 
默认在生成结果图右下角添加“图片由 AI 生成”字样，您可根据自身需要替换为其他的标识图片。
        :type LogoParam: :class:`tencentcloud.aiart.v20221229.models.LogoParam`
        :param _Definition: 清晰度，支持以下选项：
sd：基础版，分辨率512:640
hd：高清畅享版，分辨率1024:1280
hdpro：高清优享版，分辨率1024:1280（推荐）
uhd：超清版，分辨率2048:2560
不填默认为sd。

        :type Definition: str
        """
        self._ModelId = None
        self._StyleId = None
        self._ImageNum = None
        self._LogoAdd = None
        self._LogoParam = None
        self._Definition = None

    @property
    def ModelId(self):
        return self._ModelId

    @ModelId.setter
    def ModelId(self, ModelId):
        self._ModelId = ModelId

    @property
    def StyleId(self):
        return self._StyleId

    @StyleId.setter
    def StyleId(self, StyleId):
        self._StyleId = StyleId

    @property
    def ImageNum(self):
        return self._ImageNum

    @ImageNum.setter
    def ImageNum(self, ImageNum):
        self._ImageNum = ImageNum

    @property
    def LogoAdd(self):
        return self._LogoAdd

    @LogoAdd.setter
    def LogoAdd(self, LogoAdd):
        self._LogoAdd = LogoAdd

    @property
    def LogoParam(self):
        return self._LogoParam

    @LogoParam.setter
    def LogoParam(self, LogoParam):
        self._LogoParam = LogoParam

    @property
    def Definition(self):
        return self._Definition

    @Definition.setter
    def Definition(self, Definition):
        self._Definition = Definition


    def _deserialize(self, params):
        self._ModelId = params.get("ModelId")
        self._StyleId = params.get("StyleId")
        self._ImageNum = params.get("ImageNum")
        self._LogoAdd = params.get("LogoAdd")
        if params.get("LogoParam") is not None:
            self._LogoParam = LogoParam()
            self._LogoParam._deserialize(params.get("LogoParam"))
        self._Definition = params.get("Definition")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubmitDrawPortraitJobResponse(AbstractModel):
    """SubmitDrawPortraitJob返回参数结构体

    """

    def __init__(self):
        r"""
        :param _JobId: 提交生成写真图片任务 ID。

        :type JobId: str
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._JobId = None
        self._RequestId = None

    @property
    def JobId(self):
        return self._JobId

    @JobId.setter
    def JobId(self, JobId):
        self._JobId = JobId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._JobId = params.get("JobId")
        self._RequestId = params.get("RequestId")


class SubmitTextToImageProJobRequest(AbstractModel):
    """SubmitTextToImageProJob请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Prompt: 文本描述。 
算法将根据输入的文本智能生成与之相关的图像。 
不能为空，推荐使用中文。最多可传100个 utf-8 字符。
        :type Prompt: str
        :param _Style: 绘画风格。
请在 [文生图（高级版）风格列表](https://cloud.tencent.com/document/product/1668/104567) 中选择期望的风格，传入风格编号。
不传默认不指定风格。
        :type Style: str
        :param _Resolution: 生成图分辨率。
支持生成以下分辨率的图片：768:768（1:1）、768:1024（3:4）、1024:768（4:3）、1024:1024（1:1）、720:1280（9:16）、1280:720（16:9）、768:1280（3:5）、1280:768（5:3），不传默认使用1024:1024。
        :type Resolution: str
        :param _LogoAdd: 为生成结果图添加显式水印标识的开关，默认为1。  
1：添加。  
0：不添加。  
其他数值：默认按1处理。  
建议您使用显著标识来提示结果图使用了 AI 绘画技术，是 AI 生成的图片。
        :type LogoAdd: int
        :param _Engine: 文生图模型，默认使用engine1。
取值：
engine1
engine2
        :type Engine: str
        :param _Revise: prompt 扩写开关。1为开启，0为关闭，不传默认开启。
开启扩写后，将自动扩写原始输入的 prompt 并使用扩写后的 prompt 生成图片，返回生成图片结果时将一并返回扩写后的 prompt 文本。
如果关闭扩写，将直接使用原始输入的 prompt 生成图片。
建议开启，在多数场景下可提升生成图片效果、丰富生成图片细节。
        :type Revise: int
        """
        self._Prompt = None
        self._Style = None
        self._Resolution = None
        self._LogoAdd = None
        self._Engine = None
        self._Revise = None

    @property
    def Prompt(self):
        return self._Prompt

    @Prompt.setter
    def Prompt(self, Prompt):
        self._Prompt = Prompt

    @property
    def Style(self):
        return self._Style

    @Style.setter
    def Style(self, Style):
        self._Style = Style

    @property
    def Resolution(self):
        return self._Resolution

    @Resolution.setter
    def Resolution(self, Resolution):
        self._Resolution = Resolution

    @property
    def LogoAdd(self):
        return self._LogoAdd

    @LogoAdd.setter
    def LogoAdd(self, LogoAdd):
        self._LogoAdd = LogoAdd

    @property
    def Engine(self):
        return self._Engine

    @Engine.setter
    def Engine(self, Engine):
        self._Engine = Engine

    @property
    def Revise(self):
        return self._Revise

    @Revise.setter
    def Revise(self, Revise):
        self._Revise = Revise


    def _deserialize(self, params):
        self._Prompt = params.get("Prompt")
        self._Style = params.get("Style")
        self._Resolution = params.get("Resolution")
        self._LogoAdd = params.get("LogoAdd")
        self._Engine = params.get("Engine")
        self._Revise = params.get("Revise")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubmitTextToImageProJobResponse(AbstractModel):
    """SubmitTextToImageProJob返回参数结构体

    """

    def __init__(self):
        r"""
        :param _JobId: 任务 ID。
        :type JobId: str
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._JobId = None
        self._RequestId = None

    @property
    def JobId(self):
        return self._JobId

    @JobId.setter
    def JobId(self, JobId):
        self._JobId = JobId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._JobId = params.get("JobId")
        self._RequestId = params.get("RequestId")


class SubmitTrainPortraitModelJobRequest(AbstractModel):
    """SubmitTrainPortraitModelJob请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ModelId: 在上传写真训练图片时指定的写真模型 ID。 
每个 AI 写真模型自训练完成起1年内有效，有效期内可使用模型生成图片，期满后需要重新训练模型。

        :type ModelId: str
        """
        self._ModelId = None

    @property
    def ModelId(self):
        return self._ModelId

    @ModelId.setter
    def ModelId(self, ModelId):
        self._ModelId = ModelId


    def _deserialize(self, params):
        self._ModelId = params.get("ModelId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubmitTrainPortraitModelJobResponse(AbstractModel):
    """SubmitTrainPortraitModelJob返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class TextToImageRequest(AbstractModel):
    """TextToImage请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Prompt: 文本描述。
算法将根据输入的文本智能生成与之相关的图像。建议详细描述画面主体、细节、场景等，文本描述越丰富，生成效果越精美。
不能为空，推荐使用中文。最多可传256个 utf-8 字符。
        :type Prompt: str
        :param _NegativePrompt: 反向文本描述。
用于一定程度上从反面引导模型生成的走向，减少生成结果中出现描述内容的可能，但不能完全杜绝。
推荐使用中文。最多可传256个 utf-8 字符。
        :type NegativePrompt: str
        :param _Styles: 绘画风格。
请在 [智能文生图风格列表](https://cloud.tencent.com/document/product/1668/86249) 中选择期望的风格，传入风格编号。
推荐使用且只使用一种风格。不传默认使用201（日系动漫风格）。
        :type Styles: list of str
        :param _ResultConfig: 生成图结果的配置，包括输出图片分辨率和尺寸等。

支持生成以下分辨率的图片：768:768（1:1）、768:1024（3:4）、1024:768（4:3）、1024:1024（1:1）、720:1280（9:16）、1280:720（16:9）、768:1280（3:5）、1280:768（5:3）、1080:1920（9:16）、1920:1080（16:9），不传默认使用768:768。

        :type ResultConfig: :class:`tencentcloud.aiart.v20221229.models.ResultConfig`
        :param _LogoAdd: 为生成结果图添加标识的开关，默认为1。
1：添加标识。
0：不添加标识。
其他数值：默认按1处理。
建议您使用显著标识来提示结果图使用了 AI 绘画技术，是 AI 生成的图片。
        :type LogoAdd: int
        :param _LogoParam: 标识内容设置。
默认在生成结果图右下角添加“图片由 AI 生成”字样，您可根据自身需要替换为其他的标识图片。
        :type LogoParam: :class:`tencentcloud.aiart.v20221229.models.LogoParam`
        :param _RspImgType: 返回图像方式（base64 或 url) ，二选一，默认为 base64。url 有效期为1小时。
        :type RspImgType: str
        """
        self._Prompt = None
        self._NegativePrompt = None
        self._Styles = None
        self._ResultConfig = None
        self._LogoAdd = None
        self._LogoParam = None
        self._RspImgType = None

    @property
    def Prompt(self):
        return self._Prompt

    @Prompt.setter
    def Prompt(self, Prompt):
        self._Prompt = Prompt

    @property
    def NegativePrompt(self):
        return self._NegativePrompt

    @NegativePrompt.setter
    def NegativePrompt(self, NegativePrompt):
        self._NegativePrompt = NegativePrompt

    @property
    def Styles(self):
        return self._Styles

    @Styles.setter
    def Styles(self, Styles):
        self._Styles = Styles

    @property
    def ResultConfig(self):
        return self._ResultConfig

    @ResultConfig.setter
    def ResultConfig(self, ResultConfig):
        self._ResultConfig = ResultConfig

    @property
    def LogoAdd(self):
        return self._LogoAdd

    @LogoAdd.setter
    def LogoAdd(self, LogoAdd):
        self._LogoAdd = LogoAdd

    @property
    def LogoParam(self):
        return self._LogoParam

    @LogoParam.setter
    def LogoParam(self, LogoParam):
        self._LogoParam = LogoParam

    @property
    def RspImgType(self):
        return self._RspImgType

    @RspImgType.setter
    def RspImgType(self, RspImgType):
        self._RspImgType = RspImgType


    def _deserialize(self, params):
        self._Prompt = params.get("Prompt")
        self._NegativePrompt = params.get("NegativePrompt")
        self._Styles = params.get("Styles")
        if params.get("ResultConfig") is not None:
            self._ResultConfig = ResultConfig()
            self._ResultConfig._deserialize(params.get("ResultConfig"))
        self._LogoAdd = params.get("LogoAdd")
        if params.get("LogoParam") is not None:
            self._LogoParam = LogoParam()
            self._LogoParam._deserialize(params.get("LogoParam"))
        self._RspImgType = params.get("RspImgType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TextToImageResponse(AbstractModel):
    """TextToImage返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ResultImage: 根据入参 RspImgType 填入不同，返回不同的内容。
如果传入 base64 则返回生成图 Base64 编码。
如果传入 url 则返回的生成图 URL , 有效期1小时，请及时保存。
        :type ResultImage: str
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ResultImage = None
        self._RequestId = None

    @property
    def ResultImage(self):
        return self._ResultImage

    @ResultImage.setter
    def ResultImage(self, ResultImage):
        self._ResultImage = ResultImage

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._ResultImage = params.get("ResultImage")
        self._RequestId = params.get("RequestId")


class UploadTrainPortraitImagesRequest(AbstractModel):
    """UploadTrainPortraitImages请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ModelId: 写真模型 ID。由英文大小写字母、数字及下划线组成。
用于唯一标识一个写真模型，一个写真模型只能用于一个人物的写真图片生成。
        :type ModelId: str
        :param _BaseUrl: 写真模型训练用的基础图像 URL，用于固定写真模型可生成的人物。
图片数量：1张。
图片内容：单人，脸部清晰。
图片限制：单边分辨率小于2000，转成 Base64 字符串后小于 5MB。

        :type BaseUrl: str
        :param _Urls: 写真模型训练用的图像 URL 列表。
图片数量：19 - 24 张。
图片内容：单人，脸部清晰，和基础图像中的人物为同一人。
图片限制：单边分辨率小于2000，转成 Base64 字符串后小于 5MB。

        :type Urls: list of str
        :param _Filter: 训练图像质量过滤开关配置。
支持开启或关闭对训练图像分辨率下限、脸部区域大小、脸部遮挡的过滤，默认开启以上过滤。
如果训练图像内包含多人脸或无人脸、和 Base 人像不为同一人也将被过滤，不可关闭该过滤条件。
建议：关闭以上过滤可能导致写真生成效果受损，建议使用单人、正脸、脸部区域占比较大、脸部清晰无遮挡、无大角度偏转、无夸张表情的图像进行训练。
        :type Filter: :class:`tencentcloud.aiart.v20221229.models.Filter`
        :param _TrainMode: 是否开启快速训练模式。
默认不开启。开启后只需要在 BaseUrl 中传入1张图片，Urls.N 中无需传入图片。  
0：不开启  
1：开启
        :type TrainMode: int
        """
        self._ModelId = None
        self._BaseUrl = None
        self._Urls = None
        self._Filter = None
        self._TrainMode = None

    @property
    def ModelId(self):
        return self._ModelId

    @ModelId.setter
    def ModelId(self, ModelId):
        self._ModelId = ModelId

    @property
    def BaseUrl(self):
        return self._BaseUrl

    @BaseUrl.setter
    def BaseUrl(self, BaseUrl):
        self._BaseUrl = BaseUrl

    @property
    def Urls(self):
        return self._Urls

    @Urls.setter
    def Urls(self, Urls):
        self._Urls = Urls

    @property
    def Filter(self):
        return self._Filter

    @Filter.setter
    def Filter(self, Filter):
        self._Filter = Filter

    @property
    def TrainMode(self):
        return self._TrainMode

    @TrainMode.setter
    def TrainMode(self, TrainMode):
        self._TrainMode = TrainMode


    def _deserialize(self, params):
        self._ModelId = params.get("ModelId")
        self._BaseUrl = params.get("BaseUrl")
        self._Urls = params.get("Urls")
        if params.get("Filter") is not None:
            self._Filter = Filter()
            self._Filter._deserialize(params.get("Filter"))
        self._TrainMode = params.get("TrainMode")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UploadTrainPortraitImagesResponse(AbstractModel):
    """UploadTrainPortraitImages返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ResultDetails: 用于提示对应上传的Urls训练图片是否符合要求，如果未通过需要重新上传。如果基础图像不符合要求会直接通过ErrorCode提示。如果您选择了快速模式，该参数返回为空数组。
        :type ResultDetails: list of str
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ResultDetails = None
        self._RequestId = None

    @property
    def ResultDetails(self):
        return self._ResultDetails

    @ResultDetails.setter
    def ResultDetails(self, ResultDetails):
        self._ResultDetails = ResultDetails

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._ResultDetails = params.get("ResultDetails")
        self._RequestId = params.get("RequestId")