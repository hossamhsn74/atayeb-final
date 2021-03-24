from django.contrib import admin
from .models import *


class SiteIdentityAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'title',
        'logo'
    )


class ShortBannerAdmin(admin.ModelAdmin):
    list_display = (
        'question', 'answer'
    )

    class Meta:
        app_label = 'FAQ Page'


class QuestionBannerAdmin(admin.ModelAdmin):
    list_display = (
        'question', 'answer'
    )

    class Meta:
        app_label = 'FAQ Page'


class AboutUsCardAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'position'
    )


admin.site.register(SiteIdentity, SiteIdentityAdmin)

admin.site.register(FaqShortBanner, ShortBannerAdmin)
admin.site.register(FaqQuestionBanner, QuestionBannerAdmin)

admin.site.register(AboutUsCard, AboutUsCardAdmin)
admin.site.register(AboutUsParagraph)

admin.site.register(ContactMessages)
admin.site.register(ContactParagraph)
admin.site.register(ContactLocation)
admin.site.register(ContactSideParagraph)

admin.site.register(NewsLetterEmail)