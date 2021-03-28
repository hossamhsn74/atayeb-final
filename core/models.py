from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField


class HomePageLogo(models.Model):
    image = models.ImageField(null=True, blank=True,
                              default='static/recipes/images/content/atayeb_logo_300.png',
                              upload_to='core_images',
                              verbose_name='الصورة')

    class Meta:
        verbose_name_plural = "logo"


class HomePageSlider(models.Model):
    image = models.ImageField(null=True, blank=True,
                              default='static/recipes/images/content/atayeb_logo_300.png',
                              upload_to='core_images',
                              verbose_name='الصورة')

    class Meta:
        verbose_name_plural = "slider"


# FAQ PAGE


class FaqShortBanner(models.Model):
    question = models.CharField(max_length=128, verbose_name="العنوان")
    answer = models.TextField(max_length=128, verbose_name="التفاصيل")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "اقسام الاسئلة المكررة"

# FAQ PAGE


class FaqQuestionBanner(models.Model):
    question = models.CharField(max_length=128, verbose_name="العنوان")
    answer = models.TextField(max_length=128, verbose_name="التفاصيل")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "الاسئلة المكررة"


# About us
class AboutUsParagraph(models.Model):
    title = models.CharField(max_length=128, verbose_name="العنوان")
    descreption = models.TextField(verbose_name="التفاصيل", max_length=1024)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "فقرات الكتابة - معلومات عنا"

# About US page


class AboutUsCard(models.Model):
    image = ResizedImageField(
        default='static/recipes/images/assets/default_profile_picture.png', upload_to='core_images', verbose_name="الصورة")
    name = models.CharField(max_length=128, verbose_name="الاسم")
    position = models.CharField(max_length=128, verbose_name="الوظيفة")
    more_info = models.CharField(max_length=256, verbose_name="تفاصيل اخري")
    facebook_url = models.URLField(
        max_length=128, verbose_name="الملف الشخصي علي فيسبوك", blank=True)
    twitter_url = models.URLField(
        max_length=128, verbose_name="الملف الشخصي علي تويتر", blank=True)
    instgram_url = models.URLField(
        max_length=128, verbose_name="الملف الشخصي علي انستجرام", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "كروت التعريف - معلومات عنا"


class ContactMessages(models.Model):
    email = models.EmailField(max_length=128, verbose_name="البريد الالكتروني")
    address = models.CharField(max_length=128, verbose_name="العنوان")
    message = models.TextField(max_length=1024, verbose_name="الرسالة")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "رسائل الزوار - اتصل بنا"


class ContactParagraph(models.Model):
    title = models.CharField(max_length=128, verbose_name="العنوان")
    descreption = models.TextField(verbose_name="التفاصيل", max_length=1024)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "فقرات الكتابة - اتصل بنا"


class ContactLocation(models.Model):
    locationURL = models.TextField(
        verbose_name="رابط العنوان", max_length=1024)

    def __str__(self):
        return self.locationURL

    class Meta:
        verbose_name_plural = "العنوان - اتصل بنا"


class ContactSideParagraph(models.Model):
    title = models.CharField(max_length=128, verbose_name="العنوان")
    descreption = models.TextField(verbose_name="التفاصيل", max_length=1024)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "فقرات الكتابة الجانبية - اتصل بنا"


class NewsLetterEmail(models.Model):
    email = models.EmailField(verbose_name="البريد الالكتروني")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "المشتركين باخر التحديثات"
